import requests
from functions.online import *
from functions.offline import *
from pprint import pprint
import speech_recognition as sr
from random import choice
from com_text import *

from datetime import datetime

import pyttsx3
from decouple import config

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):

    engine.say(text)
    engine.runAndWait()


def greeting():

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"{choice(morning)} {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"{choice(afternoon)} {USERNAME}")
    else:
        speak(f"{choice(eveneing)} {USERNAME}")
    speak(f"i am {BOTNAME}. what can I do for you?")


def take_user_input():

    reg = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        reg.pause_threshold = 1
        audio = reg.listen(source)

    try:
        query = reg.recognize_google(audio, language='en-US')
        print(f"Your command: {query}")
        if not ('stop' in query or 'see you' in query):
            speak(choice(ready_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak(f"{choice(bye)}")
            else:
                speak(f"{choice(bye)}")
            exit()
    except Exception:
        speak(choice(no_understand))
        query = 'None'
    return query


if __name__ == '__main__':
    greeting()
    while True:
        query = take_user_input().lower()

        if 'notepad' in query:
            open_notepad()

        elif 'discord' in query:
            open_discord()

        elif 'command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'camera' in query:
            open_camera()

        elif 'calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}. It is on the screen.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you wanna search on Wikipedia?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"this is what i found on wikipedia, {results}")
            speak("everythinh is on your screen.")
            print(results)

        elif 'youtube' in query:
            speak('What do you wanna play on Youtube?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'google' in query:
            speak('what you wanna search on Google?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "email" in query:
            speak("who is the reciever? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("what is your email's subject?")
            subject = take_user_input().capitalize()
            speak("what you wanna send")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("your email was sent successfully")
            else:
                speak("error has occured. Please checking the error")

        elif 'joke' in query:
            joke = get_random_joke()
            pprint(joke)
            speak(joke)

        elif "advice" in query:
            speak(f"i have an advice for you")
            advice = get_random_advice()
            pprint(advice)
            speak(advice)

        elif "trending movies" in query:
            print(*get_trending_movies(), sep='\n')
            speak(f"some of the trending movies are: {get_trending_movies()}")

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines")
            print(*get_latest_news(), sep='\n')
            speak(get_latest_news())

        # ************************************ - incompleted
        elif "covid" in query:
            res = covid_report_global()
            print(f"the total cases is {res['TotalConfirmed']}")
            speak(f"the total cases is {res['TotalConfirmed']}")
        # ****************************************
        
        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"getting weather report for your city {city}")
            where, weather, temperature, feels_like = get_weather_report(city)
            print(
                f"Description: \n Location: {where} \n Weather: {weather} \nTemperature: {temperature} \n Feels like: {feels_like}")
            speak(
                f"you are currently in {where}, the temperature is {temperature}, but it feels like {feels_like}")
            speak(f"the weather is {weather}")

        
        
            
