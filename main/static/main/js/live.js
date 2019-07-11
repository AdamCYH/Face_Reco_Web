let initial_call = true;
let last_entry = 0;
const date_format_option = {month: 'short', day: '2-digit', hour: "2-digit", minute: "2-digit"};
let video_output;
let video_content;
let detection_detail;
let detection_list;
let control_title;
let control_subtitle;
let control_button;
let button_label;
let list_indicator;
let detail_indicator;
let detection_header_title;
let detection_map = {};
let video_width;
let video_height;

$(document).ready(function () {
    detection_detail = $("#detection-detail");
    detection_list = $("#detection-list");
    control_title = $("#control-title");
    control_subtitle = $("#control-subtitle");
    button_label = $("#button-label");
    list_indicator = $("#detection-list-indicator");
    detail_indicator = $("#detection-detail-indicator");
    video_output = $("#videoOutput");
    video_content = $("#video_content");
    detection_header_title = $("#detection-header-title");
    setupPage();

    start_live_video();

    video_output.resize(resetVideoSize);
    $(window).resize(resetVideoSize);

    get_detection_update(10);
    window.setInterval(get_detection_update, 10000);

    $(document).on('mousedown', '.detect_box', function () {

        console.log($(this).attr('data-uid'));
        get_user_details(2);

    });
    $(document).on('mousedown', '#video-info', function () {
        get_user_details(2);
    });
});

function setupPage() {
    $("file-upload").remove();
    control_title.html('STATUS');
    control_subtitle.html('Stopped');
    button_label.html('');
    button_label.append("<a id='control-button'></a>");
    button_label.attr('for', 'control-button');
    control_button = $('#control-button');
    setState(I_CAN_START);
}

function max_min_screen() {
    var live_container = $("#live_container");
    if (live_container.hasClass("full_screen")) {
        detection_detail.removeClass('detection-content-full-screen');
        live_container.removeClass("full_screen");
        live_container.find(".max_min_icon").attr('src', '/static/main/img/maximize_s.png');
        video_content.css('width', 'unset');
        resetVideoSize();
    } else {
        live_container.find(".max_min_icon").attr('src', '/static/main/img/minimize_s.png');
        live_container.addClass("full_screen");
        video_content.width($("#videoOutput").width());
        fadeout(detection_detail);
        resetVideoSize();
    }
}

function resetVideoSize() {
    video_width = video_output.width();
    video_height = video_output.height();
}

function show_detection_detail() {
    fadeout(detection_detail);

    if ($("#live_container").hasClass('full_screen')) {
        detection_detail.addClass('detection-content-full-screen');
    }

    if ($("#name_col").html().length === 0) {
        $("#info_table").css('display', 'none');
    } else {
        $("#info_table").css('display', 'table');
    }
    detection_detail.addClass('on');
    list_indicator.removeClass('on');
    detail_indicator.addClass('on');
    detection_header_title.html('DETAILS');
    fadein(detection_detail);

}

function hide_detection_detail() {
    fadeout(detection_detail);
    detection_detail.removeClass('on');
    detail_indicator.removeClass('on');
    list_indicator.addClass('on');
    detection_header_title.html('DETECTIONS');
}

function fadein(element) {
    element.animate({
        opacity: 1,
        right: 0,
    }, 300, function () {
        // Animation complete.
    });
}

function fadeout(element) {
    element.animate({
        opacity: 0,
        right: "-=30%",
        zIndex: -1,
    }, 300, function () {
        // Animation complete.
    });
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
            $("#name_col").html(data.fname + " " + data.lname);
            $("#age_col").html(data.age);
            $("#description_col").html(data.description);
            $("#img_col").attr('src', data.photo_path);
            show_detection_detail();
        },
        error: function (data) {
            console.log(data);
            console.log("Service error, please contact admin.")
        }
    })
}

function send_detection(u_id, conf_lvl) {
    if (u_id === -1) {
        return;
    }
    if (detection_map.has(u_id)) {
        if (Date.now() - detection_map.get(u_id) > 60000) {
            detection_map.delete(u_id)
        } else {
            return;
        }
    } else {
        detection_map.set(u_id, Date.now());
        do_send_detection(u_id, conf_lvl);
    }
}

function do_send_detection(u_id, conf_lvl) {
    $.ajax({
        url: "api/detection",
        dataType: "json",
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
            user: u_id,
            detect_camera: "Camera 1",
            location: "Lab",
            detected_photo_path: "",
            confidence_level: conf_lvl
        },
        context: document.body,
        success: function (data) {

        },
        error: function (data) {
            console.log("Error in sending detection data.")
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