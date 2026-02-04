"""
Test script to verify the signup endpoint works.
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup."""
    print("Testing signup endpoint...")
    
    payload = {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "SecurePass123!",
        "role": "STAFF"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/signup",
            json=payload
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Signup successful!")
            return True
        else:
            print("❌ Signup failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    """Test health endpoint."""
    print("\nTesting health endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Backend is healthy!")
            return True
        else:
            print("❌ Backend health check failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("API Test Script")
    print("=" * 50)
    
    # Test health first
    if test_health():
        # Then test signup
        test_signup()
    else:
        print("\n❌ Backend is not responding. Make sure it's running on port 8000.")
