import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import pyautogui
import platform
import psutil
import subprocess
import keyboard
import time

# -------------------- Initialize TTS Engine --------------------
engine = pyttsx3.init()

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

# -------------------- Listen from Microphone --------------------
def listen():
    """Listen to the user's voice command and return as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"📥 Command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        speak("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, the speech service is unavailable.")
        speak("Sorry, the speech service is unavailable.")
        return ""

# -------------------- Task Dispatcher --------------------
def perform_task(command):
    """Perform action based on the spoken command."""
    
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What do you want me to search for?")

    elif "shutdown system" in command:
        speak("Shutting down your system")
        os.system("shutdown /s /t 1")

    elif "restart system" in command:
        speak("Restarting your system")
        os.system("shutdown /r /t 1")

    elif "log off" in command:
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
        os.system("nircmd.exe mutesysvolume 1")

    elif "unmute system" in command:
        speak("Unmuting system")
        os.system("nircmd.exe mutesysvolume 0")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open command prompt" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "aaj ka time bato" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {today}")

    elif "open download" in command:
        speak("Opening Downloads folder")
        os.system("explorer shell:Downloads")

    elif "create note" in command or "take note" in command:
        speak("What should I write?")
        note = listen()
        if note:
            with open("note.txt", "a") as f:
                f.write(note + "\n")
            speak("Note saved.")

    else:
        speak("Sorry, I didn't understand that command.")

# -------------------- Main Loop --------------------
def main():
    speak("Hello, I am INFANITE. How can I help you?")
    while True:
        command = listen()

        if any(exit_cmd in command for exit_cmd in ["exit", "quit", "goodbye"]):
            speak("Goodbye, have a great day!")
            break

        perform_task(command)

# -------------------- Entry Point --------------------
if __name__ == "__main__":
    main()
