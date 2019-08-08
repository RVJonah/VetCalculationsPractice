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
    comment[0].style.display = "block"
    let submit = document.getElementsByClassName("submitbtn")
    submit[0].style.display = "none"
}

$('#regbtn').click(function() {
    comment = document.querySelector(".message");
    comment.style.width = "30%";
    let msg = "",
        fields = document.getElementById("regform").getElementsByTagName("input")

    for (let i = 0; i < (fields.length - 1); i++) {
        if (fields[i].value === "") {
            msg += fields[i].title + ' is required. <br>';
            fields[i].classList.add("blink");
        }
    }

    if (msg) {
        let blinks = document.getElementsByClassName("blink");
        comment.innerHTML = msg;
        comment.classList.add("alert");
        comment.style.display = "block";
        setTimeout(function() {
            comment.classList.remove("alert");
            comment.style.backgroundColor = "rgb(255, 255, 255, 0.8)";
        }, 3000);
        for( var i = 0; i < blinks.length; i++){
            setTimeout(function() {
                blinks[0].classList.remove("blink");
            }, 3000)
        }
        return false
    }
    let pass = document.getElementById("regpass").value,
        confpass = document.getElementById("confpass").value,
        email = document.getElementById("regemail").value,
        confemail = document.getElementById("confemail").value
    if (pass !== confpass) {
        comment.innerHTML = "Passwords need to match";
        comment.style.display = "block";
        comment.style.webkitAnimationPlayState = "running"
        setTimeout(function() {
            comment.style.webkitAnimationPlayState = "paused"
        }, 3000)
        return false
    }
    if (email !== confemail) {
        comment.innerHTML = "Email addresses must match";
            comment.style.display = "block";
            comment.style.webkitAnimationPlayState = "running"
            setTimeout(function() {
                comment.style.webkitAnimationPlayState = "paused"
            }, 3000)
        return false
    }
    $.get("/check?q=" + fields[0].value + "&mail=" + email,null,function (data) {
        if (data === true){
            document.getElementById("regform").submit()
        } else {
            let username = document.getElementById("username");
            let email = document.getElementById("regemail");
            if (data['username'] === true) {  
                username.value = ""
                username.classList.add("blink");
                comment.innerHTML = "Sorry that username already taken";
                comment.style.display = "block";
                comment.style.webkitAnimationPlayState = "running";
                setTimeout(function() {
                    comment.classList.remove("alert");
                    comment.style.backgroundColor = "rgb(255, 255, 255, 0.8)";
                    username.classList.remove("blink");
                }, 3000)
                return false;
            } if (data['email'] === true) {
                email.classList.add("blink");
                comment.innerHTML = "That Email address already already registered";
                comment.style.display = "block";
                setTimeout(function() {
                    comment.classList.remove("alert");
                    comment.style.backgroundColor = "rgb(255, 255, 255, 0.8)";
                    email.classList.remove("blink");
                }, 3000)
                return false;
            } else {
                username.value = ""
                username.classList.add("blink");
                comment.innerHTML = "Sorry that username already taken";
                comment.style.display = "block";
                setTimeout(function() {
                    comment.classList.remove("alert");
                    comment.style.backgroundColor = "rgb(255, 255, 255, 0.8)";
                    username.classList.remove("blink");
                }, 3000)
                return false;
            }
        }
    })
    return false
})

$('#logbtn').click(function() {
    let msg = "",
        fields = document.getElementById("loginform").getElementsByTagName("input");
    let comment = document.querySelector(".message");
    comment.style.width = "30%";
    for (let i = 0; i < (fields.length - 1); i++) {
        if (fields[i].value === "") {
            msg += fields[i].title + ' is required. \n';
            fields[i].classList.add("blink");
            setTimeout(function (){
                fields[i].classList.remove("blink");
            }, 3000);
        }
    }
    if (msg) {
        comment.innerHTML = msg;
        comment.style.display = "block";
        comment.classList.add("alert");
        setTimeout(function () {
            comment.classList.remove("alert");
        }, 3000)
        return false;
    } else {
        data = $('#loginform').serialize()
        $.post("/check", data, function(data) {
            if (data === true) {
                document.getElementById("loginform").submit();
            } else {
                msg += "Username or password incorrect";
                comment.innerHTML = msg;
                comment.style.display = "block";
                comment.classList.add("alert");
                setTimeout(function () {
                    comment.classList.remove("alert");
                }, 3000)
                fields[0].value = "";
                fields[1].value = "";
            }
        })

        
    }
    return false
})

function answercheck(numOfAns) {
    let comment = document.getElementsByClassName("comment")[0]
    if (numOfAns === 1) {
        let guess = document.getElementsByClassName("answerbox")[0].value
        let answer = document.getElementById("answer").innerHTML
        if (guess === answer) {
            comment.innerHTML = "Excellent that is the correct answer!"
            comment.style.display = "block"
            document.getElementsByClassName("newbtn")[0].style.display = "inline"
        } else {
            comment.innerHTML =
                "Sorry that is the wrong answer, please try again or use the help buttons"
            comment.style.display = "block"
        }
    }
    if (numOfAns === 2) {
        let maxGuess = document.getElementsByClassName("answerbox")[0].value
        let minGuess = document.getElementsByClassName("answerbox")[1].value
        let maxAnswer = document.getElementById("maxanswer").innerHTML
        let minAnswer = document.getElementById("minanswer").innerHTML
        if (maxGuess === maxAnswer && minGuess === minAnswer) {
            comment.innerHTML = "Excellent that is the correct answer!"
            comment.style.display = "block"
            document.getElementsByClassName("newbtn")[0].style.display = "inline"
        } else {
            comment.innerHTML =
                "Sorry that is the wrong answer, please try again or use the help buttons"
            comment.style.display = "block"
        }
    }
}

function update() {
    fields = document.getElementById("updateform").getElementsByTagName("input");
    comment = document.getElementById("comment")
    comment.style.width = "60%";
    if (fields[1].value != fields[2].value) {
        comment.innerHTML= "Passwords must match";
        comment.style.display = "block";
        comment.classList.add("alert");
        fields[1].classList.add("blink");
        fields[2].classList.add("blink");
        setTimeout(function() {
            fields[1].classList.remove("blink")
            fields[2].classList.remove("blink")
            comment.classList.remove("alert");
            comment.style.backgroundColor = "rgb(255, 255, 255, 0.8)";
            }, 3000
        )
        return false
    } else {
        data = $('#updateform').serialize()
        $.post("/update", data, function(data) {
            msg = ""
            if (data['email'] === true) {
                document.getElementById("storedEmail").innerHTML = `${fields[0].value}`
                msg += "Email"
                if (data['pass'] === true) {
                    msg += " and password updated"
                }
                else {
                    msg += " updated"
                }
            }
            else if (data['email'] === "taken"){
                msg += "Sorry email already in use"
                if (data['pass'] === true) {
                    msg += " but password has been updated"
                }
            }
            if (data['pass'] === true && data['email'] === false) {
                msg += "Password updated"
            }
            comment.innerHTML = msg
            comment.classList.remove("alert");;
            comment.style.display = "block"
            for (var i = 0; i < fields.length; i++) {
                fields[i].value = "";
            }
        })
    }

}

function returner() {
    window.location.href = '/test'

}

