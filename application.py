import os
import smtplib
from passwords import emailAddress, emailPassword
from flask import Flask, jsonify, redirect, url_for, render_template, request, session
from database_ORM import initiate_ORM, secret_Key
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_, not_, desc, func
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sslify import SSLify
from VNCalculator import Cat, Dog, Rabbit, Tablet, Fluids, Gasflow, Liquid, Injectable, testGen
from helpers import login_required, apology

## ORM object structure
# { 
#   'engine': engine,
#   'tables': {
#    "testAnswers": Test_answers,
#    "results": Results,
#    "students": Students
#   },
#    'nulldict': nulldict,
# }

app = Flask(__name__)
sslify = SSLify(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = secret_Key

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

ORM = initiate_ORM()
students = ORM['tables']['students']
testAnswers = ORM['tables']['test_answers']
results = ORM['tables']['results']
Session = sessionmaker(bind=ORM['engine'])
db = Session()

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

@app.route("/tabletcalc/quiz")
def tabletcalcQuiz():
    data = Tablet().__dict__
    return render_template("/quiz/tablet.html", data=data, session=session)

@app.route("/tabletcalc/teach")
def tabletcalcTeach():
    data = Tablet().__dict__
    return render_template("/teach/teachtablet.html", data=data, session=session)

@app.route("/liquidcalc/quiz")
def liquidCalcQuiz():
    data = Liquid().__dict__
    return render_template("/quiz/liquids.html", data=data, session=session)

@app.route("/liquidcalc/teach")
def liquidCalcTeach():
    data = Liquid().__dict__
    return render_template("/teach/teachliquids.html", data=data, session=session)

@app.route("/fluidcalc/quiz")
def fluidsCalcQuiz():
    data = Fluids().__dict__
    return render_template("/quiz/fluids.html", data=data, session=session)

@app.route("/fluidcalc/teach")
def fluidsCalcTeach():
    data = Fluids().__dict__
    return render_template("/teach/teachfluids.html", data=data, session=session)

@app.route("/gascalc/quiz")
def gasCalcQuiz():
    data = Gasflow().__dict__
    return render_template("/quiz/gases.html", data=data, session=session)

@app.route("/gascalc/teach")
def gasCalcTeach():
    data = Gasflow().__dict__  
    return render_template("/teach/teachgases.html", data=data, session=session)

@app.route("/injectioncalc/quiz")
def injectionCalcQuiz():
    data = Injectable().__dict__
    return render_template("/quiz/injections.html", data=data, session=session)

@app.route("/injectioncalc/teach")
def injectionCalcTeach():
    data = Injectable().__dict__
    return render_template("/teach/teachinjections.html", data=data, session=session)

@app.route("/test", methods=["GET", "POST"])
@login_required
def test():
    if request.method == "GET":
        return render_template("test.html", session=session)

    if request.method == "POST":
        data = testGen(request.form.get('TType')) 
        if  db.query(testAnswers).filter_by(id=session['user_id']).count() == 1:
            db.query(testAnswers).filter_by(id=session['user_id']).update(ORM['nulldict'])
            
        else:
            newAnswers = testAnswers(id=session['user_id'])
            db.add(newAnswers)
        answerDict = ORM['nulldict']
        counter = 0
        for question, answer in answerDict.items():
            if counter % 2 == 0:
                if data[counter / 2]['questType'] == "Gasflow":
                    answerDict[f"{question}"] = data[counter/2]['maxGasFlow']
                    data[counter / 2].pop('maxGasFlow')
                else:
                    answerDict[f"{question}"] = data[counter/2]['ANS']
                    data[counter / 2].pop('ANS')
            else:
                if data[(counter / 2) - 0.5]['questType'] == "Gasflow":
                    answerDict[f"{question}"] = data[(counter/2) - 0.5]['minGasFlow']
                    data[(counter / 2) - 0.5].pop('minGasFlow')
                else:
                    pass
            counter = counter + 1
        db.query(testAnswers).filter_by(id=session['user_id']).update(answerDict)
        db.commit()      
        return jsonify(data)

@app.route("/results", methods=["POST"])
@login_required
def checkAnswers():
    if request.method == "POST":
        data = request.form
        TType = request.form.get("TType")
        solutions = db.query(testAnswers).filter_by(id=session['user_id']).all()
        correct = solutions[0].__dict__
        counter = 0
        unanswered = 0
        for i in range(10):
            if data[f'{i}'] == "":
                unanswered = unanswered + 1
            elif correct[f'a{i}min'] == None:
                if data[f'{i}'] == correct[f'a{i}']:
                    counter = counter + 1
            elif data[f'{i}'] == correct[f'a{i}'] and data[f"{i}min"] == correct[f'a{i}min']:
                    counter = counter + 1   
        percentage = int((counter/10)*100)
        newResult = results(id=session['user_id'], result=percentage, test_type=TType)
        db.add(newResult)
        db.commit()
        percentage = f"{percentage}%"
        print("returning template")
        return render_template("result.html", counter=counter, unanswered=unanswered, percentage=percentage, TType=TType)
    else:
        return redirect("/test", 405)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html",)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Username must be provided", 422)
        if not request.form.get("pass") or not request.form.get("confpass"):
            return apology("Password fields must be completed", 422)
        if request.form.get("pass") != request.form.get("confpass"):
            return apology("Sorry passwords must match", 400)
        if not request.form.get("email") or  not request.form.get("confemail"):
            return apology("Email fields must be completed", 422)
        if request.form.get("email") != request.form.get("confemail"):
            return apology("Sorry email addresses must match", 400)
        if not request.form.get("firstname") or not request.form.get('lastname'):
            return apology("Both firstname and lastname must be provided", 422)

        checkDuplicateEmail = db.query(students).filter_by(email=f'{request.form.get("email")}').count()
        if checkDuplicateEmail > 0:
            return apology("Sorry email/username address already registered", 409)
        checkDuplicateUsername = db.query(students).filter_by(username=f'{request.form.get("username")}').count()
        if checkDuplicateUsername > 0:
            return apology("Sorry email/username already registered", 409)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login(emailAddress, emailPassword )
        message = "\r\n".join([
           "Subject: Veterinary Calculation Practice Registration",
            "Thank you for registering with the Veterinary Calculations Practice!",
            "You may now take tests and the results will be recorded for you",
            "Good Luck",
            " ",
            "The Veterinary Calculations Practice"])
        s.sendmail("VetCalculationsPractice", f"{request.form.get('email')}", message)
        s.quit()

        passhash = generate_password_hash(request.form.get("pass"))
        userid = db.query(students).order_by(desc(students.id)).first().id + 1
        newstudent = students(id=userid, firstname=request.form.get("firstname"), lastname=request.form.get("lastname"), hash=passhash,
                            college=request.form.get("college"), email=request.form.get("email"), username=request.form.get("username"))
        db.add(newstudent)
        db.commit()  
        session['user_id'] = newstudent.id
        return redirect("/account")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", session=session)
    
    if request.method == "POST":
        session.clear()
        if not request.form.get("username"):
            return apology("must provide username", 422)
        elif not request.form.get("password"):
            return apology("must provide password", 422)

        rows = db.query(students).filter_by(username=request.form.get("username")).all()
        if rows == []:
            return apology("invalid username and/or password", 404)
        if not check_password_hash(rows[0].hash, request.form.get("password")):
            return apology("invalid username and/or password", 404)
        if rows:
            session["user_id"] = rows[0].id
            return redirect("/account")
        else:
            return apology("invalid username and/or password", 400)
    else:
        return redirect("/login", 405)



@app.route("/account")
@login_required
def account():
    if request.method == "GET":
        bestArray = ['Tablet', 'Liquid', 'Fluids', 'Gasflow', 'Injectable', 'Hazard']
        bestResults = {}
        for i in range(len(bestArray)):
            bestResult = db.query(results).filter_by(id=session['user_id']).filter_by(test_type=bestArray[i]).order_by(desc(results.result)).first()
            if bestResult:
                bestResults.update({f'{bestArray[i]}': bestResult.result})
            else:
                bestResults.update({f'{bestArray[i]}': 'Not Taken'})

        numberOfAttempts = {}
        for i in range(len(bestArray)):
            attempts = db.query(results).filter_by(id=session['user_id']).filter_by(test_type=bestArray[i]).count()
            if attempts:
                numberOfAttempts.update({f'{bestArray[i]}': attempts})
            else:
                numberOfAttempts.update({f'{bestArray[i]}': '0'})

        studentdata = db.query(students).filter_by(id=session["user_id"]).all()
        return render_template("account.html", bestResult=bestResults, student=studentdata, attempts=numberOfAttempts, session=session)
    else:
        return redirect("/login")


@app.route("/update", methods=["POST"])
@login_required
def update():
    data = request.form
    updated = {}
    student = db.query(students).filter_by(id=session['user_id']).all()
    if data['updemail'] == "":
        updated.update({'email': False})
    else:
        userEmail = db.query(students).filter_by(email=data["updemail"]).all()
        if userEmail == []:
            student[0].email = data['updemail']
            updated.update({'email': True})
        else:
            updated.update({'email': "taken"})
    if data['updpass'] == "":
        updated.update({'pass': False})
    elif data["updpass"] == data["updconpass"]:
        newPassHash = generate_password_hash(data["updpass"])
        student[0].hash = newPassHash
        updated.update({'pass': True})
    else: 
        updated.update({'pass': False})
    db.commit()
    return jsonify(updated)

@app.route("/logincheck", methods=["POST"])
def logincheck():
    if request.method == "POST":
        rows = db.query(students).filter_by(username=request.form.get("username")).all()  
        if rows == []:
            return(jsonify(False))
        pwd = check_password_hash(rows[0].hash, request.form.get("password"))  
        if pwd == True:
            return(jsonify(True))
        else:
            return(jsonify(False))
    else: 
        return redirect("/login", 405)

@app.route("/registercheck", methods=["GET"])
def registercheck():
    if request.method == "GET":
        if not request.args.get('username'):
            return apology("Username must be provided", 400)
        if not request.args.get('mail'):
            return apology("Email must be provided", 400)
        else:
            reg = request.args.get('username')
            email = request.args.get('mail')
        rows = db.query(students).filter_by(username=f'{reg}').all()
        rows2 = db.query(students).filter_by(email=f'{email}').all()
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
    else:
        return redirect('/register', 405)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return e.name, e.code

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)