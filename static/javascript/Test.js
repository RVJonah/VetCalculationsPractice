function requesttest(TType, repeat) {
    qtype = {
        'qtype': "question",
        'TType': TType
    };
    $.post("/test", qtype, function(data) {
        if (repeat == 2) {
            document.getElementById("repeatbtn").style.display = "none"
            document.getElementById("returnbtn").style.display = "none"
        }
        document.getElementById("resultdiv").style.display = "none"
        if (repeat == 1) {
            document.getElementsByClassName("flexcontainer")[0].style.display = "none"
            document.getElementsByClassName("flexcontainer")[1].style.display = "none"
        }
        runtest(data)
    })
}


//global question number and questions variable
var qNum = 0
var questions = {}

// creates object for submitted answers
var answers = {
    'qtype': 'answers'

}

function runtest(data) {
    $("#tester").remove()
    $("#startbtn").remove()
    document.getElementById("testdiv1").style.display = "flex"
    document.getElementById("testdiv1").style.flex = "row"
    questions = data
    answers['TType'] = data[10]
    let questdiv1 = document.createElement('div')
    questdiv1.setAttribute('id', 'questdiv1')
    questdiv1.setAttribute('class', "quest")
    let questdiv2 = document.createElement('div')
    questdiv2.setAttribute('id', 'questdiv2')
    questdiv2.setAttribute('class', "quest")
    let answer = document.createElement('div')
    answer.setAttribute('id', 'answerdiv')
    let prev = document.createElement('BUTTON')
    prev.setAttribute('id', "prevbtn")
    prev.setAttribute('class', "smallbtn")
    prev.setAttribute("disabled", "")
    prev.setAttribute('onclick', "qmove(-1,questions)")
    prev.innerHTML = "Previous"
    let next = document.createElement('BUTTON')
    next.setAttribute('id', "nextbtn")
    next.setAttribute('class', "smallbtn")
    next.setAttribute('onclick', "qmove(1,questions)")
    next.innerHTML = "Next"
    let sub = document.createElement('BUTTON')
    sub.setAttribute('id', "subbtn")
    sub.setAttribute('class', "smallbtn")
    sub.setAttribute('onclick', "store(1, questions)")
    sub.innerHTML = "Submit"
    let complete = document.createElement('BUTTON')
    complete.setAttribute('id', "completebtn")
    complete.setAttribute('class', "smallbtn")
    complete.setAttribute("disabled", "")
    complete.setAttribute("onclick", "sendAnswers(answers)")
    complete.innerHTML = "Complete"
    let test1 = document.getElementById('testdiv1')
    let test2 = document.getElementById('testdiv2')
    test1.appendChild(questdiv1)
    test1.appendChild(questdiv2)
    test2.appendChild(answer)
    test2.appendChild(prev)
    test2.appendChild(next)
    test2.appendChild(sub)
    test2.appendChild(complete)

    qmove(0, questions)
}

// alters currently displayed question move arg 1 = move on, -1 = move back
function qmove(move, questions) {
    // increments or decrements question number
    if (move === 1) {
        qNum++
    }
    if (move === -1) {
        qNum--
    }

    // activates prev/next/complete buttons to prevent qNum going out of range
    if (qNum === 0) {
        document.getElementById("prevbtn").setAttribute("disabled", "")
    }
    if (qNum === 9) {
        document.getElementById("nextbtn").disabled = true
        document.getElementById("completebtn").disabled = false
    }
    if (qNum > 0 && document.getElementById("prevbtn").disabled === true) {
        document.getElementById("prevbtn").disabled = false
    }
    if (qNum < 9 && document.getElementById("nextbtn").disabled === true) {
        document.getElementById("nextbtn").disabled = false
    }
    // adds question number to top of screen
    document.getElementById('questionNum').innerHTML = `<h3>Question ${qNum + 1}</h3>`

    // generates the answer area
    answerboxgenerator(questions)

    if (questions[qNum]['questType'] === "Tablet" || questions[qNum]['questType'] === "Liquid") {
        document.getElementById('questdiv1').innerHTML =
            `<div style="padding-left: 10%; text-decoration: underline;">Patient Details</div>\n\
            <ul><li>Species: ${questions[qNum]["species"]}</li>\n\
            <li>Weight: ${questions[qNum]["bodyweight"]}kg</li> \n\
            <li>Presenting Complaint: ${questions[qNum]["symptom"]}</li></ul>`
        document.getElementById('questdiv2').innerHTML =
            `<div style="padding-left: 10%; text-decoration: underline;">Treatment Details</div>\n\
            <ul id="ul"><li>Max Dose Rate: ${questions[qNum]["dose"]}mg/kg</li>\n\
            <li>Daily Doses: ${questions[qNum]["wordDaily"]}</li>  \n\
            <li>Length Of Treatment: ${questions[qNum]["courseLength"]} days</li>`
    }
    let medstrength = document.createElement('li')
    if (questions[qNum]['questType'] === "Tablet") {
        medstrength.innerHTML = `Tablet Strength Available: ${questions[qNum]["medStrength"]}mg/tablet`
        document.getElementById("ul").appendChild(medstrength)

    }
    if (questions[qNum]['questType'] === "Liquid") {
        if (questions[qNum]['lType'] === 1) {
            medstrength.innerHTML =
                `Liquid Concentration: ${questions[qNum]['medStrength']}mg/ml`
            document.getElementById("ul").appendChild(medstrength)
        }
        if (questions[qNum]['lType'] === 2) {
            medstrength.innerHTML =
                `Liquid Concentration: ${questions[qNum]['percMedStrength']}% solution`
            document.getElementById("ul").appendChild(medstrength)
        }

    }
    if (questions[qNum]['questType'] === "gasFlow") {
        document.getElementById('questdiv1').innerHTML =
            `<div style="padding-left: 10%; text-decoration: underline;">Patient Details</div>\n\
            <ul><li>Species: ${questions[qNum]["species"]}</li>\n\
            <li>Weight: ${questions[qNum]["bodyweight"]}kg</li> \n\
            <li>Respiration Rate: ${questions[qNum]["respirationRate"]} breaths per minute</li></ul> \n\
        `
        document.getElementById('questdiv2').innerHTML =
            `<div style="padding-left: 10%; text-decoration: underline;">Circuit Details</div>\n\
            <ul><li>Circuit Type: ${questions[qNum]["circuit"]} circuit</li> \n\
            <li>Circuit Factor: ${questions[qNum]["minFactor"]}-${questions[qNum]["maxFactor"]} </li></ul>  \n\
        `
    }
    if (questions[qNum]['questType'] === "Injectable") {
        document.getElementById('questdiv1').innerHTML =
            `<div style="padding-left: 10%; text-decoration: underline;">Patient Details</div>\n\
            <ul><li>Species: ${questions[qNum]["species"]}</li>\n\
            <li>Weight: ${questions[qNum]["bodyweight"]}kg</li></ul>`
        if (questions[qNum]['lType'] === 1) {
            document.getElementById('questdiv2').innerHTML =
                `<div style="padding-left: 10%; text-decoration: underline;">Treatment Details</div>\n\
                <ul><li>Max Dose Rate: ${questions[qNum]["dose"]}mg/kg</li> \n\
                <li>Injectable Concentration: ${questions[qNum]["medStrength"]}mg/ml solution</li></ul>`
        } else {
            document.getElementById('questdiv2').innerHTML =
                `<div style="padding-left: 10%; text-decoration: underline;">Treatment Details</div>\n\
                <ul><li>Max Dose Rate: ${questions[qNum]["dose"]}mg/kg</li> \n\
                <li>Injectable Concentration: ${questions[qNum]["percMedStrength"]}% solution</li></ul>`
        }
    }
    if (questions[qNum]['questType'] === "Fluids") {
        document.getElementById('questdiv1').innerHTML =
            `<div style="padding-left: 10%; text-decoration: underline;">Patient Details</div>\n\
            <ul><li>Species: ${questions[qNum]["species"]}</li>\n\
            <li>Weight: ${questions[qNum]["bodyweight"]}kg</li></ul>`
        if (questions[qNum]["dehydration"] === 0) {
            document.getElementById('questdiv2').innerHTML =
                `<div style="padding-left: 10%; text-decoration: underline;">Treatment Details</div>\n\
                <ul id="ul"><li>Maintenance Fluid Rate: ${questions[qNum]["dailyFluids"]}ml/kg/day</li></ul>`
        } else {
            document.getElementById('questdiv2').innerHTML =
                `<div style="padding-left: 10%; text-decoration: underline;">Treatment Details</div>\n\
                <ul id="ul"><li>Maintenance Fluid Rate: ${questions[qNum]["dailyFluids"]}ml/kg/day</li>  \n\
                <li>Pecentage Dehydration: ${questions[qNum]["dehydration"]} % </li> \n\
                <li>Ongoing Fluid Loss Per Day: ${questions[qNum]["onGoingLoss"]}ml/day </li><ul>`
        }
        if (questions[qNum]['mlVsSec'] === 1) {
            let dropsPer = document.createElement('li')
            dropsPer.innerHTML = `Drops Per ml: ${questions[qNum]["dropsPerMl"]} drops`
            document.getElementById('ul').appendChild(dropsPer)
        }

    }

}



function store(move, questions) {
    if (questions[qNum]['questType'] === "gasFlow") {
        answers[qNum] = document.getElementById('ANS1').value
        answers[`${qNum}min`] = document.getElementById('ANS2').value

    } else {
        answers[qNum] = document.getElementById('ANS').value
    }

    if (qNum === 9) {
        qmove(0, questions)
    } else {
        //moves to next question
        qmove(1, questions)
    }
}

function answerboxgenerator(questions) {

    // assigns answerdiv and assigns first parts of question
    let answerdiv = document.getElementById('answerdiv')
    answerdiv.innerHTML = questions[qNum]['question']['part1'] + "<br>" + questions[qNum]['question']['part2']

    if (questions[qNum]['questType'] === "gasFlow") {
        // if gasflow calculation 2 answer boxes created and given id
        let answerbox1 = document.createElement('input')
        answerbox1.setAttribute('id', "ANS1")
        answerbox1.setAttribute('class', "answerbox")
        answerbox1.setAttribute('autocomplete', "off")

        let answerbox2 = document.createElement('input')
        answerbox2.setAttribute('id', "ANS2")
        answerbox2.setAttribute('class', "answerbox")
        answerbox2.setAttribute('autocomplete', "off")

        answerdiv.appendChild(answerbox1)
        answerdiv.innerHTML = answerdiv.innerHTML + questions[qNum]['question']['part4'] +
            "<br>" + questions[qNum]['question']['part3']
        answerdiv.appendChild(answerbox2)
        answerdiv.innerHTML = answerdiv.innerHTML + questions[qNum]['question']['part4'] + "<br>" +
            questions[qNum]['question']['part5']
    } else {
        // creates single answer box
        let answerbox = document.createElement('input')
        answerbox.setAttribute('id', "ANS")
        answerbox.setAttribute('class', "answerbox")
        answerbox.setAttribute('autocomplete', "off")

        // adds remainder of question and answerbox to div
        answerdiv.innerHTML = questions[qNum]['question']['part1'] + "<br>" + questions[qNum]['question']['part2']
        answerdiv.appendChild(answerbox)
        answerdiv.innerHTML = answerdiv.innerHTML + questions[qNum]['question']['part4'] +
            "<br>" + questions[qNum]['question']['part3']
    }
}

function sendAnswers(answers) {
    if (confirm("Are you sure you wish to submit your answers?")) {
        $.post("/test", answers, function(data) {
            qNum = 0
            document.getElementById("testpage").innerHTML = data
            document.getElementById("resultdiv").style.display = ""
            document.getElementById("testdiv1").style.display = "none"
        })
    } else return 0
}