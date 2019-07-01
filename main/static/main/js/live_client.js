/*
 * (C) Copyright 2014-2015 Kurento (http://kurento.org/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

var ws = new WebSocket('wss://' + location.hostname + ':8443/rtsp');
var videoOutput;
var webRtcPeer;
var state = null;
var video_width;
var video_height;

const I_CAN_START = 0;
const I_CAN_STOP = 1;
const I_AM_STARTING = 2;

window.onload = function () {
    videoOutput = document.getElementById('videoOutput');
    setState(I_CAN_START);
};

window.onbeforeunload = function () {
    ws.close();
};

ws.onmessage = function (message) {
    $(".detect_box").remove();
    var parsedMessage = JSON.parse(message.data);
    // console.info('Received message: ' + message.data);
    switch (parsedMessage.id) {
        case 'startResponse':
            startResponse(parsedMessage);
            $("#video_status_message").html("Building connections");
            break;
        case 'error':
            if (state == I_AM_STARTING) {
                setState(I_CAN_START);
            }
            onError('Error message from server: ' + parsedMessage.message);
            $("#video_status_message").html('Error: ' + parsedMessage.message);
            break;
        case 'iceCandidate':
            $("#video_status_message").html("Running");
            webRtcPeer.addIceCandidate(parsedMessage.candidate);
            break;
        case 'faceFound':
            var faces = JSON.parse(parsedMessage.faces.value).face;
            // console.log(faces);
            if (faces !== undefined && faces != null) {
                var x;
                for (x in faces) {
                    var bbox = faces[x].bbox;
                    var detect_box_id = "detect_box_" + x;
                    $("#overlay").append("<div class='detect_box' id=" + detect_box_id + "></div>")
                    $("#" + detect_box_id).css('width', bbox.width * video_width + "px");
                    $("#" + detect_box_id).css('height', bbox.height * video_height + "px");
                    $("#" + detect_box_id).css('transform', 'translate({0}px,{1}px)'.f(bbox.x * video_width, bbox.y * video_height));
                }
            }

            break;
        default:
            if (state == I_AM_STARTING) {
                setState(I_CAN_START);
            }
            onError('Unrecognized message', parsedMessage);
    }
};

function start() {
    $("#video_status_message").html("Initiating");
    console.log('Starting video call ...')

    // Disable start button
    setState(I_AM_STARTING);
    showSpinner(videoOutput);

    console.log('Creating WebRtcPeer and generating local sdp offer ...');

    var options = {
        remoteVideo: videoOutput,
        onicecandidate: onIceCandidate,
        dataChannels: true
    };

    webRtcPeer = kurentoUtils.WebRtcPeer.WebRtcPeerRecvonly(options, function (error) {
        if (error) return onError(error);
        this.generateOffer(onOffer);
    });
}

function onIceCandidate(candidate) {
    console.log('Local candidate' + JSON.stringify(candidate));

    var message = {
        id: 'onIceCandidate',
        candidate: candidate
    };
    sendMessage(message);
}

function onOffer(error, offerSdp) {
    if (error) return onError(error);

    console.info('Invoking SDP offer callback function ' + location.host);
    var message = {
        id: 'start',
        sdpOffer: offerSdp
    };
    sendMessage(message);
}

function onError(error) {
    console.error(error);
}

function startResponse(message) {
    setState(I_CAN_STOP);
    console.log('SDP answer received from server. Processing ...');
    webRtcPeer.processAnswer(message.sdpAnswer);
}

function stop() {
    console.log('Stopping video call ...');
    $("#video_status_message").html("Stopping");
    setState(I_CAN_START);
    if (webRtcPeer) {
        webRtcPeer.dispose();
        webRtcPeer = null;

        var message = {
            id: 'stop'
        };
        sendMessage(message);
    }
    $(".detect_box").remove();
    $("#video_status_message").html("Stopped");
    hideSpinner(videoOutput);
}

function setState(nextState) {
    switch (nextState) {
        case I_CAN_START:
            $('#start').attr('disabled', false);
            $('#start').attr('onclick', 'start()');
            $('#stop').attr('disabled', true);
            $('#stop').removeAttr('onclick');
            break;

        case I_CAN_STOP:
            $('#start').attr('disabled', true);
            $('#stop').attr('disabled', false);
            $('#stop').attr('onclick', 'stop()');
            break;

        case I_AM_STARTING:
            $('#start').attr('disabled', true);
            $('#start').removeAttr('onclick');
            $('#stop').attr('disabled', true);
            $('#stop').removeAttr('onclick');
            break;

        default:
            onError('Unknown state ' + nextState);
            return;
    }
    state = nextState;
}

function sendMessage(message) {
    var jsonMessage = JSON.stringify(message);
    console.log('Senging message: ' + jsonMessage);
    ws.send(jsonMessage);
}

function showSpinner() {
    for (var i = 0; i < arguments.length; i++) {
        // arguments[i].poster = './img/transparent-1px.png';
        // arguments[i].style.background = 'center transparent url("./img/spinner.gif") no-repeat';
        arguments[i].style.background = "center transparent url('/static/dashboard/icon/spinner.gif') no-repeat";
        arguments[i].style.backgroundSize = '50px';
    }
}

function hideSpinner() {
    for (var i = 0; i < arguments.length; i++) {
        arguments[i].src = '';
        // arguments[i].poster = './img/webrtc.png';
        arguments[i].style.background = '';
    }
}

/**
 * Lightbox utility (to display media pipeline image in a modal dialog)
 */
$(document).delegate('*[data-toggle="lightbox"]', 'click', function (event) {
    event.preventDefault();
    $(this).ekkoLightbox();
});