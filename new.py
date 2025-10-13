from flask import Flask, render_template, request, jsonify
from datetime import datetime
import wikipedia
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import os
import openai

app = Flask(__name__, static_folder='static', template_folder='.')

# ------------------------------
# 🔐 OpenAI Setup
# ------------------------------
# Make sure you have your API key stored safely as an environment variable:
# export OPENAI_API_KEY="your_api_key_here"
openai.api_key = os.getenv("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")


# ------------------------------
# 🏠 Home Route
# ------------------------------
@app.route('/')
def home():
    return render_template('infa2.html')

# ------------------------------
# 🧠 Smart Processing Route
# ------------------------------
@app.route('/process', methods=['POST'])
def process_command():
    try:
        data = request.get_json()
        command = data.get('command', '').strip()

        if not command:
            return jsonify({"response": "❌ Please enter something to search!"})

        query = command.lower()

        # --- Simple Conversational Responses ---
        if query in ['hi', 'hello', 'hey']:
            return jsonify({"response": "👋 Hello! I’m INFANITE — your intelligent AI assistant. Ask me anything!"})

        if 'time' in query:
            return jsonify({"response": f"🕒 Current time: {datetime.now().strftime('%I:%M:%S %p')}"})

        if 'date' in query:
            return jsonify({"response": f"📅 Today’s date is: {datetime.now().strftime('%A, %d %B %Y')}"})

        if 'who are you' in query or 'your name' in query:
            return jsonify({"response": "🤖 I am INFANITE — your personal AI assistant powered by GPT and the web!"})

        if 'help' in query:
            help_text = (
                "🧭 Try asking me things like:\n"
                "- What is Artificial Intelligence?\n"
                "- Who is Sundar Pichai?\n"
                "- Latest news about AI\n"
                "- Weather in New York\n"
                "- Current time or date"
            )
            return jsonify({"response": help_text})

        # ------------------------------
        # 1️⃣ Try Wikipedia
        # ------------------------------
        try:
            wikipedia.set_lang("en")
            summary = wikipedia.summary(command, sentences=3, auto_suggest=True)
            return jsonify({"response": f"📘 *From Wikipedia*:\n{summary}"})
        except wikipedia.exceptions.DisambiguationError:
            pass
        except wikipedia.exceptions.PageError:
            pass

        # ------------------------------
        # 2️⃣ Try Google Search (titles + short descriptions)
        # ------------------------------
        google_data = []
        try:
            results = list(search(command, num=5, stop=5))
            for url in results[:3]:
                try:
                    page = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(page.text, 'html.parser')
                    title = soup.title.string.strip() if soup.title else "No Title"
                    desc_tag = soup.find('meta', attrs={'name': 'description'})
                    desc = desc_tag['content'] if desc_tag and 'content' in desc_tag.attrs else "No description available."
                    google_data.append(f"🔗 **{title}**\n{desc}\n🌐 {url}\n")
                except Exception:
                    continue
        except Exception:
            pass

        # ------------------------------
        # 3️⃣ Ask GPT for Reasoning / Explanation
        # ------------------------------
        try:
            gpt_prompt = (
                f"You are INFANITE, an intelligent assistant. "
                f"Answer the following query clearly and concisely:\n\nQuery: {command}"
            )
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are INFANITE, a smart, concise assistant."},
                    {"role": "user", "content": gpt_prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            gpt_answer = response["choices"][0]["message"]["content"].strip()
        except Exception:
            gpt_answer = "⚠️ (AI not available — please set your OpenAI API key.)"

        # ------------------------------
        # Combine Everything Nicely
        # ------------------------------
        final_reply = "🤖 *INFANITE AI Answer:*\n" + gpt_answer
        if google_data:
            final_reply += "\n\n🌍 *Top Google Results:*\n" + "\n".join(google_data)

        return jsonify({"response": final_reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "⚠️ Oops! Something went wrong while processing your search."})


# ------------------------------
# 🌦️ Optional: Simple Weather API (demo using open-meteo)
# ------------------------------
@app.route('/weather/<city>')
def weather(city):
    try:
        res = requests.get(
            f"https://wttr.in/{city}?format=3"
        )
        return jsonify({"response": f"🌤️ Weather: {res.text}"})
    except Exception:
        return jsonify({"response": "⚠️ Could not fetch weather right now."})


# ------------------------------
# 🖼️ Placeholder for Image Search
# ------------------------------
@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        file = request.files.get('image')
        if not file:
            return jsonify({"response": "❌ No image uploaded."})
        return jsonify({"response": f"🖼️ Received image '{file.filename}' (Feature coming soon!)"})
    except Exception as e:
        print("Image error:", e)
        return jsonify({"response": "⚠️ Error processing image."})


# ------------------------------
# 🎤 Voice Input (future ready)
# ------------------------------
@app.route('/voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    voice_text = data.get('voice', '')
    return jsonify({"response": f"🎤 You said: '{voice_text}' — I'll search that for you!"})


# ------------------------------
# 🚀 Run
# ------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
