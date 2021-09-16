(function (){

    //Initialize Firebase
    const firebaseConfig = {
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

    //Get elements
    const preObject = document.getElementById('object');
    
    // Create references
    const dbRefObject = firebase.database().ref().child('object');
    
    // Sync object changes
    dbRefObject.on('value', snap => {
        preObject.innerText = JSON.stringify(snap.val(), null, 3);
    });

}());