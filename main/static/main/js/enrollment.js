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