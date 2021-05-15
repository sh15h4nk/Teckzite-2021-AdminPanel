var cropper = new Cropper(image_preview, {
    aspectRatio: 16 / 9,
    cropBoxResizable: false
});


$('#photo-cropX').attr('type', 'hidden');
$('#photo-cropY').attr('type', 'hidden');
$('#photo-cropWidth').attr('type', 'hidden');
$('#photo-cropHeight').attr('type', 'hidden');
$('#photo-image').attr('type', 'hidden');


$('#input-image').on('change', function (evt) {
    const [file] = this.files
    if (file) {
        cropper.destroy();

        var reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = function(e){
            imageFile = e.target.result;
            image_preview.src = imageFile;
            var ind = imageFile.indexOf('base64,') + 7;
            b_imageFile = imageFile.substr(ind)

            cropper = new Cropper(image_preview, {
                aspectRatio: 16 / 9,
                cropBoxResizable: false,
                crop(event) {

                    $('#photo-cropX').attr('value', event.detail.x);
                    $('#photo-cropY').attr('value', event.detail.y);
                    $('#photo-cropWidth').attr('value', event.detail.width);
                    $('#photo-cropHeight').attr('value', event.detail.height);
                    $('#photo-image').attr('value', b_imageFile);
                                    
                },
            });
        } 
    }
    
});
