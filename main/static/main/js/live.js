var initial_call = true;
var last_entry = 0;

$(document).ready(function () {
    videoOutput = $("#videoOutput");
    setupPage();
    start();
    videoOutput.resize(resetVideoSize);
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

function get_detection_update(num_entries) {
    $.ajax({
        url: "/api/detection",
        dataType: "json",
        type: 'GET',
        data: {
            num_entries: num_entries,
            initial_call: initial_call,
            last_entry: last_entry
        },
        context: document.body,
        success: function (data) {
            initial_call = false;
            if (data.detection_entry.length > 0) {
                last_entry = data.detection_entry[0].detection_id;
            }
            var row_content = "";
            $.each(data.detection_entry, function (k, v) {
                row_content += "<tr><td>"
                    + v.detect_time + "</td><td>"
                    + v.visitor_id + "</td><td>"
                    + v.name + "</td><td>"
                    + v.location + "</td><td><img class='live_thumbnail ' src='/media/photos/"
                    + v.detect_pic + "'/></td><td><img class='live_thumbnail' src='/media/photos/"
                    + v.regist_pic + "'/></td></tr>";

            });
            $("#detection_table tbody").prepend(row_content);
        },
        error: function (data) {
            console.log("Service error, please contact admin.")
        }
    });
}

String.prototype.format = String.prototype.f = function () {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};