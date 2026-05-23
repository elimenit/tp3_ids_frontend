const panels = document.querySelectorAll('.panel');
const overlay = document.querySelector('.overlay');
panels.forEach(panel => {
    const btnId = panel.dataset.openby
    const btnElement = document.getElementById(btnId);
    btnElement.addEventListener('click', () => {
        panel.classList.toggle('open');
        overlay.classList.toggle('active');
    });
    overlay.addEventListener('click', () => {
        panel.classList.remove('open');
        overlay.classList.remove('active');
    });
});