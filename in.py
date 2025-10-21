from flask import Flask, render_template, request, jsonify
from datetime import datetime
import wikipedia
from googlesearch import search
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import os
import openai

translator = Translator()

app = Flask(__name__, static_folder='static', template_folder='.')

# ------------------------------
# OpenAI Setup (Optional)
# ------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------------------------
# Home Route
# ------------------------------
@app.route('/')
def home():
    return render_template('in.html')

# ------------------------------
# Smart Processing Route
# ------------------------------
@app.route('/process', methods=['POST'])
def process_command():
    try:
        data = request.get_json()
        command = data.get('command', '').strip()

        if not command:
            return jsonify({"response": "Please enter something to search!"})

        query = command.lower()

        # --- Simple Conversational Responses ---
        if query in ['hi', 'hello', 'hey']:
            return jsonify({"response": "Hello! I’m INFANITE — your intelligent AI assistant. Ask me anything!"})

        if 'time' in query:
            return jsonify({"response": f"Current time: {datetime.now().strftime('%I:%M:%S %p')}"})

        if 'date' in query:
            return jsonify({"response": f"Today’s date is: {datetime.now().strftime('%A, %d %B %Y')}"})

        if 'who are you' in query or 'your name' in query:
            return jsonify({"response": "I am INFANITE — your personal AI assistant powered by Wikipedia & Google!"})

        if 'help' in query:
            help_text = (
                "Try asking me things like:\n"
                "- What is Artificial Intelligence?\n"
                "- Who is Sundar Pichai?\n"
                "- Latest news about AI\n"
                "- Weather in New York\n"
                "- Current time or date"
            )
            return jsonify({"response": help_text})

        # ------------------------------
        # 1️Wikipedia Summary
        # ------------------------------
        wiki_answer = ""
        try:
            wikipedia.set_lang("en")
            wiki_answer = wikipedia.summary(command, sentences=3, auto_suggest=True)
        except wikipedia.exceptions.DisambiguationError:
            wiki_answer = "Multiple entries found on Wikipedia. Try being more specific."
        except wikipedia.exceptions.PageError:
            wiki_answer = ""

        # ------------------------------
        # 2️Google Search (top 3 results)
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
                    google_data.append(f"**{title}**\n{desc}\n{url}\n")
                except Exception:
                    continue
        except Exception:
            pass

        # ------------------------------
        # 3️GPT AI (Optional) if key present
        # ------------------------------
        gpt_answer = ""
        if openai.api_key:
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
            except Exception as e:
                print("GPT error:", e)
                gpt_answer = ""

        # ------------------------------
        # 4️Merge All Results (Chat-style)
        # ------------------------------
        final_parts = []

        if gpt_answer:
            final_parts.append(f"*INFANITE AI Answer:*\n{gpt_answer}")

        if wiki_answer:
            final_parts.append(f"*From Wikipedia:*\n{wiki_answer}")

        if google_data:
            final_parts.append("*Top Google Results:*\n" + "\n".join(google_data))

        if not final_parts:
            final_parts.append("Sorry, no results found for your query. Try a different keyword.")

        final_reply = "\n\n".join(final_parts)

        return jsonify({"response": final_reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Oops! Something went wrong while processing your search."})

# ------------------------------
# Weather API (simple demo)
# ------------------------------
@app.route('/weather/<city>')
def weather(city):
    try:
        res = requests.get(f"https://wttr.in/{city}?format=3")
        return jsonify({"response": f"Weather: {res.text}"})
    except Exception:
        return jsonify({"response": "Could not fetch weather right now."})

# ------------------------------
# Image Upload Placeholder
# ------------------------------
@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        file = request.files.get('image')
        if not file:
            return jsonify({"response": "No image uploaded."})
        return jsonify({"response": f"Received image '{file.filename}' (Feature coming soon!)"})
    except Exception as e:
        print("Image error:", e)
        return jsonify({"response": "Error processing image."})
    
# ------------------------------
# Hinglish → English Translation
# ------------------------------
@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return jsonify({"response": "Please enter some Hinglish text to translate!"})
        
        # Google Translate: Hinglish/Hindi → English
        translation = translator.translate(text, src='hi', dest='en')
        return jsonify({"response": translation.text})
    except Exception as e:
        print("Translation error:", e)
        return jsonify({"response": "Could not translate text right now."})

# ------------------------------
# Voice Input Placeholder
# ------------------------------
@app.route('/voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    voice_text = data.get('voice', '')
    return jsonify({"response": f"You said: '{voice_text}' — I'll search that for you!"})

# ------------------------------
# Run Server
# ------------------------------
if __name__ == '__main__':
    print("INFANITE Server Running")
    print("OpenAI Key Loaded:", bool(openai.api_key))
    app.run(host='0.0.0.0', port=5000, debug=True)
