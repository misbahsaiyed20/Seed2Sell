document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       TAB SWITCHING & SLIDER
    ========================= */
    const tabs = document.querySelectorAll(".sa-tab");
    const panes = document.querySelectorAll(".sa-pane");
    const slider = document.querySelector(".sa-tab-slider");

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {

            // Move the background slider smoothly
            if (slider) {
                slider.style.transform = `translateX(${index * 100}%)`;
            }

            // Remove active classes
            tabs.forEach(t => t.classList.remove("sa-tab--active"));
            panes.forEach(p => p.classList.remove("sa-pane--active"));

            // Add active to clicked tab
            tab.classList.add("sa-tab--active");

            // Show correct pane
            const target = tab.getAttribute("data-tab");
            const activePane = document.getElementById(target);
            if(activePane) {
                activePane.classList.add("sa-pane--active");
            }
        });
    });

    /* =========================
       INPUT FOCUS EFFECT
    ========================= */
    const inputs = document.querySelectorAll(".sa-input");

    inputs.forEach(input => {
        const box = input.closest(".sa-input-box");

        if (box) {
            input.addEventListener("focus", () => {
                box.classList.add("sa-focused");
            });

            input.addEventListener("blur", () => {
                box.classList.remove("sa-focused");
            });
        }
    });

    /* =========================
       PASSWORD SHOW / HIDE
    ========================= */
    const passwordFields = document.querySelectorAll("input[type='password']");

    passwordFields.forEach(field => {
        const box = field.closest(".sa-input-box");

        if (box) {
            // Create eye button safely
            const eye = document.createElement("button");
            eye.type = "button";
            eye.innerHTML = "👁";
            eye.classList.add("sa-eye");
            eye.title = "Toggle Password Visibility";

            box.appendChild(eye);

            eye.addEventListener("click", () => {
                if (field.type === "password") {
                    field.type = "text";
                    eye.innerHTML = "🙈";
                } else {
                    field.type = "password";
                    eye.innerHTML = "👁";
                }
            });
        }
    });

});