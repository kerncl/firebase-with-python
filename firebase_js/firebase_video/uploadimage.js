function upload (){
    var image = document.getElementById("image").files[0];
    var imageName = image.name;
    var storageRef =firebase.storage().ref('images/'+imageName)
    var uploadTask = storageRef.put(image);
    uploadTask.on('state_changed', function(snapshot){
        // observe state change events such as progress, pause, resume
        // get task progress by including the number of bytes uploaded and total
        // number of bytes
        var progress = (snapshot.bytesTransferred/snapshot.totalBytes)*100;
        console.log("upload is" + progress + "done");
        },function (error){
            // handle error here
            console.log(error.message);
        },function (){
            // handle successful upload here
            uploadTask.snapshot.ref.getDownloadURL().then(function (downloadURL) {
            console.log(downloadURL);
        
        });
    });
}