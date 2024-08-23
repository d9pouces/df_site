document.addEventListener("DOMContentLoaded", () => {
    const allauthEmailRemoveTitleElt = document.getElementById("allauth-email-remove-title");
    if (allauthEmailRemoveTitleElt) {
        const message = JSON.parse(allauthEmailRemoveTitleElt.textContent);
        document.querySelectorAll('.btn-danger[name=action_remove]').forEach((action) => {
            action.addEventListener("click", function(e) {
                if (!confirm(message)) {
                    e.preventDefault();
                }
            });
        });
    }
})
