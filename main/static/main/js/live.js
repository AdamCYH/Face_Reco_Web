$(document).ready(function () {
    setupPage();
    start();
    $("#videoOutput").resize(resetVideoSize);
    $(window).resize(resetVideoSize);

});

function setupPage() {
    $("file-upload").remove();
    $("#control-title").html('STATUS');
    $("#control-subtitle").html('Initiating');
    $("#button-label").html('').append("<a id='start'>START</a>");
    $("#button-label").attr('for', 'start');
    setState(I_CAN_START);
}

function max_min_screen() {
    var live_container = $("#live_container");
    if (live_container.hasClass("full_screen")) {
        live_container.removeClass("full_screen");
        live_container.find(".max_min_icon").attr('src', '/static/main/img/maximize_s.png');
        $("#video_content").css('width', 'unset');
        resetVideoSize();
    } else {
        live_container.find(".max_min_icon").attr('src', '/static/main/img/minimize_s.png');
        live_container.addClass("full_screen");
        $("#video_content").width($("#videoOutput").width());
        resetVideoSize();
    }
}

function resetVideoSize() {
    var video = $('#videoOutput');
    video_width = video.width();
    video_height = video.height();
}

String.prototype.format = String.prototype.f = function () {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};