// Utility Functions

// Show error message with animation
function showError(message) {
  const alertContainer = document.getElementById('alert-container');
  alertContainer.innerHTML = `
    <div class="alert alert-error">
      ${message}
    </div>
  `;
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    alertContainer.innerHTML = '';
  }, 5000);
}

// Show success message
function showSuccess(message) {
  const alertContainer = document.getElementById('alert-container');
  alertContainer.innerHTML = `
    <div class="alert alert-success">
      ${message}
    </div>
  `;
  
  setTimeout(() => {
    alertContainer.innerHTML = '';
  }, 3000);
}

// Email validation
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

// Password validation
function validatePassword(password) {
  if (password.length < 8) {
    return { valid: false, message: 'Password must be at least 8 characters' };
  }
  return { valid: true };
}

// Set loading state
function setLoading(isLoading, buttonId = 'submit-btn') {
  const button = document.getElementById(buttonId);
  if (isLoading) {
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Processing...';
  } else {
    button.disabled = false;
    // Will be reset by form mode
  }
}

// Animate form switch
function animateFormSwitch() {
  const formGroups = document.querySelectorAll('.form-group');
  formGroups.forEach((group, index) => {
    group.style.opacity = '0';
    setTimeout(() => {
      group.style.animation = 'none';
      setTimeout(() => {
        group.style.animation = `fadeInUp 0.5s ease-out ${index * 0.1}s forwards`;
      }, 10);
    }, 10);
  });
}

// Export utilities
window.utils = {
  showError,
  showSuccess,
  validateEmail,
  validatePassword,
  setLoading,
  animateFormSwitch
};
