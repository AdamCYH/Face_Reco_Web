function loadImg(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#snap_image')
                .attr('src', e.target.result);
            $("[name=img_holder]").val(e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function submitform() {
    if (validate()) {
        document.info_form.submit();
    }
}


function validate() {
    if ($("[name=fname]").val().trim().length == 0 ||
        $("[name=lname]").val().trim().length == 0 ||
        $("[name=age]").val().trim().length == 0) {
        alert("Please enter all information.")
        return false;
    } else if ($("[name=img_holder]").val().trim().length == 0) {
        alert("Please take a picture.")
        return false;
    } else {
        return true;
    }
}