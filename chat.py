from flask import Flask, jsonify, render_template, request
import requests

API_KEY = "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"   # add your OpenRouter API key

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>App is running! Go to /chat to test GPT.</h2>"

@app.route("/chat", methods=["GET", "POST"])
def gpt():
    reply = None
    prompt = None

    if request.method == "POST":
        prompt = request.form.get("prompt")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Flask GPT App"
        }

        body = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body
        ).json()

        try:
            reply = response["choices"][0]["message"]["content"]
        except:
            reply = "Error: Invalid API response"

    return render_template("chat.html", prompt=prompt, result=reply)


if __name__ == "__main__":
    print("🚀 Server running on http://127.0.0.1:5000")
    app.run(debug=True)
