window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new window.SpeechRecognition();
recognition.interimResults = true;

let timeoutId; // Variable to store the timeout ID

function startConvo() {
    document.getElementById()
    recognition.addEventListener('result', (event) => {
        const transcript = Array.from(event.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('');
        console.log('Recognized words:', transcript);

        // Reset the timeout if speech is detected
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            console.log("User stopped speaking for 5 seconds.");
            recognition.stop(); // Stop recognition after 5 seconds of silence
        }, 5000); // Set timeout for 5 seconds
    });

    recognition.addEventListener('end', () => {
        // Restart the recognition after it stops
        startConvo();
    });

    recognition.start();
}

function convoLoop() {
    startConvo();
}
