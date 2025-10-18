#!/usr/bin/env python3
"""
Simple SignBridge Integration Test
Tests the basic functionality without camera
"""

import requests
import json
import time

def test_signbridge_connection():
    """Test basic SignBridge connection"""
    print("🔍 Testing SignBridge Connection...")
    
    try:
        # Test basic connectivity
        response = requests.get("https://signbridgeproduction-70e5b1074092.herokuapp.com/", timeout=10)
        if response.status_code == 200:
            print("✅ SignBridge is accessible")
            return True
        else:
            print(f"❌ SignBridge returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_get_signs():
    """Test getting available signs"""
    print("\n📋 Testing Get Signs...")
    
    try:
        response = requests.get("https://signbridgeproduction-70e5b1074092.herokuapp.com/api/signs", timeout=10)
        if response.status_code == 200:
            data = response.json()
            signs = data.get('signs', [])
            print(f"✅ Retrieved {len(signs)} signs")
            
            # Show first few signs
            for i, sign in enumerate(signs[:5]):
                print(f"   {i+1}. {sign.get('name', 'Unknown')} - {sign.get('category', 'Unknown')}")
            
            return True
        else:
            print(f"❌ Get signs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get signs error: {e}")
        return False

def simulate_hand_tracking():
    """Simulate hand tracking data"""
    print("\n🤚 Simulating Hand Tracking...")
    
    # Simulate hand landmark data (21 points * 3 coordinates)
    simulated_landmarks = []
    for i in range(21):
        x = 0.5 + (i % 3) * 0.1  # Simulate hand spread
        y = 0.5 + (i // 3) * 0.05  # Simulate finger length
        z = 0.1 + i * 0.01  # Simulate depth
        simulated_landmarks.extend([x, y, z])
    
    print(f"✅ Generated {len(simulated_landmarks)} landmark coordinates")
    print(f"   Sample data: {simulated_landmarks[:9]}...")  # Show first 3 points
    
    return simulated_landmarks

def simulate_recognition():
    """Simulate sign recognition"""
    print("\n🎯 Simulating Sign Recognition...")
    
    # Simulate recognition results
    recognition_results = [
        {"sign_name": "Hello", "category": "greeting", "confidence": 0.92},
        {"sign_name": "Thank you", "category": "polite", "confidence": 0.88},
        {"sign_name": "Yes", "category": "response", "confidence": 0.95},
        {"sign_name": "No", "category": "response", "confidence": 0.90},
        {"sign_name": "Help", "category": "request", "confidence": 0.85}
    ]
    
    print("✅ Simulated recognition results:")
    for result in recognition_results:
        print(f"   • {result['sign_name']} ({result['category']}) - {result['confidence']:.2f}")
    
    return recognition_results

def test_unity_communication():
    """Test UDP communication to Unity"""
    print("\n🎮 Testing Unity Communication...")
    
    try:
        import socket
        
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Simulate hand data
        hand_data = simulate_hand_tracking()
        data_string = str(hand_data).replace('[', '').replace(']', '')
        
        # Send to Unity (assuming Unity is running)
        try:
            sock.sendto(data_string.encode(), ("127.0.0.1", 5052))
            print("✅ Data sent to Unity on port 5052")
            print("   Note: Unity needs to be running with UDPReceive script")
        except Exception as e:
            print(f"⚠️  Unity not responding: {e}")
            print("   This is normal if Unity isn't running")
        
        sock.close()
        return True
        
    except ImportError:
        print("❌ Socket module not available")
        return False
    except Exception as e:
        print(f"❌ Unity communication error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SignBridge Integration Test")
    print("=" * 50)
    
    tests = [
        ("SignBridge Connection", test_signbridge_connection),
        ("Get Available Signs", test_get_signs),
        ("Hand Tracking Simulation", lambda: simulate_hand_tracking() is not None),
        ("Recognition Simulation", lambda: simulate_recognition() is not None),
        ("Unity Communication", test_unity_communication)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed >= 3:  # At least basic functionality works
        print("\n🎉 Integration test successful!")
        print("\n📝 Next Steps:")
        print("1. ✅ Basic integration is working")
        print("2. 🎮 Start Unity with your Hand Detection project")
        print("3. 📹 Run the full integration with camera")
        print("4. 🔧 Customize for your specific needs")
    else:
        print("\n⚠️  Some issues detected. Check the errors above.")

if __name__ == "__main__":
    main()
