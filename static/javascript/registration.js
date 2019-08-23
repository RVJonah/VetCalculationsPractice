'use strict';
var Registration = (function () {
    function registration(event) {
        event.preventDefault();
        var fields = $("input");
        var msg = "";
        var comment = $("#comment");
        var regdata = $('#regform').serialize();
        var [username, pass, confpass, email, confemail, fname, sname, college] = fields;
        $.each(fields, function(index) {
            if (this.value === "") {
                msg += this.title + ' is required. <br>';
                Alerts.blink(this);
            }
        });
        if (msg) {
            Alerts.alert(comment, msg);
            return false;
        }
        if (pass.value !== confpass.value) {
            Alerts.alert(comment, "Passwords need to match");
            return false;
        }
        if (email.value !== confemail.value) {
            Alerts.alert(comment, "Email addresses must match");
            return false;
        }
        $.get("/registercheck?username=" + username.value + "&mail=" + email.value,null,function (data) {
            if (data === true){
                $("#regform").submit();
            } else {
                if (data['username'] === true) {  
                    username.value = ""
                    Alerts.blink(username);
                    Alerts.alert(comment, "Sorry that username already taken");
                    return;
                } if (data['email'] === true) {
                    Alerts.blink(email);
                    Alerts.alert(comment,"That Email address already already registered");
                    return;
                } else {
                    username.value = ""
                    Alerts.blink(username);
                    Alerts.alert(comment, "Sorry that username already taken");
                    return;
                }
            }
        })
    }
    return registration;
}());

$(document).ready(function () {
    $("#regbtn").click(function(event) {
        Registration(event);
    });
});