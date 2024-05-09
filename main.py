from __future__ import with_statement
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import pywhatkit as kit
import sys
import pyautogui
import time
import requests
import subprocess
import math
import openai


#TODO: 1: add your openai api key after making a account om openai website.
openai.api_key = 'YOUR API KEY'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def audio(a):
    engine.say(a)
    engine.runAndWait()

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        audio("Good Morning!")
        print("Good Morning!")
    elif hour >= 12 and hour < 18:
        audio("Good Afternoon!")
        print("Good Afternoon!")
    else:
        audio("Good Evening!")
        print("Good Evening!")

    audio("What can I do for you ?")
    print("What can I do for you ?")
# def openai_query(question):
#     try:
#         response = openai.Completion.create(
#             prompt=question,
#             max_tokens=50,  # Adjust as needed based on the response length you want
#             stop=["\n", ""],  # Stop generation at newline or endoftext token
#             temperature=0.7,  # Adjust the temperature parameter for generating more diverse responses
#             n=1  # Specify the number of responses to generate
#         )
#         return response['choices'][0]['text'].strip()
#     except Exception as e:
#         print("OpenAI API Error:", e)
#         return "Sorry, I couldn't process your request at the moment."

def command():

    rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio("listening.")
        print("listening:")

        rec.pause_threshold = 1
        query1 = rec.listen(source,timeout=5)
        
        try:
            print("Recognizing...")
            query = rec.recognize_google(query1, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("repeat that again please...")
            return "None"
        return query

query = ''
#TODO: 2: add more websites to the dictionary
d1 = {'youtube':"http://youtube.com",'wikipedia':"http://wikipedia.com",'facebook':"http://facebook.com"}



greet()
while True:
    # print("listening..")
    # audio("listening")
    query = command().lower()
    audio(query)
    
    for key,value in d1.items():
        if f"open {key}" in query:
            audio(f"opening {key}")
            webbrowser.open(f"{value}")
    if "weather" in query:
        words = query.split()
        if "weather" in words:
            index = words.index("weather")
            if index + 2 < len(words):
                city = " ".join(words[index + 2:])
                #TODO: 3: add your openweat api key after making a account on openweateher website.
                api_key = "YOUR API KEY"  
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()
                if data["cod"] == 200:
                    weather_info = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                    }
                    audio(f"The weather in {weather_info['city']} is {weather_info['description']} with a temperature of {weather_info['temperature']} degrees Celsius.")
                    print(f"The weather in {weather_info['city']} is {weather_info['description']} with a temperature of {weather_info['temperature']} degrees Celsius.")
                else:
                    audio("Sorry, I couldn't retrieve the weather information for that location.")
                    print("Sorry, I couldn't retrieve the weather information for that location.")
            else:
                audio("Please specify a city for the weather query.")
                print("Please specify a city for the weather query.")
        else:
            audio("Sorry, I couldn't understand the weather query.")
            print("Sorry, I couldn't understand the weather query.")
    
    
    if 'search wikipedia' in query:
            audio('Searching Wikipedia...')
            query = query.replace("search wikipedia for", "")
            results = wikipedia.summary(query, sentences=2)
            audio("According to Wikipedia")
            print(results)
            audio(results)   
    # if f"open youtube" in query.lower():
        # audio("ok")
        # webbrowser.open("https://youtube.com")
    elif 'search on youtube' in query:
        query = query.replace("search on youtube", "")
        webbrowser.open(f"www.youtube.com/resultssearch_query={query}")
        
    elif 'open youtube' in query:
        audio("what you will like to watch ?")
        qrry = command().lower()
        kit.playonyt(f"{qrry}")
    #TODO: 4: change the names of browser to be killed with your default browser for each operation. 
    elif 'close chrome' in query:
        os.system("taskkill /f /im chrome.exe")
        
    elif 'close youtube' in query:
        os.system("taskkill /f /im opera.exe")
    elif 'open google' in query:
        audio("what should I search ?")
        qry = command().lower()
        webbrowser.open(f"{qry}")
        results = wikipedia.summary(qry, sentences=2)
        audio(results)
        
    elif 'close google' in query:
        os.system("taskkill /f /im msedge.exe")
        
    elif 'play music' in query:
    #TODO: 5: add your local stored music directory.
        music_dir = "your music directory"
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, random.choice(songs)))
        
    elif 'play movie' in query:
    #TODO: 6: add your local stored movie path.
        npath = "your movie path" 
        os.startfile(npath)
        
    elif 'close movie' in query:
        os.system("taskkill /f /im vlc.exe")
        
        
    elif 'close music' in query:
        os.system("taskkill /f /im microsoft.media.player.exe")
        
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        (f"Sir, the time is {strTime}")
        
    elif "shut down the system" in query:
        os.system("shutdown /s /t 5")
        
    elif "restart the system" in query:
        os.system("shutdown /r /t 5")
        
    elif "Lock the system" in query:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "open notepad" in query:
        subprocess.Popen("notepad.exe")
        print("Notepad is now open.")
        
    elif "close notepad" in query:
        os.system("taskkill /f /im notepad.exe")
        
    elif "open command prompt" in query:
        os.system("start cmd")
        
    elif "close command prompt" in query:
        os.system("taskkill /f /im cmd.exe")
        
        
    elif "go to sleep" in query:
        audio(' alright then, I am switching off')
        sys.exit()
    elif "take screenshot" in query:
        audio('tell me a name for the file')
        name = command().lower()
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        audio("screenshot saved")
        
    elif "calculate" in query:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio("Ready for calculation")
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            a = r.listen(source)
            try:
                calculation = r.recognize_google(a)
                print("User said:", calculation)
                result = eval(calculation)
                audio(f"The result is {result}")
            except Exception as e:
                print("Error:", e)
                audio("Sorry, I couldn't understand the calculation.")
        
    elif "what is my ip address" in query:
        audio("Checking")
        try:
            ipAdd = requests.get('https://api.ipify.org').text
            print(ipAdd)
            audio("your IP address is")
            audio(ipAdd)
        except Exception as e:
            audio("network is weak, please try again some time later")
        






    elif "volume up" in query:
        for i in range(15):
            pyautogui.press("volumeup")
        
    elif "volume down" in query:
        for i in range(15):
            pyautogui.press("volumedown")
        
    elif "mute" in query:
        pyautogui.press("volumemute")
    # elif "search now" in query:
    #     query = query.replace("search now", "")
    #     results = openai_query(query)
    #     audio(results)     
    
    
    


    if "exit" in query.lower():
        audio("ok")
        break