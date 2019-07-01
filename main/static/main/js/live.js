$(document).ready(function () {
    start();
    $("#videoOutput").resize(resetVideoSize);
    $(window).resize(resetVideoSize);

});

function max_min_screen() {
    var live_container = $("#live_container");
    if (live_container.hasClass("full_screen")) {
        live_container.removeClass("full_screen");
        live_container.find(".max_min_icon").attr('src', '/static/main/img/maximize_s.png');
        resetVideoSize();
    } else {
        live_container.find(".max_min_icon").attr('src', '/static/main/img/minimize_s.png');
        live_container.addClass("full_screen");
        resetVideoSize();
    }
}

function resetVideoSize() {
    var video = $('#videoOutput');
    video_width = video.width();
    video_height = video.height();
    console.log("new" + video_width + ":" + video_height)
}

String.prototype.format = String.prototype.f = function () {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};