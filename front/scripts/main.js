document.querySelectorAll('.service-card').forEach(card => {
    card.style.cursor = "pointer"; // Kursorni pointer qilish

    card.addEventListener('click', function () {
        const page = this.getAttribute('data-page'); // Kartaga tegishli sahifa nomi
        if (!page) return;

        // URLni pushState orqali o'zgartiramiz
        history.pushState({}, '', page.replace('.html', ''));

        // To'g'ridan-to'g'ri sahifaga o'tish
        window.location.href = page;
    });
});


// Sahifani AJAX orqali yuklash
function loadPage(page) {
    fetch(page)
        .then(response => {
            if (!response.ok) {
                throw new Error('Sahifa topilmadi');
            }
            return response.text();
        })
        .then(html => {
            document.querySelector('.content').innerHTML = html;
        })
        .catch(error => {
            console.error('Sahifa yuklanmadi:', error);
            // Agar xato bo'lsa, sahifani to'g'ridan-to'g'ri ochamiz
            window.location.href = page;
        });
}

// Brauzerning "Orqaga" tugmasi bosilganda sahifani yuklash
window.addEventListener('popstate', () => {
    const page = location.pathname.split('/').pop() || 'home.html';
    loadPage(page);
});
