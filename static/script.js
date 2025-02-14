const API_BASE_URL = "http://127.0.0.1:5000";  // Local Flask API

async function analyzeSentiment() {
    let text = document.getElementById("userInput").value;
    if (!text.trim()) {
        alert("Please enter text.");
        return;
    }

    // Send request to local Flask API
    const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    });

    const data = await response.json();
    
    if (data.error) {
        alert(data.error);
        return;
    }

    // Display the sentiment result
    document.getElementById("result").innerText = `Sentiment: ${data.sentiment}`;
}
