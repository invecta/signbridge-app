# Data Collection System for Sign Recognition
# Collects and organizes ASL gesture data for training

import cv2
import numpy as np
import os
import json
import time
from typing import List, Dict, Optional
from pathlib import Path
import mediapipe as mp

class SignDataCollector:
    """Collects ASL sign data for training"""
    
    def __init__(self, data_dir: str = "data/asl_dataset"):
        """Initialize data collector"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Data collection state
        self.current_sign = None
        self.collection_count = 0
        self.target_samples = 100  # Samples per sign
        self.collected_data = []
        
        print("âœ… Sign Data Collector initialized")
        print(f"ðŸ“ Data directory: {self.data_dir}")
    
    def start_collection(self, sign_name: str, target_samples: int = 100):
        """Start collecting data for a specific sign"""
        self.current_sign = sign_name
        self.target_samples = target_samples
        self.collection_count = 0
        
        # Create sign directory
        sign_dir = self.data_dir / sign_name
        sign_dir.mkdir(exist_ok=True)
        
        print(f"ðŸŽ¯ Starting collection for sign: {sign_name}")
        print(f"ðŸ“Š Target samples: {target_samples}")
        print("Press 'c' to capture, 'q' to quit, 'n' for next sign")
    
    def collect_sample(self, frame: np.ndarray) -> bool:
        """Collect a single sample from frame"""
        try:
            if self.current_sign is None:
                print("âŒ No sign selected for collection")
                return False
            
            # Process frame with MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                # Extract landmarks
                landmarks = []
                for hand_landmarks in results.multi_hand_landmarks:
                    for landmark in hand_landmarks.landmark:
                        landmarks.extend([landmark.x, landmark.y, landmark.z])
                
                # Save sample
                sample_data = {
                    'sign_name': self.current_sign,
                    'landmarks': landmarks,
                    'timestamp': time.time(),
                    'sample_id': self.collection_count
                }
                
                # Save to file
                sample_file = self.data_dir / self.current_sign / f"sample_{self.collection_count:04d}.json"
                with open(sample_file, 'w') as f:
                    json.dump(sample_data, f, indent=2)
                
                # Save image
                image_file = self.data_dir / self.current_sign / f"image_{self.collection_count:04d}.jpg"
                cv2.imwrite(str(image_file), frame)
                
                self.collection_count += 1
                self.collected_data.append(sample_data)
                
                print(f"âœ… Collected sample {self.collection_count}/{self.target_samples}")
                
                if self.collection_count >= self.target_samples:
                    print(f"ðŸŽ‰ Collection complete for {self.current_sign}!")
                    return True
                
                return False
            else:
                print("âš ï¸ No hands detected in frame")
                return False
                
        except Exception as e:
            print(f"âŒ Error collecting sample: {e}")
            return False
    
    def create_dataset_info(self):
        """Create dataset information file"""
        try:
            dataset_info = {
                'total_signs': len(list(self.data_dir.iterdir())),
                'signs': [],
                'total_samples': 0,
                'created_at': time.time(),
                'description': 'ASL Sign Recognition Dataset'
            }
            
            # Count samples per sign
            for sign_dir in self.data_dir.iterdir():
                if sign_dir.is_dir():
                    samples = len(list(sign_dir.glob("*.json")))
                    dataset_info['signs'].append({
                        'name': sign_dir.name,
                        'samples': samples
                    })
                    dataset_info['total_samples'] += samples
            
            # Save dataset info
            info_file = self.data_dir / "dataset_info.json"
            with open(info_file, 'w') as f:
                json.dump(dataset_info, f, indent=2)
            
            print(f"âœ… Dataset info saved: {dataset_info['total_samples']} samples across {dataset_info['total_signs']} signs")
            
        except Exception as e:
            print(f"âŒ Error creating dataset info: {e}")
    
    def visualize_collection_progress(self, frame: np.ndarray) -> np.ndarray:
        """Visualize collection progress on frame"""
        try:
            # Draw collection info
            if self.current_sign:
                cv2.putText(frame, f"Collecting: {self.current_sign}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Samples: {self.collection_count}/{self.target_samples}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # Progress bar
                progress = self.collection_count / self.target_samples
                bar_width = 300
                bar_height = 20
                bar_x, bar_y = 10, 100
                
                # Background bar
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 0, 0), -1)
                
                # Progress bar
                progress_width = int(bar_width * progress)
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), (0, 255, 0), -1)
                
                # Progress text
                cv2.putText(frame, f"{progress:.1%}", (bar_x + bar_width + 10, bar_y + bar_height), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Draw instructions
            cv2.putText(frame, "Press 'c' to capture, 'q' to quit, 'n' for next sign", 
                       (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            return frame
            
        except Exception as e:
            print(f"âŒ Error visualizing progress: {e}")
            return frame
    
    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'hands'):
            self.hands.close()
        print("âœ… Data collector cleaned up")

# Interactive data collection application
def run_data_collection():
    """Run interactive data collection"""
    print("ðŸŽ¯ ASL Data Collection Application")
    print("=" * 50)
    
    collector = SignDataCollector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("âŒ Could not access camera")
        return
    
    current_sign_index = 0
    signs_to_collect = [
        "hello", "yes", "no", "thank_you", "please", "sorry",
        "help", "water", "food", "bathroom", "love", "happy",
        "sad", "angry", "surprised", "tired", "hungry", "thirsty"
    ]
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            # Visualize progress
            frame = collector.visualize_collection_progress(frame)
            
            cv2.imshow('ASL Data Collection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                # Collect sample
                collector.collect_sample(frame)
            elif key == ord('n'):
                # Next sign
                if current_sign_index < len(signs_to_collect) - 1:
                    current_sign_index += 1
                    collector.start_collection(signs_to_collect[current_sign_index])
                else:
                    print("ðŸŽ‰ All signs collected!")
                    break
            elif key == ord('s'):
                # Start collection for current sign
                if current_sign_index < len(signs_to_collect):
                    collector.start_collection(signs_to_collect[current_sign_index])
    
    except KeyboardInterrupt:
        print("\nâ¹ï¸ Collection interrupted")
    finally:
        collector.create_dataset_info()
        collector.cleanup()
        cap.release()
        cv2.destroyAllWindows()
        print("âœ… Data collection completed")

if __name__ == "__main__":
    run_data_collection()
