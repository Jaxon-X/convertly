// auth.js

// API endpoints
const API_ENDPOINTS = {
    login: 'http://127.0.0.1:8000/api/user/login/',
    register: 'http://127.0.0.1:8000/api/user/register/'
};

// Form validation
const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

const validatePassword = (password) => {
    return password.length >= 8;
};

const validateUsername = (username) => {
    return /^[a-zA-Z\s]+$/.test(username); // faqat harflar va probel
};

// Show error message
const showError = (elementId, message) => {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
};

// Clear error messages
const clearErrors = () => {
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(element => {
        element.style.display = 'none';
        element.textContent = '';
    });
};
//
//// Handle login
//const handleLogin = async (e) => {
//    e.preventDefault();
//    clearErrors();
//
//    const email = document.getElementById('email').value;
//    const password = document.getElementById('password').value;
//
//    // Validation
//    if (!validateEmail(email)) {
//        showError('emailError', 'Please enter a valid email address');
//        return;
//    }
//
////    if (!validatePassword(password)) {
////        showError('passwordError', 'Password must be at least 8 characters long');
////        return;
////    }
//
//    try {
//        const response = await fetch(API_ENDPOINTS.login, {
//            method: 'POST',
//            headers: {
//                'Content-Type': 'application/json'
//            },
//            body: JSON.stringify({ email, password })
//        });
//
//        const data = await response.json();
//
//        if (!response.ok) {
//            throw new Error(data.error || 'Login failed');
//        }
//
//        // Save tokens
//        localStorage.setItem('accessToken', data.access);
//        localStorage.setItem('refreshToken', data.refresh);
//
//        // Redirect to main page
//        window.location.href = '/front/index.html';
//
//    } catch (error) {
//        showError('emailError', error.message);
//    }
//};

// Handle registration
const handleRegister = async (e) => {
    e.preventDefault();
    clearErrors();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Validation
    if (!validateUsername(username)) {
        showError('usernameError', 'Username should only contain letters');
        return;
    }

    if (!validateEmail(email)) {
        showError('emailError', 'Please enter a valid email address');
        return;
    }

    if (!validatePassword(password)) {
        showError('passwordError', 'Password must be at least 8 characters long');
        return;
    }

    try {
        const response = await fetch(API_ENDPOINTS.register, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Registration failed');
        }

        // Show success message and redirect to login
        window.location.href = '../login/main.html';

    } catch (error) {
        showError('emailError', error.message);
    }
};

if (document.getElementById('signupForm')) {
    document.getElementById('signupForm').addEventListener('submit', handleRegister);
}

//// Add event listeners
//if (document.getElementById('loginForm')) {
//    document.getElementById('loginForm').addEventListener('submit', handleLogin);
//}

