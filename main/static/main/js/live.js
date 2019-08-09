const date_format_option = {month: 'short', day: '2-digit', hour: "2-digit", minute: "2-digit"};
const DETECTION_LIST_NUM = 10;
const COLOR_LETTERS = '0123456789ABCDEF';
const DETECTION_MAX_ROW = 50;

let num_detection = 0;
let initial_call = true;
let last_entry = 0;
let video_output;
let video_content;
let video_overlay;
let detection_detail;
let detection_list;
let control_title;
let control_subtitle;
let control_button;
let button_label;
let list_indicator;
let detail_indicator;
let detection_header_title;
let video_width;
let video_height;
let color_map = new Map();

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
    video_overlay = $("#overlay");
    detection_header_title = $("#detection-header-title");
    setupPage();

    start_live_video();

    video_output.resize(resetVideoSize);
    $(window).resize(resetVideoSize);

    get_detection_update(DETECTION_LIST_NUM);
    window.setInterval(get_detection_update, 3000);

    $(document).on('mousedown', '.detect_box', function () {
        console.log($(this).attr('data-uid'));
        get_user_details($(this).attr('data-uid'), $(this).attr('data-cnflvl'));
    });
    // Code for quick debug
    // $(document).on('mousedown', '#video-info', function () {
    //     get_user_details(19, 0.097);
    // });
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
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        alert("Full screen is not supported on mobile devices.");
    } else {
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
}

function resetVideoSize() {
    video_width = video_output.width();
    video_height = video_output.height();
}

function show_detection_detail() {

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
        right: "-=30%",
    }, 0, function () {
        // Animation complete.
    });
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
    element.animate({
        right: "+=30%",
    }, 0, function () {
        // Animation complete.
    });
}

function get_detection_update(num_entries) {
    if (num_detection > DETECTION_MAX_ROW) {
        for (let i = 0; i < num_detection - DETECTION_MAX_ROW; i++) {
            $('#detection-table tr:last').remove();
            num_detection--;
        }
    }
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
            initial_call = false;
            if (data.length > 0) {
                last_entry = data[0].detection_id;
            }

            let row_content = "";
            let date_str;
            $.each(data, function (k, v) {
                num_detection++;
                let color_bar = `<div class='detection-color-box' style='background-color: ${getUserColor(v.user.user_id)}'></div>`
                date_str = new Date(v.detection_time).toLocaleDateString("en-US", date_format_option);
                row_content += `<tr onclick="get_detection_detail(${v.detection_id}, '')"><td>${v.user.fname} ${v.user.lname}</td><td>${date_str}</td><td><div style="position: relative"><img class='live_thumbnail' src='${v.user.photo_path}'/>${color_bar}</div></td></tr>`;
            });
            $("#detection-table tbody").prepend(row_content);
        },
        error: function (data) {
            console.log(data);
            console.log("Service error, please contact admin.")
        }
    });
}

function get_detection_detail(d_id) {
    fadeout(detection_detail);
    $("#no_match_div").remove();

    $.ajax({
        url: "/api/detection/" + d_id,
        dataType: "json",
        type: "GET",
        context: document.body,
        success: function (data) {
            $("#name_col").html(data.user.fname + " " + data.user.lname);
            $("#age_col").html(data.user.age);
            $("#cnflvl_col").html(Math.round(data.confidence_level * 10000) / 100 + "%");
            $("#description_col").html(data.user.description);
            $("#img_col").attr('src', data.user.photo_path);
            show_detection_detail();
        },
        error: function (data) {
            console.log(data);
            console.log("Service error, please contact admin.")
        }
    })

}

function get_user_details(u_id, cnflvl) {
    fadeout(detection_detail);
    $("#no_match_div").remove();
    if (u_id === "-1") {
        $("#detected_img_container").append("<div id='no_match_div'>No Match Found.</div>");
        $("#name_col").html("");
        $("#age_col").html("");
        $("#description_col").html("");
        $("#cnflvl_col").html("");
        $("#img_col").attr('src', "");
        show_detection_detail();
    } else {
        $.ajax({
            url: "/api/user/" + u_id,
            dataType: "json",
            type: "GET",
            context: document.body,
            success: function (data) {
                $("#name_col").html(data.fname + " " + data.lname);
                $("#age_col").html(data.age);
                $("#cnflvl_col").html(cnflvl);
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
}

function getUserColor(user_id) {
    if (color_map.has(user_id)) {
        return color_map.get(user_id)
    } else {
        let color = generateColor();
        color_map.set(user_id, color);
        return color;
    }
}


function generateColor() {
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += COLOR_LETTERS[Math.floor(Math.random() * 16)];
    }
    return color;
}


String.prototype.format = String.prototype.f = function () {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};