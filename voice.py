import speech_recognition as sr
import pyttsx3
import pyjokes
import pywhatkit
import wikipedia

listener = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty("rate", 178)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def intro():
    engine.say("i am sophia")
    engine.say("how can i help you")
    engine.runAndWait()

list = ['color', 'place']

def machine(question):
    engine.say('what is my favourite' + question)
    engine.runAndWait()

def taking_command(value):
    try:
        with sr.Microphone() as src:
            if value:
                intro()
            print("Speak something....")
            listener.adjust_for_ambient_noise(src)
            user_audio = listener.listen(src)
            command = listener.recognize_google(user_audio)
            action_command(command)
    except:
        pass

def marry():
    answers = []
    for x in list:
        machine(x)
        into_list = taking_command(False)
        answers.append(into_list)
    print(answers)
    return answers

def action_command(command):
    result = command
    if 'joke' in result:
        first_joke = pyjokes.get_joke()
        engine.say('Here you go ')
        engine.say(first_joke)
        engine.runAndWait()
    elif 'play' in result:
        song = result.replace('play', ' ')
        engine.say(f'playing {song} for you')
        engine.runAndWait()
        pywhatkit.playonyt(result)
    elif 'send a message' in result:
        pywhatkit.sendwhatmsg('+91**********', 'good morning', 10, 32)
        print("message sent")
    elif 'marry' in result:
        engine.say("Am already in relationship with vihara")
        engine.say('if you still want to marry me then')
        engine.say('answer to questions first')
        count_answers = marry()
        if count_answers[0] == "blue" and count_answers[1] == "india":
            engine.say("you did it")
            engine.say("Kill vihara  baby we will marry soon")
            engine.runAndWait()
        else:
            engine.say("Sorry you dont know anything about me")
            engine.say("Get Lost idiot")
            engine.runAndWait()
    elif 'who is' in result:
        person = command.replace('who is', ' ')
        engine.say(wikipedia.summary(person, 1))
        engine.runAndWait()
    elif 'vihara' in result:
        engine.say('He is my boyfriend')
        engine.say('we are in relation from past 1 month')
        engine.runAndWait()
    return result

taking_command(True)