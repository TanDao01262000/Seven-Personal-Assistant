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
engine.setProperty('rate', 230)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greeting():
    feature_list = ['open notepade, discord, cmd, camera, calculator', 'finding ip address',
                    'play youtube', 'search on google, wikipedia', 'sending email',
                    'reporting news, trending movies, weather', 'translate']

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"{choice(morning)} {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"{choice(afternoon)} {USERNAME}")
    else:
        speak(f"{choice(eveneing)} {USERNAME}")
    
    speak('First, Do you wanna know what i can help you with?')
    ans = take_user_input()
    if ans == 'yes':
        speak('Here are some action I can do:')
        for i in feature_list:
            print(i)
            speak(i)
    else:
        speak('Let me know what you want')

def take_user_input():
    reg = sr.Recognizer()
    with sr.Microphone() as source:
        print('I am listening to your command')
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

        elif 'command prompt' in query or 'cmd' in query:
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


        elif "trending movies" in query:
            print(*get_trending_movies(), sep='\n')
            speak(f"some of the trending movies are: {get_trending_movies()}")

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines")
            print(*get_latest_news(), sep='\n')
            speak(get_latest_news())

        elif "covid" in query:
            res_us= covid_report_global()
            if 'America' or 'US' in query:
                # the U.S. Covid-19 cases report including: case, deaths, and recovery
                print(f"the total case: " + str(res_us['TotalConfirmed']))
                speak(f"the total case: " + str(res_us['TotalConfirmed']))
                print(f"the total deaths: " + str(res_us['TotalDeaths']))
                speak(f"the total deaths: " +str(res_us['TotalDeaths']))
                print(f"the new deaths: " + str(res_us['NewDeaths']))
                speak(f"the new deaths: " +str(res_us['NewDeaths']))
                print(f"the total recovered case: " + str(res_us['TotalRecovered']))
                speak(f"the total recovered case:" + str(res_us['TotalRecovered']))


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

        elif 'translate' in query:
            lang = {'vietnamese':'vi', 'spanish':'es','none':'en'}
            speak('what you want to translate?')
            text = take_user_input().lower()
            print(text)
            while text == 'none':
                speak('what you want to translate?')
                text = take_user_input().lower()

            speak('what language you want to translate to?')
            to_lang = take_user_input().lower()
            while to_lang == 'none':
                speak('what language you want to translate to?')
                to_lang = take_user_input().lower()
            if to_lang in lang:
                to_lang = lang[to_lang]
                res = translate(str(text), 'en', str(to_lang))
                print(res)
                speak('The translation is on your screen now')
            else:
                speak("This language has not been supported yet, please try again")
            
