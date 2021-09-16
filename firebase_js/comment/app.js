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

var database=firebase.database();

function sendMessage(){
    //getting the required values to send to firebase database and saving them in the variables
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours()+':'+today.getMinutes()+':'+today.getSeconds();
    var dateTime = date+''+time;
    dateTime=dateTime.toString();
    
    var email = document.getElementById('email').value;
    var name = document.getElementById('name').value;
    var comment = document.getElementById('message').value;
console.log(email+name+comment+dateTime)
    var newMessageKey = database.ref().child('comments').push().key;
    database.ref('comments/'+newMessageKey+'/email').set(email);
    database.ref('comments/'+newMessageKey+'/name').set(name);
    database.ref('comments/'+newMessageKey+'/comment').set(comment);
    database.ref('comments/'+newMessageKey+'/date').set(dateTime);
}

////Listen for submit
//document.getElementById('contactForm').addEventListener('submit');

firebase.database().ref('comments').on('value', (data)=> {
    var OurData = data.val();
    console.log(OurData);
    var keys= Object.keys(OurData);
    for (let i=0; i<keys.length; i++){
        let k=keys[i];
        let keyString = k.toString();
        let email = OurData[k].email;
        let name = OurData[k].name;
        let comment = OurData[k].comment;
        let date = OurData[k].date;
        
        let list = document.getElementById('listcomment');
        
        let li = document.createElement('li');
        let paragraph = document.createElement('p');
        paragraph.innerHTML = `Name: ${name}<br>
        Email: ${email}<br>
        Comment: <br>
        ${comment}<br>
        Date: ${date}<br>`;
        
        li.appendChild(paragraph);
        list.appendChild(li)
                                
        
    }
})