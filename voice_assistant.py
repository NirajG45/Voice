from flask import Flask, render_template
import speech_recognition as sr
import pyttsx3
import os
import socket
import webbrowser
import datetime

app = Flask(__name__)
engine = pyttsx3.init()
engine.setProperty('rate', 150)
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("No voice detected, try again.")
            return ""
    try:
        if check_internet():
            command = recognizer.recognize_google(audio)
            print("Google (Online) recognized:", command)
        else:
            command = recognizer.recognize_sphinx(audio)
            print("Sphinx (Offline) recognized:", command)
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Speech recognition service unavailable."

def execute_command(command):
    nircmd_path = '"C:\\Program Files\\nircmd\\nircmd.exe"'

    exit_commands = ["exit", "shutdown", "off", "band ho ja", "jao", "close", "stop"]
    if any(word in command for word in exit_commands):
        speak("Okay Subh, shutting down. Goodbye!")
        exit()

    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "shutdown system" in command:
        speak("Shutting down your system")
        os.system("shutdown /s /t 1")

    elif "restart system" in command:
        speak("Restarting your system")
        os.system("shutdown /r /t 1")

    elif "log off" in command or "sign out" in command:
        speak("Logging off")
        os.system("shutdown -l")

    elif "increase brightness" in command:
        speak("Increasing brightness")
        os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)")

    elif "decrease brightness" in command:
        speak("Decreasing brightness")
        os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,30)")

    elif "mute system" in command:
        speak("Muting system")
        os.system(f"{nircmd_path} mutesysvolume 1")

    elif "unmute system" in command:
        speak("Unmuting system")
        os.system(f"{nircmd_path} mutesysvolume 0")

    elif "volume up" in command:
        speak("Increasing volume")
        os.system(f"{nircmd_path} changesysvolume 5000")

    elif "volume down" in command:
        speak("Decreasing volume")
        os.system(f"{nircmd_path} changesysvolume -5000")

    elif "battery status" in command:
        speak("Checking battery status")
        os.system("WMIC PATH Win32_Battery Get EstimatedChargeRemaining")

    elif "open downloads" in command:
        speak("Opening Downloads folder")
        os.system("explorer shell:Downloads")

    elif "open documents" in command:
        speak("Opening Documents folder")
        os.system("explorer shell:Personal")

    elif "open pictures" in command:
        speak("Opening Pictures folder")
        os.system("explorer shell:My Pictures")

    elif "lock screen" in command:
        speak("Locking screen")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif "switch user" in command:
        speak("Switching user")
        os.system("tsdiscon")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open cmd" in command or "open command prompt" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "empty recycle bin" in command:
        speak("Emptying Recycle Bin")
        os.system("PowerShell.exe -NoProfile -Command Clear-RecycleBin -Force")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {today}")

    elif "create note" in command or "take note" in command:
        speak("What should I write?")
        note = listen()
        if note:
            with open("note.txt", "a") as f:
                f.write(note + "\n")
            speak("Note saved.")

    else:
        speak("Sorry, I didn't understand that command.")

@app.route("/")
def index():
    return render_template("infa.html")

if __name__ == "__main__":
    speak("Hello Subh! How can I assist you?")
    while True:
        command = listen()
        if command:
            execute_command(command)
