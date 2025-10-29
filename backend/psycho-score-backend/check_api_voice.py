#!/usr/bin/env python3
"""
Check what voice ID is currently being used by the API
"""

import requests


def check_api_voice():
    print("🔍 Checking API Voice Configuration")
    print("=" * 50)

    # Test audio generation and see what voice is actually used
    try:
        response = requests.post(
            "http://localhost:8000/api/audio/generate",
            data={"text": "This is a test of the current voice configuration."},
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Audio generated successfully!")
            print(f"Audio URL: {result.get('audio_url', 'N/A')}")

            # Download and check the audio file
            audio_url = "http://localhost:8000" + result.get("audio_url", "")
            audio_response = requests.get(audio_url)

            if audio_response.status_code == 200:
                with open("current_voice_test.mp3", "wb") as f:
                    f.write(audio_response.content)
                print("💾 Downloaded audio as 'current_voice_test.mp3'")
                print("🎧 Listen to this file to verify it's your custom voice!")
            else:
                print(f"❌ Could not download audio: {audio_response.status_code}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    check_api_voice()
