'use strict';

$(document).ready(function () {
    $("#navBtn").click(function () {
        $("nav ul").slideToggle(800, function () {
            $(this).toggleClass("nav-expanded").css("display", "");
        });
    });
});