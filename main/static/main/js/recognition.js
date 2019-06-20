function loadImg(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        var fileName = input.files[0].name;
        reader.onload = function (e) {
            $('#snap_image')
                .attr('src', e.target.result);
            $("#snap_image").val(e.target.result);
            $("#img_name").val(fileName.split(".")[0]);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function submitform() {
    if (validate()) {
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
                console.log(data);
                display_result(data.data.match_users)
            }
        });
    }
}

function display_result(users) {
    var x;
    for (x in users) {
        var curr_user = users[x];
        $("#detection_container").append(
            "<div class='detection_box'>" +
            "<div class='detection_img center_parent'>" +
            "<img class='thumbnail center' src='" + curr_user.user.photo_path + "'></div>" +
            "<div class='detection_info center_parent'>" +
            "<div class='center'>" +
            "<div class='center'>" + curr_user.user.fname + " " + curr_user.user.lname + "</div>" +
            "<div class='center'>Confidence Level: " + curr_user.confidence_level + "</div>" +
            "</div>" +
            "</div>" +
            "<div class='info_holder' hidden>" +
            "<span class='name_holder'>" + curr_user.user.fname + " " + curr_user.user.lname + "</span>" +
            "<span class='age_holder'>" + curr_user.user.age + "</span>" +
            "<span class='desc_holder'>" + curr_user.user.description + "</span></div></div>");
        console.log(users[x]);
    }
    if (users.length > 0) {
        set_info(users[0].user.fname + " " + users[0].user.lname, users[0].user.age, users[0].user.description)
    }
}

function set_info(name, age, description) {
    $("#name_col").html(name);
    $("#age_col").html(age);
    $("#description_col").html(description);
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
        set_info($(this).find('.name_holder').html(), $(this).find('.age_holder').html(), $(this).find('.desc_holder').html());
    });
});