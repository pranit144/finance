# 📈 Stock Analysis Application

Complete stock analysis platform with authentication and real-time market data.

## 🚀 Quick Start

### 1. Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 2. Open Application
Open `frontend/index.html` in your browser

### 3. Login
**Test Account:**
- Email: `admin@test.com`
- Password: `SecurePass123!`

### 4. View Dashboard
Stocks display instantly after login!

## ✨ Features

- ✅ Secure authentication (JWT)
- ✅ Real-time stock data (Yahoo Finance)
- ✅ 5 popular stocks: AAPL, GOOGL, MSFT, TSLA, AMZN
- ✅ Instant loading dashboard
- ✅ Color-coded price changes
- ✅ Auto-refresh capability
- ✅ Beautiful cyberpunk UI

## 📊 Stock Data

Each stock card shows:
- Current price
- Change % (color-coded)
- Dollar change
- Trading volume

## 🔧 Tech Stack

**Backend:** FastAPI, SQLAlchemy, yfinance, JWT  
**Frontend:** HTML, CSS, JavaScript  
**Database:** SQLite (local development)

## ✅ Status

**Production Ready** - All features working!
