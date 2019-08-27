'use strict';
var Test = (function () {
    var qNum = 0;
    var questions = {};
    var answers = {};
    var testArea = null;
    var testList = null;
    return {
        createTestArea: function () {
            var testareablock = domCreate.element("article", {'id':"testarea"});
            domCreate.section("testinfo1", "Patient Details", testareablock);
            domCreate.section("testinfo2", "Treatment Details", testareablock);
            var question = domCreate.section("question", "Question", testareablock);
            domCreate.appendCreate("p", {'id': "info"}, question);
            domCreate.appendCreate("p", {'id': "quest"}, question);
            domCreate.appendCreate("p", {'id': "additional"}, question);
            domCreate.button({'id': "prevbtn", 'onclick': "Test.questionSelect(-1)"}, "Previous", question);
            domCreate.button({'id': "nextbtn", 'onclick': "Test.questionSelect(1)"}, "Next", question);
            domCreate.button({'id': "subbtn", 'onclick': "Test.storeAnswer()"}, "Submit", question);
            domCreate.button({'id': "completebtn", 'onclick': "Test.sendAnswers()"}, "Complete", question);
            $("Main").append(testareablock);
            testArea = testareablock;
    },
        deployQuestion: function () {
            $("#testinfo1 ul").remove();
            $("#testinfo2 ul").remove();
            $("#question p").empty()
            $("h1").html(`Question ${qNum + 1}`);
            domCreate.list({'id': "pdetail"}, questions[qNum].box1, $("#testinfo1"));
            domCreate.list({'id': "treatment"}, questions[qNum].box2, $("#testinfo2"));
            $("#info").text(questions[qNum].question.intro);
            $("#quest").text(questions[qNum].question.question);
            $("#additional").text(questions[qNum].question.otherinfo);

            if (questions[qNum].questType === "gasFlow") {
                var maxUnitDiv = domCreate.answerbox("max", "Max Flow Rate: ", "ANS1", "text", questions[qNum].question.units);
                var minUnitDiv = domCreate.answerbox("ANS2", "Min Flow Rate: ", "min", "text", questions[qNum].question.units);
                $("#quest").append(maxUnitDiv);
                $("#quest").append(minUnitDiv);
            } else {
                var answerDiv = domCreate.answerbox("max", "Answer: ", "ANS", "text", questions[qNum].question.units);
                $("#quest").append(answerDiv);
            }
        },
        displayResults: function (data) {
            $('h1').text("Results");
            $('main').append(data);
            $('#repeatbtn').attr('onclick', `Test.requestTest('${questions[10]}', 2)`);
            $('#returnbtn').attr('onclick', 'Test.returner()');
        },
        questionSelect: function (move) {
            if (move === 1) {
                qNum++;
            }
            if (move === -1) {
                qNum--;
            }
            if (qNum === 0) {
                $("#prevbtn").prop("disabled", "true");
            }
            if (qNum === 9) {
                $("#nextbtn").prop("disabled", "true");
                $("#completebtn").removeAttr("disabled");
            }
            if (qNum > 0) {
                $("#prevbtn").removeAttr("disabled");
            }
            if (qNum < 9) {
                $("#nextbtn").removeAttr("disabled");
                $("#completebtn").prop("disabled", "true");
            }
            this.deployQuestion();
        },
        requestTest: function (event, repeat) {
            var qtype = {};
            if (repeat === 1) {
                var testType =(event.parentElement.id);
                qtype.TType = testType;
            } else {
                qtype.TType = event
            }
            if (repeat === 1) {
                testList= $("#testlist").detach();
                if (testArea === null) {
                    this.createTestArea();
                } else {
                    $('main').append(testArea);
                }
            }
            if (repeat === 2) {
                $('main').append(testArea);
                $('#results').remove();
            }
            $.post("/test", qtype, function(data) {
                qNum = 0;
                questions = data;
                for (var i = 0; i < 10; i++) {
                    answers[i] = "";
                } 
                answers.TType = data[10];
                console.log(answers);
                Test.questionSelect(0);
            });
        },
        returner: function() {
            $('h1').text("Test");
            $('#results').remove();
            $('main').append(testList);
        },
        sendAnswers: function () {
            if (confirm ("Are you sure you wish to submit your answers?")) {
                $.post("/results", answers, function (data) {
                    qNum = 0;
                    Test.displayResults(data);
                    $('h1').text("Results");
                    $('#testarea').detach();
                });
            }
        },
        storeAnswer : function () {
            if (questions[qNum]['questType'] === "gasFlow") {
                answers[qNum] = $('#ANS1').val();
                answers[`${qNum}min`] = $('#ANS2').val();

            } else {
                answers[qNum] = $('#ANS').val();
            }
            if (qNum === 9) {
                questionSelect(0);
            } else {
                questionSelect(1);
            }
        }
    };
}());

$(document).ready(function () {
    $.each($('button'), function (index, button) {
        button.setAttribute("onclick", "Test.requestTest(this, 1)");
    });
});