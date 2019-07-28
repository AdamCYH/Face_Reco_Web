$(document).ready(setupPage);

function setupPage() {
    $("#control-title").html('IMAGE UPLOAD');
    $("#control-subtitle").html('Upload a image with one face.');
    $("#control-button-div").append("<input id='file-upload' type='file' onclick='uploadMode()' onchange='loadImg(this);' hidden/>");
    $("#button-label").html('UPLOAD').attr('for', 'file-upload');

    $("#upload-tool").append("<div class='control-button-div' id='control-button-div2' style='right: 7rem'>" +
        "<label id='photo-button' class='button-1' onclick='photoMode()'>CAMERA</label></div>")
}

function photoMode() {
    $("[name=img_holder]").val("");
    $("#photo-module").css('display', 'block');
    $("#snap_image").css('display', 'none');
    setUpPhotoStream();
}

function uploadMode() {
    $("[name=img_holder]").val("");
    $("#photo-module").css('display', 'none');
    $("#snap_image").css('display', 'block');
}


function loadImg(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        var fileName = input.files[0].name;
        reader.onload = function (e) {
            $('#snap_image')
                .attr('src', e.target.result);
            $("[name=img_holder]").val(e.target.result);
            $("#default-overlay").remove();
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function submitform() {
    $("#message").html("");
    if (validate()) {
        document.info_form.submit();
    }
}

function validate() {
    if ($("[name=img_holder]").val().trim().length === 0) {
        $("#message").html("Please upload a image.");
        return false;
    } else if ($("[name=fname]").val().trim().length === 0) {
        $("#message").html("Please enter your first name.");
        return false;
    } else if ($("[name=lname]").val().trim().length === 0) {
        $("#message").html("Please enter your last name.");
        return false;
    } else if ($("[name=age]").val().trim().length !== 0 && isNaN($("[name=age]").val().trim())) {
        $("#message").html("Age should be numbers only.");
        return false;
    } else {
        return true;
    }
}

function setUpPhotoStream() {

    // References to all the element we will need.
    var video = document.querySelector('#camera-stream'),
        image = document.querySelector('#snap'),
        controls = document.querySelector('.controls'),
        take_photo_btn = document.querySelector('#take-photo'),
        delete_photo_btn = document.querySelector('#delete-photo'),
        snap_image = document.querySelector("#snap_image"),
        error_message = document.querySelector('#error-message');


    // The getUserMedia interface is used for handling camera input.
    // Some browsers need a prefix so here we're covering all the options
    navigator.getMedia = (navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia);


    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({video: true})
            .then(function (stream) {
                video.srcObject = stream;
            })
            .catch(function (err0r) {
                console.log("Something went wrong!");
            });
    }


    take_photo_btn.addEventListener("click", function (e) {

        e.preventDefault();

        var snap = takeSnapshot();

        // Show image.
        image.setAttribute('src', snap);
        image.classList.add("visible");

        // Enable delete and save buttons
        delete_photo_btn.classList.remove("disabled");
        // download_photo_btn.classList.remove("disabled");

        // Set the href attribute of the download button to the snap url.
        // download_photo_btn.href = snap;
        snap_image.value = snap;
        $("[name=img_holder]").val(snap);

        // Pause video playback of stream.
        video.pause();

    });


    delete_photo_btn.addEventListener("click", function (e) {

        e.preventDefault();

        // Hide image.
        image.setAttribute('src', "");
        image.classList.remove("visible");
        snap_image.value = "";
        $("[name=img_holder]").val("");
        // Disable delete and save buttons
        delete_photo_btn.classList.add("disabled");

        // Resume playback of stream.
        video.play();

    });


    function showVideo() {
        // Display the video stream and the controls.

        hideUI();
        video.classList.add("visible");
        controls.classList.add("visible");
    }


    function takeSnapshot() {
        // Here we're using a trick that involves a hidden canvas element.

        var hidden_canvas = document.querySelector('canvas'),
            context = hidden_canvas.getContext('2d');

        var width = video.videoWidth,
            height = video.videoHeight;

        if (width && height) {

            // Setup a canvas with the same dimensions as the video.
            hidden_canvas.width = width;
            hidden_canvas.height = height;

            // Make a copy of the current frame in the video on the canvas.
            context.drawImage(video, 0, 0, width, height);

            // Turn the canvas image into a dataURL that can be used as a src for our photo.
            return hidden_canvas.toDataURL('image/png');
        }
    }


    function displayErrorMessage(error_msg, error) {
        error = error || "";
        if (error) {
            console.error(error);
        }

        error_message.innerText = error_msg;

        hideUI();
        error_message.classList.add("visible");
    }


    function hideUI() {
        // Helper function for clearing the app UI.

        controls.classList.remove("visible");
        start_camera.classList.remove("visible");
        video.classList.remove("visible");
        snap.classList.remove("visible");
        error_message.classList.remove("visible");
    }


}