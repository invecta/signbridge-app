#!/usr/bin/env python3
"""
SignBridge API Test Script
Tests the connection and basic functionality of SignBridge APIs
"""

import requests
import json
import time
import cv2
import numpy as np

class SignBridgeTester:
    def __init__(self, base_url="https://signbridgeproduction-70e5b1074092.herokuapp.com"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_api_health(self):
        """Test if SignBridge API is accessible"""
        print("🔍 Testing SignBridge API Health...")
        try:
            # Test basic connectivity
            response = self.session.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                print("✅ SignBridge API is accessible")
                return True
            else:
                print(f"❌ API returned status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_get_signs(self):
        """Test getting available signs"""
        print("\n📋 Testing Get Signs API...")
        try:
            response = self.session.get(f"{self.base_url}/api/signs", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Successfully retrieved signs")
                print(f"   Response keys: {list(data.keys())}")
                return True
            else:
                print(f"❌ Get signs failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Get signs error: {e}")
            return False
    
    def test_start_session(self):
        """Test starting a learning session"""
        print("\n🎓 Testing Start Learning Session...")
        try:
            response = self.session.post(f"{self.base_url}/api/learning/start-session", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Learning session started successfully")
                print(f"   Session data: {data}")
                return True
            else:
                print(f"❌ Start session failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Start session error: {e}")
            return False
    
    def test_recognition_with_sample_image(self):
        """Test recognition with a sample image"""
        print("\n🎯 Testing Recognition API...")
        try:
            # Create a simple test image (white background with some content)
            test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
            cv2.putText(test_image, "TEST IMAGE", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
            
            # Encode image
            _, buffer = cv2.imencode('.jpg', test_image)
            image_data = buffer.tobytes()
            
            # Send to recognition API
            files = {'image': ('test.jpg', image_data, 'image/jpeg')}
            response = self.session.post(f"{self.base_url}/api/recognize", files=files, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Recognition API responded successfully")
                print(f"   Response: {data}")
                return True
            else:
                print(f"❌ Recognition failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Recognition error: {e}")
            return False
    
    def test_avatar_system(self):
        """Test avatar system"""
        print("\n👤 Testing Avatar System...")
        try:
            avatar_data = {
                "text": "Hello",
                "gesture_type": "greeting",
                "confidence": 0.95
            }
            
            response = self.session.post(
                f"{self.base_url}/api/avatar/process-text",
                json=avatar_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Avatar system responded successfully")
                print(f"   Response: {data}")
                return True
            else:
                print(f"❌ Avatar system failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Avatar system error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting SignBridge API Tests")
        print("=" * 50)
        
        tests = [
            ("API Health", self.test_api_health),
            ("Get Signs", self.test_get_signs),
            ("Start Session", self.test_start_session),
            ("Recognition", self.test_recognition_with_sample_image),
            ("Avatar System", self.test_avatar_system)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name} test crashed: {e}")
                results[test_name] = False
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        passed = sum(results.values())
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:20} {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! SignBridge integration is ready.")
        else:
            print("⚠️  Some tests failed. Check the issues above.")
        
        return results

def main():
    tester = SignBridgeTester()
    results = tester.run_all_tests()
    
    # Additional info
    print("\n📝 Next Steps:")
    if results.get("API Health", False):
        print("1. ✅ SignBridge API is accessible")
        print("2. 🔧 You can now run the integration script")
        print("3. 🎮 Test with your Unity project")
    else:
        print("1. ❌ Check your internet connection")
        print("2. 🔍 Verify SignBridge URL is correct")
        print("3. 🛠️  Try again later if the service is down")

if __name__ == "__main__":
    main()
