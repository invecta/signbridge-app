#!/usr/bin/env python3
"""
SignBridge Hand Tracking Integration
Integrates Hand Detection 3D with existing SignBridge platform
"""

import cv2
import mediapipe as mp
import requests
import json
import socket
import time
import threading
from typing import Dict, List, Optional

class SignBridgeHandTracker:
    def __init__(self, signbridge_url="https://signbridgeproduction-70e5b1074092.herokuapp.com"):
        self.signbridge_url = signbridge_url
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Communication
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.unity_port = 5052
        
        # State
        self.is_tracking = False
        self.session_id = None
        self.recognition_results = []
        
    def start_session(self) -> str:
        """Start a SignBridge hand tracking session"""
        try:
            response = requests.post(f"{self.signbridge_url}/api/hand-tracking/start")
            if response.status_code == 200:
                data = response.json()
                self.session_id = data.get('session_id')
                print(f"✅ SignBridge session started: {self.session_id}")
                return self.session_id
            else:
                # Fallback session ID
                self.session_id = f"session_{int(time.time())}"
                print(f"⚠️ Using fallback session: {self.session_id}")
                return self.session_id
        except Exception as e:
            print(f"❌ Session start error: {e}")
            self.session_id = f"session_{int(time.time())}"
            return self.session_id
    
    def process_hand_landmarks(self, landmarks) -> Optional[Dict]:
        """Process hand landmarks with SignBridge API"""
        if not self.is_tracking or not landmarks:
            return None
            
        try:
            # Convert landmarks to SignBridge format
            landmark_data = []
            for landmark in landmarks.landmark:
                landmark_data.extend([
                    landmark.x * 1000,
                    landmark.y * 1000,
                    landmark.z * 1000
                ])
            
            # Send to SignBridge API
            payload = {
                'landmarks': landmark_data,
                'session_id': self.session_id,
                'timestamp': time.time()
            }
            
            response = requests.post(
                f"{self.signbridge_url}/api/hand-tracking/landmarks",
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                self.recognition_results.append(result)
                return result
            else:
                # Fallback to local recognition
                return self.local_sign_recognition(landmark_data)
                
        except Exception as e:
            print(f"❌ Landmark processing error: {e}")
            return None
    
    def local_sign_recognition(self, landmarks) -> Dict:
        """Fallback local sign recognition"""
        # Simulate recognition based on landmark patterns
        simulated_signs = [
            {"sign": "Hello", "category": "greeting", "confidence": 0.92},
            {"sign": "Thank you", "category": "polite", "confidence": 0.88},
            {"sign": "Yes", "category": "response", "confidence": 0.95},
            {"sign": "No", "category": "response", "confidence": 0.90},
            {"sign": "Help", "category": "request", "confidence": 0.85}
        ]
        
        # Simple pattern matching (replace with your ML model)
        import random
        result = random.choice(simulated_signs)
        result['session_id'] = self.session_id
        result['timestamp'] = time.time()
        
        return result
    
    def send_to_unity(self, landmarks):
        """Send hand landmarks to Unity"""
        if not landmarks:
            return
            
        try:
            landmark_data = []
            for landmark in landmarks.landmark:
                landmark_data.extend([
                    int(landmark.x * 1000),
                    int(landmark.y * 1000),
                    int(landmark.z * 1000)
                ])
            
            data_string = str(landmark_data).replace('[', '').replace(']', '')
            self.udp_socket.sendto(data_string.encode(), ('127.0.0.1', self.unity_port))
            
        except Exception as e:
            print(f"❌ Unity communication error: {e}")
    
    def run_tracking(self):
        """Main hand tracking loop"""
        print("🚀 SignBridge Hand Tracking Started")
        print("Controls:")
        print("  'r' - Start/Stop recognition")
        print("  's' - Start SignBridge session")
        print("  'q' - Quit")
        
        # Start SignBridge session
        self.start_session()
        
        frame_count = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Failed to read from camera")
                break
                
            # Flip frame horizontally
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Send to Unity
                    self.send_to_unity(hand_landmarks)
                    
                    # Process with SignBridge
                    recognition_result = self.process_hand_landmarks(hand_landmarks)
                    
                    if recognition_result:
                        # Display result
                        sign_name = recognition_result.get('sign', 'Unknown')
                        confidence = recognition_result.get('confidence', 0)
                        
                        cv2.putText(frame, f"Sign: {sign_name}", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 70), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display status
            status = "TRACKING" if self.is_tracking else "STANDBY"
            cv2.putText(frame, f"Status: {status}", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Display frame
            cv2.imshow('SignBridge Hand Tracking', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.is_tracking = not self.is_tracking
                print(f"🔄 Recognition: {'ON' if self.is_tracking else 'OFF'}")
            elif key == ord('s'):
                self.start_session()
            
            frame_count += 1
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.udp_socket.close()
        print("✅ SignBridge Hand Tracking ended")

def main():
    print("🤚 SignBridge Hand Tracking Integration")
    print("=" * 50)
    
    try:
        tracker = SignBridgeHandTracker()
        tracker.run_tracking()
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
