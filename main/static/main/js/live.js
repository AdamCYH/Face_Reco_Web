var initial_call = true;
var last_entry = 0;
const date_format_option = {month: 'short', day: '2-digit', hour: "2-digit", minute: "2-digit"};
var videoOutput;

$(document).ready(function () {
    setupPage();

    videoOutput = $("#videoOutput");

    videoOutput.resize(resetVideoSize);
    $(window).resize(resetVideoSize);

    get_detection_update(5);
    window.setInterval(get_detection_update, 10000);

    $(document).on('mousedown', '.detect_box', function () {
        console.log($(this).attr('data-uid'));
        show_detection_detail();
        get_user_details(2);
    });
    // $(document).on('mousedown', '#video-info', function () {
    //     show_detection_detail();
    //     get_user_details(2);
    // });
});

function setupPage() {
    $("file-upload").remove();
    setState(I_CAN_START);
    $("#control-title").html('STATUS');
    $("#control-subtitle").html('Stopped');
    $("#button-label").html('');
    $("#button-label").append("<a id='control-button'></a>");
    $("#button-label").attr('for', 'control-button');
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

function show_detection_detail() {
    $("#detection-list").removeClass('on');
    $("#detection-detail").addClass('on');
    // $("#detection-detail").animate({
    //     opacity: 0.25,
    //     left: "+=50",
    //     height: "toggle"
    // }, 5000, function () {
    //     // Animation complete.
    // });
}

function get_detection_update(num_entries) {
    $.ajax({
        url: "/api/detection_update",
        dataType: "json",
        type: 'GET',
        data: {
            num_entries: num_entries,
            initial_call: initial_call,
            last_entry: last_entry
        },
        context: document.body,
        success: function (data) {
            console.log(data);
            initial_call = false;
            if (data.length > 0) {
                last_entry = data[0].detection_id;
            }

            var row_content = "";
            var date_str;
            $.each(data, function (k, v) {
                date_str = new Date(v.detection_time).toLocaleDateString("en-US", date_format_option);
                row_content += `<tr><td>${v.user.fname} ${v.user.lname}</td><td>${date_str}</td><td><img class='live_thumbnail' src='${v.user.photo_path}'/></td></tr>`;
            });
            $("#detection-table tbody").prepend(row_content);
        },
        error: function (data) {
            console.log(data);
            console.log("Service error, please contact admin.")
        }
    });
}

function get_user_details(u_id) {
    $.ajax({
        url: "/api/user/" + u_id,
        dataType: "json",
        type: "GET",
        context: document.body,
        success: function (data) {
            console.log(data)
            $("#name_col").html(data.fname + " " + data.lname);
            $("#age_col").html(data.age);
            $("#description_col").html(data.description);
            $("#img_col").attr('src', data.photo_path);
        },
        error: function (data) {
            console.log(data);
            console.log("Service error, please contact admin.")
        }
    })
}

String.prototype.format = String.prototype.f = function () {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};