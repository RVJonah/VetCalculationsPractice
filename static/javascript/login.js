'use strict';
var Login = (function () {
    function login(event) {
        event.preventDefault();
        var data = $('#loginform').serialize();
        var msg = "";
        var fields = $("input");
        var comment = $("#comment");
        $.each(fields, function () {
            if (this.value === "") {
                msg += this.title + ' is required. <br>';
                Alerts.blink(this);
            }
        });
        if (msg) {
            Alerts.alert(comment, msg);
            return false;
        }
        $.post("/logincheck", data, function (data) {
            if (data === true) {
                $("#loginform").submit();
            } else {
                Alerts.alert(comment,"Username or password incorrect");
                fields[0].value = "";
                fields[1].value = "";
                return false;
            }
        });
    }
    return login;
}());

$(document).ready(function () {
    $("#logbtn").click(function (event) {
        Login(event);
    });
});