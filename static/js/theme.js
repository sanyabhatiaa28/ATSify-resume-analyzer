// --- UNIFIED PERSISTENT THEME PARSING ENGINE ---
// Searches for either class name variation to keep both pages happy!
const themeToggleBtn = document.querySelector('.theme-toggle') || document.querySelector('.theme-toggle-btn');

// 1. Check local storage memory immediately on layout load
const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
    if (themeToggleBtn) themeToggleBtn.textContent = '☀️'; // Switch to sun icon
} else {
    document.body.classList.remove('dark-mode');
    if (themeToggleBtn) themeToggleBtn.textContent = '🌙'; // Ensure moon icon
}

// 2. Click event listener to persist choices across redirects
if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        
        let theme = 'light';
        if (document.body.classList.contains('dark-mode')) {
            theme = 'dark';
            themeToggleBtn.textContent = '☀️';
        } else {
            themeToggleBtn.textContent = '🌙';
        }
        
        // Save the selection right to browser memory
        localStorage.setItem('theme', theme);
    });
}

// --- SAFE LOGIN / SIGNUP VIEW TOGGLING ---
const loginSection = document.getElementById("login-section");
const signupSection = document.getElementById("signup-section");
const switchToSignupLink = document.getElementById("go-to-signup");
const switchToLoginLink = document.getElementById("go-to-login");

if (switchToSignupLink && switchToLoginLink && loginSection && signupSection) {
    switchToSignupLink.addEventListener("click", (e) => {
        e.preventDefault();
        loginSection.style.display = "none";
        signupSection.style.display = "block";
    });

    switchToLoginLink.addEventListener("click", (e) => {
        e.preventDefault();
        signupSection.style.display = "none";
        loginSection.style.display = "block";
    });
}

// --- SAFE PASSWORD VISIBILITY EYE TOGGLE ---
const eyeIcons = document.querySelectorAll(".toggle-password");
eyeIcons.forEach(icon => {
    icon.addEventListener("click", function() {
        const targetId = this.getAttribute("data-target");
        const passwordInput = document.getElementById(targetId);
        
        if (passwordInput && passwordInput.type === "password") {
            passwordInput.type = "text";
            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");
        } else if (passwordInput) {
            passwordInput.type = "password";
            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");
        }
    });
});

// --- SAFE BACKEND LOGIN / SIGNUP SUBMISSIONS ---
const signupForm = document.getElementById("signup-form");
if (signupForm) {
    signupForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append("username", document.getElementById("signup-username").value);
        formData.append("email", document.getElementById("signup-email").value);
        formData.append("password", document.getElementById("signup-password").value);
        
        fetch("/signup", { method: "POST", body: formData })
        .then(response => {
            if (response.ok) {
                alert("Signup successful, bro! Redirecting you to login.");
                signupForm.reset();
                if(signupSection && loginSection) {
                    signupSection.style.display = "none";
                    loginSection.style.display = "block";
                }
            } else {
                return response.text().then(text => { alert(text); });
            }
        })
        .catch(err => alert("Error during signup: " + err));
    });
}

const loginForm = document.getElementById("login-form");
if (loginForm) {
    loginForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append("email", document.getElementById("login-email").value);
        formData.append("password", document.getElementById("login-password").value);
        
        fetch("/login", { method: "POST", body: formData })
        .then(response => {
            if (response.redirected) {
                // Securely transition window viewport directly to authenticated dashboard
                window.location.href = response.url;
            } else {
                return response.text().then(text => { alert(text); });
            }
        })
        .catch(err => alert("Error during login: " + err));
    });
}