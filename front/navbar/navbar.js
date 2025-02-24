
document.addEventListener('DOMContentLoaded', function() {
    // Login va register tugmalariga hodisalarni ulash
    const loginButton = document.getElementById('loginBtn');
    const signUpButton = document.getElementById('signUpBtn');
    const logoutButton = document.getElementById('logoutBtn');

    // Login tugmasini ulash
    if (loginButton) {
        loginButton.addEventListener('click', function() {
            window.location.href = './auth/login/main.html';
        });
    }

    // Register tugmasini ulash
    if (signUpButton) {
        signUpButton.addEventListener('click', function() {
            window.location.href = './auth/signup/main.html';
        });
    }

    // Logout tugmasini ulash
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('isLoggedIn');
            localStorage.removeItem('userData');
            window.location.reload(); // Sahifani yangilash
        });
    }

    // Sessiyani tekshirish va foydalanuvchi ma'lumotlarini ko'rsatish
    checkUserSession();
});

function checkUserSession() {
   const isLoggedIn = localStorage.getItem('isLoggedIn');
    const userData = localStorage.getItem('userData');

    const navButtons = document.querySelector('.nav-buttons');
    const userProfile = document.querySelector('.user-profile');

    if (isLoggedIn === 'true') {
        // Foydalanuvchi tizimga kirgan bo'lsa
        if (navButtons) navButtons.style.display = 'none';
        if (userProfile) {
            userProfile.style.display = 'flex';

            // Foydalanuvchi ismini ko'rsatish
            const profileName = document.querySelector('.profile-name');
            if (profileName && userData) {
            console.log(userData)
            console.log(profileName)
                profileName.textContent = userData;
            }
        }
    } else {
        // Foydalanuvchi tizimga kirmagan bo'lsa
        if (navButtons) navButtons.style.display = 'flex';
        if (userProfile) userProfile.style.display = 'none';
    }
}
