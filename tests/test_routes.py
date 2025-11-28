import requests
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, expected_status=200):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        print(f"{'✅' if response.status_code == expected_status else '❌'} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        return response.status_code == expected_status
    except Exception as e:
        print(f"{endpoint}: Error - {e}")
        return False

print("Testing DataInsight API Routes...")
print("=" * 50)

# Test all endpoints
endpoints = [
    "/",
    "/health/",  # Note the trailing slash due to prefix
    "/metrics/summary",
    "/metrics/top-products",
    "/metrics/sales-trend", 
    "/metrics/customer-analysis",
    "/docs"
]

success_count = 0
for endpoint in endpoints:
    if test_endpoint(endpoint):
        success_count += 1
    time.sleep(0.5)  # Small delay between requests

print("=" * 50)
print(f"Results: {success_count}/{len(endpoints)} endpoints working")

if success_count == len(endpoints):
    print("All endpoints are working correctly!")
else:
    print("Some endpoints need fixing.")