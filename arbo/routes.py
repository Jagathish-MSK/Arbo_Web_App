from flask import render_template, url_for, redirect, flash, session, make_response
from pdfkit import from_string
from arbo.forms import Registration, Login
import speech_recognition as sr
from arbo import credentials
from arbo import app
import pyttsx3

import pyjokes
import pywhatkit
import wikipedia


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Registration()
    name = form.user_name.data
    email = form.email.data
    password = form.password.data
    if form.validate_on_submit():
        checking_name = credentials.name_check(name)
        check_email = credentials.email_check(email)
        if checking_name:
            flash("Sorry Username Already Exists", category="danger")
        elif check_email:
            flash('Sorry Email Already Used', category='danger')
        else:
            result = credentials.register(name, email, password)
            if result:
                flash(f"Account Created {form.user_name.data}", category="success")
                return redirect(url_for('login'))
    return render_template('register.html', title="Registration Page", form=form)


@app.route('/', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        username = form.user_name.data
        password = form.password.data
        res = credentials.login_validate(username, password)
        if res:
            session['logged_in'] = True
            session['name'] = username
            return redirect(url_for('home'))
        else:
            flash("Sorry, User not found Try again", category="danger")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/preview')
def preview():
    r = sr.Recognizer()
    Zira = pyttsx3.init()

    Zira.setProperty("rate", 130)

    Zira.say("Hai, I am VIHARA, Welcome to Arbo.com .")
    Zira.runAndWait()

    def For_Temp1():
        dict1 = {}
        per_det = ["Name", "father name", "Age", "Mobile Number"]

        for i in per_det:
            b = call_func(str(i))
            i = i.replace(" ", "")
            dict1[i] = b

        # edu_det = ["SSLC", "HSC", "UG", "Skill", "Interest"]
        # edu_det1 = ["School Name", "School Board", "Percentage", "Passed out year"]
        #
        # for i in edu_det:
        #     if i == "Interest" or i == "Skill":
        #         b = call_func(i)
        #         dict1[i] = b
        #         break
        #
        #     else:
        #         dict1[i] = {}
        #     for j in edu_det1:
        #         if i == "UG" and j == "School Name":
        #             j = "College Name"
        #         elif i == "UG" and j == "School Board":
        #             continue
        #         b = call_func(i + " " + j)
        #         n1 = i + j
        #         n1 = n1.replace(" ", "")
        #         dict1[i][n1] = b
        #
        # add_det = ["Door Number", "Street", "District", "City", "Pin Code", "Mobile Number", "E mail Id"]
        #
        # for i in add_det:
        #     b = call_func(str(i))
        #     i = i.replace(" ", "")
        #     dict1[i] = b
        return dict1

    def err_mes(func, arg, ob):
        obj = ob
        if "inter" in ob:
            obj = "interest"
        elif "skill" in ob:
            obj = "skill"
        try:
            val = r.recognize_google(arg)
            print("You have said " + r.recognize_google(arg))

            Zira.say(obj + " Added successfully ")
            Zira.runAndWait()
            return val
        except Exception as e:
            Zira.say("Sorry, there were some " + str(e) + " issues while trying to recognizing  " + str(obj))
            Zira.say("Please continue with recording " + str(obj))
            Zira.runAndWait()
            func(obj)

    def call_func(input1):
        with sr.Microphone() as source:
            ob = input1
            r.adjust_for_ambient_noise(source)
            if ob == 'Interest':
                Zira.say("Please tell only three Interest you have ")
                Zira.runAndWait()
                h = {}
                def inter(val1):
                    Zira.say("Please tell your " + str(val1))
                    Zira.runAndWait()
                    audio1 = r.listen(source)
                    ob1 = err_mes(inter, audio1, "inter" + str(val1))
                    return ob1

                for i in range(1, 4):
                    h[i] = inter(ob)
                return h
            elif ob == 'Skill':
                Zira.say("Please tell only four Skills you have ")
                Zira.runAndWait()
                h = {}

                def skill(val2):
                    Zira.say("Please tell your " + str(val2))
                    Zira.runAndWait()
                    audio1 = r.listen(source)
                    ob1 = err_mes(skill, audio1, "skill " + str(val2))
                    return ob1

                for i in range(1, 5):
                    h[i] = skill(ob)
                return h
            else:
                Zira.say("What is your " + input1)
                Zira.runAndWait()
                audio = r.listen(source)
                ob = err_mes(call_func, audio, ob)
                return ob

    val = For_Temp1()
    rd = render_template("preview.html", **locals())

    try:
        pdf = from_string(rd, 'ResumeTemplate1.pdf', css="arbo/static/css/Style1.css")
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    except Exception as e:
        return rd


@app.route('/preview2')
def preview2():
    r = sr.Recognizer()
    Zira = pyttsx3.init()
    Zira.setProperty("rate", 130)

    Zira.say("Hai, I am VIHARA, Welcome to Arbo.com .")
    Zira.runAndWait()

    def For_Temp1():
        dict1 = {}
        per_det = ["Name"]

        for i in per_det:
            b = call_func(str(i))
            i = i.replace(" ", "")
            dict1[i] = b

        edu_det = ["SSLC", "HSC", "UG", "Skill"]
        edu_det1 = ["School Name", "School Board", "Percentage"]

        for i in edu_det:
            if i == "Interest" or i == "Skill":
                b = call_func(i)
                dict1[i] = b
                break

            else:
                dict1[i] = {}
            for j in edu_det1:
                if i == "UG" and j == "School Name":
                    j = "College Name"
                elif i == "UG" and j == "School Board":
                    continue
                b = call_func(i + " " + j)
                n1 = i + j
                n1 = n1.replace(" ", "")
                dict1[i][n1] = b

        add_det = ["Door Number", "Street", "City", "Mobile Number", "E mail Id"]

        for i in add_det:
            b = call_func(str(i))
            i = i.replace(" ", "")
            dict1[i] = b

        Zira.say("Thank you for using Arbo.com, Please click on resume to download")
        Zira.runAndWait()
        return dict1

    def err_mes(func, arg, ob):
        obj = ob
        if "inter" in ob:
            obj = "interest"
        elif "skill" in ob:
            obj = "skill"
        try:
            val = r.recognize_google(arg)
            print("You have said " + r.recognize_google(arg))

            Zira.say(obj + " Added successfully ")
            Zira.runAndWait()
            return val
        except Exception as e:
            Zira.say("Sorry, there were some " + str(e) + " issues while trying to recognizing  " + str(obj))
            Zira.say("Please continue with recording " + str(obj))
            Zira.runAndWait()
            func(obj)

    def call_func(input1):
        with sr.Microphone() as source:
            ob = input1
            r.adjust_for_ambient_noise(source)
            if ob == 'Interest':
                Zira.say("Please tell only three Interest you have ")
                Zira.runAndWait()
                h = {}

                def inter(val1):
                    Zira.say("Please tell your " + str(val1))
                    Zira.runAndWait()
                    audio1 = r.listen(source)
                    ob1 = err_mes(inter, audio1, "inter" + str(val1))
                    return ob1

                for i in range(1, 4):
                    h[i] = inter(ob)
                return h
            elif ob == 'Skill':
                Zira.say("Please tell only four Skills you have ")
                Zira.runAndWait()
                h = {}

                def skill(val2):
                    Zira.say("Please tell your " + str(val2))
                    Zira.runAndWait()
                    audio1 = r.listen(source)
                    ob1 = err_mes(skill, audio1, "skill " + str(val2))
                    return ob1

                for i in range(1, 5):
                    h[i] = skill(ob)
                return h
            else:
                Zira.say("What is your " + input1)
                Zira.runAndWait()
                audio = r.listen(source)
                ob = err_mes(call_func, audio, ob)
                return ob

    val = For_Temp1()
    rd = render_template("preview2.html", **locals())

    try:
        pdf = from_string(rd, 'ResumeTemplate2.pdf', css="arbo/static/css/Style1.css")
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    except Exception as e:
        return rd


@app.route('/preview3')
def preview3():
    r = sr.Recognizer()
    Zira = pyttsx3.init()
    Zira.setProperty("rate", 130)

    Zira.say("Hai, I am VIHARA, Welcome to Arbo.com .")
    Zira.runAndWait()

    def For_Temp1():
        dict1 = {}
        per_det = ["Name", "Gender", "Date of Birth", "Marital Status"]

        for i in per_det:
            b = call_func(str(i))
            i = i.replace(" ", "")
            dict1[i] = b

        edu_det = ["SSLC", "HSC", "UG", "Skill", "Interest"]
        edu_det1 = ["School Name", "School Board", "Percentage", "Passed out year"]

        for i in edu_det:
            if i == "Interest" or i == "Skill":
                b = call_func(i)
                dict1[i] = b
                break

            else:
                dict1[i] = {}
            for j in edu_det1:
                if i == "UG" and j == "School Name":
                    j = "College Name"
                elif i == "UG" and j == "School Board":
                    continue
                b = call_func(i + " " + j)
                n1 = i + j
                n1 = n1.replace(" ", "")
                dict1[i][n1] = b

        add_det = ["Door Number", "Street", "District", "City", "Pin Code", "Mobile Number", "E mail Id"]

        for i in add_det:
            b = call_func(str(i))
            i = i.replace(" ", "")
            dict1[i] = b
        return dict1

    def err_mes(func, arg, ob):
        obj = ob
        if "inter" in ob:
            obj = "interest"
        elif "skill" in ob:
            obj = "skill"
        try:
            val = r.recognize_google(arg)
            print("You have said " + r.recognize_google(arg))

            Zira.say(obj + " Added successfully ")
            Zira.runAndWait()
            return val
        except Exception as e:
            Zira.say("Sorry, there were some " + str(e) + " issues while trying to recognizing  " + str(obj))
            Zira.say("Please continue with recording " + str(obj))
            Zira.runAndWait()
            func(obj)

    def call_func(input1):
        with sr.Microphone() as source:
            ob = input1
            r.adjust_for_ambient_noise(source)
            if ob == 'Interest':
                Zira.say("Please tell only three Interest you have ")
                Zira.runAndWait()
                h = {}

                def inter(val1):
                    Zira.say("Please tell your " + str(val1))
                    Zira.runAndWait()
                    audio1 = r.listen(source)
                    ob1 = err_mes(inter, audio1, "inter" + str(val1))
                    return ob1

                for i in range(1, 4):
                    h[i] = inter(ob)
                return h
            elif ob == 'Skill':
                Zira.say("Please tell only four Skills you have ")
                Zira.runAndWait()
                h = {}

                def skill(val2):
                    Zira.say("Please tell your " + str(val2))
                    Zira.runAndWait()
                    audio1 = r.listen(source)
                    ob1 = err_mes(skill, audio1, "skill " + str(val2))
                    return ob1

                for i in range(1, 5):
                    h[i] = skill(ob)
                return h
            else:
                Zira.say("What is your " + input1)
                Zira.runAndWait()
                audio = r.listen(source)
                ob = err_mes(call_func, audio, ob)
                return ob

    val = For_Temp1()
    # print(val)
    rd = render_template("preview3.html", **locals())

    try:
        pdf = from_string(rd, 'ResumeTemplate3.pdf', css="arbo/static/css/Style1.css")
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    except Exception as e:
        return rd



@app.route('/working')
def working():
    return render_template('working.html')


@app.route('/working2')
def working2():
    return render_template('working2.html')


@app.route('/working5')
def working3():
    return render_template('working3.html')


@app.route('/TemplatePreview')
def Temppreview():
    return render_template('TemplatePreview.html')


@app.route('/Template1')
def Temp1():
    return render_template('Template1_sample.html')


@app.route('/Template2')
def Temp2():
    return render_template('Template2_sample.html')


@app.route('/Template5')
def Temp5():
    return render_template('Template5_sample.html')


@app.errorhandler(404)
def something(e):
    return render_template('404.html')

@app.route('/sophia')
def sophia():
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
            joke = result.replace('play', ' ')
            first_joke = pyjokes.get_joke()
            engine.say(f'saying a {joke} for you')
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
    return('', 204)