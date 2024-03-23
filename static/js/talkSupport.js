window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new window.SpeechRecognition();
recognition.interimResults = true;

let timeoutId; // Variable to store the timeout ID



function startConvo() {
     
//  changing button text
 const startbtn=document.getElementById('startbtn');
 startbtn.innerHTML="Stop";
 startbtn.style.backgroundColor="red"

    recognition.start();
    recognition.addEventListener('result', (event) => {
        const transcript = Array.from(event.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('');
           
        console.log('Recognized words:', transcript);

        // Reset the timeout when speech is detected
        clearTimeout(timeoutId);
        timeoutId = setTimeout(stopConvo, 5000); // Stop the conversation after 5 seconds of silence
    });

    recognition.addEventListener('end', () => {
        startbtn.innerHTML="Start";
        startbtn.style.backgroundColor="greenyellow"
        startTimeout();
    });
}

function stopConvo() {
    recognition.stop(); // Stop the speech recognition
}

function startTimeout() {
    // Start the timeout when the conversation ends
    timeoutId = setTimeout(stopConvo, 5000); // Stop the conversation after 5 seconds of silence
}

function convoLoop() {
    startConvo();
}


