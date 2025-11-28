import requests
import time
import statistics

BASE_URL = "http://localhost:8000"

def measure_endpoint_performance(endpoint, num_requests=10):
    """Measure actual response times for an endpoint"""
    print(f"Testing {endpoint}...")
    
    response_times = []
    
    for i in range(num_requests):
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                response_time_ms = (end_time - start_time) * 1000
                response_times.append(response_time_ms)
                
                # Get performance data from API response if available
                data = response.json()
                if 'performance' in data and 'response_time_ms' in data['performance']:
                    api_reported_time = data['performance']['response_time_ms']
                    print(f"  Request {i+1}: {response_time_ms:.0f}ms (API: {api_reported_time}ms)")
                else:
                    print(f"  Request {i+1}: {response_time_ms:.0f}ms")
            else:
                print(f"  Request {i+1}: Failed - Status {response.status_code}")
                
        except Exception as e:
            print(f"  Request {i+1}: Error - {e}")
        
        # Small delay between requests
        time.sleep(0.1)
    
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"{endpoint}")
        print(f"   Average: {avg_time:.0f}ms | Min: {min_time:.0f}ms | Max: {max_time:.0f}ms")
        print(f"   Sample Size: {len(response_times)} requests")
        return avg_time
    else:
        print(f"{endpoint}: No successful measurements")
        return None

def main():
    print("Measuring Real API Performance...")
    print("=" * 60)
    
    endpoints = [
        "/metrics/summary",
        "/metrics/top-products", 
        "/metrics/sales-trend",
        "/metrics/customer-analysis",
        "/health/"
    ]
    
    results = {}
    
    for endpoint in endpoints:
        avg_time = measure_endpoint_performance(endpoint)
        if avg_time:
            results[endpoint] = avg_time
        print()
    
    print("=" * 60)
    print("FINAL PERFORMANCE RESULTS:")
    print("=" * 60)
    
    for endpoint, avg_time in results.items():
        print(f"{endpoint}: {avg_time:.0f}ms")
    
    overall_avg = statistics.mean(results.values()) if results else 0
    print("=" * 60)
    print(f"Overall Average: {overall_avg:.0f}ms")

if __name__ == "__main__":
    main()