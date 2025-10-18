import cv2
import mediapipe as mp
import requests
import json
import socket
import threading
import time
from typing import Dict, List, Optional

class SignBridgeIntegration:
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
        
        # Recognition state
        self.is_recording = False
        self.recognition_results = []
        self.current_session_id = None
        
    def start_learning_session(self) -> str:
        """Start a new learning session with SignBridge"""
        try:
            # Generate a simple session ID since the endpoint might not exist
            self.current_session_id = f"session_{int(time.time())}"
            print(f"✅ Learning session started: {self.current_session_id}")
            return self.current_session_id
        except Exception as e:
            print(f"❌ Error starting session: {e}")
            return None
    
    def recognize_sign_from_frame(self, frame) -> Optional[Dict]:
        """Send frame to SignBridge for recognition"""
        if not self.is_recording:
            return None
            
        try:
            # For now, simulate recognition since the API needs proper setup
            # In a real implementation, you would send the frame to SignBridge
            
            # Simulate a recognition result based on hand landmarks
            simulated_result = {
                "sign_name": "Hello",
                "category": "greeting", 
                "confidence": 0.85,
                "session_id": self.current_session_id
            }
            
            self.recognition_results.append(simulated_result)
            print(f"🎯 Simulated recognition: {simulated_result['sign_name']}")
            return simulated_result
                
        except Exception as e:
            print(f"❌ Recognition error: {e}")
            return None
    
    def get_available_signs(self) -> List[Dict]:
        """Get list of available signs from SignBridge"""
        try:
            response = requests.get(f"{self.signbridge_url}/api/signs")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get signs: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting signs: {e}")
            return []
    
    def create_avatar_from_gesture(self, gesture_data: Dict) -> Optional[str]:
        """Create avatar animation from recognized gesture"""
        try:
            # Simulate avatar creation for now
            sign_name = gesture_data.get('sign_name', 'Unknown')
            print(f"✅ Avatar animation created for gesture: {sign_name}")
            print(f"   Category: {gesture_data.get('category', 'unknown')}")
            print(f"   Confidence: {gesture_data.get('confidence', 0):.2f}")
            
            # Return a simulated animation URL
            return f"avatar_animation_{sign_name.lower()}.mp4"
                
        except Exception as e:
            print(f"❌ Avatar creation error: {e}")
            return None
    
    def send_hand_landmarks_to_unity(self, landmarks, udp_ip="127.0.0.1", udp_port=5052):
        """Send hand landmarks to Unity (your existing system)"""
        if landmarks is None:
            return
            
        # Convert landmarks to Unity format
        hand_data = []
        for landmark in landmarks.landmark:
            x = int(landmark.x * 1000)
            y = int(landmark.y * 1000)
            z = int(landmark.z * 1000)
            hand_data.extend([x, y, z])
        
        data_string = str(hand_data).replace('[', '').replace(']', '')
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data_string.encode(), (udp_ip, udp_port))
            sock.close()
        except Exception as e:
            print(f"❌ Unity communication error: {e}")
    
    def run_integrated_tracking(self):
        """Main integrated tracking loop"""
        print("🚀 Starting SignBridge + Hand Tracking Integration")
        print("Controls:")
        print("  'r' - Start/Stop recognition")
        print("  's' - Get available signs")
        print("  'a' - Start avatar session")
        print("  'q' - Quit")
        
        # Start learning session
        self.start_learning_session()
        
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
                    
                    # Send to Unity (your existing system)
                    self.send_hand_landmarks_to_unity(hand_landmarks)
                    
                    # Send to SignBridge for recognition
                    recognition_result = self.recognize_sign_from_frame(frame)
                    
                    if recognition_result:
                        # Display recognition result
                        sign_name = recognition_result.get('sign_name', 'Unknown')
                        confidence = recognition_result.get('confidence', 0)
                        
                        cv2.putText(frame, f"Sign: {sign_name}", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 70), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Create avatar animation
                        self.create_avatar_from_gesture(recognition_result)
            
            # Display status
            status = "RECORDING" if self.is_recording else "STANDBY"
            cv2.putText(frame, f"Status: {status}", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Display frame
            cv2.imshow('SignBridge + Hand Tracking', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.is_recording = not self.is_recording
                print(f"🔄 Recognition: {'ON' if self.is_recording else 'OFF'}")
            elif key == ord('s'):
                signs = self.get_available_signs()
                print(f"📋 Available signs: {len(signs)}")
                for sign in signs[:5]:  # Show first 5
                    print(f"  - {sign.get('name', 'Unknown')}")
            elif key == ord('a'):
                self.start_learning_session()
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Integration session ended")

if __name__ == "__main__":
    integration = SignBridgeIntegration()
    integration.run_integrated_tracking()
