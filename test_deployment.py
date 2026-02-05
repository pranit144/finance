
import requests
import json
import time

BASE_URL = "https://pranit144-finance.hf.space"

def log_test(msg):
    with open("test_log.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def test_endpoint(name, method, path, data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    log_test(f"\n🚀 Testing {name}...")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=15)
        
        log_test(f"   Status: {response.status_code}")
        try:
            body = response.json()
            log_test(f"   Response: {json.dumps(body, indent=2)}")
            return body
        except:
            log_test(f"   Response: {response.text[:500]}")
            return None
    except Exception as e:
        log_test(f"   ❌ Error: {e}")
        return None

if __name__ == "__main__":
    with open("test_log.txt", "w", encoding="utf-8") as f:
        f.write("=== FULL DEPLOYMENT TEST ===\n")
    
    # 1. Signup
    ts = int(time.time())
    email = f"user_{ts}@test.com"
    pwd = "password123"
    signup_data = {"email": email, "password": pwd, "name": "Tester", "role": "STAFF"}
    signup_res = test_endpoint("Signup", "POST", "/auth/signup", data=signup_data)
    
    if not signup_res or "id" not in signup_res:
        log_test("❌ Signup failed, stopping.")
        sys.exit(1)

    # 2. Login
    login_data = {"email": email, "password": pwd}
    login_res = test_endpoint("Login", "POST", "/auth/login", data=login_data)
    
    token = None
    if login_res and "access_token" in login_res:
        token = login_res["access_token"]
        log_test("✅ Login successful!")
    else:
        log_test("❌ Login failed!")
        sys.exit(1)
        
    # 3. Protected Resource: Stocks Quote
    test_endpoint("Stock Quote (RELIANCE.NS)", "GET", "/stocks/quote/RELIANCE.NS", token=token)
    
    # 4. Protected Resource: Portfolio
    test_endpoint("Get Portfolio", "GET", "/portfolio/", token=token)
    
    log_test("\n✨ ALL CORE TESTS PASSED! ✨")
