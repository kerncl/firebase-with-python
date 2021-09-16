// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
var firebaseConfig = {
    apiKey: "AIzaSyDjWtpIS2Mwx7N0yPItYEDbZTXLkZJtmIw",
    authDomain: "bursa-60b86.firebaseapp.com",
    databaseURL: "https://bursa-60b86.firebaseio.com",
    projectId: "bursa-60b86",
    storageBucket: "bursa-60b86.appspot.com",
    messagingSenderId: "181734006071",
    appId: "1:181734006071:web:44dd0763b6a343e6dd8eb2",
    measurementId: "G-0JNP9THHSM"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
//firebase.analytics();

//Get elements
var uploader = document.getElementById('uploader');
var fileButton = document.getElementById('fileButton');
//$('#List').find('tbody').html('')
//$('#Image').find('body').html('')
// Listen for file selection
fileButton.addEventListener('change', function(e){
    // Get file
    var file = e.target.files[0];
    // Create a storage ref     
    var storageRef = firebase.storage().ref('video/' + file.name);   
    // Upload file
    var task = storageRef.put(file);
    //update progress bar
    task.on('state_changed',
        function progress(snapshot){
        var percentage = (snapshot.bytesTransferred / snapshot.totalBytes) * 100
        uploader.value = percentage;
        },
           function error(err){
        },
            function complete(){
        }
    );
});

function downloadVideo(){
    var storageRef = firebase.storage().ref();
    storageRef.child('video/').listAll().then(function(result){
            result.items.forEach(function(imageRef){
                displayImage(imageRef)
                })
    })
    
}

function displayImage(images) {
    images.getDownloadURL().then(function(url){
      console.log(url);
        let new_html = '';
        new_html += '<tr>';
        new_html += '<td>';
        new_html += '<video width="640" height="480" autoplay controls muted>'
        new_html += '<source src="' +url+ '" type="video/mp4">';
        new_html += '</video>'
        new_html += '</td>'
        new_html += '</tr>'
        $('#List').find('tbody').append(new_html);
        
    });
};

function download(){
    var DstorageRef = firebase.storage().ref();
    var vimref = DstorageRef.child('image/vim.png');
    vimref.getDownloadURL().then(function(url) {
          // Insert url into an <img> tag to 'download'         
        console.log('Image reference ' + url);
        let img = '<img src="' +url+ '>';
        $('#Image').find('tbody').append(img);
        
        
    }).catch(function(error){
        switch (error.code){
            // https://firebase.google.com/docs/storage/web/handle-erros
            case 'storage/object-not-found':
                console.log('file doesnt exist')
                break;
            case 'storage/unauthorized':
                console.log('user doesnt have permission to access the object')
                break;
            case 'storage/canceled':
                console.log('user canceled the upload')
                break;
            case 'storage/unknown':
                console.log('unknown error occurred, inspect the server response')
                break;
        }
    })
    console.log('run finish')
}

var database = firebase.database();

function sendMessage(){
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours()+':'+today.getMinutes()+':'+today.getSeconds();
    var dateTime = date+''+time;
    dateTime = dateTime.toString();
    
    var email = document.getElementById('email').value;
    var name = document.getElementById('name').value;
    var comment = document.getElementById('message').value;
    var newMessageKey = database.ref().child('comments').push().key;    // comments can be variable
    database.ref('comments/'+newMessageKey+'/email').set(email);
    database.ref('comments/'+newMessageKey+'/name').set(name);
    database.ref('comments/'+newMessageKey+'/comment').set(comment);
    database.ref('comments/'+newMessageKey+'/date').set(dateTime);
}

firebase.database().ref('comments').on('value', (data)=>{
    var OurData = data.val();
    var keys = Object.keys(OurData);
    for (let i=0; i<keys.length; i++){
        let k=keys[i];
        let keyString = k.toString();
        let email = OurData[k].email;
        let name = OurData[k].name;
        let comment = OurData[k].comment;
        let date = OurData[k].date;
        
        let list= document.getElementById('listcomment');
        let li=document.createElement('li');
        let paragraph = document.createElement('p');
        paragraph.innerHTML = `Name: ${name}<br>
        Email: ${email}<br>
        Comment: <br>
        ${comment}<br>
        Date: ${date}<br>`;
        
        li.appendChild(paragraph);
        list.appendChild(li);
    }
})