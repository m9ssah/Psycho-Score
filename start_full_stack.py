#!/usr/bin/env python3
"""
Start both backend and frontend servers for integration testing
"""

import subprocess
import sys
import os
import time
import requests


def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def check_frontend_health():
    """Check if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        return response.status_code == 200
    except:
        return False


def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    backend_dir = (
        r"c:\Users\Hp\Documents\GitHub\psycho-score\backend\psycho-score-backend\src"
    )
    python_exe = r"C:/Users/Hp/Documents/GitHub/psycho-score/venv/Scripts/python.exe"

    try:
        os.chdir(backend_dir)
        backend_process = subprocess.Popen(
            [
                python_exe,
                "-m",
                "uvicorn",
                "main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for backend to start
        print("⏳ Waiting for backend to start...")
        for i in range(30):  # Wait up to 30 seconds
            if check_backend_health():
                print("✅ Backend is running on http://localhost:8000")
                return backend_process
            time.sleep(1)
            print(f"   Attempt {i + 1}/30...")

        print("❌ Backend failed to start")
        return None
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None


def start_frontend():
    """Start the React frontend server"""
    print("🚀 Starting React frontend server...")
    frontend_dir = r"c:\Users\Hp\Documents\GitHub\psycho-score\frontend\hackortreat"

    try:
        os.chdir(frontend_dir)
        frontend_process = subprocess.Popen(
            ["npm", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        # Wait for frontend to start
        print("⏳ Waiting for frontend to start...")
        for i in range(60):  # Wait up to 60 seconds
            if check_frontend_health():
                print("✅ Frontend is running on http://localhost:3000")
                return frontend_process
            time.sleep(1)
            if i % 10 == 0:
                print(f"   Attempt {i + 1}/60...")

        print("❌ Frontend failed to start")
        return None
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None


def main():
    print("🎭 Psycho Score - Full Stack Integration Test")
    print("=" * 60)

    # Check if backend is already running
    if check_backend_health():
        print("✅ Backend already running on http://localhost:8000")
        backend_process = None
    else:
        backend_process = start_backend()
        if not backend_process:
            print("❌ Failed to start backend. Exiting.")
            return

    # Check if frontend is already running
    if check_frontend_health():
        print("✅ Frontend already running on http://localhost:3000")
        frontend_process = None
    else:
        frontend_process = start_frontend()
        if not frontend_process:
            print("❌ Failed to start frontend. Exiting.")
            if backend_process:
                backend_process.terminate()
            return

    print("\n🎉 Both servers are running!")
    print("=" * 60)
    print("🔗 Backend API: http://localhost:8000")
    print("🔗 Backend Docs: http://localhost:8000/docs")
    print("🔗 Frontend App: http://localhost:3000")
    print("=" * 60)
    print("\n🧪 Ready for testing:")
    print("1. Upload business cards for analysis")
    print("2. Test ALPHA vs BETA battles")
    print("3. Listen to Patrick's voice critiques")
    print("\nPress Ctrl+C to stop both servers")

    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Servers stopped")


if __name__ == "__main__":
    main()
