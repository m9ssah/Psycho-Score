#!/usr/bin/env python3
"""
Upload your own business card for analysis
"""

import requests
import sys
import os


def upload_business_card(image_path):
    """Upload a business card image for analysis"""

    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return

    print(f"🃏 Uploading business card: {image_path}")
    print("=" * 50)

    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                "http://localhost:8000/api/analyze/psycho-score", files=files
            )

        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis completed successfully!")
            print("\n🎭 Patrick's Analysis:")
            print("-" * 30)
            print(
                result.get("analysis", {}).get(
                    "patrick_critique", "No critique available"
                )
            )
            print(
                f"\n📊 Psycho Score: {result.get('analysis', {}).get('psycho_score', 'N/A')}/10"
            )
            print(
                f"\n🔊 Audio file: http://localhost:8000{result.get('audio_url', '')}"
            )
            print(
                "\n💡 You can listen to the audio by opening the URL above in your browser!"
            )
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error uploading file: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_card.py <path_to_image>")
        print("Example: python upload_card.py my_business_card.jpg")
    else:
        upload_business_card(sys.argv[1])
