// scripts.js
// Toggle billing plan display between monthly and yearly
document.addEventListener("DOMContentLoaded", function () {
    console.log("scripts.js loaded and DOM ready");
    const alerts = document.querySelectorAll('.auto-dismiss');
    console.log("Found", alerts.length, "alerts");

    const toggleGroup = document.getElementById("billing-toggle");
    if (!toggleGroup) return; // gracefully exit if not found

    const buttons = toggleGroup.querySelectorAll("button");
    const prices = document.querySelectorAll(".price");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            // Toggle active class
            buttons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            // Switch prices
            const billing = button.dataset.billing; // 'monthly' or 'yearly'
            prices.forEach(span => {
                span.textContent = span.dataset[billing];
            });

            // Update /month label
            const label = billing === "monthly" ? "/month" : "/year";
            document.querySelectorAll(".fs-6.text-muted").forEach(el => {
                el.textContent = label;
            });
        });
    });

    alerts.forEach(function (alert) {
        setTimeout(() => {
            console.log("Fading alert:", alert.textContent.trim());
            alert.classList.add('fade-out');
            alert.addEventListener('transitionend', () => {
                alert.remove();
                console.log("Alert removed");
            });
        }, 4000);
    });

});

// Auto-fade Django messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.auto-dismiss');

    alerts.forEach(function (alert) {
        setTimeout(() => {
            alert.classList.add('fade-out'); // triggers CSS fade
            // Remove from DOM after transition
            setTimeout(() => alert.remove(), 800);
        }, 4000);
    });
});