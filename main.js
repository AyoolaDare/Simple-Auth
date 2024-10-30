// Set the API endpoint
const API_BASE_URL = "";

// Utility function to check if user is logged in
function isLoggedIn() {
    return localStorage.getItem("username") !== null;
}

async function handleRegister(event) {
    event.preventDefault();

    const data = {
        httpMethod: "POST",
        path: "/register",
        body: JSON.stringify({
            username: document.getElementById("username").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    };

    try {
        console.log("Sending registration data:", data);
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log("Registration response:", result);

        if (response.ok) {
            alert("Registration successful!");
            document.getElementById("registerMessage").textContent = result.message;
            window.location.href = "login.html";
        } else {
            alert("Registration failed: " + (result.error || "Unknown error"));
            document.getElementById("registerMessage").textContent = result.error || "Unknown error";
        }
    } catch (error) {
        console.error("Error registering user:", error);
        document.getElementById("registerMessage").textContent = "Registration failed: Network error";
    }
}

async function handleLogin(event) {
    event.preventDefault();

    const data = {
        httpMethod: "POST",
        path: "/login",
        body: JSON.stringify({
            username: document.getElementById("loginUsername").value,
            password: document.getElementById("loginPassword").value
        })
    };

    try {
        console.log("Sending login data:", data);
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log("Login response:", result);

        if (response.ok) {
            const username = JSON.parse(data.body).username;
            localStorage.setItem("username", username);
            console.log("Username stored in localStorage:", username);
            alert("Login successful!");
            window.location.href = "dashboard.html";
        } else {
            alert("Login failed: " + (result.error || "Unknown error"));
            document.getElementById("loginMessage").textContent = result.error || "Unknown error";
        }
    } catch (error) {
        console.error("Error logging in:", error);
        document.getElementById("loginMessage").textContent = "Login failed: Network error";
    }
}

async function loadDashboard() {
    console.log("Attempting to load dashboard...");
    const username = localStorage.getItem("username");
    console.log("Retrieved username from localStorage:", username);

    if (!username) {
        console.log("No username found, redirecting to login");
        window.location.href = "login.html";
        return;
    }

    const dashboardMessage = document.getElementById("dashboardMessage");
    if (!dashboardMessage) {
        console.error("Dashboard message element not found!");
        return;
    }

    try {
        console.log("Fetching dashboard data for user:", username);
        const response = await fetch(`${API_BASE_URL}/dashboard?username=${username}`);
        const result = await response.json();
        console.log("Dashboard data received:", result);

        if (response.ok) {
            dashboardMessage.textContent = `Welcome, ${result.username}!`;
            if (result.email) {
                dashboardMessage.textContent += ` (${result.email})`;
            }
        } else {
            dashboardMessage.textContent = "Error loading dashboard: " + (result.error || "Unknown error");
        }
    } catch (error) {
        console.error("Error loading dashboard:", error);
        dashboardMessage.textContent = "Error loading dashboard: Network error";
    }
}

function handleLogout() {
    console.log("Logging out...");
    localStorage.clear(); // Clear all localStorage data
    alert("You have been logged out.");
    window.location.href = "login.html";
}

// Initialize page-specific functionality
function initializePage() {
    console.log("Current page:", window.location.pathname);

    // Register form handler
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", handleRegister);
    }

    // Login form handler
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", handleLogin);
    }

    // Logout button handler
    const logoutButton = document.getElementById("logout");
    if (logoutButton) {
        logoutButton.addEventListener("click", handleLogout);
        console.log("Logout button handler attached");
    }

    // Load dashboard if on dashboard page
    if (window.location.pathname.endsWith("dashboard.html")) {
        if (!isLoggedIn()) {
            window.location.href = "login.html";
        } else {
            loadDashboard();
        }
    }
}

// Initialize when DOM is fully loaded
document.addEventListener("DOMContentLoaded", initializePage);
