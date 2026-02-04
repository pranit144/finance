"""
Quick test to create a user via API
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

print("=" * 50)
print("Creating test account...")
print("=" * 50)

payload = {
    "email": "admin@test.com",
    "name": "Admin User",
    "password": "SecurePass123!",
    "role": "ADMIN"
}

try:
    response = requests.post(
        f"{API_BASE_URL}/auth/signup",
        json=payload
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 201:
        print("\n✅ Account created successfully!")
        print("\nYou can now login with:")
        print(f"Email: {payload['email']}")
        print(f"Password: {payload['password']}")
    else:
        print("\n❌ Failed to create account!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure the backend is running on http://localhost:8000")
