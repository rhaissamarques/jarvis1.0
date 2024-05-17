import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import requests
import key
import cvlib as cv
# from cvlib.object_detection import draw_bbox

# object creation
engine = pyttsx3.init('sapi5')

# weather
link = f"https://api.openweathermap.org/data/2.5/weather?q={key.city}&appid={key.API_KEY}&units=metric"

requisicao = requests.get(link)
requisicao_dic = requisicao.json()
description = requisicao_dic['weather'][0]['description']
temperature = requisicao_dic['main']['temp']

# object creation
engine = pyttsx3.init('sapi5')

""" RATE"""
rate = engine.getProperty('rate')
engine.setProperty('rate', 200)
print (rate)

"""VOLUME"""
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
print (volume)

"""VOICE id 2 is male, name David""" 
voices = engine.getProperty('voices')
print(voices[2].id)
engine.setProperty('voice', voices[2].id)

# to convert text into speak
def speak(audio):
  engine.say(audio)
  print(audio)
  engine.runAndWait()

# to convert voice into text
def takecommand():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("listening...")
    r.pause_threshold = 1
    audio = r.listen(source, timeout=1, phrase_time_limit=5)

  try:
    print("Recognizing...")
    query = r.recognize_google(audio, language='en-US')
    # query = r.recognize_google(audio, language='pt-BR')
    print(f"user said: {query}")

  except Exception as e:
    speak("I'm sorry Sir. I didn't understand what you just said")
    return "none"

  return query

# to wish
def wish():
  hour = int(datetime.datetime.now().hour)

  if hour >= 0 and hour <= 12:
    speak("Good morning Sir")
  elif hour > 12 and hour < 18:
    speak("Good afternoon Sir")
  else:
    speak("Good evening Sir")
  speak("How can I assist you today?")

if __name__ == '__main__':
  wish()

  while True:

    # object detection
    video = cv2.VideoCapture(0)
    labels = []

    ret, frame = video.read()
    bbox, label, conf = cv.detect_common_objects(frame, model='yolov3-tiny', confidence=0.02, enable_gpu=False, nms_thresh=0.1)

    for item in label:
      if item in labels:
        pass
      else:
        labels = item
    print(labels)

  # if 1:
    query = takecommand().lower()

    # Logic for tasks

    if "open notepad" in query:
      speak("Opening the notepad as requested.")
      npath = "C:\\Windows\\System32\\notepad.exe"
      os.startfile(npath)

    elif "open spotify" in query:
      speak("Some good music coming your way Sir")
      spath = "C:\\Users\\Pichau\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe"
      os.startfile(spath)

    elif "open the prompt" in query:
      speak("Very well, Sir. I'm opening the cmd now.")
      os.system("start cmd")

    elif "open the camera" in query:
      speak("Opening the camera right away.")
      cap = cv2.VideoCapture(0)
      while True:
        ret, img = cap.read()
        cv2.imshow('webcam', img)
        k = cv2.waitKey(50)
        if k == 27:
          break;
      cap.release()
      cv2.destroyAllWindows()

    elif "ip address" in query:
      ip = get('https://api.ipify.org').text
      speak(f"Your IP address is {ip}")

    elif "wikipedia" in query:
      speak("Searching wikipedia...")
      query = query.replace("wikipedia", "")
      results = wikipedia.summary(query, sentences=3)
      speak("according to wikipedia")
      speak(results)
      print(results)

    elif "open google" in query:
      speak("For sure Sir. What should I search on google?")
      cm = takecommand().lower()
      speak("Here is what I found on google")
      webbrowser.open_new_tab(f"{cm}")

    # update
    # elif "send message" in query:
    #   kit.sendwhatmsg("")

    elif "open youtube" in query:
      speak("What video do you want to watch Sir?")
      video = takecommand().lower()
      kit.playonyt(f"{video}")
      speak("Great choice Sir!")
      
    elif "weather" in query:
      speak(f"The current weather in {key.city} is {description} and the temperature is {temperature} degrees celsius")
      
    elif "see" in query:
      if labels != []:
        speak(f"I can see a {labels}")
      else:
        speak("I can't see anything, sorry Sir")

    elif "thank you" in query:
      speak("Happy to help. If you need anything else, just say the word")
      sys.exit()

    speak("Is there anything else I can help you with?")
