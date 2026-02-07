---
title: Stocklyze - Professional Portfolio Analytics
emoji: 📈
colorFrom: teal
colorTo: blue
sdk: docker
pinned: false
---

<div align="center">
  <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/chart-line.svg" width="80" height="80" alt="Stocklyze Logo" />
  <h1>🚀 STOCKLYZE</h1>
  <p><b>Premium Real-Time Stock Market Dashboard & Portfolio Analytics System</b></p>

  <p>
    <img src="https://img.shields.io/badge/Maintained%3F-yes-00b4a6?style=for-the-badge" alt="Maintained" />
    <img src="https://img.shields.io/badge/Security-Bank--Level-10b981?style=for-the-badge" alt="Security" />
    <img src="https://img.shields.io/badge/Deployment-Docker-blue?style=for-the-badge" alt="Deployment" />
    <img src="https://img.shields.io/badge/UI-Vibrant%20Light-f0f7ff?style=for-the-badge" alt="UI" />
  </p>
  
  <p>
    <a href="https://pranit144-finance.hf.space"><strong>Live Demo »</strong></a> |
    <a href="#-key-features">Features</a> |
    <a href="#-getting-started">Installation</a> |
    <a href="#-tech-stack">Stack</a>
  </p>
</div>

---

## 📖 Overview

**Stocklyze** is a high-performance, professional-grade web application engineered for investors who demand real-time visibility into their market positions. Specializing in the **NSE India** market, it combines a sophisticated financial backend with a cutting-edge front-end experience.

The application is built on the philosophy of **"Simplicity through Analytics"**, providing a curated view of top-performing assets alongside a deep-dive portfolio tracking system that calculates your realized and unrealized gains in real-time.

---

## ✨ Key Features

### 📊 Market Overview (Dashboard)
- **Real-Time Data Syncing**: Direct integration with market feeds for up-to-the-minute price tracking.
- **Smart Summary Cards**: Instant visibility into Market Status, Top Gainer, Top Loser, and tracking coverage.
- **Vibrant Asset Cards**: High-definition stock cards with trend indicators, market cap tracking, and volume analysis.

### 💼 Portfolio Management
- **Centralized Vault**: Manage all your NSE holdings in one high-security location.
- **Dynamic P&L Tracking**: Automatic calculation of Profit/Loss percentages and nominal values based on your entry prices.
- **Global Portfolio Analytics**: View your total Net Value and aggregate ROI across all assets.
- **Visual Trends**: Mini-sparklines for every asset showing 30-day performance history.

### 🎨 Premium User Experience
- **Mesh Gradient Backgrounds**: A dynamic, "living" background system that shifts with bluish-teal tints.
- **Glassmorphism UI**: High-end transparency effects with frosted-glass containers.
- **Responsive Mastery**: Fully optimized for Desktop, Tablet, and Mobile viewing.

---

## 🛠 Tech Stack

### Backend Architecture
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python)
- **Database**: [Supabase](https://supabase.com/) & [SQLAlchemy](https://www.sqlalchemy.org/)
- **Security**: OAuth2 with JWT Bearer tokens & Bcrypt hashing.

### Frontend Engine
- **Logic**: ES6+ Vanilla JavaScript (No heavy frameworks for maximum speed).
- **Design**: Modern CSS3 using CSS Variables, Flexbox, and Grid.
- **Animations**: CSS Keyframe animations for fluid, organic transitions.

### DevOps & Deployment
- **Containerization**: Docker (Multi-stage build)
- **Sync Engine**: GitHub Actions automated pipeline.
- **Hosting**: Hugging Face Spaces & Vercel.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Pip
- A Supabase account (Optional, local SQLite supported by default)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pranit144/finance.git
   cd finance
   ```

2. **Set up Environment Variables**
   Create a `.env` file in the root:
   ```env
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   SECRET_KEY=generate_a_secure_key
   ```

3. **Install Dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Launch the Application**
   ```bash
   python app.py
   ```

5. **Access the App**
   Open your browser and navigate to `http://localhost:7860/app`

---

## 📁 Project Structure

```text
├── .github/workflows/      # Automated deployment & Sync
├── backend/                # Core Python API
│   ├── app/                # FastAPI logic & routes
│   └── requirements.txt    # Python dependencies
├── frontend/               # Premium Web Interface
│   ├── css/                # Design System & UI
│   ├── js/                 # Application Logic
│   └── *.html              # Structured Templates
├── Dockerfile              # Container configuration
└── app.py                  # Main entry point
```

---

<div align="center">
  <p><i>Road to Financial Freedom 🏁</i></p>
  <p>Developed with ❤️ by <b>Pranit</b></p>
</div>