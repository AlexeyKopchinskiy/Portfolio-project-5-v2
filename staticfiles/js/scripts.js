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