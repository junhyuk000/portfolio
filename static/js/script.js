
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

function openEmailPopup() {
    window.open("{{ url_for('email') }}", "emailPopup", "width=600,height=700,resizable=yes,scrollbars=yes");
}

