document.addEventListener("DOMContentLoaded", () => {
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
    const root = document.querySelector("html");
    if ((root.dataset.bsTheme === "auto") && prefersDarkScheme.matches) {
        root.dataset.bsTheme = root.dataset.dfDarkTheme;
    } else if (root.dataset.bsTheme === "auto") {
        root.dataset.bsTheme = root.dataset.dfLightTheme;
    }

    document.querySelectorAll("a.df-theme-switcher").forEach((a: HTMLAnchorElement) => {
        a.addEventListener("click", (event) => {
            event.preventDefault();
            const response = fetch(a.href, {
                headers: {
                    "Accept": "application/json",
                },
            });
            response.then((response) => {
                if (response.ok) {
                    try {
                        response.json().then((json) => {
                            root.dataset.bsTheme = json.theme;
                            document.querySelectorAll("a.df-theme-switcher").forEach((a_: HTMLAnchorElement) => {
                                a_.href = json.href;
                                a.innerHTML = "<i class=\"fa fa-" + json.icon + "\"></i>";
                            });
                        });
                    } catch (e) {
                        console.error("Failed to switch theme", e);
                    }
                } else {
                    console.error("Failed to switch theme", response);
                }

            });
        });

    });
});

