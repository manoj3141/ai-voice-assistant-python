import os
import random
import warnings
import re

# 🔕 Hide pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# 🔕 Suppress specific deprecation warning
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")
import time
import requests
from datetime import datetime

import pygame
import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser
from pathlib import Path
import subprocess
import pywhatkit as kit
import pygetwindow as gw
from ddgs import DDGS


from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chil_memory as cm
import chil_conversation as cc

# ------------------ Speech Setup ------------------
r = sr.Recognizer()
# ------------------ GLOBAL DRIVER ------------------
driver = None
current_index = 0
playlist = []
ispygame = False
isstop = False
isVideo = False
frnd = cc.frnd

# Music
music_path = Path.home() / "Music"


# AI initialise
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

# 🧠 memory store
messages = cm.messages

# FALLBACK MODELS
MODELS = [
    "deepseek/deepseek-chat",
    "mistralai/mistral-7b-instruct",
    "meta-llama/llama-3-8b-instruct",
    "google/gemma-2-9b-it",
]


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)  # faster like Jarvis
    print("🤖:", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


r.energy_threshold = 200  # ignore low noise
mic = sr.Microphone()

with mic as source:
    r.adjust_for_ambient_noise(source, duration=0.5)


def listen():
    with mic as source:
        print("🎙 Listening...")
        audio = r.listen(source, timeout=None)
    return audio


def cleanSymbols(speech):
    reply = re.sub(r"[*#@_\-•]+", "", speech)
    speak(reply)


def web_search(query):
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=1):
            cleanSymbols(r.get("body", ""))


def ask_ai(text):
    global messages
    try:
        # 👤 Add user message
        messages.append({"role": "user", "content": text})

        # 🧹 Keep memory small
        if len(messages) > 30:
            messages[:] = messages[:1] + messages[-28:]

        # 🔄 Try models one by one
        for model in MODELS:
            try:
                data = {
                    "model": model,
                    "messages": messages,
                    "temperature": random.uniform(0.2, 0.3),
                }
                # print(f"\n🔍 Trying model: {model}")

                res = requests.post(url, headers=headers, json=data, timeout=30)
                # ✅ Success
                if res.status_code == 200:
                    result = res.json()
                    reply = (
                        result.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )
                    if reply.strip():
                        cleanSymbols(reply)
                        # 💾 Save assistant reply
                        messages.append({"role": "assistant", "content": reply})
                        cm.save_AiMemory(messages)
                        return

            except Exception as model_error:
                print(f"⚠️ Error with {model}: {model_error}")
                continue
        # 🌐 If all AI models fail
        print("🌐 All AI models failed. Using web search...")
        web_search(text)

    except Exception as e:
        print("❌ AI Error:", e)
        web_search(text)


def load_playlist(folder_path=music_path):
    songs = []

    for root, dir, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".mp3", ".wav", ".ogg")):
                songs.append(os.path.join(root, file))

    return songs


def play_current():
    global current_index
    songName = playlist[current_index]
    speak(f"Playing song {os.path.basename(songName)}")
    pygame.mixer.music.load(songName)
    pygame.mixer.music.play()
    current_index = (current_index + 1) % len(playlist)


# ------------------ Greetings ------------------
def greet():
    hour = datetime.now().hour
    if hour < 12:
        speak("Good morning ")
    elif hour < 18:
        speak("Good afternoon boss ")
    else:
        speak("Good evening boss ")


# ------------------ CHECK INTERNET ------------------
def is_internet_available():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False


# ------------------ OPEN YOUTUBE ------------------
def open_youtube():
    global driver

    # Step 1: Check internet first 🌐
    if not is_internet_available():
        speak("No internet connection. Please check your network")
        return
    try:
        # Step 2: Open using Selenium 🤖
        if not check_app_status("youtube"):
            driver = webdriver.Edge()
            driver.get("https://www.youtube.com")
            speak("YouTube opened")
    except Exception as e:
        speak("Something went wrong while opening YouTube")


def check_app_status(name):
    for win in gw.getAllWindows():
        if name.lower() in win.title.lower():
            try:
                if isstop:
                    win.close()
                    speak(f"Closing {name} ")
                elif win.isActive:
                    win.maximize()
                else:
                    if not win.isMinimized:
                        win.minimize()
                    win.restore()
                    win.activate()
                    speak(f"Bringing {name} back to life")
            except Exception as e:
                speak(f"Can't to this operation for {name} due to system security")
            return True
    return False


def handleSearch(text, splitword):
    # If splitword not present, return full text (fallback)
    if splitword not in text:
        return text

    # Extract query safely
    parts = text.split(splitword, 1)
    query = parts[1].strip() if len(parts) > 1 else ""

    # Remove filler words
    words = query.split()
    if words and words[0] in {"for", "about"}:
        query = " ".join(words[1:])

    if not query:
        speak(f"What to {splitword} bro")
        return None

    return query


def play_video(query, isPlay=True):
    try:
        wait = WebDriverWait(driver, 10)

        box = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))
        box.clear()
        box.send_keys(query + Keys.RETURN)

        speak(f"Searching {query}")

        if isPlay:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '(//ytd-video-renderer//a[@id="thumbnail"])[1]')
                )
            ).click()

            speak(f"Playing {query} on YouTube")

    except WebDriverException:
        speak("Error playing video1")


def play_video_by_number(text):
    try:
        videos = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
        print(len(videos))
        if not videos:
            play_video(text)
            return

        num_map = {"first": 0, "second": 1, "third": 2, "fourth": 3, "fifth": 4}

        # ---- NUMBER MATCH ----
        for key, idx in num_map.items():
            if key in text and len(videos) > idx:
                print("click")
                videos[idx].click()
                print("sick")
                speak(f"Playing {key} video")
                return

        # ---- EXACT MATCH ----
        for v in videos:
            if text in v.text.lower():
                v.click()
                speak(f"Playing {text}")
                return

        # ---- PARTIAL MATCH ----
        words = text.split()
        for v in videos:
            title = v.text.lower()
            if any(w in title for w in words):
                v.click()
                speak(f"Playing {title}")
                return

        # ---- FALLBACK ----
        play_video(text)

    except Exception:
        speak("Error playing video")


def confirmOper(action):
    speak(f"Hey {frnd}, are you sure you want to {action}? say yes or no.")

    while True:
        reply = get_command()
        if "yes" in reply or "do it" in reply:
            speak(f"Alright {frnd}, {action} in progress ")
            return True

        elif "no" in reply or "cancel" in reply:
            speak(f"Okay {frnd}, cancelled 👍")
            return False

        elif reply == "":
            continue

        else:
            return False


def playYoutubeMusic(query):
    open_youtube()
    if driver is not None:
        play_video(query)
    else:
        kit.playonyt(query)
        speak(f"Playing {query} on YouTube ▶️")


def get_command():
    command = r.recognize_google(listen()).lower().strip()
    print("🧑 You:", command)
    return command


# ------- check app visible ------
def is_app_shown(title):
    for win in gw.getAllWindows():
        if title.lower() in win.title.lower():
            if win.isActive:
                return True
    return False


# ----------- play,search,type handling ---------


def handle_media_command(text):
    for cmd in ["search", "type"]:
        if cmd in text:
            query = handleSearch(text, cmd)
            if query:
                play_video(query, False)
                return True

    # ---- PLAY / CLICK ----
    if ("play" in text or "click" in text) and (
        not isVideo or ("next" not in text and text != "play")
    ):
        query = handleSearch(text, "play")
        if query:
            play_video_by_number(query)
            return True

    return False


# ---------- volume Control -------------


def volumeControl(text):
    if "volume" in text:
        if any(w in text for w in ["increase", "raise", "up", "maximise"]):
            pyautogui.press("volumeup")
            return True
        elif any(w in text for w in ["decrease", "reduce", "down", "minimise"]):
            pyautogui.press("volumedown")
            return True
    return False


def openAppsCommands(text, first_word):
    global isstop

    isstop = first_word in ("exit", "close")
    if "youtube" in text:
        open_youtube()
        if len(text.split()) > 2:
            handle_media_command(text)
    elif (any(w in text for w in ("map","location","where am i","my place"))):
        speak(f"Tracking you like a satellite, {frnd}.")
        webbrowser.open("https://www.google.com/maps/@?api=1&map_action=map")

    elif "google" in text:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    else:
        apps = {
            "notepad": {
                "keywords": ["notepad", "notes"],
                "cmd": ["notepad"],
            },
            "calculator": {
                "keywords": ["calculator", "calc"],
                "cmd": ["calc"],
            },
            "command prompt": {
                "keywords": ["cmd", "command prompt", "terminal"],
                "cmd": ["cmd"],
            },
            "powershell": {
                "keywords": ["powershell"],
                "cmd": ["powershell"],
            },
            "task manager": {
                "keywords": ["task manager", "tasks"],
                "cmd": ["taskmgr"],
            },
            "settings": {
                "keywords": ["settings", "windows settings"],
                "cmd": ["explorer", "ms-settings:"],
            },
            "file explorer": {
                "keywords": ["explorer", "files", "file manager"],
                "cmd": ["explorer"],
            },
            "control panel": {
                "keywords": ["control panel"],
                "cmd": ["control"],
            },
            "chrome": {
                "keywords": ["chrome", "google chrome"],
                "cmd": ["start", "chrome"],
            },
            "edge": {
                "keywords": ["edge", "microsoft edge", "browser"],
                "cmd": ["msedge"],
            },
            "snipping tool": {
                "keywords": ["snip", "snipping tool", "screenshot"],
                "cmd": ["snippingtool"],
            },
            "paint": {
                "keywords": ["paint", "mspaint"],
                "cmd": ["mspaint"],
            },
        }
        for app, data in apps.items():
            if any(keyword in text for keyword in data["keywords"]):
                if not check_app_status(app):
                    try:
                        subprocess.Popen(data["cmd"])
                    except Exception:
                        speak(f"I could not open {app}")
                return
        # ✅ fallback OUTSIDE loop
        if isstop:
            pyautogui.hotkey("alt", "f4")
            return
        app_name = text.replace("open ", "")
        if not app_name:
            speak(f"Tell the App Name to open, {frnd}")
            return
        pyautogui.press("win")
        time.sleep(1)

        # Type app name
        pyautogui.write(app_name)
        time.sleep(1)

        # Press Enter
        pyautogui.press("enter")


# ------------------ Core Brain ------------------
def handle_command(text, first_word):
    global driver
    global ispygame
    global current_index
    global playlist
    global isVideo

    # 🎮 Notepad Controls:
    if is_app_shown("Notepad"):
        # 🎤 START TYPING MODE
        if "start typing" in text:
            typing_mode = True
            speak("Typing mode activated")

            while typing_mode:
                command = get_command()

                if "stop typing" in command:
                    typing_mode = False
                    speak("Stopped typing")
                elif command != "":
                    pyautogui.write(command + " ", interval=0.05)
        else:
            for i in ("type", "write", "delete", "remove", "cut"):
                if i in first_word:
                    msg = text.replace(i, "", 1).strip()

                    if not msg:
                        speak(f"What should I {i}?")
                        return

                    match i:
                        case "type" | "write":
                            # your typing logic here
                            speak(f"Typing {msg}")

                        case "delete" | "remove":
                            # your delete logic here
                            speak("Deleting text")

        # elif "copy" in command:
        #     edit.type_keys("^a")  # select all
        #     edit.type_keys("^c")
        # elif "cut" in command:
        #     edit.type_keys("^a")
        #     edit.type_keys("^x")
        #     speak("Cut everything")
        # elif "paste" in text:
        #     edit.type_keys("^v")
        #     speak("Pasted")

        # elif "select all" in text:
        #     edit = connect_notepad()
        #     edit.type_keys("^a")
        # elif "":
        #     edit.type_keys("{BACKSPACE}")
        # elif "undo" in command:
        #     edit.type_keys("^z")

        # elif "redo" in command:
        #     edit.type_keys("^y")

        # elif "new line" in command:
        #     edit.type_keys("{ENTER}")

        # elif "delete last word" in command:
        #     edit.type_keys("^+{LEFT}")  # select last word
        #     edit.type_keys("{BACKSPACE}")

        # elif "clear" in command:
        #     edit.set_edit_text("")
        #     speak("Cleared all text")

        # elif "save" in command:
        #     edit.type_keys("^s")

        #     speak("What should be the file name?")
        #     filename = get_command()

        #     edit.type_keys(filename + ".txt", with_spaces=True)
        #     edit.type_keys("{ENTER}")

        #     speak("File saved")
    # 🎮 Youtube Controls:

    elif is_app_shown("YouTube"):
        if driver is not None:
            isVideo = "watch" in driver.current_url
            if handle_media_command(text):
                return

            elif any(
                w in text
                for w in ("full screen", "minimise", "minimize", "reduce video")
            ):
                if isVideo:
                    driver.find_element(By.TAG_NAME, "body").send_keys("f")

            elif isVideo and any(
                w in text for w in ("play", "pause", "stop", "resume")
            ):
                driver.find_element(By.TAG_NAME, "body").send_keys("k")

            elif "next" in text and isVideo:
                speak("playing Next video")
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SHIFT, "n")

            elif volumeControl(text):
                return

            elif any(w in text for w in ["mute", "silence", "quiet"]):
                driver.find_element(By.TAG_NAME, "body").send_keys("m")

            elif "scroll down" in text or "move down" in text:
                driver.execute_script("window.scrollBy(0, 800);")

            elif "scroll up" in text or "move up" in text:
                driver.execute_script("window.scrollBy(0, -800);")

            elif "back" in text:
                driver.back()

            elif "home" in text:
                driver.get("https://www.youtube.com")
                speak("Opening Home")

            elif "shorts" in text:
                driver.get("https://www.youtube.com/shorts")
                speak("Opening Shorts")

            elif "library" in text:
                driver.get("https://www.youtube.com/feed/library")
                speak("Opening Library")

        # manual youtube commands
        else:
            if "search" in text:
                query = handleSearch(text, "search")
                if query:
                    pyautogui.press("/")  # focus search bar
                    pyautogui.write(query, interval=0.05)
                    pyautogui.press("enter")
            elif any(w in text for w in ("play", "pause", "stop", "resume")):
                pyautogui.press("k")

            elif "next" in text:
                pyautogui.hotkey("shift", "n")

            elif volumeControl(text):
                return

            elif any(w in text for w in ["mute", "silence", "quiet"]):
                pyautogui.press("m")

            elif any(w in text for w in ("full screen", "maximise", "maximize")):
                pyautogui.press("f")

            elif "forward" in text:
                pyautogui.press("right")

            elif "back" in text:
                pyautogui.press("left")

            elif "close" in text:
                pyautogui.hotkey("alt", "f4")
                speak("Browser closed")

    elif "search" in text:
        query = handleSearch(text, "play")
        if not query:
            speak(f"Searching for {query} {frnd}")
            webbrowser.open(f"https://www.google.com/search?q={query}")

    elif pygame.mixer.music.get_busy() or (
        ispygame and ("resume" in text or "change music" in text)
    ):

        # 🛑 Stop / Pause
        if "stop" in text or "pause" in text:
            pygame.mixer.music.pause()
            speak(f"Paused the music. Say resume when you're ready {frnd}")

        # ⏭ Next song
        elif "change" in text or "next" in text:
            pygame.mixer.music.stop()
            speak("Skipping to the next track")
            play_current()

        # ⏮ Previous song
        elif "previous" in text:
            pygame.mixer.music.stop()
            if current_index > 1:
                current_index -= 2
                speak("Going back to the previous track ")
                play_current()

            else:
                speak(f"You're already at the first song {frnd}🎵")

        # ▶ Resume
        elif "resume" in text:
            pygame.mixer.music.unpause()
            speak(f"Back to the music {frnd} 🎶")

    # ---- Music ----
    elif any(w in text for w in ["play music", "start music", "some music","my favourite song"]):
        playlist = load_playlist()
        if playlist:
            ispygame = True
            pygame.mixer.init()
            play_current()
            return
        speak(f"Music not found in this {music_path}{frnd}, playing in youtube")
        playYoutubeMusic("music")

    elif first_word == "play":
        query = handleSearch(text, "play")
        playYoutubeMusic(query)

    # ---- Screenshot ----
    elif "screenshot" in text:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # ---- Notes ----
    elif "take note" in text:
        speak("What should I write?")
        note = listen()
        with open("notes.txt", "a") as f:
            f.write(note + "\n")
        speak("Note saved")

    # ---- System Control ----
    elif "shutdown" in text or "shut down" in text:
        if confirmOper("shutdown the system"):
            os.system("shutdown /s /t 5")

    elif "restart" in text:
        if confirmOper("restart the system"):
            os.system("shutdown /r /t 5")

    else:
        ask_ai(text)


speak(cc.welTxt)
loopCount = 0
listening = True
while True:
    try:
        command = get_command()
        first_word = command.split()[0]

        listening = (
            False
            if "sleep" in command
            else True if ("wake up" in command or "hey chil" in command) else listening
        )

        # 🚫 Ignore everything if not listening
        if not listening:
            continue

        # 🪟 Window controls
        if command in ("maximise", "maximize", "maximise it"):
            pyautogui.hotkey("win", "up")
        elif first_word in ("minimise", "minimize") and not isVideo:
            for _ in range(2):
                pyautogui.hotkey("win", "down")

        # 🚀 App commands
        elif first_word in ("open", "show", "maximize", "maximise", "exit", "close"):
            openAppsCommands(command, first_word)

        # 🧠 Conversation handler
        elif cc.handle_conv_command(command, first_word, loopCount):
            pass

        else:
            handle_command(command, first_word)

    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        speak("Network issue detected")
    loopCount += 1
