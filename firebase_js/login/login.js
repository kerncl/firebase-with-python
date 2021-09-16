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


const txtEmail = document.getElementById('txtEmail');
const txtPassword = document.getElementById('txtPassword');
const btnLogin = document.getElementById('btnLogin');
const btnSignUp = document.getElementById('btnSignUp');
const btnLogout = document.getElementById('btnLogout');


btnLogin.addEventListener('click', e=>{
    //Get email and password
    const email = txtEmail.value;
    const pass = txtPassword.value;
    const auth = firebase.auth();
    
    //Sign in
    const promise = auth.signInWithEmailAndPassword(email, pass);
    promise.catch(e=> console.log(e.message))
})

btnSignUp.addEventListener('click', e=> {
    //Get email and password
    const email = txtEmail.value;
    const pass = txtPassword.value;
    const auth = firebase.auth();
    
    //Sign in
    const promise = auth.signInWithEmailAndPassword(email, pass);
    promise.catch(e=> console.log(e.message))
});

btnLogout.addEventListener('click', e=>{
    firebase.auth().signOut();
});

firebase.auth().onAuthStateChanged(firebaseUser => {
    if (firebaseUser){
        console.log(firebaseUser);
        btnLogout.classList.remove('hide')
    } else{
        console.log('not logged in');
        btnLogout.classList.add('hide')
    }
});

