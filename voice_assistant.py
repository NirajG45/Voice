import speech_recognition as sr
import pyttsx3
import socket
import webbrowser
import os

# Text-to-Speech (TTS) Setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def check_internet():
    """Check if internet is available"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False

def listen():
    """Recognize voice input"""
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
    """Perform action based on command"""
    
    # ✅ **Exit Commands**
    exit_commands = ["exit", "shutdown", "off", "band ho ja", "jao", "close", "stop"]
    if any(word in command for word in exit_commands):
        speak("Okay Subh, shutting down. Goodbye!")
        exit()
    
    # ✅ **Google Search**
    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # ✅ **Open Websites**
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    # ✅ **System Commands**
    elif "shutdown system" in command:
        speak("Shutting down your system")
        os.system("shutdown /s /t 1")
    elif "restart system" in command:
        speak("Restarting your system")
        os.system("shutdown /r /t 1")
    elif "log off" in command or "sign out" in command:
        speak("Logging off")
        os.system("shutdown -l")

    # ✅ **Brightness Control** (Windows ke liye)
    elif "increase brightness" in command:
        speak("Increasing brightness")
        os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)")
    elif "decrease brightness" in command:
        speak("Decreasing brightness")
        os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,30)")

    # ✅ **Open Applications**
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "open command prompt" in command or "open cmd" in command:
        speak("Opening Command Prompt")
        os.system("cmd")
    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    else:
        speak("Sorry, I didn't understand that command.")

def main():
    """Main loop for voice assistant"""
    speak("Hello Subh! How can I assist you?")
    
    while True:
        command = listen()
        if command:
            execute_command(command)

if __name__ == "__main__":
    main()
