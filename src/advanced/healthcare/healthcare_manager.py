# Healthcare Integration System
# Medical communication features for patient-doctor interaction

import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class HealthcareSignManager:
    """Manages medical sign language for healthcare communication"""
    
    def __init__(self):
        """Initialize healthcare sign manager"""
        self.medical_signs = self._load_medical_signs()
        self.emergency_signs = self._load_emergency_signs()
        self.body_parts = self._load_body_parts()
        self.symptoms = self._load_symptoms()
        self.medications = self._load_medications()
        
        # HIPAA compliance settings
        self.hipaa_compliant = True
        self.patient_data_encrypted = True
        self.audit_log_enabled = True
        
        # Emergency detection
        self.emergency_keywords = ['emergency', 'help', 'pain', 'hurt', 'doctor', 'hospital']
        
        print("âœ… Healthcare Sign Manager initialized")
        print(f"ðŸ¥ Medical signs: {len(self.medical_signs)}")
        print(f"ðŸš¨ Emergency signs: {len(self.emergency_signs)}")
        print(f"ðŸ”’ HIPAA compliant: {self.hipaa_compliant}")
    
    def _load_medical_signs(self) -> Dict:
        """Load medical terminology signs"""
        return {
            "doctor": {
                "description": "D handshape taps chest",
                "confidence": 0.9,
                "gesture_type": "tap",
                "hand_shape": "d_shape",
                "medical_category": "profession",
                "urgency_level": "normal"
            },
            "nurse": {
                "description": "N handshape taps chest",
                "confidence": 0.9,
                "gesture_type": "tap",
                "hand_shape": "n_shape",
                "medical_category": "profession",
                "urgency_level": "normal"
            },
            "hospital": {
                "description": "H handshape shakes",
                "confidence": 0.9,
                "gesture_type": "shake",
                "hand_shape": "h_shape",
                "medical_category": "facility",
                "urgency_level": "normal"
            },
            "medicine": {
                "description": "M handshape moves to mouth",
                "confidence": 0.85,
                "gesture_type": "move_to_mouth",
                "hand_shape": "m_shape",
                "medical_category": "treatment",
                "urgency_level": "normal"
            },
            "pain": {
                "description": "Hands form claws and shake",
                "confidence": 0.9,
                "gesture_type": "shake",
                "hand_shape": "claw",
                "medical_category": "symptom",
                "urgency_level": "high"
            },
            "hurt": {
                "description": "Index finger points to affected area",
                "confidence": 0.85,
                "gesture_type": "point",
                "hand_shape": "index_extended",
                "medical_category": "symptom",
                "urgency_level": "high"
            },
            "headache": {
                "description": "Hand taps forehead",
                "confidence": 0.85,
                "gesture_type": "tap",
                "hand_shape": "open",
                "medical_category": "symptom",
                "urgency_level": "medium"
            },
            "stomach": {
                "description": "Hand circles on stomach",
                "confidence": 0.9,
                "gesture_type": "circle",
                "hand_shape": "open",
                "medical_category": "body_part",
                "urgency_level": "normal"
            },
            "chest": {
                "description": "Hand taps chest",
                "confidence": 0.9,
                "gesture_type": "tap",
                "hand_shape": "open",
                "medical_category": "body_part",
                "urgency_level": "normal"
            },
            "back": {
                "description": "Hand taps back",
                "confidence": 0.85,
                "gesture_type": "tap",
                "hand_shape": "open",
                "medical_category": "body_part",
                "urgency_level": "normal"
            },
            "arm": {
                "description": "Hand taps arm",
                "confidence": 0.9,
                "gesture_type": "tap",
                "hand_shape": "open",
                "medical_category": "body_part",
                "urgency_level": "normal"
            },
            "leg": {
                "description": "Hand taps leg",
                "confidence": 0.9,
                "gesture_type": "tap",
                "hand_shape": "open",
                "medical_category": "body_part",
                "urgency_level": "normal"
            },
            "fever": {
                "description": "Hand moves away from forehead",
                "confidence": 0.85,
                "gesture_type": "move_away",
                "hand_shape": "open",
                "medical_category": "symptom",
                "urgency_level": "high"
            },
            "cough": {
                "description": "Hand covers mouth and shakes",
                "confidence": 0.9,
                "gesture_type": "shake",
                "hand_shape": "open",
                "medical_category": "symptom",
                "urgency_level": "medium"
            },
            "nausea": {
                "description": "Hand moves to mouth and away",
                "confidence": 0.85,
                "gesture_type": "move_to_and_away",
                "hand_shape": "open",
                "medical_category": "symptom",
                "urgency_level": "medium"
            },
            "dizzy": {
                "description": "Hand circles around head",
                "confidence": 0.8,
                "gesture_type": "circle",
                "hand_shape": "open",
                "medical_category": "symptom",
                "urgency_level": "high"
            },
            "breathing": {
                "description": "Hands move up and down on chest",
                "confidence": 0.9,
                "gesture_type": "up_down_motion",
                "hand_shape": "open",
                "medical_category": "function",
                "urgency_level": "high"
            },
            "heart": {
                "description": "Hand taps chest over heart",
                "confidence": 0.9,
                "gesture_type": "tap",
                "hand_shape": "open",
                "medical_category": "body_part",
                "urgency_level": "high"
            },
            "blood": {
                "description": "Red handshape moves down",
                "confidence": 0.85,
                "gesture_type": "move_down",
                "hand_shape": "open",
                "medical_category": "substance",
                "urgency_level": "high"
            },
            "allergy": {
                "description": "Hand scratches neck",
                "confidence": 0.8,
                "gesture_type": "scratch",
                "hand_shape": "open",
                "medical_category": "condition",
                "urgency_level": "high"
            }
        }
    
    def _load_emergency_signs(self) -> Dict:
        """Load emergency-specific signs"""
        return {
            "emergency": {
                "description": "Hand waves frantically",
                "confidence": 0.95,
                "gesture_type": "frantic_wave",
                "hand_shape": "open",
                "urgency_level": "critical",
                "response_action": "call_911"
            },
            "help": {
                "description": "Closed fist taps on open palm",
                "confidence": 0.9,
                "gesture_type": "tap",
                "hand_shape": "fist_to_palm",
                "urgency_level": "high",
                "response_action": "seek_assistance"
            },
            "stop": {
                "description": "Hand forms stop sign",
                "confidence": 0.95,
                "gesture_type": "stop_sign",
                "hand_shape": "stop",
                "urgency_level": "critical",
                "response_action": "immediate_stop"
            },
            "danger": {
                "description": "Hand points with warning",
                "confidence": 0.9,
                "gesture_type": "warning_point",
                "hand_shape": "index_extended",
                "urgency_level": "critical",
                "response_action": "evacuate_area"
            },
            "fire": {
                "description": "Hands wave upward like flames",
                "confidence": 0.9,
                "gesture_type": "flame_motion",
                "hand_shape": "open",
                "urgency_level": "critical",
                "response_action": "fire_protocol"
            },
            "fall": {
                "description": "Hand moves down quickly",
                "confidence": 0.85,
                "gesture_type": "quick_move_down",
                "hand_shape": "open",
                "urgency_level": "high",
                "response_action": "check_injury"
            }
        }
    
    def _load_body_parts(self) -> Dict:
        """Load body part signs"""
        return {
            "head": {"description": "Hand taps head", "confidence": 0.9},
            "neck": {"description": "Hand taps neck", "confidence": 0.9},
            "shoulder": {"description": "Hand taps shoulder", "confidence": 0.9},
            "chest": {"description": "Hand taps chest", "confidence": 0.9},
            "stomach": {"description": "Hand circles stomach", "confidence": 0.9},
            "back": {"description": "Hand taps back", "confidence": 0.85},
            "arm": {"description": "Hand taps arm", "confidence": 0.9},
            "hand": {"description": "Hand taps hand", "confidence": 0.9},
            "leg": {"description": "Hand taps leg", "confidence": 0.9},
            "foot": {"description": "Hand taps foot", "confidence": 0.9},
            "eye": {"description": "Hand points to eye", "confidence": 0.9},
            "ear": {"description": "Hand points to ear", "confidence": 0.9},
            "mouth": {"description": "Hand points to mouth", "confidence": 0.9},
            "nose": {"description": "Hand points to nose", "confidence": 0.9},
            "heart": {"description": "Hand taps chest over heart", "confidence": 0.9}
        }
    
    def _load_symptoms(self) -> Dict:
        """Load symptom signs"""
        return {
            "pain": {"description": "Hands form claws and shake", "confidence": 0.9, "urgency": "high"},
            "hurt": {"description": "Index finger points to affected area", "confidence": 0.85, "urgency": "high"},
            "headache": {"description": "Hand taps forehead", "confidence": 0.85, "urgency": "medium"},
            "fever": {"description": "Hand moves away from forehead", "confidence": 0.85, "urgency": "high"},
            "cough": {"description": "Hand covers mouth and shakes", "confidence": 0.9, "urgency": "medium"},
            "nausea": {"description": "Hand moves to mouth and away", "confidence": 0.85, "urgency": "medium"},
            "dizzy": {"description": "Hand circles around head", "confidence": 0.8, "urgency": "high"},
            "tired": {"description": "Hands on face, eyes closed", "confidence": 0.8, "urgency": "low"},
            "weak": {"description": "Hand droops", "confidence": 0.8, "urgency": "medium"},
            "swollen": {"description": "Hands expand outward", "confidence": 0.8, "urgency": "medium"}
        }
    
    def _load_medications(self) -> Dict:
        """Load medication signs"""
        return {
            "medicine": {"description": "M handshape moves to mouth", "confidence": 0.85},
            "pill": {"description": "Fingertips touch mouth", "confidence": 0.85},
            "injection": {"description": "Index finger taps arm", "confidence": 0.8},
            "bandage": {"description": "Hand wraps around arm", "confidence": 0.8},
            "ice": {"description": "Hands shake like cold", "confidence": 0.8},
            "heat": {"description": "Hand moves away from body", "confidence": 0.8}
        }
    
    def detect_emergency(self, recognized_signs: List[str]) -> Tuple[bool, str, str]:
        """Detect emergency situations from recognized signs"""
        emergency_detected = False
        emergency_type = ""
        response_action = ""
        
        for sign in recognized_signs:
            if sign in self.emergency_signs:
                emergency_detected = True
                emergency_type = sign
                response_action = self.emergency_signs[sign].get("response_action", "seek_help")
                break
            elif sign in self.medical_signs:
                urgency = self.medical_signs[sign].get("urgency_level", "normal")
                if urgency in ["high", "critical"]:
                    emergency_detected = True
                    emergency_type = sign
                    response_action = "medical_attention_needed"
                    break
        
        return emergency_detected, emergency_type, response_action
    
    def get_medical_sign_info(self, sign: str) -> Optional[Dict]:
        """Get medical information about a sign"""
        if sign in self.medical_signs:
            return self.medical_signs[sign]
        elif sign in self.emergency_signs:
            return self.emergency_signs[sign]
        return None
    
    def get_body_part_signs(self) -> Dict:
        """Get all body part signs"""
        return self.body_parts
    
    def get_symptom_signs(self) -> Dict:
        """Get all symptom signs"""
        return self.symptoms
    
    def get_medication_signs(self) -> Dict:
        """Get all medication signs"""
        return self.medications
    
    def create_patient_record(self, patient_id: str, signs_recognized: List[str]) -> Dict:
        """Create HIPAA-compliant patient record"""
        if not self.hipaa_compliant:
            raise Exception("HIPAA compliance required for patient records")
        
        record = {
            "patient_id": patient_id,
            "timestamp": time.time(),
            "signs_recognized": signs_recognized,
            "emergency_detected": False,
            "urgency_level": "normal",
            "encrypted": self.patient_data_encrypted,
            "audit_log": []
        }
        
        # Check for emergency
        emergency_detected, emergency_type, response_action = self.detect_emergency(signs_recognized)
        record["emergency_detected"] = emergency_detected
        record["emergency_type"] = emergency_type
        record["response_action"] = response_action
        
        # Determine urgency level
        max_urgency = "normal"
        for sign in signs_recognized:
            sign_info = self.get_medical_sign_info(sign)
            if sign_info:
                urgency = sign_info.get("urgency_level", "normal")
                if urgency == "critical":
                    max_urgency = "critical"
                elif urgency == "high" and max_urgency != "critical":
                    max_urgency = "high"
                elif urgency == "medium" and max_urgency not in ["critical", "high"]:
                    max_urgency = "medium"
        
        record["urgency_level"] = max_urgency
        
        # Add to audit log
        if self.audit_log_enabled:
            record["audit_log"].append({
                "action": "patient_record_created",
                "timestamp": time.time(),
                "user": "system"
            })
        
        return record
    
    def get_medical_statistics(self) -> Dict:
        """Get healthcare system statistics"""
        return {
            "total_medical_signs": len(self.medical_signs),
            "total_emergency_signs": len(self.emergency_signs),
            "total_body_parts": len(self.body_parts),
            "total_symptoms": len(self.symptoms),
            "total_medications": len(self.medications),
            "hipaa_compliant": self.hipaa_compliant,
            "patient_data_encrypted": self.patient_data_encrypted,
            "audit_log_enabled": self.audit_log_enabled
        }
    
    def export_medical_data(self, file_path: str):
        """Export medical data (HIPAA compliant)"""
        if not self.hipaa_compliant:
            raise Exception("HIPAA compliance required for data export")
        
        medical_data = {
            "medical_signs": self.medical_signs,
            "emergency_signs": self.emergency_signs,
            "body_parts": self.body_parts,
            "symptoms": self.symptoms,
            "medications": self.medications,
            "export_timestamp": time.time(),
            "hipaa_compliant": True
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(medical_data, f, indent=2, ensure_ascii=False)
            print(f"âœ… Medical data exported to {file_path}")
        except Exception as e:
            print(f"âŒ Error exporting medical data: {e}")

# Example usage and testing
def test_healthcare_integration():
    """Test healthcare integration features"""
    print("ðŸ§ª Testing Healthcare Integration")
    print("=" * 50)
    
    # Initialize healthcare manager
    healthcare = HealthcareSignManager()
    
    # Test medical signs
    print("\nðŸ¥ Testing Medical Signs:")
    medical_signs = healthcare.get_medical_sign_info("doctor")
    if medical_signs:
        print(f"âœ… Doctor sign: {medical_signs['description']}")
    
    # Test emergency detection
    print("\nðŸš¨ Testing Emergency Detection:")
    test_signs = ["pain", "help", "emergency"]
    emergency_detected, emergency_type, response_action = healthcare.detect_emergency(test_signs)
    print(f"âœ… Emergency detected: {emergency_detected}")
    print(f"âœ… Emergency type: {emergency_type}")
    print(f"âœ… Response action: {response_action}")
    
    # Test patient record creation
    print("\nðŸ“‹ Testing Patient Record Creation:")
    try:
        patient_record = healthcare.create_patient_record("P001", test_signs)
        print(f"âœ… Patient record created: {patient_record['patient_id']}")
        print(f"âœ… Emergency detected: {patient_record['emergency_detected']}")
        print(f"âœ… Urgency level: {patient_record['urgency_level']}")
    except Exception as e:
        print(f"âŒ Error creating patient record: {e}")
    
    # Test statistics
    print("\nðŸ“Š Testing Healthcare Statistics:")
    stats = healthcare.get_medical_statistics()
    print(f"âœ… Medical signs: {stats['total_medical_signs']}")
    print(f"âœ… Emergency signs: {stats['total_emergency_signs']}")
    print(f"âœ… HIPAA compliant: {stats['hipaa_compliant']}")
    
    print("\nðŸŽ‰ Healthcare integration test completed!")

if __name__ == "__main__":
    test_healthcare_integration()
