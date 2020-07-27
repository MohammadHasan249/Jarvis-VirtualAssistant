import pyttsx3 as pt
from datetime import datetime as dt
import speech_recognition as sr
import wikipedia
import webbrowser
from typing import Optional
from playsound import playsound
import smtplib
import pyautogui
import os
import time

"""
    This program is designed to be a virtual assistant for my own desktop. I
    named it Jarvis, for the sake of culture, after Tony Stark's AI.
"""


# Have a contact name as keys, and email addresses as the values
emails_dict = {'REDACTED': 'REDACTED', 'REDACTED2': 'REDACTED'}

engine = pt.init('sapi5')

voices = engine.getProperty('voices')
# voices[1] has the male voice, the others have the female voice
engine.setProperty('voice', voices[1].id)

webbrowser.register('chrome', None,
                    webbrowser.BackgroundBrowser
                    ("C:\\Program Files (x86)\\Google\\Chrome\\Application"
                     "\\chrome.exe"))


def speak(audio: str) -> None:
    """
    Print the audio, and then make Jarvis say it.
    """
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def greetings() -> None:
    """
    Jarvis launches up, and depending on the time, says the right greeting.
    """
    speak("Powering up...")
    hour = int(dt.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 17:
        speak("Good Afternoon!")
    elif 17 <= hour < 20:
        speak("Good Evening!")
    else:
        speak("Good Night!")

    speak("I am Jarvis. How may I help you today, sir?")


def understand_audio() -> Optional[str]:
    """
    Adjusts the energy threshold on the microphone dynamically and try to
    recognize the user's speech. If it doesn't work, let the user repeat. If
    it does, repeat to the user what they said, just for confirmation. Then,
    return whatever they said as a command/query.
    """
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.dynamic_energy_threshold = True

    with sr.Microphone() as src:
        print("Please wait. Adjusting your microphone...")
        r.adjust_for_ambient_noise(src, duration=2)
        speak('Listening...')
        audio = r.listen(src)

        query = "None"
        try:
            speak('Trying to understand...')
            query = r.recognize_google(audio, language='en-US')
            speak('You said: ' + query + '\n')
        except sr.UnknownValueError:
            speak('Sorry, I couldn\'t catch that! Please repeat.\n')
            understand_audio()
        except sr.RequestError:
            speak('Sorry, requesting results from Google Speech '
                  'Recognition failed.\n')
        except Exception:
            speak('Unknown error.')

    return query


def perform_action(q: str) -> None:
    """
    Based on a query/command, perform an action on it.
    """
    if 'wikipedia' in q:
        speak('Browsing through Wikipedia...')
        q = q.replace('wikipedia', '')
        results = wikipedia.summary(q, sentences=2)
        speak('According to Wikipedia')
        speak(results)

    elif 'open youtube' in q:
        webbrowser.get('chrome').open('youtube.com')

    elif 'open google' in q:
        webbrowser.get('chrome').open('google.com')

    elif 'watch osman' in q or 'watch usman' in q:
        webbrowser.get('chrome').open('kayifamily.com')

    elif 'best team' in q:
        speak('Real Madrid is the best team in the world. Hala Madrid!')

    elif 'play music' in q:
        os.startfile('C:\\Users\\emax\\AppData\\Roaming\\Spotify\\Spotify.exe')
        pyautogui.click(188, 218)
        pyautogui.click(161, 440)
        pyautogui.click(442, 296)

    elif 'pause music' in q:
        pyautogui.click(x=723, y=1066)
        pyautogui.click(x=435, y=293)

    elif 'leave' in q or 'quit' in q or 'shut down' in q or 'shutdown' in q:
        time.sleep(1)
        playsound('deathaudio.mp3', True)
        exit(0)

    elif 'the time' in q:
        current_time = dt.now().strftime('%H:%M')
        speak('The time is ' + current_time)

    elif 'send email' in q:
        try:
            speak("What should I say?")
            content = understand_audio()

            speak("Who should I send it to?")
            address = understand_audio().lower()

            if address in emails_dict:
                to = emails_dict[address]
            else:
                speak("Unknown Contact.\n")

            send_email(to, content)
            speak("Your email has been sent!\n")
        except Exception:
            speak("Uh oh! Something went wrong, and the email hasn't been"
                  " sent.\n")

    else:
        speak("I do not have the mental capacity to understand this command.")


def send_email(target: str, content: str):
    """
    Send an email containing content, to target.
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('REDACTED', 'REDACTED')
    server.sendmail('REDACTED', target, content)
    server.close()


if __name__ == "__main__":
    greetings()
    while True:
        query_param = understand_audio().lower()
        perform_action(query_param)
