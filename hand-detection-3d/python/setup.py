#!/usr/bin/env python3
"""
Setup script for Hand Detection 3D project
This script helps install dependencies and run the hand tracking system
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_camera():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Camera is working!")
                return True
        print("❌ Camera not available or not working")
        return False
    except ImportError:
        print("❌ OpenCV not installed")
        return False

def main():
    print("🎯 Hand Detection 3D - Setup Script")
    print("=" * 40)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check camera
    if not check_camera():
        print("⚠️  Camera check failed, but you can still try running the script")
    
    print("\n🚀 Setup complete!")
    print("\nNext steps:")
    print("1. Make sure Unity is running with your Hand Detection project")
    print("2. Run: python hand_tracking.py")
    print("3. Press 'q' to quit the tracking")
    print("\nNote: The script will send hand data to Unity on port 5052")

if __name__ == "__main__":
    main()
