import pyttsx3
import subprocess
import wolframalpha
import webbrowser
import pywhatkit as kt
#import json
import shutil
import random
from datetime import datetime
import operator
import wikipedia
import random
import requests
import time
import os
import speech_recognition as sr
#from rbp import *
import RPi.GPIO as GPIO
import threading

engine=pyttsx3.init("espeak")
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[11].id)
engine.setProperty('rate',150)
GPIO.setwarnings(False)
servo1 = 12
servo2 = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)

def speak_motion_start():
    s1 = GPIO.PWM(servo1, 50) # GPIO 17 for PWM with 50Hz
    #s2 = GPIO.PWM(servo2, 50)
    s1.start(2.5) # Initialization
    #s2.start(2.5)
    try:
        while True:
            global stop_threads
            if(stop_threads==True):
                s1.ChangeDutyCycle(7.5)
                #s2.ChangeDutyCycle(10)
                break
            s1.ChangeDutyCycle(10)
            #s2.ChangeDutyCycle(5)
            time.sleep(0.2)
            s1.ChangeDutyCycle(7.5  )
            #s2.ChangeDutyCycle(7.5)
            time.sleep(0.2)
            '''s1.ChangeDutyCycle(10)
            s2.ChangeDutyCycle(5)
            time.sleep(0.2)'''
            
    except KeyboardInterrupt:
      s1.stop()
      s2.stop()
      GPIO.cleanup()


def speak(audio):
    global stop_threads
    engine = pyttsx3.init()
    t1 = threading.Thread(target=speak_motion_start, name='t1')
    stop_threads = False
    engine.say(audio)
    t1.start()
    engine.runAndWait()
    stop_threads = True
    t1.join()
    
def username():
    speak("What should I call you?")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns=shutil.get_terminal_size().columns
    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))
    
    speak("How can i Help you, Sir")
    
def takeCommand():
     
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,phrase_time_limit=5)
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
        return "None" 
     
    return query
if _name_ == '_main_':
    clear = lambda: os.system('cls')
    clear()
    username()
    while True:
         
        query = takeCommand().lower()
         
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results=wikipedia.summary(query,4)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            
        elif 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'how are you' in query or 'how have you been' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")
 
        elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine")
        elif 'who made you' in query or 'who is your creator' in query:
            speak("I was created by you")
        elif 'favorite food' in query:
            speak("I would love a pizza")
        elif 'joke' in query:
            a=["When does a joke become a dad joke? It's very apparent"
            ,"What do you call a boomerang that won’t come back? A stick"
            ,"What does a cloud wear under his raincoat? Thunderwear"
            ,"Two pickles fell out of a jar onto the floor. What did one say to the other? Dill with it."
            ,"What time is it when the clock strikes 13? Time to get a new clock."
            ,"A blind man walked into a bar, then a table, and then a chair."
            ,"What do you call a person with no body and no nose? Nobody knows."
            ,"A Spanish magician said that he is going to vanish at the count of 3. He said 'uno, dos' and poof! He disappeared without a tres."]
            ans=random.choice(a)
            print(ans)
            speak(ans)
        elif 'what can you do' in query:
            b=["I am a Speech Assistant, much like the Google Assistant or Alexa that you are, no doubt, familiar with"
               ,"I am a Speech Assistant, but beware for my programming is quite limited"
               ,"I can open a few commonly used websites"
               ,"I can give a few generic responses to generic, boring questions"]
            resp=random.choice(b)
            print(resp)
            speak(resp)
            
            
        elif 'who are you' in query or 'what are you' in query or 'what is your name' in query:
             b=["I am the bot you programmed. Did you forget lol?"
                ,"My name is Natasha, nice to meet you!"]
             speak(random.choice(b))
        elif 'open google' in query:
            speak("Opening Google...\n")
            webbrowser.open("google.com")
        elif 'date and time' in query or "today's date and time" in query:
            now=datetime.now()
            d_string=now.strftime("%m/%d/%y")
            speak("The current date is")
            speak(d_string)
            t_string=now.strftime("%H:%M%S")
            speak("The current time is")
            speak(t_string)
        elif "current time" in query:
            now=datetime.now()
            t_string=now.strftime("%H:%M%S")
            speak("The current time is")
            speak(t_string)
        elif "current date" in query:
            now=datetime.now()
            d_string=now.strftime("%m/%d/%y")
            speak("The current time is")
            speak(d_string)
        elif "google" in query:
            query=query.replace("search google for","")
            target=query
            speak("Searching google for")
            speak(query)
            kt.search(target)