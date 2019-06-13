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