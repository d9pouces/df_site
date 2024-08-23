import {showCookieBar} from 'django-cookie-consent';

document.addEventListener("DOMContentLoaded", () => {
    const template = document.getElementById("cookie-consent__cookie-bar");
    const statusUrl = template.dataset.dfCookiesStatus;
    showCookieBar({
        statusUrl: statusUrl,
        templateSelector: '#cookie-consent__cookie-bar',
        cookieGroupsSelector: '#cookie-consent__cookie-groups',
        onShow: () => document.querySelector('body').classList.add('with-cookie-bar'),
        onAccept: () => document.querySelector('body').classList.remove('with-cookie-bar'),
        onDecline: () => document.querySelector('body').classList.remove('with-cookie-bar'),
    });
});

