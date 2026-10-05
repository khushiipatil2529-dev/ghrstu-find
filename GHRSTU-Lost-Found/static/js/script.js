/* =========================================================
   GHRSTU FIND
   Interactive Frontend
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       BUTTON RIPPLE EFFECT
    ========================== */

    const buttons = document.querySelectorAll("button");

    buttons.forEach((button) => {

        button.addEventListener("click", function (event) {

            const ripple = document.createElement("span");

            ripple.classList.add("ripple");

            const rect = button.getBoundingClientRect();

            ripple.style.left =
                `${event.clientX - rect.left}px`;

            ripple.style.top =
                `${event.clientY - rect.top}px`;

            button.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);

        });

    });


    /* =========================
       SMOOTH NAVIGATION
    ========================== */

    const navLinks = document.querySelectorAll(
        'a[href^="#"]'
    );

    navLinks.forEach((link) => {

        link.addEventListener("click", (event) => {

            const targetId =
                link.getAttribute("href");

            const target =
                document.querySelector(targetId);

            if (target) {

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        });

    });


    /* =========================
       SCROLL REVEAL
    ========================== */

    const revealElements = document.querySelectorAll(
        ".stat-card, .item-card, .step, .action-card"
    );


    const revealObserver =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        entry.target.classList.add(
                            "reveal-visible"
                        );

                        revealObserver.unobserve(
                            entry.target
                        );

                    }

                });

            },
            {
                threshold: 0.12
            }
        );


    revealElements.forEach((element) => {

        element.classList.add("reveal-hidden");

        revealObserver.observe(element);

    });


    /* =========================
       MOUSE PARALLAX
    ========================== */

    const heroVisual =
        document.querySelector(".hero-visual");


    if (heroVisual) {

        heroVisual.addEventListener(
            "mousemove",
            (event) => {

                const rect =
                    heroVisual.getBoundingClientRect();

                const x =
                    event.clientX - rect.left;

                const y =
                    event.clientY - rect.top;

                const moveX =
                    (x / rect.width - 0.5) * 12;

                const moveY =
                    (y / rect.height - 0.5) * 12;

                heroVisual.style.transform =
                    `translate(${moveX}px, ${moveY}px)`;

            }
        );


        heroVisual.addEventListener(
            "mouseleave",
            () => {

                heroVisual.style.transform =
                    "translate(0, 0)";

            }
        );

    }


    /* =========================
       NAVBAR SCROLL EFFECT
    ========================== */

    const navbar =
        document.querySelector(".navbar");


    window.addEventListener(
        "scroll",
        () => {

            if (!navbar) return;

            if (window.scrollY > 50) {

                navbar.classList.add(
                    "navbar-scrolled"
                );

            } else {

                navbar.classList.remove(
                    "navbar-scrolled"
                );

            }

        }
    );


    /* =========================
       DYNAMIC YEAR
    ========================== */

    const footerYear =
        document.querySelector(
            "footer span"
        );


    if (footerYear) {

        footerYear.textContent =
            `© ${new Date().getFullYear()} G H Raisoni Skill Tech University`;

    }


    /* =========================
       ITEM CARD TILT
    ========================== */

    const itemCards =
        document.querySelectorAll(".item-card");


    itemCards.forEach((card) => {

        card.addEventListener(
            "mousemove",
            (event) => {

                const rect =
                    card.getBoundingClientRect();

                const x =
                    event.clientX - rect.left;

                const y =
                    event.clientY - rect.top;

                const rotateX =
                    ((y / rect.height) - 0.5) * -5;

                const rotateY =
                    ((x / rect.width) - 0.5) * 5;

                card.style.transform =
                    `perspective(800px)
                     rotateX(${rotateX}deg)
                     rotateY(${rotateY}deg)
                     translateY(-6px)`;

            }
        );


        card.addEventListener(
            "mouseleave",
            () => {

                card.style.transform =
                    "";

            }
        );

    });


    /* =========================
       WELCOME CONSOLE
    ========================== */

    console.log(
        "%c GHRSTU FIND ",
        "background: linear-gradient(90deg,#8b5cf6,#ec4899); color:white; padding:8px 15px; border-radius:8px; font-weight:bold;"
    );

    console.log(
        "Lost something? Let's find it. 🔎"
    );

});
/* =========================================================
   REPORT UX — drag/drop + toast auto-hide
   ========================================================= */
const toastElements = document.querySelectorAll(".toast");
toastElements.forEach((toast) => {
    setTimeout(() => {
        toast.style.transition = "opacity .35s ease, transform .35s ease";
        toast.style.opacity = "0";
        toast.style.transform = "translateY(-8px)";
        setTimeout(() => toast.remove(), 400);
    }, 4200);
});

const uploadBox = document.querySelector(".upload-box");
const imageInput = document.getElementById("image");
if (uploadBox && imageInput) {
    ["dragenter", "dragover"].forEach((eventName) => {
        uploadBox.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadBox.classList.add("drag-active");
        });
    });
    ["dragleave", "drop"].forEach((eventName) => {
        uploadBox.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadBox.classList.remove("drag-active");
        });
    });
    uploadBox.addEventListener("drop", (event) => {
        const files = event.dataTransfer.files;
        if (files && files.length) {
            imageInput.files = files;
            imageInput.dispatchEvent(new Event("change", { bubbles: true }));
        }
    });
}
