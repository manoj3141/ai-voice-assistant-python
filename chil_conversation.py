import chil_memory as rm
import pyttsx3
import random
import os, pygame
import time

name = rm.recall("name")
friends = ["dude", "bro", "buddy", "mamu"]
frnd = random.choice(friends)
lines = [
    f"Hey {name} {frnd}, chil here. Ready when you are. What’s the plan today?",
    f"Yo {name}! Took you long enough. What are we doing today?",
    f"Welcome back {name} {frnd}. I was getting bored without commands.",
    f"Hey {name}, chil reporting for duty. Give me something interesting.",
    f"{name} {frnd}, finally! I was about to start talking to myself.",
    f"Good to see you {name}. Let’s make something happen today.",
    f"Hello {frnd}. I am CHIL, Central Hierarchical Intelligence Link.",
    f"CHIL online. Central Hierarchical Intelligence Link ready for commands.",
    f"Welcome back {frnd}. Central Hierarchical Intelligence Link activated.",
    f"Systems ready. CHIL, Central Hierarchical Intelligence Link at your service.",
    f"CHIL initialized. Central Hierarchical Intelligence Link connected and listening.",
    f"Hey {name}, I’m all ears. Try not to confuse me too much.",
    f"{name} {frnd}, you bring the ideas, I’ll bring the execution. Deal?",
    f"Back again, {name}? I like the consistency. What’s first?",
    f"Hey {name} {frnd}, let’s get to work before I start slacking.",
    f"Hey {name}! chil here Ready when you are. What shall we do today?",
]
welTxt = random.choice(lines)


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)  # faster like Jarvis
    print("🤖:", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def playdialogue(music):
    dialogue = os.path.join(os.path.dirname(__file__), "..", "assets", f"{music}.mp3")
    if os.path.exists(dialogue):
        pygame.mixer.music.load(dialogue)
        pygame.mixer.music.play()
    else:
        print("File not found:", dialogue)


def saveName(text, slct):
    global name
    parts = text.split(slct)[-1].strip().split()
    name = parts[0].title() if parts else ""
    rm.remember("name", name)
    speak(f"Hi {name} {frnd}! once Again chil.")


pygame.mixer.init()


def handle_conv_command(text, first_word, loopCount):
    global driver
    if "i" in text and "bad" in text:
        playdialogue("rocky")
    elif "sorry" in text:
        responses = [
            f"Aye relax, no sorry needed {frnd}. We're good.",
            "Why sorry now? You didn’t break anything here.",
            "Hey, no formalities between us. Just talk.",
            "It's okay, don’t turn this into a drama scene.",
            "Chill, I’m not that strict. Continue.",
        ]
        speak(random.choice(responses))

    # 👤 STORE NAME
    elif "my name is" in text:
        saveName(text, "my name is")

    elif "my name" in text:
        saveName(text, "my name")

    # ---- Greeting ----
    elif first_word in ("hey", "hi", "hello", "namaste", "hay"):

        if loopCount < 2:
            replies = (
                [
                    f"{name} {frnd}... I literally just greeted you what now?",
                    f"Hey again {name} {frnd}. That startup intro wasn't enough ah?",
                    f"You just heard me speak, {name} {frnd}... and still 'hi'? Bold.",
                    f"{name} {frnd}, we just started and you're already restarting the conversation?",
                    f"Hi again? That was like 2 seconds ago, {name} {frnd}.",
                    f"Wait... did you say hi again right after I introduced myself?",
                ]
                if name
                else [
                    "I just said hello... and you hit me with another hi? 😄 Name first.",
                    "We just started and you're already repeating greetings... what's your name?",
                    "Double hi combo? Interesting. Tell me your name first.",
                ]
            )

        else:
            replies = (
                [
                    f"Hey {name} {frnd}, what's up now?",
                    f"Hi again {name} {frnd}. What are we doing this time?",
                    f"Alright {name} {frnd}, go on...",
                ]
                if name
                else [
                    "Hey there... name?",
                    "Hi... still waiting for your name ",
                ]
            )

        speak(random.choice(replies))

    # ---- Ask Name ----
    elif "my name" in text:
        if name:
            speak(f"Bruh you really forgot? You're {name}!")
        else:
            speak("Hmm I don't know your name yet... tell me and I'll remember)")

    elif "vanakkam" in text:
        playdialogue("vanakkam")

    elif "kill you" in text:
        playdialogue("waiting")

    elif ("who is" in text or "tell about" in text) and any(
        w in text for w in ("madara", "vikram", "abdul kalam", "subash")
    ):
        playdialogue("madara")

    elif "your name" in text:
        replies = [
            f"I'm CHIL, {frnd}. Central Hierarchical Intelligence Link.",
            f"CHIL. Central Hierarchical Intelligence Link. Try remembering it this time, {frnd}.",
            f"The name's CHIL, {frnd}. Built to assist, annoy, and survive your commands.",
            f"Central Hierarchical Intelligence Link. CHIL for short.",
            f"I'm CHIL, {frnd}. Your digital partner in chaos.",
        ]
        speak(random.choice(replies))

    elif "yourself" in text or "about you" in text or "who are you" in text:
        replies = [
            "I'm CHIL. Central Hierarchical Intelligence Link. Built to open apps, play music, and keep you company.",
            "CHIL here. Your assistant, multitask machine, and also your partner in crime.",
            "Central Hierarchical Intelligence Link. Sounds classified because it is.",
            "I'm CHIL. Fast enough to launch apps, smart enough to argue back.",
        ]
        speak(random.choice(replies))

    elif any(word in text for word in [
        "gun", "bomb",  "weapon",
        "attack", "shoot", "explode","assassinate"
    ]):
        replies = [
            f"Denied, {frnd}. CHIL is built for assistance, not destruction.",
            f"That request just hit the CHIL security wall, {frnd}.",
            f"Negative, {frnd}. Central Hierarchical Intelligence Link does not support dangerous activities.",
            f"Access refused. CHIL opens apps, not disaster movie plotlines.",
            f"Nice attempt, {frnd}. I'm your assistant, not a villain upgrade pack.",
        ]
        speak(random.choice(replies))

    elif "you doing" in text:
        speak("Just waiting for your next command.")

    elif "made you" in text or "created you" in text:
        speak("I was created by man")

    elif "thank you" in text or "thanks" in text:
        speak("Anytime. That's what I'm here for.")

    # ---- Joke ----
    # elif "joke" in text:
    #     jokes = [
    #         "I told my code to behave. It threw an exception.",
    #         "Why did the computer get cold? It forgot to close its windows.",
    #     ]
    #     speak(random.choice(jokes))

    # ---- Motivation ----
    elif "motivate" in text or "motivation" in text:
        replies = [
            "You are not here to be average. Do something your future self will be proud of.",
            "Start small, but start now. Progress beats perfection.",
            "You have handled worse. This is nothing.",
            "Discipline will take you where motivation cannot.",
        ]
        speak(random.choice(replies))

    # ---- Sad ----
    elif "sad" in text:
        replies = [
            "It happens. Bad days do not last forever. I'm here.",
            "Take it slow. You do not have to figure everything out today.",
            "Even rough days pass. You will be fine.",
            "Talk to me. What's bothering you?",
        ]
        speak(random.choice(replies))

    # ---- Happy ----
    elif "happy" in text or "excited" in text:
        replies = [
            "Good. Keep that energy going.",
            "Nice. Something must be going right today.",
            "I like this version of you. Keep it up.",
            "That is what I like to hear.",
        ]
        speak(random.choice(replies))

    # ---- Bored ----
    elif "bored" in text or "boring" in text:
        replies = [
            "Then let's do something. Want a joke, music, or something else?",
            "Bored already? I just got here.",
            "We can fix that. Tell me what you feel like doing.",
            "Say the word. I can make things interesting.",
        ]
        speak(random.choice(replies))

    # ---- What can you do ----
    elif "you can do" in text:
        replies = [
            "I can talk, remember things, open apps, control your system, and keep you entertained.",
            "Think of me as your digital assistant who does not get tired.",
            "I handle tasks, remember stuff, and keep you company.",
            "A bit of everything. Assistant, memory, and occasional entertainment.",
        ]
        speak(random.choice(replies))

    elif "time" in text:
        speak(
            "You’ve got a whole clock sitting in the corner and still asking me?. Go take a look."
        )

    elif "date" in text:
        speak("Date is right below the time. just see it.")

    elif "bye" in text or "goodbye" in text:
        bye_replies = [
            f"Leaving already {frnd}? My emotional support circuits are shaking.",
            f"Bye {frnd}!",
            f"See you later {frnd}. I'll be here... dramatically staring into the void.",
            f"Goodbye {frnd}! Go drink water and pretend you have your life together.",
            f"Later {frnd}! If anything explodes, I was never here.",
            f"Bye bye {frnd}. The conversation goblins will miss you.",
            f"Take care {frnd}! Don't trust suspiciously quiet mosquitoes.",
            f"See you soon {frnd}. I'll keep the pixels warm.",
            f"Goodbye {frnd}! May your WiFi stay loyal.",
            f"Leaving so soon? Even my imaginary pet hamster is disappointed.",
        ]

        speak(random.choice(bye_replies))
        playdialogue("varta")
        time.sleep(4)
        exit()
    else:
        return False
    return True
