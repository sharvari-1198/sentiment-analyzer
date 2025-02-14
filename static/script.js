const API_BASE_URL = "https://sentiment-analyzer-one.vercel.app/";  // Change this to your actual URL

async function analyzeSentiment() {
    let text = document.getElementById("userInput").value;

    const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    });

    const data = await response.json();
    document.getElementById("result").innerText = `Sentiment: ${data.sentiment} (Confidence: ${data.confidence.toFixed(2)})`;

    // Save to Firebase
    await saveToFirebase({ text: text, sentiment: data.sentiment, confidence: data.confidence });
}

async function saveToFirebase(sentimentData) {
    await fetch(`${API_BASE_URL}/save_to_firebase`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sentimentData)
    });
}
