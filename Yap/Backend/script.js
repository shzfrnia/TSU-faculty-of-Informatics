function showJson(data, root) { //todo 2arg root true folse
    var list = $("<ul/>");
    var item = $("<li/>");
    var discription = $("<div class='discription'/>")
    var informationForDiscription = [data.type, data.size];
    informationForDiscription.forEach(function(item) {
        discription.append(item + "<br>") ;
    })
    item.append(`<b onclick="myFunction(this)" data-path="${data.path}">${data.name}</b>`) // name
    //item.append(`${typeof(root) == 'string' ? `<a href="getJsonOfDir/${data.back}">..</a> <br>` : ""}`) // link back
    if (data.type == 'file') {
        item.append(`<button onclick="location.href='/downloadFile/${data.path}'">Download file</button>`);
        item.append(`<button onclick="location.href='/previewFile/${data.path}'">Preview file</button>`)
        item.append(`<button onclick="myDelete(this)" data-path="${data.path}">Delete</button>`);
    } else {
        if ((data.children === null || data.children.length == 0)) {
            item.append(`<button onclick="myDelete(this)" data-path="${data.path}">Delete</button>`);
        }
        item.append(`<button onclick="createDir(this)" data-path="${data.path}">Create Folder</button>`)
        // item.append(`<button>Upload file</button>`);
    }
    
    //item.append(`<i><small><small> <br> ${data.type} <br> ${data.size}</small></small></i>`) // discription
    item.append(discription);
    item.append((data.children || []).map(showJson));
    list.append(item);
    return list;
}

//Мб сделать подтверждение удаления Через Confirm js

// $(function myPreview() { in the future its will be normal preview picture. 
//     // Multiple images preview in browser
//     var imagesPreview = function(input, placeToInsertImagePreview) {
//         if (input.files) {
//             var filesAmount = input.files.length;
//             for (i = 0; i < filesAmount; i++) {
//                 var reader = new FileReader();
//                 reader.onload = function(event) {
//                     $($.parseHTML('<img>')).attr('src', event.target.result).appendTo(placeToInsertImagePreview);
//                 }
//                 reader.readAsDataURL(input.files[i]);
//             }
//         }
//     };

//     $('#gallery-photo-add').on('change', function() {
//         imagesPreview(this, 'div.gallery');
//     });
// });

function createDir(elmnt) {
    var el = $(elmnt)
    var path = el.attr("data-path");
    var folderName = prompt("Please enter folder name:", "New folder");
    if (folderName == "") {
        alert("You cannot create folder without name.");
        return;
    } else if (folderName == null) {
        return;
    } else {
        $.get("createDir/" + path + "/" + folderName);
        location.reload();
    }
}

function myDelete(elmnt) {
    var el = $(elmnt)
    var path = el.attr("data-path");
    $.get("delete/" + path);
    location.reload();
}

// function myFunction(elmnt) {
//     var me = $(elmnt);
//     var path = me.attr("data-path");
//     $.get("getJsonOfDir/" + path, function(data) {
//         console.log(data);
//         me
//             .html("")
//             .append(showJson(data));
//     }, "json");
// }

$(function () {
    $.get("getJsonOfDir/pika", function (data) {
        console.log(data);
        showJson(data, "true")
            .appendTo("body");
    }, "json");
});