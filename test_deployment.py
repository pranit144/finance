
import requests
import json
import time

BASE_URL = "https://pranit144-finance.hf.space"
# Optional: test local if needed
# BASE_URL = "http://localhost:8000"

def test_endpoint(name, method, path, data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    print(f"\n🚀 Testing {name}...")
    print(f"   {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=15)
        
        print(f"   Status: {response.status_code}")
        try:
            body = response.json()
            print(f"   Response: {json.dumps(body, indent=2)}")
            return body
        except:
            print(f"   Response: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def run_all_tests():
    print(f"=== DEPLOYMENT TEST SUITE: {BASE_URL} ===")
    
    # 1. Health
    test_endpoint("Health Check", "GET", "/health")
    
    # 2. Signup
    timestamp = int(time.time())
    test_email = f"test_user_{timestamp}@example.com"
    signup_data = {
        "email": test_email,
        "password": "password123",
        "name": "Test User",
        "role": "STAFF"
    }
    signup_res = test_endpoint("Signup", "POST", "/auth/signup", data=signup_data)
    
    # 3. Login
    login_data = {
        "email": test_email,
        "password": "password123"
    }
    login_res = test_endpoint("Login", "POST", "/auth/login", data=login_data)
    
    token = None
    if login_res and "access_token" in login_res:
        token = login_res["access_token"]
        print("   ✅ Got Auth Token!")
    else:
        print("   ❌ Failed to get auth token")
        return

    # 4. Protected: Get Popular Stocks
    test_endpoint("Popular Stocks (Auth)", "GET", "/stocks/popular", token=token)
    
    # 5. Protected: Get Portfolio (Expected empty)
    test_endpoint("Get Portfolio (Auth)", "GET", "/portfolio/", token=token)

if __name__ == "__main__":
    run_all_tests()
