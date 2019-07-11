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

var ws;

var webRtcPeer;
var state = null;

const I_CAN_START = 0;
const I_CAN_STOP = 1;
const I_AM_STARTING = 2;

/*
websocket is moved to start_live_video so that the page is ready, and we can display error message.
Instead of onload, separate function is written because onload and ready function in live.js may perform asyncly,
ws connection may be set before the page is ready so undefined video source may happen.
*/
function start_live_video() {
    ws = new WebSocket('wss://' + location.hostname + ':8443/rtsp');
    setState(I_CAN_START);

    ws.onmessage = function (message) {
        var parsedMessage = JSON.parse(message.data);
        $(".detect_box").remove();
        // console.info('Received message: ' + message.data);
        switch (parsedMessage.id) {
            case 'startResponse':
                startResponse(parsedMessage);
                control_subtitle.html("Building connections");
                break;
            case 'error':
                if (state == I_AM_STARTING) {
                    setState(I_CAN_START);
                }
                onError('Error message from server: ' + parsedMessage.message);
                control_subtitle.html('Error: ' + parsedMessage.message);
                break;
            case 'iceCandidate':
                control_subtitle.html("Running");
                webRtcPeer.addIceCandidate(parsedMessage.candidate);
                break;
            case 'faceFound':
                var facesList = JSON.parse(parsedMessage.faces.value);
                // console.log(faces);
                if (facesList !== undefined && facesList != null) {
                    faces = facesList.face;
                    var x;
                    for (x in faces) {
                        send_detection(faces[x].matching.user_id, faces[x].matching.score);
                        var bbox = faces[x].bbox;
                        var detect_box_id = "boundary_" + x;
                        var matching_user = faces[x].matching.user_id;
                        $("#overlay").append("<div class='detect_box' id=" + detect_box_id + " data-uid=" + matching_user + "></div>");
                        var detect_box = $("#" + detect_box_id);
                        detect_box.css('width', bbox.width * video_width + "px");
                        detect_box.css('height', bbox.height * video_height + "px");
                        detect_box.css('transform', 'translate({0}px,{1}px)'.f(bbox.x * video_width, bbox.y * video_height));
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
    ws.onopen = function () {
        console.log('connected');
        control_subtitle.html("Ready");
        start();
    };

    ws.onclose = function (evt) {
        if (evt.code == 3001) {
            console.log('ws closed');
            ws = null;
        } else {
            ws = null;
            console.log('ws connection error');
            control_subtitle.html("System error, please contact admin or refresh and try again");
        }
    };

    ws.onerror = function (evt) {
        if (ws.readyState == 1) {
            console.log('ws normal error: ' + evt.type);
        }
    };
}


window.onbeforeunload = function () {
    ws.close();
};


function start() {
    control_subtitle.html("Initiating");
    console.log('Starting video call ...');

    // Disable start button
    setState(I_AM_STARTING);

    showSpinner(video_output);

    console.log('Creating WebRtcPeer and generating local sdp offer ...');

    var options = {
        remoteVideo: video_output[0],
        onicecandidate: onIceCandidate,
        dataChannels: true
    };

    webRtcPeer = kurentoUtils.WebRtcPeer.WebRtcPeerRecvonly(options, function (error) {
        if (error) return onError(error);
        this.generateOffer(onOffer);
    });
}

function onIceCandidate(candidate) {
    // console.log('Local candidate' + JSON.stringify(candidate));

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
    control_subtitle.html("System error, please contact admin or refresh and try again");
}

function startResponse(message) {
    setState(I_CAN_STOP);
    console.log('SDP answer received from server. Processing ...');
    webRtcPeer.processAnswer(message.sdpAnswer);
}

function stop() {
    console.log('Stopping video call ...');
    control_subtitle.html("Stopping");
    $(".detect_box").remove();
    setState(I_CAN_START);
    if (webRtcPeer) {
        webRtcPeer.dispose();
        webRtcPeer = null;

        var message = {
            id: 'stop'
        };
        sendMessage(message);
    }
    control_subtitle.html("Stopped");
    hideSpinner(video_output);
    $(".detect_box").remove();
    hide_detection_detail();
}

function setState(nextState) {
    switch (nextState) {
        case I_CAN_START:
            control_button.attr('onclick', 'start()');
            control_button.html('START');
            button_label.removeClass("stop-label");
            button_label.removeClass("starting-label");
            button_label.addClass("start-label");
            break;

        case I_CAN_STOP:
            control_button.attr('onclick', 'stop()');
            control_button.html('STOP');
            button_label.removeClass("start-label");
            button_label.removeClass("starting-label");
            button_label.addClass("stop-label");
            break;

        case I_AM_STARTING:
            control_button.attr('onclick', '');
            control_button.html('STARTING');
            button_label.removeClass("start-label");
            button_label.addClass("starting-label");
            break;

        default:
            onError('Unknown state ' + nextState);
            return;
    }
    state = nextState;
}

function sendMessage(message) {
    var jsonMessage = JSON.stringify(message);
    // console.log('Senging message: ' + jsonMessage);
    try {
        ws.send(jsonMessage);
    } catch (e) {
        control_subtitle.html("System error, please contact admin or refresh and try again");
        setState(I_CAN_START);
        hideSpinner(video_output)
    }

}

function showSpinner() {
    for (var i = 0; i < arguments.length; i++) {
        arguments[i].css('background', "center transparent url('/static/main/img/loading_live.gif') no-repeat");
        arguments[i].css('background-size', '40rem');
    }
}

function hideSpinner() {
    for (var i = 0; i < arguments.length; i++) {
        arguments[i].attr('src', '');
        arguments[i].css('background', '');
    }
}

/**
 * Lightbox utility (to display media pipeline image in a modal dialog)
 */
$(document).delegate('*[data-toggle="lightbox"]', 'click', function (event) {
    event.preventDefault();
    $(this).ekkoLightbox();
});
