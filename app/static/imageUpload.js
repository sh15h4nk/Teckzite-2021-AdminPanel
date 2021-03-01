function dataURItoBlob(dataURI) {
    // convert base64 to raw binary data held in a string
    // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
    var byteString = atob(dataURI.split(',')[1]);

    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    // write the bytes of the string to an ArrayBuffer
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }

    //Old Code
    //write the ArrayBuffer to a blob, and you're done
    //var bb = new BlobBuilder();
    //bb.append(ab);
    //return bb.getBlob(mimeString);

    //New Code
    return new Blob([ab], {type: mimeString});


}



let count = 0;

$(".gambar").attr("src", "");
var $uploadCrop,
tempFilename,
rawImg,
imageId;
function readFile(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {

            if (count > 0)
                location.reload();

            $('.upload-demo').addClass('ready');
            $('#cropImagePop').modal('show');
            rawImg = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
        
    }
    else {
        swal("Sorry - you're browser doesn't support the FileReader API");
    }
}

$uploadCrop = $('#upload-demo').croppie({
    viewport: {
        width: 211,
        height: 210.5,
    },
    
    enforceBoundary: false,
    enableExif: true


});



$(document).ready(function(){
    
    $(document).on('shown.bs.modal','.modal', function () {
        
        $uploadCrop.croppie('bind', {
            url: rawImg
        }).then(function(){
            console.log('jQuery bind complete');
        });
    });
});


$('#cropImageBtn').on('click', function (ev) {

    count++;

    $uploadCrop.croppie('result', {
        type: 'base64',
        format: 'jpeg',
        size: {width: 211, height: 210.5}
    }).then(function (resp) {
        $('#item-img-output').attr('src', resp);
        
        $('#uri').val(resp);
        

        $('#cropImagePop').modal('hide');
    });


});


$('.item-img').on('change', function () { 

    imageId = $(this).data('id'); 
    tempFilename = $(this).val();
    $('#cancelCropBtn').data('id', imageId);
    readFile(this); 
});
