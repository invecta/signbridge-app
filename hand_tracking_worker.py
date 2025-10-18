import time
import os

def hand_tracking_worker():
    """Background worker for hand tracking processing"""
    print("🔄 Hand Tracking Worker started")
    
    while True:
        try:
            # Simulate hand tracking processing
            print("📤 Processing hand tracking data...")
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    hand_tracking_worker()
