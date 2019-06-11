
function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;
    var byteCharacters = atob(b64Data);
    var byteArrays = [];
    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);
        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }
        var byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
    }
    var blob = new Blob(byteArrays, { type: contentType });
    return blob;
}

function imagetoblob(ImageURL) {
    var block = ImageURL.split(";");
    var contentType = block[0].split(":")[1];
    var realData = block[1].split(",")[1];
    return b64toBlob(realData, contentType);
}

function compress(source_img_obj, quality, maxWidth, output_format) {
    return new Promise(function (resolve, reject) {
        var mime_type = "image/jpeg";
        if (typeof output_format !== "undefined" && output_format == "png") {
            mime_type = "image/png";
        }

        var result_image_obj = new Image();

        var image = new Image()
        image.onload = function (event) {
            try {
                maxWidth = maxWidth || 1000;
                var natW = image.naturalWidth;
                var natH = image.naturalHeight;
                var ratio = natH / natW;
                if (natW > maxWidth) {
                    natW = maxWidth;
                    natH = ratio * maxWidth;
                }
                var cvs = document.createElement('canvas');
                cvs.width = natW;
                cvs.height = natH;
                var ctx = cvs.getContext("2d").drawImage(image, 0, 0, natW, natH);
                var newImageData = cvs.toDataURL(mime_type, quality / 100);
                result_image_obj.src = newImageData;
                // console.log(image.size);
                resolve(result_image_obj);
            } catch (e) {
                alert(e);
            }
        };
        image.src = source_img_obj;   
    }) 
}

function dataURLtoFile(dataurl, filename) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
}

function formatDate(date) {
    date = new Date(date)
    var year = date.getFullYear(),
        month = date.getMonth() + 1, // months are zero indexed
        monthFormatted = month < 10 ? "0" + month : month,
        day = date.getDate(),
        dayFormatted = day < 10 ? "0" + day : day,
        hour = date.getHours(),
        minute = date.getMinutes(),
        minuteFormatted = minute < 10 ? "0" + minute : minute;

    return dayFormatted + "-" + monthFormatted + "-" + year + " " + hour + ":" +
        minuteFormatted;
}

export { compress, dataURLtoFile, imagetoblob, formatDate}