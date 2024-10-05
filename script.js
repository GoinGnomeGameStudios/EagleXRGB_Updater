document.addEventListener("DOMContentLoaded", function() {
    // Section toggling for new features, improvements, and bug fixes
    const sections = document.querySelectorAll('.section-title');
    sections.forEach(section => {
        section.addEventListener('click', () => {
            const items = section.nextElementSibling;
            items.style.display = items.style.display === 'none' ? 'block' : 'none';
            section.classList.toggle('active');
        });
    });

    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Dark/Light mode toggle
    const modeToggle = document.getElementById('mode-toggle');
    modeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        modeToggle.textContent = isDark ? "Switch to Light Mode" : "Switch to Dark Mode";
    });
});
