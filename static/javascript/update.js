'use strict';
var Update = (function () {
    function update (event) {
        event.preventDefault();
        var fields = $("input");
        var data = $('#updateform').serialize()
        var [email, pass, conf] = fields;
        var msg = "";
        var comment = $("#comment");
        if (email.value === "" && pass.value === "" && conf.value === "")
        {
            return false;
        }
        if (pass.value != conf.value) {
            Alerts.alert(comment,"Passwords must match");
            Alerts.blink(pass);
            Alerts.blink(conf);
            return false
        } else {
            $.post("/update", data, function (data) {
                if (data['email'] === true) {
                    msg += "Email";
                    $("#updemail").attr("placeholder", email.value );
                    if (data['pass'] === true) {
                        msg += " and password updated";
                    }
                    else {
                        msg += " updated";
                    }
                }
                else if (data['email'] === "taken"){
                    msg += "Sorry email already in use";
                    if (data['pass'] === true) {
                        msg += " but password has still been updated";
                    }
                }
                if (data['pass'] === true && data['email'] === false) {
                    msg += "Password updated";
                }
                Alerts.alert(comment, msg);
                $.each(fields, function () {
                    this.value = "";
                });
            })
        }

    }
    return update;
}())

$(document).ready(function () {
    $("#updatebtn").click(function (event) {
        Update(event);
    });
});