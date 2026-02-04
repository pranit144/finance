// Authentication Logic

const { API_BASE_URL, TOKEN_KEY, USER_KEY } = window.CONFIG;
const { showError, showSuccess, validateEmail, validatePassword, setLoading, animateFormSwitch } = window.utils;

// Current auth mode
let authMode = 'login'; // 'login' or 'signup'

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  // Check if already authenticated
  if (getToken()) {
    redirectToDashboard();
    return;
  }
  
  // Set up event listeners
  setupEventListeners();
  
  // Set initial mode
  setAuthMode('login');
});

// Set up event listeners
function setupEventListeners() {
  const form = document.getElementById('auth-form');
  const toggleLink = document.getElementById('toggle-auth');
  
  form.addEventListener('submit', handleSubmit);
  toggleLink.addEventListener('click', toggleAuthMode);
}

// Toggle between login and signup
function toggleAuthMode(e) {
  e.preventDefault();
  authMode = authMode === 'login' ? 'signup' : 'login';
  setAuthMode(authMode);
  animateFormSwitch();
}

// Set auth mode UI
function setAuthMode(mode) {
  const title = document.getElementById('auth-title');
  const subtitle = document.getElementById('auth-subtitle');
  const nameGroup = document.getElementById('name-group');
  const roleGroup = document.getElementById('role-group');
  const submitBtn = document.getElementById('submit-btn');
  const toggleText = document.getElementById('toggle-text');
  const toggleLink = document.getElementById('toggle-auth');
  
  if (mode === 'login') {
    title.textContent = 'Welcome Back';
    subtitle.textContent = 'Sign in to access your portfolio';
    nameGroup.classList.add('hidden');
    roleGroup.classList.add('hidden');
    submitBtn.textContent = 'Sign In';
    toggleText.textContent = "Don't have an account? ";
    toggleLink.textContent = 'Create one';
  } else {
    title.textContent = 'Create Account';
    subtitle.textContent = 'Join the stock analysis platform';
    nameGroup.classList.remove('hidden');
    roleGroup.classList.remove('hidden');
    submitBtn.textContent = 'Sign Up';
    toggleText.textContent = 'Already have an account? ';
    toggleLink.textContent = 'Sign in';
  }
}

// Handle form submission
async function handleSubmit(e) {
  e.preventDefault();
  
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  
  // Validation
  if (!validateEmail(email)) {
    showError('Please enter a valid email address');
    return;
  }
  
  const passwordCheck = validatePassword(password);
  if (!passwordCheck.valid) {
    showError(passwordCheck.message);
    return;
  }
  
  if (authMode === 'login') {
    await handleLogin(email, password);
  } else {
    const name = document.getElementById('name').value.trim();
    const role = document.querySelector('input[name="role"]:checked')?.value || 'STAFF';
    
    if (!name) {
      showError('Please enter your name');
      return;
    }
    
    await handleSignup(email, name, password, role);
  }
}

// Handle login
async function handleLogin(email, password) {
  setLoading(true);
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      saveToken(data.access_token);
      await fetchUserData();
      showSuccess('Login successful! Redirecting...');
      setTimeout(() => redirectToDashboard(), 1000);
    } else {
      showError(data.detail || 'Invalid email or password');
      setLoading(false);
    }
  } catch (error) {
    console.error('Login error:', error);
    showError('Unable to connect to server. Please try again.');
    setLoading(false);
  }
}

// Handle signup
async function handleSignup(email, name, password, role) {
  setLoading(true);
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, name, password, role })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      showSuccess('Account created! Logging you in...');
      // Auto-login after signup
      setTimeout(() => handleLogin(email, password), 1000);
    } else {
      showError(data.detail || 'Unable to create account');
      setLoading(false);
    }
  } catch (error) {
    console.error('Signup error:', error);
    showError('Unable to connect to server. Please try again.');
    setLoading(false);
  }
}

// Fetch user data
async function fetchUserData() {
  const token = getToken();
  if (!token) return null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const userData = await response.json();
      saveUser(userData);
      return userData;
    } else {
      // Token invalid, clear it
      clearAuth();
      return null;
    }
  } catch (error) {
    console.error('Fetch user error:', error);
    return null;
  }
}

// Save token to localStorage
function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

// Get token from localStorage
function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

// Save user data
function saveUser(userData) {
  localStorage.setItem(USER_KEY, JSON.stringify(userData));
}

// Get user data
function getUser() {
  const userData = localStorage.getItem(USER_KEY);
  return userData ? JSON.parse(userData) : null;
}

// Clear authentication
function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

// Logout
function logout() {
  clearAuth();
  window.location.href = 'index.html';
}

// Redirect to dashboard
function redirectToDashboard() {
  window.location.href = 'dashboard.html';
}

// Export functions
window.auth = {
  getToken,
  getUser,
  logout,
  fetchUserData,
  clearAuth
};
