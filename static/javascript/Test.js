'use strict';
var Test = (function () {
    var testObj = {
        qNum: 0,
        questions: {
        },
        answers: {},
        testArea: null,
        testList: null,
        createTestArea: function () {
            var testarea = domCreate.element("article", {'id':"testarea"});
            domCreate.section("testinfo1", "Patient Details", testarea);
            domCreate.section("testinfo2", "Treatment Details", testarea);
            var question = domCreate.section("question", "Question", testarea);
            domCreate.appendCreate("p", {'id': "info"}, question);
            domCreate.appendCreate("p", {'id': "quest"}, question);
            domCreate.appendCreate("p", {'id': "additional"}, question);
            domCreate.button({'id': "prevbtn", 'onclick': "Test.questionSelect(-1)"}, "Previous", question);
            domCreate.button({'id': "nextbtn", 'onclick': "Test.questionSelect(1)"}, "Next", question);
            domCreate.button({'id': "subbtn", 'onclick': "Test.storeAnswer()"}, "Submit", question);
            domCreate.button({'id': "completebtn", 'onclick': "Test.sendAnswers(Test.answers)"}, "Complete", question);
            $("Main").append(testarea);
            this.testArea = testarea;
        },
        deployQuestion: function () {
            $("#testinfo1 ul").remove();
            $("#testinfo2 ul").remove();
            $("#question p").empty()
            $("h1").html(`Question ${this.qNum + 1}`);
            domCreate.list({'id': "pdetail"}, this.questions[this.qNum].box1, $("#testinfo1"));
            domCreate.list({'id': "treatment"}, this.questions[this.qNum].box2, $("#testinfo2"));
            $("#info").text(this.questions[this.qNum].question.intro);
            $("#quest").text(this.questions[this.qNum].question.question);
            $("#additional").text(this.questions[this.qNum].question.otherinfo);

            if (this.questions[this.qNum].questType === "gasFlow") {
                var maxUnitDiv = domCreate.answerbox("max", "Max Flow Rate: ", "ANS1", "text", this.questions[this.qNum].question.units);
                var minUnitDiv = domCreate.answerbox("ANS2", "Min Flow Rate: ", "min", "text", this.questions[this.qNum].question.units);
                $("#quest").append(maxUnitDiv);
                $("#quest").append(minUnitDiv);
            } else {
                var answerDiv = domCreate.answerbox("max", "Answer: ", "ANS", "text", this.questions[this.qNum].question.units);
                $("#quest").append(answerDiv);
            }
        },
        displayResults: function (data) {
            $('h1').text("Results");
            $('main').append(data);
            $('#repeatbtn').attr('onclick', `Test.requestTest('${Test.questions[10]}', 2)`);
            $('#returnbtn').attr('onclick', 'Test.returner()');
        },
        questionSelect: function (move) {
            if (move === 1) {
                this.qNum++;
            }
            if (move === -1) {
                this.qNum--;
            }
            if (this.qNum === 0) {
                $("#prevbtn").prop("disabled", "true");
            }
            if (this.qNum === 9) {
                $("#nextbtn").prop("disabled", "true");
                $("#completebtn").removeAttr("disabled");
            }
            if (this.qNum > 0) {
                $("#prevbtn").removeAttr("disabled");
            }
            if (this.qNum < 9) {
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
                this.testList= $("#testlist").detach();
                if (this.testArea === null) {
                    this.createTestArea();
                } else {
                    $('main').append(this.testArea);
                }
            }
            if (repeat === 2) {
                $('main').append(this.testArea);
                $('#results').remove();
            }
            $.post("/test", qtype, function(data) {
                Test.qNum = 0;
                Test.questions = data;
                for (var i = 0; i < 10; i++) {
                    Test.answers[i] = "";
                } 
                Test.answers.TType = data[10];
                Test.questionSelect(0);
            });
        },
        returner: function() {
            $('h1').text("Test");
            $('#results').remove();
            $('main').append(this.testList);
        },
        sendAnswers: function (answers) {
            if (confirm ("Are you sure you wish to submit your answers?")) {
                $.post("/results", answers, function (data) {
                    Test.qNum = 0;
                    Test.displayResults(data);
                    $('h1').text("Results");
                    $('#testarea').detach();
                });
            }
        },
        storeAnswer : function () {
            if (this.questions[this.qNum]['questType'] === "gasFlow") {
                this.answers[this.qNum] = $('#ANS1').val();
                this.answers[`${this.qNum}min`] = $('#ANS2').val();

            } else {
                this.answers[this.qNum] = $('#ANS').val();
            }
            if (this.qNum === 9) {
                this.questionSelect(0);
            } else {
                this.questionSelect(1);
            }
        }
    };
    return testObj;
}());

$(document).ready(function () {
    $.each($('button'), function (index, button) {
        button.setAttribute("onclick", "Test.requestTest(this, 1)");
    });
});