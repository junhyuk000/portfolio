
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
function openYoutubePopup() {
    const width = 800;
    const height = 450;
    const left = (window.innerWidth - width) / 2;
    const top = (window.innerHeight - height) / 2;

    const url = "https://www.youtube.com/embed/5LbdMNlKQfM?autoplay=1";

    window.open(
        url,
        "youtubePopup",
        `width=${width},height=${height},left=${left},top=${top},resizable=yes`
    );
}

function openSmartcityYoutubePopup() {
    const width = 800;
    const height = 450;
    const left = (window.innerWidth - width) / 2;
    const top = (window.innerHeight - height) / 2;
    const url = "https://www.youtube.com/embed/Wto9AjWays8?autoplay=1";

    window.open(
        url,
        "smartcityYoutubePopup",
        `width=${width},height=${height},left=${left},top=${top},resizable=yes`
    );
}

