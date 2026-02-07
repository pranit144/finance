/**
 * STOCKLYZE - GLOBAL LAYOUT ENGINE
 * Handles dynamic navbar, background, and session management.
 */

const TOKEN_KEY = 'stock_analysis_token';

document.addEventListener('DOMContentLoaded', () => {
    initLayout();
});

function initLayout() {
    const body = document.body;
    
    // 1. Inject Background Blobs if not present
    if (!document.querySelector('.bg-blob-container')) {
        const blobContainer = document.createElement('div');
        blobContainer.className = 'bg-blob-container';
        blobContainer.innerHTML = `
            <div class="bg-blob blob-1"></div>
            <div class="bg-blob blob-2"></div>
        `;
        body.prepend(blobContainer);
    }

    // 2. Inject Navbar
    injectNavbar();
}

function injectNavbar() {
    const currentPath = window.location.pathname;
    const isDashboard = currentPath.includes('dashboard.html');
    const isPortfolio = currentPath.includes('portfolio.html');
    const isAuth = currentPath.includes('index.html') || currentPath === '/app' || currentPath === '/';
    
    const token = localStorage.getItem(TOKEN_KEY);
    
    // We only show the full navbar for authenticated pages
    if (isAuth && !token) return;

    const nav = document.createElement('nav');
    nav.className = 'main-nav';
    
    // Logic for toggling buttons (User request: when in portfolio see dashboard and vice versa)
    let actionButtons = '';
    
    if (token) {
        if (isDashboard) {
            actionButtons = `<a href="portfolio.html" class="nav-btn nav-btn-outline">💼 My Portfolio</a>`;
        } else if (isPortfolio) {
            actionButtons = `<a href="dashboard.html" class="nav-btn nav-btn-outline">📈 Dashboard</a>`;
        } else {
            // Default/Other
            actionButtons = `
                <a href="dashboard.html" class="nav-btn nav-btn-outline">📈 Dashboard</a>
                <a href="portfolio.html" class="nav-btn nav-btn-outline">💼 Portfolio</a>
            `;
        }
        
        actionButtons += `
            <div class="logout-btn" onclick="handleLogout()" title="Logout">
                🚪
            </div>
        `;
    } else if (!isAuth) {
        // Not on auth page but no token? Redirect to login
        window.location.href = 'index.html';
        return;
    }

    nav.innerHTML = `
        <a href="dashboard.html" class="brand">
            <div class="brand-name">STOCK<span style="color:var(--primary)">LYZE</span></div>
        </a>
        <div class="nav-links">
            ${actionButtons}
        </div>
    `;

    // Prepend to body or replace existing placeholder
    const existingHeader = document.querySelector('header') || document.querySelector('.header') || document.querySelector('.main-nav');
    if (existingHeader) {
        existingHeader.replaceWith(nav);
    } else {
        document.body.prepend(nav);
    }
}

function handleLogout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem('stock_analysis_user');
    window.location.href = 'index.html';
}
