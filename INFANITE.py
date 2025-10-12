from flask import Flask, render_template, request, jsonify
import pyttsx3
import pywhatkit
import datetime
import wikipedia

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 170)

def speak(text):
    """Speak the given text aloud."""
    print("Nex:", text)
    engine.say(text)
    engine.runAndWait()

@app.route("/")
def home():
    # Serve your HTML file
    return render_template("infa.html")

@app.route("/process", methods=["POST"])
def process():
    """Handle commands from frontend."""
    data = request.get_json()
    command = data.get("command", "").lower().strip()
    response = ""

    try:
        if "play" in command:
            song = command.replace("play", "").strip()
            if song:
                response = f"Playing {song} on YouTube."
                speak(response)
                pywhatkit.playonyt(song)
            else:
                response = "Please say or type the song name clearly."

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}."
            speak(response)

        elif "who is" in command:
            name = command.replace("who is", "").strip()
            if name:
                try:
                    info = wikipedia.summary(name, 1)
                    response = info
                    speak(info)
                except wikipedia.exceptions.DisambiguationError:
                    response = "There are multiple results for that name. Please be specific."
                except wikipedia.exceptions.PageError:
                    response = "I couldn’t find any information about that."
            else:
                response = "Please specify the name you want to know about."

        elif any(x in command for x in ["stop", "exit", "goodbye", "quit"]):
            response = "Goodbye! Have a nice day."
            speak(response)

        elif command == "":
            response = "I didn’t catch that, please try again."

        else:
            response = "I could not understand your command."
            speak(response)

    except Exception as e:
        response = f"An error occurred: {e}"
        print("Error:", e)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
