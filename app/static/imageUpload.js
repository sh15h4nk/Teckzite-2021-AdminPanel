var cropper = new Cropper($('.image_preview')['0'], {
    aspectRatio: 16 / 9,
    cropBoxResizable: false
});
  

$('.input-image').on('change', function (evt) {
    cropper.destroy();   
    var preview = $($(this).next()['0']).children()['0']
    const [file] = this.files
    if (file) {
        

        var reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = function(e){
            imageFile = e.target.result;
            preview.src = imageFile;
            var ind = imageFile.indexOf('base64,') + 7;
            b_imageFile = imageFile.substr(ind)

            cropper = new Cropper(preview, {
                aspectRatio: 16 / 9,
                cropBoxResizable: false,
                crop(event) {

                    $('.cropX').attr('value', event.detail.x);
                    $('.cropY').attr('value', event.detail.y);
                    $('.cropWidth').attr('value', event.detail.width);
                    $('.cropHeight').attr('value', event.detail.height);
                    $('.image').attr('value', b_imageFile);
                                    
                },
            });
        } 
    }
    
});
