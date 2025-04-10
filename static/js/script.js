
function toggleTheme() {
    document.body.classList.toggle('light');
}
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function toggleFab() {
    const buttons = document.getElementById('fab-buttons');
    buttons.style.display = (buttons.style.display === 'flex') ? 'none' : 'flex';
}
