#!/usr/bin/env python3
"""
Quick endpoint test script to verify all routes work correctly
"""

import asyncio
import httpx
import sys

BASE_URL = "http://localhost:8000"


async def test_endpoint(method: str, url: str, description: str, **kwargs):
    """Test a single endpoint"""
    print(f"Testing {method} {url} - {description}")
    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, **kwargs)
            elif method.upper() == "POST":
                response = await client.post(url, **kwargs)
            else:
                print(f"❌ Unsupported method: {method}")
                return False

            print(f"   Status: {response.status_code}")
            if response.status_code < 400:
                print(f"   ✅ SUCCESS")
                return True
            else:
                print(f"   ❌ ERROR: {response.text}")
                return False
    except Exception as e:
        print(f"   💥 EXCEPTION: {e}")
        return False


async def main():
    """Test all endpoints"""
    print("🧪 Testing Psycho Score API Endpoints")
    print("=" * 50)

    tests = [
        # Basic endpoints
        ("GET", f"{BASE_URL}/", "Home page"),
        ("GET", f"{BASE_URL}/health", "Health check"),
        ("GET", f"{BASE_URL}/api", "API info"),
        ("GET", f"{BASE_URL}/docs", "API documentation"),
        # Analysis endpoints (these require files, so we'll test if they respond correctly to missing files)
        ("POST", f"{BASE_URL}/api/analyze/psycho-score", "Main psycho score endpoint"),
        ("POST", f"{BASE_URL}/api/analyze/quick-analysis", "Quick analysis endpoint"),
        ("GET", f"{BASE_URL}/api/analyze/health", "Analysis health check"),
        # Audio endpoints
        ("GET", f"{BASE_URL}/api/audio/voices", "Get voices"),
        (
            "POST",
            f"{BASE_URL}/api/audio/generate",
            "Generate audio",
            {"data": {"text": "test"}},
        ),
        ("GET", f"{BASE_URL}/api/audio/health", "Audio health check"),
    ]

    results = []
    for test_args in tests:
        method, url, description = test_args[:3]
        kwargs = test_args[3] if len(test_args) > 3 else {}
        result = await test_endpoint(method, url, description, **kwargs)
        results.append((f"{method} {url}", result))
        print()

    print("=" * 50)
    print("📊 Test Summary:")
    print("-" * 20)

    passed = 0
    for endpoint, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{endpoint:<50} {status}")
        if result:
            passed += 1

    print(f"\nPassed: {passed}/{len(results)}")

    if passed < len(results):
        print("\n💡 Common issues:")
        print("   - Server not running: uvicorn src.main:app --reload")
        print("   - Wrong URL/port: Check if server is on localhost:8000")
        print("   - Import errors: Check if all dependencies are installed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted")
    except Exception as e:
        print(f"\n💥 Test runner error: {e}")
