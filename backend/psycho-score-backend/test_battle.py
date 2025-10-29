#!/usr/bin/env python3
"""
Test the ALPHA vs BETA battle feature
"""

import requests
import sys
import os
import json


def battle_test(original_path, contender_path):
    """Test the alpha vs beta battle endpoint"""

    if not os.path.exists(original_path):
        print(f"❌ Original card not found: {original_path}")
        return

    if not os.path.exists(contender_path):
        print(f"❌ Contender card not found: {contender_path}")
        return

    print("🥊 BUSINESS CARD BATTLE: ALPHA VS BETA")
    print("=" * 60)
    print(f"🃏 Original Card: {original_path}")
    print(f"⚔️  Contender Card: {contender_path}")
    print("-" * 60)

    try:
        with (
            open(original_path, "rb") as orig_file,
            open(contender_path, "rb") as cont_file,
        ):
            files = {"original": orig_file, "contender": cont_file}

            print("📤 Uploading cards for Patrick's judgment...")
            response = requests.post(
                "http://localhost:8000/api/analyze/alpha-vs-beta",
                files=files,
                timeout=120,  # Battle analysis might take longer
            )

        print(f"📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            battle_result = result.get("battle_result", {})
            detailed_analysis = result.get("detailed_analysis", {})
            scores = result.get("scores", {})

            print("\n" + "🏆" * 20)
            print("🎭 PATRICK'S VERDICT")
            print("🏆" * 20)

            verdict = battle_result.get("verdict", "UNKNOWN")
            winner = battle_result.get("winner", "unknown")
            announcement = battle_result.get("announcement", "No announcement")

            print(f"\n🎯 FINAL VERDICT: {verdict}")
            print(f"👑 WINNER: {winner.upper()}")
            print(f"📢 ANNOUNCEMENT: {announcement}")

            print(f"\n📊 BATTLE SCORES:")
            print(f"   Original Card: {scores.get('original_score', 'N/A')}/10")
            print(f"   Contender Card: {scores.get('contender_score', 'N/A')}/10")

            print(f"\n🎤 Patrick's Full Analysis:")
            print("-" * 40)
            patrick_analysis = detailed_analysis.get(
                "patrick_comparison", "No analysis available"
            )
            print(patrick_analysis)

            audio_url = battle_result.get("audio_url", "")
            if audio_url:
                print(f"\n🔊 Audio Verdict: http://localhost:8000{audio_url}")

                # Download the audio
                try:
                    audio_response = requests.get(f"http://localhost:8000{audio_url}")
                    if audio_response.status_code == 200:
                        filename = f"battle_verdict_{verdict.lower()}.mp3"
                        with open(filename, "wb") as f:
                            f.write(audio_response.content)
                        print(f"💾 Audio saved as: {filename}")
                        print("🎧 Listen to Patrick announce the winner!")
                except Exception as e:
                    print(f"❌ Could not download audio: {e}")

            print("\n" + "🏆" * 20)

        else:
            print(f"❌ Battle failed: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error during battle: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_battle.py <original_card_path> <contender_card_path>")
        print("Example: python test_battle.py my_card.jpg their_card.jpg")
        print("\n🥊 Let Patrick decide who has the superior business card!")
    else:
        battle_test(sys.argv[1], sys.argv[2])
