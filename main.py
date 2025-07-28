 
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv
import webbrowser
import os
import musicLibrary
import time
import requests
from openai import OpenAI
import threading

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
newsapi  = os.getenv("newsapi")
recognizer = sr.Recognizer()

def aiProcess(command):
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis, skilled in general tasks like Alexa and Google Assistant."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "temp.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)


def processCommand(c):
    c = c.lower()
    print(f"Processing command: {c}")
    output_text.insert(tk.END, f"\nProcessing: {c}")

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        webbrowser.open("http://youtube.com")

    elif "open linkedin" in c:
        webbrowser.open("http://linkedin.com")

    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)

    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for i in range(min(3, len(articles))):
                headline = articles[i]['title']
                output_text.insert(tk.END, f"\nNews {i+1}: {headline}")
                speak(headline)
        else:
            output_text.insert(tk.END, "\nFailed to fetch news")
            speak("Sorry, I couldn't fetch the news")

    else:
        output = aiProcess(c)
        output_text.insert(tk.END, f"\nJarvis: {output}")
        speak(output)


def listenAndProcess():
    try:
        with sr.Microphone() as source:
            output_text.insert(tk.END, "\nListening for wake word...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                output_text.insert(tk.END, "\nWake word detected!")
                speak("Yes, how can I help you?")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                output_text.insert(tk.END, f"\nYou said: {command}")
                if "hello" in command.lower():
                    speak("JAI SHREE RAM", lang='en')
                else:
                    speak(f"You said {command}")

                if "hi" or "hye" in command.lower():
                    speak("JAI SHREE RAM", lang='en')
                else:
                    speak(f"You said {command}")

                if "who is your developer" in command.lower():
                    speak("Ram dubey", lang='en')
                else:
                    speak(f"You said {command}")    

                

                processCommand(command)
    except sr.UnknownValueError:
        output_text.insert(tk.END, "\nCould not understand audio.")
        speak("Sorry, I didn't catch that.")
    except Exception as e:
        output_text.insert(tk.END, f"\nError: {str(e)}")
        speak("Sorry, I did not catch that.")


def startListeningThread():
    threading.Thread(target=listenAndProcess).start()


root = tk.Tk()
root.title("Jarvis Voice Assistant")
root.geometry("600x400")
root.configure(bg="#1c1c1c")

title_label = tk.Label(root, text="Jarvis - Voice Assistant", font=("Arial", 18, "bold"), bg="#1c1c1c", fg="white")
title_label.pack(pady=10)

command_entry = tk.Entry(root, font=("Arial", 14), width=50)
command_entry.pack(pady=10)

mic_button = tk.Button(root, text="🎤 Speak", font=("Arial", 14), bg="#2c2c2c", fg="white", command=startListeningThread)
mic_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10, font=("Arial", 12), bg="#2c2c2c", fg="white")
output_text.pack(pady=10)


root.mainloop()