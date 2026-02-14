document.addEventListener('DOMContentLoaded', () => {
    const yearEl = document.getElementById('current-year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    const menuToggle = document.getElementById('menuToggle');
    const body = document.body;

    // Toggle Menu
    menuToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        body.classList.toggle('menu-open');
        const isOpen = body.classList.contains('menu-open');
        menuToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close menu when clicking a link
    const navLinks = document.querySelectorAll('.menuItem a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            body.classList.remove('menu-open');
            menuToggle.setAttribute('aria-expanded', 'false');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (body.classList.contains('menu-open') && !e.target.closest('#menu')) {
            body.classList.remove('menu-open');
            menuToggle.setAttribute('aria-expanded', 'false');
        }
    });
});