
document.querySelectorAll('.service-card').forEach(card => {
    card.style.cursor = "pointer";
    card.addEventListener('click', function() {
        const page = this.getAttribute('data-page');
        if (!page) return;

        const cleanPath = page.replace('.html', '');
        history.pushState({}, '', cleanPath);
        loadPage(page);
    });
});

// Load page content via AJAX
function loadPage(page) {
    fetch(page)
        .then(response => {
            if (!response.ok) throw new Error('Page not found');
            return response.text();
        })
        .then(html => {
            document.querySelector('.content').innerHTML = html;
        })
        .catch(error => {
            console.error('Page load failed:', error);
            window.location.href = page;
        });
}
//
//// Navigation handling
//const routes = {
//    '/': 'index.html',
//    '/word-to-pdf': '/home/jaxon/Python_Projects/convertly/front/pages/wordtopdf/index.html'
//};
//
//function handleRoute(pathname) {
//    const page = routes[pathname] || routes['/'];
//    loadPage(page);
//}
//
//// Event listeners for navigation
//document.querySelector('.converter-page').onclick = (e) => {
//    e.preventDefault();
//    history.pushState({}, '', '/');
//    handleRoute('/');
//};
//
//document.querySelector('.service-url').onclick = (e) => {
//    e.preventDefault();
//    history.pushState({}, '', '/word-to-pdf');
//    handleRoute('/word-to-pdf');
//};

// Browser back/forward button handling
window.onpopstate = () => handleRoute(window.location.pathname);

// Initial route handling
handleRoute(window.location.pathname);