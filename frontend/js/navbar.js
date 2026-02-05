document.addEventListener('DOMContentLoaded', () => {
    // Determine active page
    const currentPath = window.location.pathname;
    const isDashboard = currentPath.includes('dashboard.html');
    const isPortfolio = currentPath.includes('portfolio.html');
    
    // Check auth
    const token = localStorage.getItem('stock_analysis_token');
    
    // Inject header HTML
    const headerContainer = document.querySelector('.header'); // Or create it if missing
    
    if (headerContainer) {
        headerContainer.innerHTML = `
            <div class="header-content">
                <a href="${token ? 'dashboard.html' : 'index.html'}" class="brand">
                    <div class="brand-icon">📈</div>
                    <div class="brand-name">STOCKLYZE</div>
                </a>
                <div class="nav">
                    ${token ? `
                        <a href="dashboard.html" class="nav-link ${isDashboard ? 'active' : ''}">Dashboard</a>
                        <a href="portfolio.html" class="nav-link ${isPortfolio ? 'active' : ''}">Portfolio</a>
                        <button class="profile-btn" onclick="logout()" title="Logout">
                            <span style="font-size: 16px;">👤</span>
                        </button>
                    ` : `
                        <a href="index.html" class="btn-login">Log In</a>
                        <a href="index.html" class="btn-signup">Get Started</a>
                    `}
                </div>
            </div>
        `;
    }
});

function logout() {
    localStorage.removeItem('stock_analysis_token');
    localStorage.removeItem('stock_analysis_user');
    window.location.href = 'index.html';
}
