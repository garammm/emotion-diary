// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

const firebaseConfig = {
  apiKey: "AIzaSyB4X9JmjPhYfUDPhHU0ZFscmRmIIiEUUvo",
  authDomain: "emotion-diary-kau.firebaseapp.com",
  projectId: "emotion-diary-kau",
  storageBucket: "emotion-diary-kau.appspot.com",
  messagingSenderId: "271731822502",
  appId: "1:271731822502:web:725bf5d6444fb1acedc967",
  measurementId: "G-VQCKLR1DNV",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);
