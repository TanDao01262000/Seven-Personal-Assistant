import requests
import wikipedia
from email.message import EmailMessage
import smtplib
from decouple import config
import pywhatkit as kit
import json

NEWS_API_KEY = config("NEWS_API_KEY")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
TMDB_API_KEY = config("TMDB_API_KEY")
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")


# get user's ip address
def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


# search on wikipedia
def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

# play a video on youtube
def play_on_youtube(video):
    kit.playonyt(video)

# search with google 
def search_on_google(query):
    kit.search(query)

# send email
def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


# get some news 
def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={NEWS_API_KEY}").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


# get weather report based on the user's location (city)
def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    where = res['sys']['country']
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return where, weather, f"{temperature}℃", f"{feels_like}℃"


# get trending movies
def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

# get a joke
def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


# get covid-19 report in the US
def covid_report_global():
    res = requests.get("https://api.covid19api.com/summary").json()
    with open('covid_report.json', 'w') as f:
        json.dump(res, f)
    for con in res["Countries"]:
        if con['CountryCode'] == 'US':  
            return con

# english definition
def get_eng_definition():
    pass
