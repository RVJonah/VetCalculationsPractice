import os
import smtplib
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import or_, and_, not_, desc, func
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sslify import SSLify
from VNCalculator import Cat, Dog, Rabbit, Tablet, Fluids, Gasflow, Liquid, Injectable, testGen
from helpers import login_required, apology


# Configure application
app = Flask(__name__)
sslify = SSLify(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://xywgxwohkpazsi:0957cae8ba1949f4856ee6e9f67b12813fad1b5db143ab87bd5f12c90cf278d3@ec2-54-228-252-67.eu-west-1.compute.amazonaws.com:5432/d6jlevpabapb7l"
db = SQLAlchemy(app)
Session(app)

class students(db.Model):
    __tablename__ = 'students'
    id = db.Column( 'id', db.Integer, primary_key=True)
    firstname = db.Column('firstname', db.String(255), nullable=False)
    lastname = db.Column('lastname', db.String(255), nullable=False)
    hash = db.Column('hash', db.String(512), nullable=False)
    college = db.Column('college', db.String(255),nullable=True)
    email = db.Column('email', db.String(512), nullable=False)
    username = db.Column('username', db.String(255), nullable=False)


class results(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    result = db.Column(db.Integer, nullable=False)
    test_type = db.Column(db.String(10))

    def __repr__(self):
        return f"User: '{self.id}', Primary Key'{self.Primary_Key}'"


class test_answers(db.Model):
    __tablename__ = 'test_answers'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    a0 = db.Column('a0', db.Float, nullable=True)
    a0min = db.Column('a0min', db.Float, nullable=True)
    a1 = db.Column('a1', db.Float, nullable=True)
    a1min = db.Column('a1min', db.Float, nullable=True)
    a2 = db.Column('a2', db.Float, nullable=True)
    a2min = db.Column('a2min', db.Float, nullable=True)
    a3 = db.Column('a3', db.Float, nullable=True)
    a3min = db.Column('a3min', db.Float, nullable=True)
    a4 = db.Column('a4', db.Float, nullable=True)
    a4min = db.Column('a4min', db.Float, nullable=True)
    a5 = db.Column('a5', db.Float, nullable=True)
    a5min = db.Column('a5min', db.Float, nullable=True)
    a6 = db.Column('a6', db.Float, nullable=True)
    a6min = db.Column('a6min', db.Float, nullable=True)
    a7 = db.Column('a7', db.Float, nullable=True)
    a7min = db.Column('a7min', db.Float, nullable=True)
    a8 = db.Column('a8', db.Float, nullable=True)
    a8min = db.Column('a8min', db.Float, nullable=True)
    a9 = db.Column('a9', db.Float, nullable=True)
    a9min = db.Column('a9min', db.Float, nullable=True)

    def __init__(self, id=0, a0=0, a0min=0, a1=0, a1min=0, a2=0, a2min=0, a3=0, a3min=0, a4=0, a4min=0,
                a5=0, a5min=0, a6=0, a6min=0, a7=0, a7min=0, a8=0, a8min=0, a9=0, a9min=0):
        self.id = id
        self.a0 = a0,
        self.a0min = a0min,
        self.a1 = a1,
        self.a1min = a1min,
        self.a2 = a2,
        self.a2min = a2min,
        self.a3 = a3,
        self.a3min = a3min,
        self.a4 = a4,
        self.a4min = a4min,
        self.a5 = a5,
        self.a5min = a5min,
        self.a6 = a6,
        self.a6min = a6min,
        self.a7 = a7,
        self.a7min = a7min,
        self.a8 = a8,
        self.a8min = a8min,
        self.a9 = a9,
        self.a9min = a9min

nulldict = {'a0': None, 'a0min': None, 'a1': None, 'a1min': None,'a2': None, 'a2min': None, 'a3': None, 'a3min': None,
            'a4': None, 'a4min': None, 'a5': None, 'a5min': None, 'a6': None, 'a6min': None, 'a7': None, 'a7min': None,
            'a8': None, 'a8min': None, 'a9': None, 'a9min': None
}


@app.route("/")
def index():
    return render_template("index.html", session=session)


@app.route("/pharmacy")
def pharmacy():
    return render_template("pharmacy.html", session=session)


@app.route("/kennels")
def kennels():
    return render_template("kennels.html", session=session)


@app.route("/theatre")
def theatre():
    return render_template("theatre.html", session=session)


@app.route("/tabletcalc")
def tabletcalc():
    data = Tablet().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/tablet.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachtablet.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 400)


@app.route("/liquidcalc")
def liquidcalc():
    data = Liquid().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/liquids.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachliquids.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 400)


@app.route("/fluidcalc")
def fluidscalc():
    data = Fluids().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/fluids.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachfluids.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 400)


@app.route("/gascalc")
def gascalc():
    data = Gasflow().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/gases.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachgases.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 400)


@app.route("/injectioncalc")
def injectioncalc():
    data = Injectable().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/injections.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachinjections.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 400)


@app.route("/test", methods=["GET", "POST"])
@login_required
def test():
    # GET returns test start screen
    if request.method == "GET":
        return render_template("test.html", session=session)

    # POST returns either question objects or calculates score depending on data from post
    if request.method == "POST":
        try:
            # if question request generates and returns question objects in JSON
            if request.form.get('qtype') == "question":
                data = testGen(request.form.get('TType')) 
                if test_answers.query.filter_by(id=session['user_id']).count() == 1:
                    test_answers.query.filter_by(id=session['user_id']).update(nulldict)
                    db.session.commit()
                else:
                    newAnswers = test_answers(session['user_id'])
                    print(newAnswers.id)
                    print(newAnswers.a0)
                    db.session.add(newAnswers)
                    db.session.commit()
                    print("ANSWERS ADDED")
                answerDict = {'a0': None, 'a0min': None, 'a1': None, 'a1min': None,'a2': None, 'a2min': None, 'a3': None, 'a3min': None,
                    'a4': None, 'a4min': None, 'a5': None, 'a5min': None, 'a6': None, 'a6min': None, 'a7': None, 'a7min': None,
                    'a8': None, 'a8min': None, 'a9': None, 'a9min': None}
                counter = 0
                for question, answer in answerDict.items():
                    if counter % 2 == 0:
                        if data[counter / 2]['questType'] == "gasFlow":
                            answerDict[f"{question}"] = data[counter/2]['maxGasFlow']
                            data[counter / 2].pop('maxGasFlow')
                        else:
                            answerDict[f"{question}"] = data[counter/2]['ANS']
                            data[counter / 2].pop('ANS')
                    else:
                        if data[(counter / 2) - 0.5]['questType'] == "gasFlow":
                            answerDict[f"{question}"] = data[(counter/2) - 0.5]['minGasFlow']
                            data[(counter / 2) - 0.5].pop('minGasFlow')
                        else:
                            pass
                    counter = counter + 1
                test_answers.query.filter_by(id=session['user_id']).update(answerDict)
                db.session.commit()      
                return jsonify(data)

            # checks answers from test aginst database and stores + returns score
            if request.form.get("qtype") == "answers":
                data = request.form
                TType = request.form.get("TType")
                # retrieves answers from db
                solutions = test_answers.query.filter_by(id=session['user_id']).all()
                correct = solutions[0].__dict__
                counter = 0
                unanswered = 0
                for i in range(10):
                    try:
                        if correct[f'a{i}min'] == None:
                            if data[f'{i}'] == correct[f'a{i}']:
                                print("OTHER CALCULATION SELECTED")
                                counter = counter + 1
                            else:
                                pass
                        elif data[f'{i}'] == correct[f'a{i}'] and data[f"{i}min"] == correct[f'a{i}min']:
                                counter = counter + 1
                        else:
                                pass
                    except:
                        unanswered = unanswered + 1
                percentage = int((counter/10)*100)
                newResult = results(id=session['user_id'], result=percentage, test_type=TType)
                db.session.add(newResult)
                db.session.commit()
                percentage = f"{percentage}%"
                return render_template("result.html", counter=counter, unanswered=unanswered, percentage=percentage, TType=TType)
        except:
            return apology("Test error, either your results were corrupted or your test request failed", 400)


@app.route("/register", methods=["GET", "POST"])
# register user
def register():
    if request.method == "GET":
        return render_template("register.html",)
    if request.method == "POST":
        try:
            # get data and ensure form completed
            if not request.form.get("username"):
                return apology("Username must be provided", 400)
            # ensures matching password/email fields
            try:
                if request.form.get("pass") != request.form.get("confpass"):
                    return apology("Sorry passwords must match", 400)
            except:
                return apology("Password fields must be completed", 40)
            try:
                if request.form.get("email") != request.form.get("confemail"):
                    return apology("Sorry email addresses must match", 400)
            except:
                return apology("Email fields must be complete", 400)

            if not request.form.get("firstname") or not request.form.get('lastname'):
                return apology("Both firstname and lastname must be provided", 400)

            # search for duplicate account
            check = students.query.filter_by(email=f'{request.form.get("email")}').count()
            if check > 0:
                return apology("Sorry email address already registered", 400)
            check = students.query.filter_by(username=f'{request.form.get("username")}').count()
            if check > 0:
                return apology("Sorry username already registered", 400)

            # logs into gmail and send a welcome email to the student on registration
            #s = smtplib.SMTP('smtp.gmail.com', 587)
            #s.ehlo()
            #s.starttls()
            #s.login("vetcalculationspractice@gmail.com", "Vetcalcprac")
            #message = "\r\n".join([
            #   "Subject: Veterinary Calculation Practice Registration",
            #    "Thank you for registering with the Veterinary Calculations Practice",
            #    "You may now take tests and the results will be recorded for you",
            #    "Good Luck",
            #    " ",
            #    "The Veterinary Calculations Practice"])
            #s.sendmail("VetCalculationsPractice", f"{request.form.get('email')}", message)
            #s.quit()

            # hashes password then adds user to database
            passhash = generate_password_hash(request.form.get("pass"))
            newstudent = students(firstname=request.form.get("firstname"), lastname=request.form.get("lastname"), hash=passhash,
                                college=request.form.get("college"), email=request.form.get("email"), username=request.form.get("username"))
            db.session.add(newstudent)
            db.session.commit()

            # log user in            
            session['user_id'] = newstudent.id
            
            # redirect user to homepage
            return redirect("/account")
        except:
            return apology("Registration Failed", 400)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", session=session)

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        try:
            # Ensure username was submitted
            if not request.form.get("username"):
                return apology("must provide username", 400)

            # Ensure password was submitted
            elif not request.form.get("password"):
                return apology("must provide password", 400)

            # Query database for username
            rows = students.query.filter_by(username=request.form.get("username")).all()
            # Ensure username exists and password is correct
            if not check_password_hash(rows[0].hash, request.form.get("password")):
                return apology("invalid username and/or password", 400)
            if rows:
                # Remember which user has logged in
                session["user_id"] = rows[0].id

                # Redirect user to home page
                return redirect("/account")
            else:
                return apology("invalid username and/or password", 400)

        # User reached route via GET (as by clicking a link or via redirect)
        except:
            return apology("Login Failed", 400)


@app.route("/account")
@login_required
def account():
    if request.method == "GET":
        try:
            bestArray = ['Tablet', 'Liquid', 'Fluids', 'gasFlow', 'Injectable', 'Hazard']
            # collects best result for each test
            bestResults = {}
            for i in range(len(bestArray)):
                bestResult = results.query.filter_by(id=session['user_id']).filter_by(test_type=bestArray[i]).order_by(desc(results.result)).first()
                try:
                    bestResults.update({f'{bestArray[i]}': bestResult.result})
                except:
                    bestResults.update({f'{bestArray[i]}': 'Not Taken'})
            # collects number of test taken of each type
            numberOfAttempts = {}
            for i in range(len(bestArray)):
                attempts = results.query.filter_by(id=session['user_id']).filter_by(test_type=bestArray[i]).count()
                try:
                    numberOfAttempts.update({f'{bestArray[i]}': attempts})
                except:
                    numberOfAttempts.update({f'{bestArray[i]}': '0'})
            # collects student data
            studentdata = students.query.filter_by(id=session["user_id"]).all()
            return render_template("account.html", bestResult=bestResults, student=studentdata, attempts=numberOfAttempts, session=session)
        except:
            return apology("Account details not available at this time", 400)


@app.route("/update", methods=["POST"])
@login_required
def update():
    data = request.form
    updated = {}
    student = students.query.filter_by(id=session['user_id']).all()
    try:
        if data['updemail'] == "":
            updated.update({'email': False})
        else:
            email = students.query.filter_by(email=data['updemail']).all()
            if email == []:
                student[0].email = data['updemail']
                updated.update({'email': True})
            else:
                updated.update({'email': "taken"})
    except:
        updated.update({'email': False})
    try:
        if data['updpass'] == "":
            updated.update({'pass': False})
        elif data["updpass"] == data["updconpass"]:
            newPassHash = generate_password_hash(data["updpass"])
            student[0].hash = newPassHash
            updated.update({'pass': True})
    except:
        updated.update({'pass': False})
    db.session.commit()
    return jsonify(updated)

@app.route("/check", methods=["GET", "POST"])
def check():
    if request.method == "GET":
        try:
            if not request.args.get('q'):
                return apology("Username must be provided", 400)
            if not request.args.get('mail'):
                return apology("Email must be provided", 400)
            else:
                reg = request.args.get('q')
                email = request.args.get('mail')
            rows = students.query.filter_by(username=f'{reg}').all()
            rows2 = students.query.filter_by(email=f'{email}').all()
            if rows == [] and rows2 == []:
                return (jsonify(True), 200)
            elif rows == []:
                return (jsonify({
                    "username": False,
                    "email": True,
                    "code": 200
                    }))
            elif rows2 == []:
                return jsonify({
                    "username": True,
                    "email": False,
                    "code": 200
                    })
            else: 
                return (jsonify(False), 200)
        except:
            return redirect("/")
    if request.method == "POST":
        try:
            rows = students.query.filter_by(username=request.form.get("username")).all()  
            pwd = check_password_hash(rows[0].hash, request.form.get("password"))        
            if rows == []:
                return(jsonify(False))
            if pwd == True:
                return(jsonify(True))
            else:
                return(jsonify(False))
        except:
            return redirect("/login")

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return e.name, e.code


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)