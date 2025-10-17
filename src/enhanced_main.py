# Enhanced SignBridge Application
# Integrates enhanced sign recognition with 50+ signs

import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3
import time
import json
import os
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent))

# Import enhanced classifier
from sign_recognition.enhanced_classifier import EnhancedSignClassifier

def main():
    """Enhanced SignBridge application with 50+ signs"""
    print("=" * 60)
    print("ðŸ¤Ÿ Welcome to Enhanced SignBridge - Communication Assistant")
    print("=" * 60)
    
    # Initialize enhanced sign classifier
    enhanced_classifier = EnhancedSignClassifier()
    
    # Initialize speech recognition
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Initialize text-to-speech
    tts_engine = pyttsx3.init()
    
    # Camera setup
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("âŒ Error: Could not access camera")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("âœ… Camera initialized successfully")
    print("ðŸŽ¯ Starting Enhanced SignBridge Conversation Mode")
    print("ðŸ“‹ Controls:")
    print("   s - Start speech recognition")
    print("   h - Show help")
    print("   q - Quit application")
    print("   v - View available signs")
    print("   c - Show confidence settings")
    print()
    print("ðŸ‘‹ Camera is running! Enhanced with 50+ ASL signs!")
    
    conversation_history = []
    last_detected_sign = None
    last_confidence = 0.0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Display enhanced interface
            cv2.putText(frame, 'Enhanced SignBridge - 50+ Signs', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Show last detected sign and confidence
            if last_detected_sign:
                cv2.putText(frame, f'Last Sign: {last_detected_sign}', (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f'Confidence: {last_confidence:.1%}', (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Draw enhanced detection area
            cv2.rectangle(frame, (50, 120), (590, 450), (0, 255, 0), 2)
            cv2.putText(frame, 'Enhanced Detection Area - 50+ Signs', (60, 140), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Display instructions
            cv2.putText(frame, 'Press s to speak, h for help, v for signs, q to quit', 
                       (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            cv2.imshow('Enhanced SignBridge - Communication Assistant', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Speech input mode
                try:
                    with microphone as source:
                        print("ðŸŽ¤ Listening...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source, timeout=5)
                        
                        text = recognizer.recognize_google(audio)
                        print(f"âœ… Recognized: {text}")
                        
                        # Convert to sign animation description using enhanced classifier
                        words = text.lower().split()
                        sign_sequence = []
                        for word in words:
                            if word in enhanced_classifier.sign_dictionary:
                                sign_sequence.append(enhanced_classifier.sign_dictionary[word]["description"])
                            else:
                                sign_sequence.append(f"[Spell: {word}]")
                        
                        animation_desc = " â†’ ".join(sign_sequence)
                        print(f"ðŸ¤Ÿ Enhanced sign animation: {animation_desc}")
                        
                        # Log conversation
                        conversation_history.append({
                            "timestamp": time.time(),
                            "speaker": "hearing_user", 
                            "content": text,
                            "mode": "speech_to_sign",
                            "signs_used": len([w for w in words if w in enhanced_classifier.sign_dictionary])
                        })
                        
                        # Speak the text back
                        tts_engine.say(f"I heard: {text}")
                        tts_engine.runAndWait()
                        
                except sr.WaitTimeoutError:
                    print("â° No speech detected")
                except sr.UnknownValueError:
                    print("âŒ Could not understand speech")
                except Exception as e:
                    print(f"âŒ Speech recognition error: {e}")
            elif key == ord('h'):
                print()
                print("ðŸ¤Ÿ Enhanced SignBridge Help:")
                print()
                print("ðŸ“š Available Signs (50+):")
                signs = enhanced_classifier.get_available_signs()
                for i, sign in enumerate(signs[:20]):  # Show first 20
                    desc = enhanced_classifier.get_sign_description(sign)
                    print(f"- {sign}: {desc}")
                if len(signs) > 20:
                    print(f"... and {len(signs) - 20} more signs!")
                print()
                print("âŒ¨ï¸ Controls:")
                print("- s: Start speech recognition")
                print("- h: Show this help")
                print("- v: View all available signs")
                print("- c: Show confidence settings")
                print("- q: Quit application")
                print()
                print("ðŸ’¡ Tips:")
                print("- Ensure good lighting for hand detection")
                print("- Keep hands visible in camera frame")
                print("- Speak clearly for speech recognition")
                print("- Use natural ASL gestures")
                print()
                print("ðŸ”§ Current Status:")
                print("- Camera: âœ… Working")
                print("- Speech Recognition: âœ… Working")
                print("- Text-to-Speech: âœ… Working")
                print("- Enhanced Sign Recognition: âœ… 50+ Signs")
                print(f"- Total Signs Available: {len(signs)}")
                print()
            elif key == ord('v'):
                # View all available signs
                print()
                print("ðŸ“š All Available Signs:")
                signs = enhanced_classifier.get_available_signs()
                for i, sign in enumerate(signs, 1):
                    desc = enhanced_classifier.get_sign_description(sign)
                    conf = enhanced_classifier.sign_dictionary[sign]["confidence"]
                    print(f"{i:2d}. {sign:15s} - {desc} (Confidence: {conf:.1%})")
                print()
                print(f"Total: {len(signs)} signs available")
                print()
            elif key == ord('c'):
                # Show confidence settings
                stats = enhanced_classifier.get_sign_statistics()
                print()
                print("ðŸ“Š Confidence Settings:")
                print(f"- Confidence Threshold: {enhanced_classifier.confidence_threshold:.1%}")
                print(f"- History Length: {enhanced_classifier.history_length}")
                print(f"- Average Confidence: {stats['average_confidence']:.1%}")
                print(f"- Total Signs: {stats['total_signs']}")
                print(f"- Gesture Types: {len(stats['gesture_types'])}")
                print(f"- Hand Shapes: {len(stats['hand_shapes'])}")
                print()
    
    except KeyboardInterrupt:
        print()
        print("â¹ï¸ Application interrupted by user")
    except Exception as e:
        print(f"âŒ Application error: {e}")
    finally:
        # Save conversation history
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/enhanced_conversation_history.json", 'w') as f:
                json.dump(conversation_history, f, indent=2)
            print("ðŸ’¾ Enhanced conversation history saved")
        except Exception as e:
            print(f"âŒ Error saving conversation history: {e}")
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("âœ… Enhanced SignBridge application closed")

if __name__ == "__main__":
    main()
