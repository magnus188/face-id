// Initialize Firebase
var config = {
    apiKey: "AIzaSyCW2NVUXvaItBiqV06QMgtf7HkgmjhHKeU",
    authDomain: "facial-recognintion.firebaseapp.com",
    databaseURL: "https://facial-recognintion.firebaseio.com",
    projectId: "facial-recognintion",
    storageBucket: "facial-recognintion.appspot.com",
    messagingSenderId: "949254238331"
};
firebase.initializeApp(config);

const firebase = require("firebase");
require("firebase/firestore");

var db = firebase.firestore();

db.collection("persons").get().then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
        console.log(`${doc.id} => ${doc.data()}`);
    });
});