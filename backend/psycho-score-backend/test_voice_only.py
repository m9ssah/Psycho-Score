#!/usr/bin/env python3
"""
Quick test with just text-to-speech to verify voice is working
"""

import requests


def test_just_voice():
    print("🎤 Testing JUST the voice functionality")
    print("=" * 50)

    try:
        # Test with a specific text
        data = {
            "text": "Look at that subtle off-white coloring. The tasteful thickness of it. Oh my God, it even has a watermark. This should be in your custom voice."
        }

        print("📤 Sending text to audio generation...")
        response = requests.post(
            "http://localhost:8000/api/audio/generate", data=data, timeout=30
        )

        print(f"📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Audio generated successfully!")
            print(f"🔊 Audio URL: http://localhost:8000{result.get('audio_url', '')}")

            # Download the audio to test
            audio_url = "http://localhost:8000" + result.get("audio_url", "")
            audio_response = requests.get(audio_url)

            if audio_response.status_code == 200:
                with open("voice_test_only.mp3", "wb") as f:
                    f.write(audio_response.content)
                print("💾 Downloaded as 'voice_test_only.mp3'")
                print("🎧 Listen to this - it should be your custom voice!")
            else:
                print(f"❌ Could not download audio: {audio_response.status_code}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_just_voice()
