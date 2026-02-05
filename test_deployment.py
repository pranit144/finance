
import requests
import json
import time
import sys

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
            log_test(f"   Response: {response.text[:1000]}")
            return None
    except Exception as e:
        log_test(f"   ❌ Error: {e}")
        return None

if __name__ == "__main__":
    with open("test_log.txt", "w", encoding="utf-8") as f:
        f.write("=== LOG START ===\n")
    
    # Health
    test_endpoint("Health", "GET", "/health")
    
    # Signup
    ts = int(time.time())
    email = f"user_{ts}@test.com"
    signup_data = {"email": email, "password": "password123", "name": "Test User", "role": "STAFF"}
    test_endpoint("Signup", "POST", "/auth/signup", data=signup_data)
