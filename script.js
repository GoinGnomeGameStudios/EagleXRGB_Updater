document.addEventListener("DOMContentLoaded", function () {
    const modeToggle = document.getElementById("mode-toggle");
    const sections = document.querySelectorAll(".section-title");

    // Toggle Dark Mode
    modeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
    });

    // Expand/Collapse sections
    sections.forEach(section => {
        section.addEventListener("click", function () {
            const items = section.nextElementSibling;
            items.style.display = items.style.display === "block" ? "none" : "block";
            section.classList.toggle("active");
        });
    });
});
