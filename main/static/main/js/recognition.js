function loadImg(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        var fileName = input.files[0].name
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
            url: "/detection",
            dataType: "json",
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
                img_name: $("#img_name").val(),
                img_data: $('#snap_image').val()
            },
            context: document.body,
            success: function (data) {

            }
        });
    }
}


function validate() {
    if ($('#snap_image').val().trim().length == 0) {
        alert("Please upload a picture.")
        return false;
    } else {
        return true;
    }
}