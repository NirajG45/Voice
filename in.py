from flask import Flask, render_template, request, jsonify
from datetime import datetime
import wikipedia
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import os
import openai

# ------------------------------
# Load API Keys from Environment
# ------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__, static_folder='static', template_folder='.')

# ------------------------------
# Home Route
# ------------------------------
@app.route('/')
def home():
    return render_template('infa2.html')

# ------------------------------
# Main Smart Search / AI Logic
# ------------------------------
@app.route('/process', methods=['POST'])
def process_command():
    try:
        data = request.get_json()
        command = data.get('command', '').strip()

        if not command:
            return jsonify({"response": "Please enter something to search!"})

        query = command.lower()

        # Basic Conversational Responses
        if query in ['hi', 'hello', 'hey']:
            return jsonify({"response": "Hello! I’m INFANITE — your intelligent AI assistant. Ask me anything!"})

        if 'time' in query:
            return jsonify({"response": f"Current time: {datetime.now().strftime('%I:%M:%S %p')}"})

        if 'date' in query:
            return jsonify({"response": f"Today’s date: {datetime.now().strftime('%A, %d %B %Y')}"})

        if 'who are you' in query or 'your name' in query:
            return jsonify({"response": "I am INFANITE — your personal AI assistant powered by GPT, Wikipedia, Google & APIs!"})

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
        # Weather Check
        # ------------------------------
        if 'weather' in query:
            try:
                # Extract city name
                city = query.replace("weather in", "").replace("weather", "").strip()
                if not city:
                    return jsonify({"response": "Please specify a city, e.g. 'weather in Delhi'."})

                weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
                res = requests.get(weather_url).json()

                if res.get("cod") != 200:
                    return jsonify({"response": f"Could not find weather for '{city}'."})

                temp = res["main"]["temp"]
                desc = res["weather"][0]["description"].capitalize()
                humidity = res["main"]["humidity"]
                wind = res["wind"]["speed"]

                weather_text = (
                    f"*Weather in {city.title()}*\n"
                    f"Temperature: {temp}°C\n"
                    f"Condition: {desc}\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind: {wind} m/s"
                )
                return jsonify({"response": weather_text})
            except Exception as e:
                print("Weather error:", e)
                return jsonify({"response": "Could not fetch weather right now."})

        # ------------------------------
        # News Check
        # ------------------------------
        if 'news' in query:
            try:
                topic = query.replace("news", "").strip() or "latest"
                url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&language=en&pageSize=3"
                res = requests.get(url).json()

                if res["status"] != "ok" or not res["articles"]:
                    return jsonify({"response": f"No news found for '{topic}'."})

                articles = res["articles"][:3]
                news_list = "\n\n".join([
                    f"**{a['title']}**\n{a.get('description', 'No description.')}\n{a['url']}"
                    for a in articles
                ])
                return jsonify({"response": f"*Top News on {topic.title()}:*\n\n{news_list}"})
            except Exception as e:
                print("News error:", e)
                return jsonify({"response": "Could not fetch news right now."})

        # ------------------------------
        # Wikipedia Summary
        # ------------------------------
        try:
            wikipedia.set_lang("en")
            summary = wikipedia.summary(command, sentences=3, auto_suggest=True)
            return jsonify({"response": f"*From Wikipedia:*\n{summary}"})
        except wikipedia.exceptions.DisambiguationError:
            pass
        except wikipedia.exceptions.PageError:
            pass

        # ------------------------------
        # Google Search Results
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
        # GPT AI Assistant Response
        # ------------------------------
        gpt_answer = ""
        try:
            from openai import OpenAI

            client = OpenAI(api_key=openai.api_key)  # Already loaded from env
            prompt = f"You are INFANITE, an intelligent assistant. Answer this clearly:\n\n{command}"

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are INFANITE, a smart, concise, and helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            gpt_answer = response.choices[0].message.content.strip()

        except Exception as e:
            print("GPT error:", e)
            gpt_answer = "AI response unavailable — please check your OpenAI API key."

        # ------------------------------
        # Combine Results
        # ------------------------------
        final_reply = f"*INFANITE AI Answer:*\n{gpt_answer}"
        if google_data:
            final_reply += "\n\n*Top Google Results:*\n" + "\n".join(google_data)

        return jsonify({"response": final_reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Oops! Something went wrong while processing your search."})


# ------------------------------
# Run Server
# ------------------------------
if __name__ == '__main__':
    print("INFANITE Server Running")
    print("OpenAI Key Loaded:", bool(openai.api_key))
    print("News API Loaded:", bool(NEWS_API_KEY))
    print("Weather API Loaded:", bool(WEATHER_API_KEY))
    app.run(host='0.0.0.0', port=5000, debug=True)
