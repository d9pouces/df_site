document.addEventListener('DOMContentLoaded', function () {
    "use strict";
    document.querySelectorAll('[data-mpm-color]').forEach(function (element) {
        element.style.backgroundColor = element.getAttribute('data-mpm-color');
        if (element.classList.contains("html-color-5")) {
            element.style.width = "5em";
            element.style.height = "1em";
        } else {
            element.style.width = "2em";
            element.style.height = "1em";
        }
    });
});
