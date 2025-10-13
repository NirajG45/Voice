from flask import Flask, render_template, request, jsonify
from datetime import datetime
import wikipedia
from googlesearch import search
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static', template_folder='.')

# ------------------------------
# 🏠 HOME ROUTE
# ------------------------------
@app.route('/')
def home():
    return render_template('infa.html')

# ------------------------------
# 🧠 MAIN SMART SEARCH ROUTE
# ------------------------------
@app.route('/process', methods=['POST'])
def process_command():
    try:
        data = request.get_json()
        command = data.get('command', '').strip()

        if not command:
            return jsonify({"response": "❌ Please enter something to search!"})

        query = command.lower()

        # Basic conversational responses
        if query in ['hi', 'hello', 'hey']:
            return jsonify({"response": "👋 Hello! I’m INFANITE — how can I assist you today?"})

        if 'time' in query:
            time_now = datetime.now().strftime("%I:%M:%S %p")
            return jsonify({"response": f"🕒 The current time is {time_now}"})

        if 'date' in query:
            today = datetime.now().strftime("%A, %d %B %Y")
            return jsonify({"response": f"📅 Today’s date is {today}"})

        if 'who are you' in query or 'your name' in query:
            return jsonify({"response": "🤖 I’m INFANITE, your intelligent AI assistant created to help you search and discover anything easily."})

        if 'help' in query:
            help_text = (
                "🧭 You can ask me things like:\n"
                "- 'What is Artificial Intelligence?'\n"
                "- 'Search latest AI news'\n"
                "- 'Show top Google results for climate change'\n"
                "- 'Who is Albert Einstein?'\n"
                "- 'Current time or date'"
            )
            return jsonify({"response": help_text})

        # Try fetching from Wikipedia first
        try:
            wikipedia.set_lang("en")
            summary = wikipedia.summary(command, sentences=3, auto_suggest=True)
            return jsonify({"response": f"📘 *From Wikipedia*:\n{summary}"})
        except wikipedia.exceptions.DisambiguationError:
            return jsonify({"response": f"🤔 Too many possible matches for '{command}'. Please be more specific."})
        except wikipedia.exceptions.PageError:
            pass  # No Wikipedia page found → try Google

        # If Wikipedia fails, go to Google
        try:
            google_results = list(search(command, num=5, stop=5))
            if not google_results:
                return jsonify({"response": "❌ Sorry, no results found online."})

            # Scrape the title & short description for each link
            search_data = []
            for url in google_results[:3]:
                try:
                    page = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(page.text, 'html.parser')
                    title = soup.title.string if soup.title else "No title"
                    desc = soup.find('meta', attrs={'name': 'description'})
                    description = desc['content'] if desc and 'content' in desc.attrs else "No description available."
                    search_data.append(f"🔗 **{title}**\n{description}\n🌐 {url}\n")
                except Exception:
                    search_data.append(f"🌐 {url}")

            google_reply = "🌍 *Top Google Search Results:*\n\n" + "\n".join(search_data)
            return jsonify({"response": google_reply})

        except Exception:
            return jsonify({"response": f"⚠️ Couldn’t fetch live data for '{command}'. Try again later."})

    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "⚠️ Oops! Something went wrong while processing your query."})

# ------------------------------
# 🖼️ IMAGE SEARCH PLACEHOLDER
# ------------------------------
@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        file = request.files.get('image')
        if not file:
            return jsonify({"response": "❌ No image uploaded."})
        return jsonify({"response": f"🖼️ Received image: {file.filename} — (Image analysis feature coming soon!)"})
    except Exception as e:
        print("Image error:", e)
        return jsonify({"response": "⚠️ Error processing the image."})

# ------------------------------
# 🎤 VOICE INPUT ROUTE
# ------------------------------
@app.route('/voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    voice_text = data.get('voice', '')
    return jsonify({"response": f"🎤 You said: '{voice_text}' — searching that for you..."})

# ------------------------------
# 🚀 RUN APP
# ------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
