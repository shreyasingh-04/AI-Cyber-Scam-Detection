async function detectScam() {

    const message = document.getElementById("message").value;

    if(message.trim() === ""){
        alert("Please enter a message");
        return;
    }

    // Show loading
    document.getElementById("loading").style.display = "block";
    document.getElementById("result").innerHTML = "";

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    // Hide loading
    document.getElementById("loading").style.display = "none";

    let color;

    if (data.prediction === "Scam") {
        color = "red";
    } 
    else if (data.prediction === "Suspicious") {
        color = "orange";
    } 
    else {
        color = "green";
    }

    document.getElementById("result").innerHTML =
        `<span style="color:${color}">
            Result: ${data.prediction} <br>
            Confidence: ${data.confidence}
        </span>`;
}