// Auto-dismiss alerts after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            const instance = bootstrap.Alert.getOrCreateInstance(alert);
            instance.close();
        }, 5000);
    });
});

// Close the navbar when clicking outside of it
// This is to ensure the navbar collapses when clicking outside of it
document.addEventListener('click', function (event) {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const isOpen = navbarCollapse.classList.contains('show');

    // Check if click is outside the navbar
    if (isOpen && !navbarCollapse.contains(event.target)) {
        const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
            toggle: true,
        });
        bsCollapse.hide();
    }
});

// Cookies consent banner
document.addEventListener("DOMContentLoaded", function () {
    const banner = document.getElementById("cookie-banner");
    const acceptBtn = document.getElementById("cookie-accept");
    const rejectBtn = document.getElementById("cookie-reject");

    const consent = localStorage.getItem("cookieConsent");

    if (!consent) {
        banner.style.display = "block";
    }

    acceptBtn.addEventListener("click", function () {
        localStorage.setItem("cookieConsent", "accepted");
        banner.style.display = "none";
        // Optional: enable analytics
    });

    rejectBtn.addEventListener("click", function () {
        localStorage.setItem("cookieConsent", "rejected");
        banner.style.display = "none";
        // Optional: disable analytics
        window["ga-disable-UA-XXXXXXX-Y"] = true; // Replace with your GA ID
    });
});

// Admin user management form validation and dynamic population
document.addEventListener('DOMContentLoaded', function () {
    // Form validation
    const updateForm = document.getElementById('updateUserForm');
    const alertBox = document.getElementById('warningAlert');

    if (updateForm) {
        updateForm.addEventListener('submit', function (e) {
            if (!updateForm.checkValidity()) {
                e.preventDefault();
                alertBox.classList.remove('d-none');
                updateForm.classList.add('was-validated');
            } else {
                alertBox.classList.add('d-none');
                updateForm.classList.remove('was-validated');
            }
        });
    }

    // Dynamic form population
    const rawJsonElement = document.getElementById('userDataJson');
    let userData = {};

    if (rawJsonElement) {
        const rawJson = rawJsonElement.textContent.trim();

        if (rawJson && rawJson !== "undefined") {
            try {
                userData = JSON.parse(rawJson);
            } catch (error) {
                console.error("❌ Failed to parse user data JSON:", error);
                return;
            }
        } else {
            console.warn("⚠️ rawJson is empty or invalid:", rawJson);
        }
    }

    const userSelect = document.getElementById('userSelect');
    if (userSelect) {
        userSelect.addEventListener('change', function () {
            const selectedId = this.value;
            const data = userData[selectedId];

            if (data) {
                document.getElementById('firstName').value = data.first_name || '';
                document.getElementById('lastName').value = data.last_name || '';
                document.getElementById('emailUpdate').value = data.email || '';
                document.getElementById('isActive').value = data.is_active ? 'true' : 'false';
                document.getElementById('isStaff').value = data.is_staff ? 'true' : 'false';
            }
        });
    }
});