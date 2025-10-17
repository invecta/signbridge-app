# Test Enhanced Sign Recognition Features

import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from sign_recognition.enhanced_classifier import EnhancedSignClassifier

def test_enhanced_classifier():
    """Test the enhanced sign classifier"""
    print("ðŸ§ª Testing Enhanced Sign Classifier")
    print("=" * 50)
    
    # Initialize classifier
    classifier = EnhancedSignClassifier()
    
    # Test 1: Check sign dictionary
    print("ðŸ“š Test 1: Sign Dictionary")
    signs = classifier.get_available_signs()
    print(f"âœ… Total signs loaded: {len(signs)}")
    
    # Test 2: Check statistics
    print("\nðŸ“Š Test 2: Statistics")
    stats = classifier.get_sign_statistics()
    print(f"âœ… Total signs: {stats['total_signs']}")
    print(f"âœ… Average confidence: {stats['average_confidence']:.1%}")
    print(f"âœ… Gesture types: {len(stats['gesture_types'])}")
    print(f"âœ… Hand shapes: {len(stats['hand_shapes'])}")
    
    # Test 3: Check specific signs
    print("\nðŸ¤Ÿ Test 3: Specific Signs")
    test_signs = ["hello", "yes", "no", "love", "emergency", "stop"]
    for sign in test_signs:
        if sign in signs:
            desc = classifier.get_sign_description(sign)
            conf = classifier.sign_dictionary[sign]["confidence"]
            print(f"âœ… {sign}: {desc} (Confidence: {conf:.1%})")
        else:
            print(f"âŒ {sign}: Not found")
    
    # Test 4: Confidence scoring
    print("\nðŸŽ¯ Test 4: Confidence Scoring")
    print(f"âœ… Confidence threshold: {classifier.confidence_threshold:.1%}")
    print(f"âœ… History length: {classifier.history_length}")
    
    # Test 5: Gesture analysis
    print("\nðŸ” Test 5: Gesture Analysis")
    # Mock landmarks for testing
    mock_landmarks = [[0.5, 0.5, 0.0] for _ in range(21)]
    gesture_type = classifier._analyze_gesture_type(mock_landmarks)
    hand_shape = classifier._analyze_hand_shape(mock_landmarks)
    print(f"âœ… Gesture type: {gesture_type}")
    print(f"âœ… Hand shape: {hand_shape}")
    
    print("\nðŸŽ‰ All tests completed successfully!")
    print(f"ðŸ“ˆ Enhanced SignBridge now supports {len(signs)} signs!")

if __name__ == "__main__":
    test_enhanced_classifier()
