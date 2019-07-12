$(document).ready(setupPage);

function setupPage() {
    $("#control-title").html('IMAGE UPLOAD');
    $("#control-subtitle").html('Upload a image with one face.');
    $("#control-button-div").append("<input id='file-upload' type='file' onchange='loadImg(this);' hidden/>");
    $("#button-label").html('Upload').attr('for', 'file-upload');
}

function loadImg(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        var fileName = input.files[0].name;
        reader.onload = function (e) {
            $('#snap_image')
                .attr('src', e.target.result);
            $("#snap_image").val(e.target.result);
            $("#img_name").val(fileName.split(".")[0]);
            $("#default-overlay").remove();
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function doMatch() {
    if (validate()) {
        clear_info();
        $(".scan-overlay").css("display", "block");
        $.ajax({
            url: "recognition",
            dataType: "json",
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
                img_name: $("#img_name").val(),
                img_data: $('#snap_image').val()
            },
            context: document.body,
            success: function (data) {
                $(".scan-overlay").css("display", "none");
                if (data.data.match_users === undefined || data.data.match_users === null) {
                    $("#detected_img_container").append("<div class='center' id='no_match_div'>" + data.data + "</div>");
                } else {
                    if (data.data.match_users.length === 0) {
                        console.log("no match found");
                        $("#detected_img_container").append("<div class='center' id='no_match_div'>No Match Found.</div>");
                    } else {
                        $("#detected_img_container").append("<img class='center' id='img_col'>");
                        display_result(data.data.match_users)
                    }
                }
            }
        });
    }
}

function display_result(users) {
    $(".default-match-block").css('display', 'none');
    var x;
    for (x in users) {
        var curr_user = users[x];
        $("#detection_container").append(
            "<div class='detection_box left-border center-parent'>" +
            "<img class='thumbnail center' src='" + curr_user.user.photo_path + "'>" +
            "<div class='conf-level-container'>" + Math.round(curr_user.confidence_level * 10000) / 100 + "%</div>" +
            "<div class='info_holder' hidden>" +
            "<span class='name_holder'>" + curr_user.user.fname + " " + curr_user.user.lname + "</span>" +
            "<span class='age_holder'>" + curr_user.user.age + "</span>" +
            "<span class='desc_holder'>" + curr_user.user.description + "</span>" +
            "<span class='img_holder'>" + curr_user.user.photo_path + "</span></div></div>");
        console.log(users[x]);
    }
    if (users.length > 0) {
        set_info(users[0].user.fname + " " + users[0].user.lname, users[0].user.age, users[0].user.description, users[0].user.photo_path)
    }
}

function set_info(name, age, description, img) {
    $("#name_col").html(name);
    $("#age_col").html(age);
    $("#description_col").html(description);
    $("#img_col").attr('src', img);
}

function clear_info() {
    $("#no_match_div").remove();
    $("#img_col").remove();
    $("#name_col").html("");
    $("#age_col").html("");
    $("#description_col").html("");
    $(".detection_box").remove();
    $(".default-match-block").css('display', 'inline-block');
}

function validate() {
    if ($('#snap_image').val().trim().length == 0) {
        alert("Please upload a picture.")
        return false;
    } else {
        return true;
    }
}

$(document).ready(function () {
    $(document).on('click', '.detection_box', function () {
        set_info($(this).find('.name_holder').html(), $(this).find('.age_holder').html(),
            $(this).find('.desc_holder').html(), $(this).find('.img_holder').html());
    });
});