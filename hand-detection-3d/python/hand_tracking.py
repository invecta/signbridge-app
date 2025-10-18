import cv2
import mediapipe as mp
import socket
import json
import numpy as np

class HandTracker:
    def __init__(self, udp_ip="127.0.0.1", udp_port=5052):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # UDP setup
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
    def send_hand_data(self, landmarks):
        """Send hand landmark data to Unity via UDP"""
        if landmarks is None:
            return
            
        # Convert landmarks to list format expected by Unity
        hand_data = []
        for landmark in landmarks.landmark:
            # Scale coordinates to match Unity's expected format
            x = int(landmark.x * 1000)  # Scale up for better precision
            y = int(landmark.y * 1000)
            z = int(landmark.z * 1000)
            hand_data.extend([x, y, z])
        
        # Convert to string format expected by Unity
        data_string = str(hand_data).replace('[', '').replace(']', '')
        
        try:
            self.sock.sendto(data_string.encode(), (self.udp_ip, self.udp_port))
            print(f"Sent data: {len(hand_data)} coordinates")
        except Exception as e:
            print(f"Error sending data: {e}")
    
    def run(self):
        """Main tracking loop"""
        print("Starting hand tracking...")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read from camera")
                break
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks on frame
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Send data to Unity
                    self.send_hand_data(hand_landmarks)
            
            # Display frame
            cv2.imshow('Hand Tracking', frame)
            
            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.sock.close()

if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()
