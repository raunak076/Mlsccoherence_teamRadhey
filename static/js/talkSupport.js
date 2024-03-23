const base_url = "http://localhost:8000"

var resultDiv = document.getElementById("result");
var transcript = ''

function listen() {
    var speech = true;
    window.SpeechRecognition = window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.interimResults = true;
    recognition.continuous = true; // Enable continuous listening

    let timeoutId;

    recognition.addEventListener('result', e => {
        transcript = Array.from(e.results)
            .map(result => result[0])
            .map(result => result.transcript);

        console.log(transcript);
        clearTimeout(timeoutId); // Reset the timeout
        timeoutId = setTimeout(() => {
            console.log("No speech detected. Stopping recognition.");
            recognition.stop(); // Stop recognition if no speech is detected for a certain period
        }, 5000); // Adjust the timeout period as needed (e.g., 5 seconds)
    });

    recognition.addEventListener('end', () => {
        console.log("Recognition ended.");
        sendText(transcript)
    });

    if (speech) {
        recognition.start();
    }
}

function speakUp(receivedText){
    const speech = new SpeechSynthesisUtterance()
    speech.text = receivedText
    window.speechSynthesis.speak(speech)
}

async function sendText(transcript) {
    // Implement sending text functionality
    const data = {
        "text":transcript.join()
    }
    await fetch(`${base_url}/sendText`,{
        headers:{
            'Content-Type':'application/json'
        },
        method:'POST',
        body:JSON.stringify(data)
    }).then((response)=>{
        const resData = response.json()
        return resData
    }).then((resData)=>{
        console.log(resData['message'])
        speakUp(resData['message'])
    })
}
