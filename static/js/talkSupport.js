let url = `ws://${window.location.host}/ws/socket-server/`;

const chatSocket = new WebSocket(url);

var langFlag = ""

chatSocket.onmessage = function (e) {
  let data = JSON.parse(e.data);
  console.log("Data:", data);
};

// chatSocket.onopen = function () {
//     chatSocket.send(JSON.stringify({
//         'type':'information',
//         'message':'Hi'
//     }));
// };

const base_url = "http://localhost:8000";

var resultDiv = document.getElementById("result");
var transcript = "";

function listen() {
  document.getElementById("startbtn").textContent = "STOP";
  var speech = true;
  window.SpeechRecognition = window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.interimResults = true;
  recognition.continuous = true; // Enable continuous listening

  let timeoutId;

  recognition.addEventListener("result", (e) => {
    transcript = Array.from(e.results)
      .map((result) => result[0])
      .map((result) => result.transcript);

    console.log(transcript);
    clearTimeout(timeoutId); // Reset the timeout
    timeoutId = setTimeout(() => {
      console.log("No speech detected. Stopping recognition.");
      recognition.stop(); // Stop recognition if no speech is detected for a certain period
    }, 5000); // Adjust the timeout period as needed (e.g., 5 seconds)
  });

  recognition.addEventListener("end", () => {
    console.log("Recognition ended.");
    sendText(transcript);
  });

  if (speech) {
    recognition.start();
  }
}

function speakUp(receivedText) {
  const speech = new SpeechSynthesisUtterance();
  speech.text = receivedText;
  window.speechSynthesis.speak(speech);
}

async function sendText(transcript) {
  // Implement sending text functionality
  const data = {
    text: transcript.join(),
    flag:langFlag
  };
  // await fetch(`${base_url}/sendText`, {
  //     headers: {
  //         'Content-Type': 'application/json'
  //     },
  //     method: 'POST',
  //     body: JSON.stringify(data)
  // })
  chatSocket.send(
    JSON.stringify({
      type: "information",
      message: data["text"],
    })
  );

  chatSocket.onmessage = async function (e) {
    let data = JSON.parse(e.data);
    // console.log('Data:', data)
    speakUp(data["message"]);
    document.getElementById("startbtn").textContent = "START";
  };

  // .then((response) => {
  //     const resData = response.json()
  //     return resData
  // }).then((resData) => {
  //     console.log(resData['message'])
  //     speakUp(resData['message'])
  // })
}



//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

function toggleLanguage(lang){
  const disButton = (lang == 'E') ? 'H' : 'E'
  document.getElementById(disButton).disabled = true
  langFlag = lang
  alert(langFlag)
}