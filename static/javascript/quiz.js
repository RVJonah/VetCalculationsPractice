'use strict';

var AnswerCheck = (function () {
    function answercheck() {
        var comment = $("#comment");
        if ($("#answer")) {
            var guess = $("#answerbox").val();
            var answer = $("#answer").text();
            if (guess === answer) {
                Alerts.alert(comment, "Excellent that is the correct answer!");
                $("#newbtn").css("visibility", "visible");
                $(".disable").attr("disabled", "true");
            } else {
                Alerts.alert(comment, "Sorry that is the wrong answer, please try again or use the help buttons");
            }
        } else {
            var maxGuess = $("#maxguess").val();
            var minGuess = $("#minguess").val();
            var maxAnswer = $("#maxguess").text();
            var minAnswer = $("#maxanswer").text();
            if (maxGuess === maxAnswer && minGuess === minAnswer) {
                Alerts.alert(comment, "Excellent that is the correct answer!");
                $("#newbtn").css("visibility", "visible");
                $(".disable").attr("disabled", "true");
            } else {
                Alerts.alert(comment, "Sorry that is the wrong answer, please try again or use the help buttons")
            }
        }
    }
    return answercheck;
}());

$(document).ready(function () {
    $("#hintbtn").click(function () {
        DOM.hint();
    });
    $("#answerbtn").click(function () {
        DOM.answer();
    });
    $("#submitbtn").click(function () {
        AnswerCheck();
    });
    $("#newbtn").click(function () {
        location.reload(true);
    });
});





