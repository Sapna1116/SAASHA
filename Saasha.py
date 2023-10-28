
import pyttsx3 as pt
import datetime as dt
import speech_recognition as sr  # pip install SpeechRecognition
import wikipedia as wiki
import webbrowser as wb
import os
import pyautogui as pg
import time
import psutil
import pyjokes
import random

engine = pt.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
rate = 150
engine.setProperty('rate', rate)


def speak(msg):
    engine.say(msg)
    engine.runAndWait()


def tellDate():
    speak("Today is - ")
    time = dt.datetime.now().strftime("%d %B %Y %A")
    speak(time)


def tellTime():
    speak("Right now, The time is - ")
    time = dt.datetime.now().strftime("%I:%M:%S %p")
    speak(time)


def wishMe():
    hr = dt.datetime.now().hour
    if hr >= 6 and hr < 12:
        greeting = "Good Morning!!"
    elif hr >= 12 and hr < 18:
        greeting = "Good Afternoon!!"
    elif hr >= 18 and hr < 24:
        greeting = "Good Evening!!"
    else:
        greeting = "Hello!!"
    speak(greeting)
    speak("I am SAASHAA, Your Voice Assistant!")
    speak("How can I assist you today??")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        r.non_speaking_duration = 0.5
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language='en-IN')
            print("You said - " + command)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            print(e)
            speak("Pardon me...")
            return "None"
        return command


def search(query):
    try:
        speak("Searching...")
        result = wiki.summary(query, sentences=1)
        speak("According to Wikipedia...")
        printSpeak(result)
    except Exception as e:
        print(e)
        printSpeak("Please repeat... ")
        return "None"


def printSpeak(msg):
    print(msg)
    speak(msg)


def openWebsite(msg):
    # chromepath = "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    # printSpeak("What website should I open?")
    # website = takeCommand().lower()
    try:
        # wb.get(chromepath).open_new_tab("https://www." + msg + '.com')
        url = "https://www." + msg + '.com'.replace(" ", "")
        wb.open(url)
    except Exception as e:
        print(e)
        printSpeak("Could not open the web browser.")


def control_laptop(action):
    try:
        if action == 'shutdown':
            os.system("shutdown /s /t 0")
        elif action == 'restart':
            os.system("shutdown /r /t 0")
        elif action == 'sleep':
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif action == 'hibernate':
            os.system("shutdown /h")
        elif action == 'signout':
            os.system("shutdown /l")
        elif action == 'switchuser':
            os.system("tsdiscon")
    except Exception as e:
        print("An error occurred:", str(e))


def playSongs():
    songsDir = "D:\C - MUSIC"
    songs = os.listdir(songsDir)
    os.startfile(os.path.join(songsDir, songs[0]))


def remember():
    data = takeCommand()
    with open('data.txt', 'a') as rem:
        rem.write(data + "\n")
    printSpeak(data)


def repeatRemembered():
    try:
        with open('data.txt', 'r') as rem:
            data = rem.read()
            if data:
                printSpeak("Here's what I remember:")
                printSpeak(data)
            else:
                printSpeak("Nothing feeded to remembered.")
    except FileNotFoundError:
        printSpeak("File Not Found.")


def deleteData():
    try:
        with open('data.txt', 'w') as rem:
            rem.truncate(0)
        printSpeak("All stored information has been deleted.")
    except FileNotFoundError:
        printSpeak("There is no stored information to delete.")


screenshot_counter = 0
subfolder_path = r"C:\Users\Admin\Desktop\PROJECTS\Saasha\SAASHA_The_Voice_Assistant\screenShot\\"


def screenShot():
    global screenshot_counter
    img = pg.screenshot()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(
        subfolder_path, f"screenshot_{timestamp}_{screenshot_counter}.png")
    img.save(filename)
    screenshot_counter += 1
    speak(f"Screenshot taken successfully")


def cpuInfo():
    try:
        usage = psutil.cpu_percent()
        printSpeak("CPU is at - " + str(usage) + "%")

        total_ram = psutil.virtual_memory().total
        printSpeak(f"Total RAM: {total_ram / (1024 ** 3):.2f} GB")
        available_ram = psutil.virtual_memory().available
        printSpeak(f"Available RAM: {available_ram / (1024 ** 3):.2f} GB")

        disk_usage = psutil.disk_usage('/')
        printSpeak(
            f"Total Disk Space: {disk_usage.total / (1024 ** 3):.2f} GB")
        printSpeak(f"Used Disk Space: {disk_usage.used / (1024 ** 3):.2f} GB")

        battery = psutil.sensors_battery()
        if battery is not None:
            printSpeak(f"Battery Percent: {battery.percent}")
            printSpeak(f"Battery Status: {battery.power_plugged}")
        else:
            printSpeak("Battery information not available.")
    except AttributeError as e:
        print(e)
        printSpeak("The requested CPU information is not available.")


def tellJokes():
    joke = pyjokes.get_joke()
    speak(joke)


speak("Hello")

if __name__ == "__main__":
    while (True):
        query = takeCommand().lower()

        if any(keyword in query for keyword in ['hi', 'hello', 'hey', 'name']):
            wishMe()
        elif any(keyword in query for keyword in ['search', 'browse', 'find']):
            search(query)
        elif 'open' in query:
            openWebsite(' '.join(query.split()[1:]))
        elif any(keyword in query for keyword in ['google', 'web', 'browser']):
            wb.open("https://www.google.com")
        elif ('VS Code') in query:
            os.system("code")
        elif 'close' in query:
            printSpeak(
                "Choose option from (shutdown, restart, sleep, hibernate, signout, switchuser)")
            action = takeCommand().lower().replace(" ", "")
            control_laptop(action)
        elif any(keyword in query for keyword in ['songs', 'play']):
            playSongs()
        elif 'remember' in query:
            remember()
        elif 'repeat' in query:
            repeatRemembered()
        elif 'screenshot' in query:
            screenShot()
        elif 'cpu' in query:
            cpuInfo()
        elif 'joke' in query:
            tellJokes()
        elif any(keyword in query for keyword in ['delete', 'remove']):
            deleteData()
        elif any(keyword in query for keyword in ['date', 'day']):
            tellDate()
        elif 'time' in query:
            tellTime()
        elif any(keyword in query for keyword in ['offline', 'exit', 'quit', 'bye', 'goodbye', 'close']):
            speak("See Ya laters! Goodbye!")
            break
