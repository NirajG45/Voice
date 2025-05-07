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

# Initialize speech engine
engine = pyttsx3.init()

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        speak("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, the speech service is unavailable.")
        speak("Sorry, the speech service is unavailable.")
        return ""

# Function to perform system operations
def perform_task(command):
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

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

    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {today}")

    elif "open downloads" in command:
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

# Main program loop
def main():
    speak("Hello, I am your assistant. How can I help you?")
    while True:
        command = listen()

        if "exit" in command or "quit" in command or "goodbye" in command:
            speak("Goodbye, have a great day!")
            break

        perform_task(command)

if __name__ == "__main__":
    main()
