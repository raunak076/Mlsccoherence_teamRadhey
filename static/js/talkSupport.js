function startConvo() {
    var recordButton = document.getElementById("recordButton");
    // Decrease opacity
    recordButton.style.opacity = "0.5";
    // Disable button
    recordButton.disabled = true;


    var r = document.getElementById('result');
    var spr = new webkitSpeechRecognition(); //Initialisation of web Kit
    spr.continuous = false; //True if continous conversion is needed, false to stop transalation when paused 
    spr.interimResults = true;
    spr.lang = 'en-IN'; // Set Input language
    spr.start(); //Start Recording the voice 
    var ftr = '';
    spr.onresult = function (event) {
        var interimTranscripts = '';
        for (var i = event.resultIndex; i < event.results.length; i++) {
            var transcript = event.results[i][0].transcript;
            transcript.replace("\n", "<br>")
            if (event.results[i].isFinal) {
                ftr += transcript;
            }
            else
                interimTranscripts += transcript;
        }
        r.innerHTML = ftr + interimTranscripts;
    };

    spr.onerror = function (event) { };
}