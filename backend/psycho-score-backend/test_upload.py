#!/usr/bin/env python3
"""
Comprehensive test script for Psycho Score API
Tests file upload functionality with sample business card
"""

import requests
from io import BytesIO
from PIL import Image


def create_sample_business_card():
    """Create a simple sample business card image for testing"""
    # Create a simple business card image
    img = Image.new("RGB", (400, 250), color="white")

    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes


def test_psycho_score_api():
    """Test the main psycho score endpoint"""
    base_url = "http://localhost:8000"

    print("🧪 Testing Psycho Score API - File Upload")
    print("=" * 50)

    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # Test 2: Get available voices
    print("\n2. Getting available voices...")
    try:
        response = requests.get(f"{base_url}/api/audio/voices")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            voices = response.json()
            print(f"   Found {len(voices.get('voices', []))} voices")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 3: Main psycho score analysis
    print("\n3. Testing business card analysis...")
    try:
        # Create sample image
        sample_image = create_sample_business_card()

        files = {"file": ("business_card.png", sample_image, "image/png")}

        print("   Uploading sample business card...")
        response = requests.post(f"{base_url}/api/analyze/psycho-score", files=files)

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("   ✅ Analysis completed successfully!")
            print(f"   Analysis: {result.get('analysis', 'N/A')[:100]}...")
            print(f"   Audio file: {result.get('audio_url', 'N/A')}")
        else:
            print(f"   ❌ Error response: {response.text}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 4: Simple text to speech
    print("\n4. Testing simple text-to-speech...")
    try:
        data = {
            "text": "Look at that subtle off-white coloring. The tasteful thickness of it."
        }

        response = requests.post(f"{base_url}/api/audio/generate", data=data)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("   ✅ Audio generated successfully!")
            print(f"   Audio URL: {result.get('audio_url', 'N/A')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n🏁 Testing complete!")
    print("\n💡 Tips:")
    print("   - Upload a real business card image for better results")
    print("   - Visit http://localhost:8000/docs for interactive testing")
    print("   - Check the audio files in the outputs/audio directory")


if __name__ == "__main__":
    test_psycho_score_api()
