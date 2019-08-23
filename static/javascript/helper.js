'use strict';
var DOM = (function() {
    var DOMobj = {
        display: function (element) {
            $(element).show();
            $(element).addClass("alert");
        },
        answer: function () {
            var comment = $("#comment");
            this.display("#hint");
            this.display("#ans");
            Alerts.alert(comment, "Now you've seen how it's done maybe try another question?");
            $("#submitbtn").attr("disabled", "true");
            $("#newbtn").css("visibility", "visible");
        },
        hint: function () {
            this.display("#hint");
        },
        redirect: function (location) {
                window.location.href = location;
        }
    };
    return DOMobj;
}());

var Alerts = (function (){
    var Alerts = {
        alert: function (element, error) {
            element.html(error);
            element.show();
            element.addClass("alert");
            setTimeout(function () {
                element.removeClass("alert");
            }, 3000);
        },
        blink: function (element) {
            element.classList.add("blink");
            setTimeout(function () {
                element.classList.remove("blink");
            }, 3000);
        }
    };
    return Alerts;
}());
