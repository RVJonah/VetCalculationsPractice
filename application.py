import os
import smtplib
from VNCalculator import *
from helpers import *
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sslify import SSLify

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


# Configure Library to use SQLite database
db = SQL("sqlite:///VNTester.db")

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
        return apology("You must select either a quiz or a lesson", 403)


@app.route("/liquidcalc")
def liquidcalc():
    data = Liquid().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/liquids.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachliquids.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 403)


@app.route("/fluidcalc")
def fluidscalc():
    data = Fluids().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/fluids.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachfluids.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 403)


@app.route("/gascalc")
def gascalc():
    data = Gasflow().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/gases.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachgases.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 403)


@app.route("/injectioncalc")
def injectioncalc():
    data = Injectable().__dict__
    try:
        if request.args['q'] == 'quiz':
            return render_template("/quiz/injections.html", data=data, session=session)
        if request.args['q'] == 'teach':
            return render_template("/teach/teachinjections.html", data=data, session=session)
    except:
        return apology("You must select either a quiz or a lesson", 403)


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
                db.execute(f"INSERT INTO Test_Answers (id) VALUES ('{session['user_id']}')")
                db.execute(
                    f"UPDATE Test_Answers SET A1min=NULL,A2min=NULL,A3min=NULL,A4min=NULL,A5min=NULL,A6min=NULL,A7min=NULL,A8min=NULL,A9min=NULL,A0min=NULL WHERE id={session['user_id']}")
                for i in range(10):
                    if data[i]['questType'] == "gasFlow":
                        db.execute(
                            f"UPDATE Test_Answers SET A{i} = {data[i]['maxGasFlow']}, A{i}min = '{data[i]['minGasFlow']}' WHERE id = '{session['user_id']}'")
                        data[i].pop('minGasFlow')
                        data[i].pop('maxGasFlow')
                    else:
                        db.execute(f"UPDATE Test_Answers SET A{i} = {data[i]['ANS']}  WHERE id = '{session['user_id']}'")
                        data[i].pop('ANS')
                return jsonify(data)

            # checks answers from test aginst database and stores + returns score
            if request.form.get("qtype") == "answers":
                data = request.form
                TType = request.form.get("TType")

                # sets correct answer counter to 0
                counter = 0
                unanswered = 0

                # retrieves answers from db
                solutions = db.execute(f"SELECT * FROM Test_Answers WHERE id='{session['user_id']}'")
                db.execute(
                    f"UPDATE Test_Answers SET A1=NULL,A2=NULL,A3=NULL,A4=NULL,A5=NULL,A6=NULL,A7=NULL,A8=NULL,A9=NULL,A0=NULL WHERE id={session['user_id']}")
                for i in range(10):
                    if solutions[0][f"A{i}min"] == None:
                        try:
                            if (float(data[f'{i}']) == solutions[0][f"A{i}"]):
                                counter = counter + 1
                        except:
                            unanswered = unanswered + 1
                    else:
                        try:
                            if (float(data[f'{i}']) == solutions[0][f"A{i}"]) and (float(data[f'{i}min']) == solutions[0][f"A{i}min"]):
                                counter = counter + 1
                        except:
                            unanswered = unanswered + 1

                percentage = int((counter/10)*100)
                db.execute(
                    f"INSERT INTO Results (id,Result,Test_Type) VALUES ('{session['user_id']}','{percentage}%','{TType}')")
                return render_template("result.html", counter=counter, unanswered=unanswered, percentage=percentage, TType=TType)
        except:
            return apology("Test error, either your result were corrupted or your test request failed", 403)


@app.route("/register", methods=["GET", "POST"])
# register user
def register():
    if request.method == "GET":
        return render_template("register.html",)
    if request.method == "POST":
        try:
            # get data and ensure form completed
            if not request.form.get("username"):
                return apology("Username must be provided", 403)

            # ensures matching password/email fields
            try:
                if request.form.get("pass") != request.form.get("confpass"):
                    return apology("Sorry passwords must match", 403)
            except:
                return apology("Password fields must be completed", 403)
            try:
                if request.form.get("email") != request.form.get("confemail"):
                    return apology("Sorry email addresses must match", 403)
            except:
                return apology("Email fields must be complete", 403)

            if not request.form.get("firstname") or not request.form.get('lastname'):
                return apology("Both firstname and lastname must be provided", 403)

            # search for duplicate account
            check = db.execute(f"SELECT * FROM students WHERE Firstname = :firstname AND Lastname = :lastname",
                               firstname=request.form.get("firstname"), lastname=request.form.get("lastname"))
            if len(check) != 0:
                return apology("Sorry you are already registered", 403)
            check = db.execute(
                "SELECT * FROM students WHERE username = :username", username=request.form.get("username"))
            if len(check) != 0:
                return apology("Sorry username already registered", 403)

            ''' logs into gmail and send a welcome email to the student on registration
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.login("vetcalculationspractice@gmail.com", "")
            message = "\r\n".join([
                "Subject: Veterinary Calculation Practice Registration",
                "Thank you for registering with the Veterinary Calculations Practice",
                "You may now take tests and the results will be recorded for you",
                "Good Luck",
                " ",
                "The Veterinary Calculations Practice"])
            s.sendmail("VetCalculationsPractice", f"{request.form.get('email')}", message)
            s.quit()
            '''
            # hashes password then adds user to database
            passhash = generate_password_hash(request.form.get("pass"))
            db.execute(f"INSERT INTO students(Username, Hash, Firstname, Lastname, Email, College) VALUES (:username,  '{passhash}', :firstname, :lastname, :email, :college)",
                       username=request.form.get("username"), firstname=request.form.get("firstname"), lastname=request.form.get("lastname"), email=request.form.get("email"), college=request.form.get("college"))

            # log user in
            data = db.execute("SELECT * FROM students WHERE Username=:username",
                              username=request.form.get("username"))
            session['user_id'] = data[0]["id"]

            # redirect user to homepage
            return redirect("/account")
        except:
            return apology("Registration Failed", 403)


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
                return apology("must provide username", 403)

            # Ensure password was submitted
            elif not request.form.get("password"):
                return apology("must provide password", 403)

            # Query database for username
            rows = db.execute("SELECT * FROM Students WHERE username = :username",
                              username=request.form.get("username"))

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["Hash"], request.form.get("password")):
                return apology("invalid username and/or password", 403)

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/account")

        # User reached route via GET (as by clicking a link or via redirect)
        except:
            return apology("Login Failed", 403)


@app.route("/account")
@login_required
def account():
    if request.method == "GET":
        try:
            bestArray = ['Tablet', 'Liquid', 'Fluids', 'gasFlow', 'Injectable', 'Hazard']
            # collects best result for each test
            bestResults = {}
            for i in range(len(bestArray)):
                bestResult = db.execute(
                    f"SELECT * FROM Results WHERE id = {session['user_id']} AND Test_Type = '{bestArray[i]}' ORDER BY 2 DESC  LIMIT 1")
                try:
                    bestResults.update({f'{bestArray[i]}': bestResult[0]['Result']})
                except:
                    bestResults.update({f'{bestArray[i]}': 'Not Taken'})
            # collects number of test taken of each type
            numberOfAttempts = {}
            for i in range(len(bestArray)):
                try:
                    numberOfAttempts.update({f'{bestArray[i]}': len(db.execute(
                        f"SELECT * FROM Results WHERE id = {session['user_id']} AND Test_Type = '{bestArray[i]}'"))})
                except:
                    numberOfAttempts.update({f'{bestArray[i]}': '0'})
            # total number of tests taken
            totalTests = len(db.execute(f"SELECT * FROM Results WHERE id = {session['user_id']}"))

            # collects student data
            studentdata = db.execute(f"SELECT Username,Email FROM Students WHERE id = {session['user_id']}")

            return render_template("account.html", bestResult=bestResults, student=studentdata, attempts=numberOfAttempts, totalTests=totalTests, session=session)
        except:
            return apology("Account details not available at this time", 403)


@app.route("/update", methods=["POST"])
@login_required
def update():
    data = request.form
    updated = {}
    try:
        if data['updemail'] == "":
            updated.update({'email': False})
        else:
            db.execute(f"UPDATE Students SET Email= :email WHERE id='{session['user_id']}'", email=data['updemail'])
            updated.update({'email': True})
    except:
        updated.update({'email': False})
    try:
        if data['updpass'] == "":
            updated.update({'pass': False})
        elif data["updpass"] == data["updconpass"]:
            newPassHash = generate_password_hash(data["updpass"])
            db.execute(f"UPDATE Students SET Hash='{newPassHash}' WHERE id='{session['user_id']}'")
            updated.update({'pass': True})
    except:
        updated.update({'pass': False})
    return jsonify(updated)

@app.route("/check")
def check():
    print(request.args.get('q'))
    if not request.args.get('q'):
        return apology("Username my be provided", 403)
    else:
        reg = request.args.get('q')
    rows = db.execute(f"SELECT * FROM Students WHERE username=:username", username=reg)
    if len(rows) == 0:
        return (jsonify(True), 200)
    else:
        return (jsonify(False), 200)

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return e.name, e.code


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)