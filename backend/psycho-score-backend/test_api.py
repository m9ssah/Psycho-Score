#!/usr/bin/env python3
"""
Psycho Score Backend Test Script
"Let's see how well this API performs... the attention to detail must be flawless."
"""

import asyncio
import httpx
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"


async def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing health check...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200


async def test_api_info():
    """Test the API info endpoint"""
    print("\n📊 Testing API info...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200


async def test_business_card_analysis(image_path: str = None):
    """Test business card analysis endpoint"""
    print(f"\n🎴 Testing business card analysis...")

    if not image_path or not Path(image_path).exists():
        print("⚠️  No test image provided or file doesn't exist")
        print("   To test image analysis, provide a business card image path")
        return False

    async with httpx.AsyncClient(timeout=60.0) as client:
        with open(image_path, "rb") as f:
            files = {"file": ("business_card.jpg", f, "image/jpeg")}
            data = {"include_audio": "true"}

            response = await client.post(
                f"{BASE_URL}/api/analyze/business-card", files=files, data=data
            )

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis successful!")
            print(f"Psycho Score: {result['analysis']['psycho_score']}")
            print(
                f"Patrick's Critique: {result['analysis']['patrick_critique'][:100]}..."
            )
            if result.get("audio"):
                print(f"Audio URL: {result['audio']['audio_url']}")
        else:
            print(f"❌ Error: {response.text}")

        return response.status_code == 200


async def test_audio_generation():
    """Test audio generation endpoint"""
    print(f"\n🎵 Testing audio generation...")

    test_text = "Look at that subtle off-white coloring. The tasteful thickness of it. Oh my God, it even has a watermark."

    async with httpx.AsyncClient(timeout=60.0) as client:
        data = {"text": test_text}
        response = await client.post(f"{BASE_URL}/api/audio/generate", data=data)

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Audio generation successful!")
            print(f"Audio URL: {result['audio_url']}")
            print(f"File size: {result.get('file_size', 'Unknown')} bytes")
        else:
            print(f"❌ Error: {response.text}")

        return response.status_code == 200


async def test_voices_endpoint():
    """Test ElevenLabs voices endpoint"""
    print(f"\n🎤 Testing voices endpoint...")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/api/audio/voices")

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Voices retrieved successfully!")
            if "voices" in result:
                print(f"Available voices: {len(result['voices'])}")
        else:
            print(f"❌ Error: {response.text}")

        return response.status_code == 200


async def main():
    """Run all tests"""
    print("🎭 Psycho Score Backend Test Suite")
    print("=" * 50)

    tests = [
        ("Health Check", test_health_check()),
        ("API Info", test_api_info()),
        ("Audio Generation", test_audio_generation()),
        ("Voices Endpoint", test_voices_endpoint()),
    ]

    # Optional: Test with actual image if provided
    import sys

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        tests.append(
            ("Business Card Analysis", test_business_card_analysis(image_path))
        )
    else:
        print("\n💡 Tip: Run with an image path to test business card analysis:")
        print("   python test_api.py /path/to/business_card.jpg")

    results = []
    for test_name, test_coro in tests:
        try:
            result = await test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print("-" * 20)

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1

    print(f"\nPassed: {passed}/{len(results)}")

    if passed == len(results):
        print(
            "\n🎉 All tests passed! The API is performing with Patrick Bateman-level perfection."
        )
    else:
        print(
            f"\n⚠️  {len(results) - passed} test(s) failed. Even Patrick would be disappointed."
        )

    print(
        '\n"That\'s not a test suite... THIS is a test suite." - Patrick Bateman, probably'
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted. Patrick doesn't like interruptions.")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Even the most sophisticated APIs have their moments...")
