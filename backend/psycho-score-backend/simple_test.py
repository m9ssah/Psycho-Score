"""
Simple test using built-in urllib to check endpoints
"""

import urllib.request
import urllib.error
import json


def test_get_endpoint(url, description):
    """Test a GET endpoint"""
    print(f"Testing GET {url} - {description}")
    try:
        with urllib.request.urlopen(url) as response:
            status = response.getcode()
            print(f"   Status: {status}")
            if status == 200:
                print("   ✅ SUCCESS")
                return True
            else:
                print(f"   ❌ ERROR: HTTP {status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"   ❌ HTTP ERROR: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"   💥 EXCEPTION: {e}")
        return False


def test_post_endpoint(url, description):
    """Test a POST endpoint (without data)"""
    print(f"Testing POST {url} - {description}")
    try:
        req = urllib.request.Request(url, method="POST")
        req.add_header("Content-Type", "application/json")

        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            print(f"   Status: {status}")
            if status == 200:
                print("   ✅ SUCCESS")
                return True
            else:
                print(f"   ❌ ERROR: HTTP {status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"   ❌ HTTP ERROR: {e.code} - {e.reason}")
        if e.code == 422:  # Unprocessable Entity (missing required data)
            print(
                "   ℹ️  Endpoint exists but requires data (expected for file upload endpoints)"
            )
            return True
        return False
    except Exception as e:
        print(f"   💥 EXCEPTION: {e}")
        return False


def main():
    """Test basic endpoints"""
    base_url = "http://localhost:8000"

    print("🧪 Testing Psycho Score API Endpoints (Basic)")
    print("=" * 50)

    # Test GET endpoints
    get_tests = [
        (f"{base_url}/", "Home page"),
        (f"{base_url}/health", "Health check"),
        (f"{base_url}/api", "API info"),
        (f"{base_url}/docs", "API documentation"),
        (f"{base_url}/api/analyze/health", "Analyze health check"),
        (f"{base_url}/api/audio/health", "Audio health check"),
        (f"{base_url}/api/audio/voices", "Get voices"),
    ]

    # Test POST endpoints (these should return 422 for missing data, not 405)
    post_tests = [
        (f"{base_url}/api/analyze/psycho-score", "Main psycho score endpoint"),
        (f"{base_url}/api/analyze/quick-analysis", "Quick analysis endpoint"),
        (f"{base_url}/api/audio/generate", "Generate audio"),
    ]

    results = []

    for url, description in get_tests:
        result = test_get_endpoint(url, description)
        results.append((f"GET {url}", result))
        print()

    for url, description in post_tests:
        result = test_post_endpoint(url, description)
        results.append((f"POST {url}", result))
        print()

    print("=" * 50)
    print("📊 Test Summary:")
    print("-" * 20)

    passed = 0
    for endpoint, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{endpoint:<60} {status}")
        if result:
            passed += 1

    print(f"\nPassed: {passed}/{len(results)}")

    if passed < len(results):
        print("\n💡 If you see 405 Method Not Allowed errors:")
        print("   - Check if server is running: uvicorn src.main:app --reload")
        print("   - Verify you're testing the correct URLs")
        print("   - Check for route conflicts in main.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted")
    except Exception as e:
        print(f"\n💥 Test runner error: {e}")
