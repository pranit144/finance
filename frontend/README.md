# Frontend - Stock Analysis Authentication UI

A **visually stunning authentication interface** with dark cyberpunk aesthetics.

## 🎨 Design Features

- **Dark Cyberpunk Theme** - Deep space blue with neon cyan/green accents
- **Unique Typography** - Syne, JetBrains Mono, Orbitron (NO generic fonts!)
- **Animated Gradient Background** - Smooth color shifting
- **Floating Particles** - CSS-only geometric animations
- **Glassmorphism** - Blurred card effects
- **Glowing Inputs** - Neon border effects on focus
- **Smooth Micro-interactions** - 60fps animations
- **Fully Responsive** - Mobile, tablet, desktop

## 📁 Structure

```
frontend/
├── index.html              # Login/Signup page
├── dashboard.html          # Protected dashboard
├── css/
│   ├── variables.css       # Design tokens
│   ├── base.css            # Reset & typography
│   ├── animations.css      # Keyframe animations
│   └── auth.css            # Auth page styles
└── js/
    ├── config.js           # API configuration
    ├── utils.js            # Helper functions
    └── auth.js             # Authentication logic
```

## 🚀 Quick Start

### 1. Make sure backend is running

```bash
cd ../backend
uvicorn app.main:app --reload
```

Backend should be running on `http://localhost:8000`

### 2. Open the frontend

**Option A: Using Live Server (VS Code)**
1. Install "Live Server" extension
2. Right-click `index.html`
3. Select "Open with Live Server"

**Option B: Direct File**
1. Simply open `index.html` in your browser
2. File path: `E:\VsCode\New_PProject\Stock_anaylsis\frontend\index.html`

## 🎯 Features

### Authentication Pages

**Login Mode** (Default)
- Email + Password
- Smooth form validation
- Loading states
- Error messages with shake animation

**Signup Mode** (Toggle)
- Email + Name + Password + Role
- Role selector (Staff/Admin)
- Auto-login after signup
- Animated form expansion

### Protected Dashboard

- Requires valid JWT token
- Auto-redirects if not authenticated
- Displays user info
- Logout functionality
- Placeholder for portfolio features

## 🔐 How It Works

### Authentication Flow

1. **User enters credentials** → Form validation
2. **Submit** → API call to backend
3. **Success** → JWT token saved to localStorage
4. **Redirect** → Dashboard page
5. **Dashboard loads** → Verifies token with `/auth/me`
6. **Token valid** → Display user info
7. **Token invalid** → Redirect to login

### Token Management

```javascript
// Token stored in localStorage
localStorage.setItem('stock_analysis_token', token);

// Used in API calls
fetch(`${API_BASE_URL}/auth/me`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

## 🎨 Design System

### Colors

```css
--bg-primary: #0a0e1a;       /* Deep space blue */
--accent-cyan: #00f0ff;      /* Primary accent */
--accent-green: #39ff14;     /* Success */
--accent-purple: #b026ff;    /* Hover */
--accent-red: #ff0055;       /* Errors */
```

### Typography

```css
--font-heading: 'Syne'           /* Bold geometric */
--font-body: 'JetBrains Mono'    /* Monospace */
--font-accent: 'Orbitron'        /* Futuristic */
```

### Animations

- **Page Load**: Staggered fadeInUp (0.1s delay each)
- **Input Focus**: Glow + lift effect
- **Button Hover**: Glow expand + lift
- **Form Toggle**: Smooth opacity transition
- **Error**: Shake animation
- **Background**: Infinite gradient shift

## 📱 Responsive Breakpoints

- **Desktop** (1024px+): Side-by-side layout
- **Tablet** (768px-1023px): Stacked layout
- **Mobile** (< 768px): Full-screen card

## 🧪 Testing

### Test Login

1. Open `index.html`
2. Use credentials from backend signup
3. Click "Sign In"
4. Should redirect to dashboard

### Test Signup

1. Click "Create one"
2. Fill all fields
3. Select role (Staff/Admin)
4. Click "Sign Up"
5. Should auto-login and redirect

### Test Protected Route

1. Open `dashboard.html` directly (no login)
2. Should redirect to `index.html`
3. Login first
4. Then access dashboard
5. Should show user info

### Test Token Persistence

1. Login successfully
2. Close browser
3. Reopen `index.html`
4. Should auto-redirect to dashboard (token still valid)

### Test Logout

1. On dashboard, click "Logout"
2. Should clear token
3. Should redirect to login

## 🎭 Animation Showcase

### Page Load Sequence

1. Background gradient fades in (0s)
2. Floating particles appear (0.2s)
3. Auth card scales in (0.8s)
4. Title fades in (1s)
5. Form fields stagger in (1.1s - 1.5s)

### Micro-interactions

- **Input focus**: Cyan glow + 2px lift
- **Button hover**: Shadow expand + 3px lift
- **Form submit**: Button → spinner
- **Error**: Red glow + horizontal shake
- **Success**: Green flash

## 🔧 Configuration

### Change API URL

Edit `js/config.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### Customize Colors

Edit `css/variables.css`:

```css
:root {
  --accent-cyan: #00f0ff;  /* Change to your color */
}
```

## 🌟 Highlights

### What Makes This Unique

✅ **NOT generic AI design** - Custom cyberpunk aesthetic  
✅ **Distinctive fonts** - Syne, JetBrains Mono, Orbitron  
✅ **Bold color choices** - Neon accents on dark backgrounds  
✅ **Atmospheric backgrounds** - Animated gradients + particles  
✅ **Smooth 60fps animations** - CSS-only, performant  
✅ **Production-ready** - Full error handling, validation  

### Portfolio Talking Points

> "I designed and built a custom authentication UI with a dark cyberpunk aesthetic, featuring animated gradient backgrounds, glassmorphism effects, and smooth micro-interactions. The interface uses vanilla JavaScript for JWT token management and API integration, with a fully responsive design that works across all devices."

## 📝 Next Steps

- [ ] Add password strength indicator
- [ ] Add "Remember me" checkbox
- [ ] Add "Forgot password" flow
- [ ] Add social login buttons
- [ ] Add email verification
- [ ] Build portfolio management features

## 🐛 Troubleshooting

**Styles not loading?**
- Check file paths in HTML
- Ensure all CSS files exist

**API calls failing?**
- Verify backend is running on port 8000
- Check CORS settings in backend

**Animations not smooth?**
- Use modern browser (Chrome, Firefox, Edge)
- Check hardware acceleration enabled

**Token not persisting?**
- Check browser localStorage is enabled
- Check for private/incognito mode

---

**Built with ❤️ and attention to detail**
