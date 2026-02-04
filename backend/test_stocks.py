"""
Test stock API endpoint
"""
import requests

API_BASE_URL = "http://localhost:8000"

# First, login to get token
print("=" * 50)
print("Testing Stock API")
print("=" * 50)

# Login
print("\n1. Logging in...")
login_response = requests.post(
    f"{API_BASE_URL}/auth/login",
    json={"email": "admin@test.com", "password": "SecurePass123!"}
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print("✅ Login successful!")
    
    # Test stock endpoint
    print("\n2. Fetching popular stocks...")
    stock_response = requests.get(
        f"{API_BASE_URL}/stocks/popular",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status Code: {stock_response.status_code}")
    
    if stock_response.status_code == 200:
        data = stock_response.json()
        print(f"✅ Got {data['count']} stocks!")
        for stock in data['stocks']:
            print(f"\n{stock['symbol']}: ${stock['price']} ({stock['change_percent']:+.2f}%)")
    else:
        print(f"❌ Error: {stock_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")
