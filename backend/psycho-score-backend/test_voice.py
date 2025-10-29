#!/usr/bin/env python3
"""
Test your custom ElevenLabs voice
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_voice():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("PATRICK_VOICE_ID")
    base_url = os.getenv("ELEVENLABS_BASE_URL")

    print(f"🎙️ Testing Custom Voice")
    print("=" * 50)
    print(f"Voice ID: {voice_id}")
    print(f"API Key: {api_key[:10]}..." if api_key else "No API key found")

    # Test 1: Check if voice exists
    print("\n1. Checking if voice exists...")
    try:
        headers = {"Accept": "application/json", "xi-api-key": api_key}
        response = requests.get(f"{base_url}/voices", headers=headers)

        if response.status_code == 200:
            voices = response.json()
            voice_found = False
            for voice in voices.get("voices", []):
                if voice["voice_id"] == voice_id:
                    print(f"   ✅ Found voice: {voice['name']}")
                    voice_found = True
                    break

            if not voice_found:
                print(f"   ❌ Voice ID {voice_id} not found in your account")
                print("   Available voices:")
                for voice in voices.get("voices", [])[:5]:  # Show first 5
                    print(f"      - {voice['name']}: {voice['voice_id']}")
        else:
            print(f"   ❌ Error fetching voices: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 2: Generate sample audio
    print("\n2. Testing audio generation...")
    try:
        url = f"{base_url}/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key,
        }

        data = {
            "text": "Look at that subtle off-white coloring. The tasteful thickness of it.",
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
                "style": 0.0,
                "use_speaker_boost": True,
            },
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print("   ✅ Audio generation successful!")
            print(f"   Audio size: {len(response.content)} bytes")

            # Save test audio
            with open("test_voice.mp3", "wb") as f:
                f.write(response.content)
            print("   💾 Saved as 'test_voice.mp3'")
        else:
            print(f"   ❌ Audio generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    test_voice()
