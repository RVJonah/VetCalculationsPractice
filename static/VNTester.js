var buttons = document.getElementsByClassName('subbtn')
for (i = 0; i < buttons.length; i++) {
    buttons[0].addEventListener("click", function() { event.preventDefault() })
}

function hintreveal() {
    let x = document.getElementsByClassName("hint")
    x[0].style.display = "block"
}

function answerreveal() {
    let x = document.getElementsByClassName("hint")
    x[0].style.display = "block"
    let y = document.getElementsByClassName("answer")
    y[0].style.display = "block"
    let newbtn = document.getElementsByClassName("newbtn")
    newbtn[0].style.display = "inline"
    let comment = document.getElementsByClassName("comment")
    comment[0].innerHTML = "Now you've seen how it's done maybe try another question?"
    let submit = document.getElementsByClassName("submitbtn")
    submit[0].style.display = "none"
}

$('#regbtn').click(function() {
    let msg = "",
        fields = document.getElementById("regform").getElementsByTagName("input")

    for (let i = 0; i < (fields.length - 1); i++) {
        if (fields[i].value == "")
            msg += fields[i].title + ' is required. \n'
    }

    if (msg) {
        alert(msg)
        return false
    }
    let pass = document.getElementById("regpass").value,
        confpass = document.getElementById("confpass").value,
        email = document.getElementById("regemail").value,
        confemail = document.getElementById("confemail").value
    if (pass !== confpass) {
        alert("Passwords do not match")
        return false
    }
    if (email !== confemail) {
        alert("Emails do not match")
        return false
    }
    $.get("/check?q=" + fields[0].value,null,function (data) {
        if (data === true){
            document.getElementById("regform").submit()
        } else {
            alert("Username already taken")
        }
    })
    return false
})

$('#logbtn').click(function() {
    let msg = "",
        fields = document.getElementById("loginform").getElementsByTagName("input")

    for (let i = 0; i < (fields.length); i++) {
        if (fields[i].value == "")
            msg += fields[i].title + ' is required. \n'
    }

    if (msg) {
        alert(msg)
        return false
    }
    document.getElementById("loginform").submit()
    return false
})


function login(valid) {
    if (valid == true) {
        var form = document.getElementsByName('dataform')
        form[0].submit()
    } else {
        alert("Invalid Username/Password")
    }
}

function answercheck(numOfAns) {
    if (numOfAns == 1) {
        let guess = document.getElementsByClassName("answerbox")[0].value
        let answer = document.getElementById("answer").innerHTML
        if (guess === answer) {
            document.getElementsByClassName("comment")[0].innerHTML = "Excellent that is the correct answer!"
            document.getElementsByClassName("newbtn")[0].style.display = "inline"
        } else {
            document.getElementsByClassName("comment")[0].innerHTML =
                "Sorry that is the wrong answer, please try again or use the help buttons"
        }
    }
    if (numOfAns == 2) {
        let maxGuess = document.getElementsByClassName("answerbox")[0].value
        let minGuess = document.getElementsByClassName("answerbox")[1].value
        let maxAnswer = document.getElementById("maxanswer").innerHTML
        let minAnswer = document.getElementById("minanswer").innerHTML
        if (maxGuess === maxAnswer && minGuess === minAnswer) {
            document.getElementsByClassName("comment")[0].innerHTML = "Excellent that is the correct answer!"
            document.getElementsByClassName("newbtn")[0].style.display = "inline"
        } else {
            document.getElementsByClassName("comment")[0].innerHTML =
                "Sorry that is the wrong answer, please try again or use the help buttons"
        }
    }
}

function update() {
    fields = document.getElementById("updateform").getElementsByTagName("input")
    if (fields[1].value != fields[2].value) {
        alert("Passwords must match")
        return false
    } else {
        data = $('#updateform').serialize()
        $.post("/update", data, function(data) {
            comment = document.getElementById("comment")
            msg = ""
            if (data['email'] === true) {
                document.getElementById("storedEmail").innerHTML = `Current Email Address: ${fields[0].value}`
                msg += "Email Updated "
            }
            if (data['pass'] === true) {
                msg += "Password Updated"
            }
            comment.innerHTML = msg
        })
    }

}

function returner() {
    window.location.href = 'https://ide50-rvjonah.legacy.cs50.io:8080/test'

}

