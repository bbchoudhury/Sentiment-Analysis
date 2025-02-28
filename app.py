from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"  # Change if Ollama runs on different port or address
MODEL_NAME = "llama2"

def get_sentiment(text):
    prompt = f"Analyze the sentiment of the following text. Respond with only one word: Positive, Negative, or Neutral.\n\nText: {text}\n\nSentiment:"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response_data = response.json()

    if 'response' in response_data:
        sentiment = response_data['response'].strip().lower()
        if "positive" in sentiment:
            return "Positive"
        elif "negative" in sentiment:
            return "Negative"
        else:
            return "Neutral"
    else:
        return "Error analyzing sentiment"

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/analyse-sentiment', methods=['POST'])
def analyse_sentiment():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    sentiment = get_sentiment(text)
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    app.run(debug=True)
