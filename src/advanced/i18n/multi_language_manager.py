# Multi-Language Sign Language Support
# International sign language recognition and translation

import json
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class MultiLanguageSignManager:
    """Manages multiple international sign languages"""
    
    def __init__(self):
        """Initialize multi-language sign manager"""
        self.supported_languages = {
            'asl': 'American Sign Language',
            'bsl': 'British Sign Language', 
            'lsf': 'French Sign Language',
            'dgs': 'German Sign Language',
            'jsl': 'Japanese Sign Language',
            'csl': 'Chinese Sign Language',
            'isl': 'Irish Sign Language',
            'auslan': 'Australian Sign Language'
        }
        
        self.current_language = 'asl'
        self.sign_dictionaries = {}
        self.translation_mappings = {}
        
        # Load all language dictionaries
        self.load_all_languages()
        
        print("âœ… Multi-Language Sign Manager initialized")
        print(f"ðŸŒ Supported languages: {len(self.supported_languages)}")
        print(f"ðŸŽ¯ Current language: {self.current_language.upper()}")
    
    def load_all_languages(self):
        """Load sign dictionaries for all supported languages"""
        for lang_code, lang_name in self.supported_languages.items():
            self.sign_dictionaries[lang_code] = self._create_language_dictionary(lang_code)
        
        # Create translation mappings
        self._create_translation_mappings()
    
    def _create_language_dictionary(self, lang_code: str) -> Dict:
        """Create sign dictionary for specific language"""
        if lang_code == 'asl':
            return self._get_asl_dictionary()
        elif lang_code == 'bsl':
            return self._get_bsl_dictionary()
        elif lang_code == 'lsf':
            return self._get_lsf_dictionary()
        elif lang_code == 'dgs':
            return self._get_dgs_dictionary()
        elif lang_code == 'jsl':
            return self._get_jsl_dictionary()
        elif lang_code == 'csl':
            return self._get_csl_dictionary()
        elif lang_code == 'isl':
            return self._get_isl_dictionary()
        elif lang_code == 'auslan':
            return self._get_auslan_dictionary()
        else:
            return {}
    
    def _get_asl_dictionary(self) -> Dict:
        """American Sign Language dictionary"""
        return {
            "hello": {
                "description": "Wave hand in greeting motion",
                "confidence": 0.9,
                "gesture_type": "wave",
                "hand_shape": "open",
                "cultural_note": "Standard American greeting"
            },
            "yes": {
                "description": "Make fist and nod up and down",
                "confidence": 0.9,
                "gesture_type": "nod",
                "hand_shape": "fist",
                "cultural_note": "Universal affirmation"
            },
            "no": {
                "description": "Index finger shakes side to side",
                "confidence": 0.85,
                "gesture_type": "shake",
                "hand_shape": "index_extended",
                "cultural_note": "Universal negation"
            },
            "thank_you": {
                "description": "Flat hand touches chin and moves forward",
                "confidence": 0.85,
                "gesture_type": "touch_and_move",
                "hand_shape": "flat",
                "cultural_note": "Polite expression"
            },
            "please": {
                "description": "Flat hand circles on chest",
                "confidence": 0.85,
                "gesture_type": "circle",
                "hand_shape": "flat",
                "cultural_note": "Polite request"
            },
            "sorry": {
                "description": "Closed fist circles on chest",
                "confidence": 0.8,
                "gesture_type": "circle",
                "hand_shape": "fist",
                "cultural_note": "Apology gesture"
            },
            "help": {
                "description": "Closed fist taps on open palm",
                "confidence": 0.85,
                "gesture_type": "tap",
                "hand_shape": "fist_to_palm",
                "cultural_note": "Assistance request"
            },
            "water": {
                "description": "W handshape taps chin",
                "confidence": 0.8,
                "gesture_type": "tap",
                "hand_shape": "w_shape",
                "cultural_note": "Basic need"
            },
            "food": {
                "description": "Fingertips touch mouth",
                "confidence": 0.85,
                "gesture_type": "touch",
                "hand_shape": "fingertips",
                "cultural_note": "Basic need"
            },
            "bathroom": {
                "description": "T handshape shakes",
                "confidence": 0.8,
                "gesture_type": "shake",
                "hand_shape": "t_shape",
                "cultural_note": "Basic need"
            },
            "love": {
                "description": "Hands form heart shape",
                "confidence": 0.9,
                "gesture_type": "heart_shape",
                "hand_shape": "heart",
                "cultural_note": "Emotional expression"
            },
            "family": {
                "description": "Both hands form F shape",
                "confidence": 0.8,
                "gesture_type": "f_shape",
                "hand_shape": "f_shape",
                "cultural_note": "Social concept"
            },
            "friend": {
                "description": "Index fingers hook together",
                "confidence": 0.8,
                "gesture_type": "hook_together",
                "hand_shape": "index_extended",
                "cultural_note": "Social relationship"
            },
            "work": {
                "description": "Both hands form W shape",
                "confidence": 0.8,
                "gesture_type": "w_shape",
                "hand_shape": "w_shape",
                "cultural_note": "Professional activity"
            },
            "home": {
                "description": "Hand forms roof shape",
                "confidence": 0.85,
                "gesture_type": "roof_shape",
                "hand_shape": "roof",
                "cultural_note": "Living space"
            },
            "school": {
                "description": "Both hands clap",
                "confidence": 0.8,
                "gesture_type": "clap",
                "hand_shape": "open",
                "cultural_note": "Educational institution"
            },
            "money": {
                "description": "Hand rubs thumb and fingers",
                "confidence": 0.85,
                "gesture_type": "rub_fingers",
                "hand_shape": "pinch",
                "cultural_note": "Economic concept"
            },
            "time": {
                "description": "Index finger taps wrist",
                "confidence": 0.8,
                "gesture_type": "tap_wrist",
                "hand_shape": "index_extended",
                "cultural_note": "Temporal concept"
            },
            "emergency": {
                "description": "Hand waves frantically",
                "confidence": 0.9,
                "gesture_type": "frantic_wave",
                "hand_shape": "open",
                "cultural_note": "Urgent situation"
            },
            "stop": {
                "description": "Hand forms stop sign",
                "confidence": 0.95,
                "gesture_type": "stop_sign",
                "hand_shape": "stop",
                "cultural_note": "Universal command"
            }
        }
    
    def _get_bsl_dictionary(self) -> Dict:
        """British Sign Language dictionary"""
        return {
            "hello": {
                "description": "Wave hand with palm facing outward",
                "confidence": 0.9,
                "gesture_type": "wave",
                "hand_shape": "open",
                "cultural_note": "British greeting style"
            },
            "yes": {
                "description": "Fist nods up and down",
                "confidence": 0.9,
                "gesture_type": "nod",
                "hand_shape": "fist",
                "cultural_note": "British affirmation"
            },
            "no": {
                "description": "Index finger shakes side to side",
                "confidence": 0.85,
                "gesture_type": "shake",
                "hand_shape": "index_extended",
                "cultural_note": "British negation"
            },
            "thank_you": {
                "description": "Flat hand touches chin and moves forward",
                "confidence": 0.85,
                "gesture_type": "touch_and_move",
                "hand_shape": "flat",
                "cultural_note": "British politeness"
            },
            "please": {
                "description": "Flat hand circles on chest",
                "confidence": 0.85,
                "gesture_type": "circle",
                "hand_shape": "flat",
                "cultural_note": "British request"
            },
            "sorry": {
                "description": "Closed fist circles on chest",
                "confidence": 0.8,
                "gesture_type": "circle",
                "hand_shape": "fist",
                "cultural_note": "British apology"
            },
            "help": {
                "description": "Closed fist taps on open palm",
                "confidence": 0.85,
                "gesture_type": "tap",
                "hand_shape": "fist_to_palm",
                "cultural_note": "British assistance"
            },
            "water": {
                "description": "W handshape taps chin",
                "confidence": 0.8,
                "gesture_type": "tap",
                "hand_shape": "w_shape",
                "cultural_note": "British water sign"
            },
            "food": {
                "description": "Fingertips touch mouth",
                "confidence": 0.85,
                "gesture_type": "touch",
                "hand_shape": "fingertips",
                "cultural_note": "British food sign"
            },
            "bathroom": {
                "description": "T handshape shakes",
                "confidence": 0.8,
                "gesture_type": "shake",
                "hand_shape": "t_shape",
                "cultural_note": "British bathroom sign"
            }
        }
    
    def _get_lsf_dictionary(self) -> Dict:
        """French Sign Language dictionary"""
        return {
            "hello": {
                "description": "Wave hand with French style",
                "confidence": 0.9,
                "gesture_type": "wave",
                "hand_shape": "open",
                "cultural_note": "French greeting"
            },
            "yes": {
                "description": "Fist nods with French style",
                "confidence": 0.9,
                "gesture_type": "nod",
                "hand_shape": "fist",
                "cultural_note": "French affirmation"
            },
            "no": {
                "description": "Index finger shakes French style",
                "confidence": 0.85,
                "gesture_type": "shake",
                "hand_shape": "index_extended",
                "cultural_note": "French negation"
            },
            "thank_you": {
                "description": "French thank you gesture",
                "confidence": 0.85,
                "gesture_type": "touch_and_move",
                "hand_shape": "flat",
                "cultural_note": "French politeness"
            },
            "please": {
                "description": "French please gesture",
                "confidence": 0.85,
                "gesture_type": "circle",
                "hand_shape": "flat",
                "cultural_note": "French request"
            }
        }
    
    def _get_dgs_dictionary(self) -> Dict:
        """German Sign Language dictionary"""
        return {
            "hello": {
                "description": "German greeting style",
                "confidence": 0.9,
                "gesture_type": "wave",
                "hand_shape": "open",
                "cultural_note": "German greeting"
            },
            "yes": {
                "description": "German affirmation style",
                "confidence": 0.9,
                "gesture_type": "nod",
                "hand_shape": "fist",
                "cultural_note": "German affirmation"
            },
            "no": {
                "description": "German negation style",
                "confidence": 0.85,
                "gesture_type": "shake",
                "hand_shape": "index_extended",
                "cultural_note": "German negation"
            }
        }
    
    def _get_jsl_dictionary(self) -> Dict:
        """Japanese Sign Language dictionary"""
        return {
            "hello": {
                "description": "Japanese greeting style",
                "confidence": 0.9,
                "gesture_type": "wave",
                "hand_shape": "open",
                "cultural_note": "Japanese greeting"
            },
            "yes": {
                "description": "Japanese affirmation style",
                "confidence": 0.9,
                "gesture_type": "nod",
                "hand_shape": "fist",
                "cultural_note": "Japanese affirmation"
            },
            "no": {
                "description": "Japanese negation style",
                "confidence": 0.85,
                "gesture_type": "shake",
                "hand_shape": "index_extended",
                "cultural_note": "Japanese negation"
            }
        }
    
    def _get_csl_dictionary(self) -> Dict:
        """Chinese Sign Language dictionary"""
        return {
            "hello": {
                "description": "Chinese greeting style",
                "confidence": 0.9,
                "gesture_type": "wave",
                "hand_shape": "open",
                "cultural_note": "Chinese greeting"
            },
            "yes": {
                "description": "Chinese affirmation style",
                "confidence": 0.9,
                "gesture_type": "nod",
                "hand_shape": "fist",
                "cultural_note": "Chinese affirmation"
            },
            "no": {
                "description": "Chinese negation style",
                "confidence": 0.85,
                "gesture_type": "shake",
                "hand_shape": "index_extended",
                "cultural_note": "Chinese negation"
            }
        }
    
    def _get_isl_dictionary(self) -> Dict:
        """Irish Sign Language dictionary"""
        return {
            "hello": {
                "description": "Irish greeting style",
                "confidence": 0.9,
                "gesture_type": "wave",
                "hand_shape": "open",
                "cultural_note": "Irish greeting"
            },
            "yes": {
                "description": "Irish affirmation style",
                "confidence": 0.9,
                "gesture_type": "nod",
                "hand_shape": "fist",
                "cultural_note": "Irish affirmation"
            },
            "no": {
                "description": "Irish negation style",
                "confidence": 0.85,
                "gesture_type": "shake",
                "hand_shape": "index_extended",
                "cultural_note": "Irish negation"
            }
        }
    
    def _get_auslan_dictionary(self) -> Dict:
        """Australian Sign Language dictionary"""
        return {
            "hello": {
                "description": "Australian greeting style",
                "confidence": 0.9,
                "gesture_type": "wave",
                "hand_shape": "open",
                "cultural_note": "Australian greeting"
            },
            "yes": {
                "description": "Australian affirmation style",
                "confidence": 0.9,
                "gesture_type": "nod",
                "hand_shape": "fist",
                "cultural_note": "Australian affirmation"
            },
            "no": {
                "description": "Australian negation style",
                "confidence": 0.85,
                "gesture_type": "shake",
                "hand_shape": "index_extended",
                "cultural_note": "Australian negation"
            }
        }
    
    def _create_translation_mappings(self):
        """Create translation mappings between languages"""
        # Basic translation mappings (simplified)
        self.translation_mappings = {
            'asl_to_bsl': {
                'hello': 'hello',
                'yes': 'yes',
                'no': 'no',
                'thank_you': 'thank_you',
                'please': 'please'
            },
            'bsl_to_asl': {
                'hello': 'hello',
                'yes': 'yes',
                'no': 'no',
                'thank_you': 'thank_you',
                'please': 'please'
            }
        }
    
    def set_language(self, language_code: str) -> bool:
        """Set the current sign language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            print(f"âœ… Language changed to: {self.supported_languages[language_code]}")
            return True
        else:
            print(f"âŒ Unsupported language: {language_code}")
            return False
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get all supported languages"""
        return self.supported_languages
    
    def get_sign_dictionary(self, language_code: Optional[str] = None) -> Dict:
        """Get sign dictionary for specific language"""
        if language_code is None:
            language_code = self.current_language
        
        return self.sign_dictionaries.get(language_code, {})
    
    def translate_sign(self, sign: str, from_lang: str, to_lang: str) -> Optional[str]:
        """Translate sign between languages"""
        mapping_key = f"{from_lang}_to_{to_lang}"
        if mapping_key in self.translation_mappings:
            return self.translation_mappings[mapping_key].get(sign)
        return None
    
    def get_sign_info(self, sign: str, language_code: Optional[str] = None) -> Optional[Dict]:
        """Get detailed information about a sign"""
        if language_code is None:
            language_code = self.current_language
        
        dictionary = self.get_sign_dictionary(language_code)
        return dictionary.get(sign)
    
    def get_language_statistics(self) -> Dict:
        """Get statistics about all languages"""
        stats = {}
        for lang_code, lang_name in self.supported_languages.items():
            dictionary = self.get_sign_dictionary(lang_code)
            stats[lang_code] = {
                'name': lang_name,
                'sign_count': len(dictionary),
                'signs': list(dictionary.keys())
            }
        return stats
    
    def add_custom_sign(self, sign: str, description: str, language_code: Optional[str] = None):
        """Add custom sign to dictionary"""
        if language_code is None:
            language_code = self.current_language
        
        if language_code in self.sign_dictionaries:
            self.sign_dictionaries[language_code][sign] = {
                'description': description,
                'confidence': 0.8,
                'gesture_type': 'custom',
                'hand_shape': 'custom',
                'cultural_note': 'User-defined sign'
            }
            print(f"âœ… Custom sign '{sign}' added to {language_code.upper()}")
    
    def export_language_data(self, language_code: str, file_path: str):
        """Export language data to JSON file"""
        try:
            dictionary = self.get_sign_dictionary(language_code)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(dictionary, f, indent=2, ensure_ascii=False)
            print(f"âœ… Language data exported to {file_path}")
        except Exception as e:
            print(f"âŒ Error exporting language data: {e}")
    
    def import_language_data(self, language_code: str, file_path: str):
        """Import language data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                dictionary = json.load(f)
            self.sign_dictionaries[language_code] = dictionary
            print(f"âœ… Language data imported from {file_path}")
        except Exception as e:
            print(f"âŒ Error importing language data: {e}")

# Example usage and testing
def test_multi_language_support():
    """Test multi-language sign support"""
    print("ðŸ§ª Testing Multi-Language Sign Support")
    print("=" * 50)
    
    # Initialize manager
    manager = MultiLanguageSignManager()
    
    # Test language switching
    print("\nðŸŒ Testing Language Switching:")
    for lang_code in ['asl', 'bsl', 'lsf', 'dgs', 'jsl']:
        if manager.set_language(lang_code):
            dictionary = manager.get_sign_dictionary()
            print(f"âœ… {lang_code.upper()}: {len(dictionary)} signs")
    
    # Test sign information
    print("\nðŸ“š Testing Sign Information:")
    manager.set_language('asl')
    hello_info = manager.get_sign_info('hello')
    if hello_info:
        print(f"âœ… ASL 'hello': {hello_info['description']}")
    
    # Test statistics
    print("\nðŸ“Š Testing Language Statistics:")
    stats = manager.get_language_statistics()
    for lang_code, stat in stats.items():
        print(f"âœ… {lang_code.upper()}: {stat['sign_count']} signs")
    
    print("\nðŸŽ‰ Multi-language support test completed!")

if __name__ == "__main__":
    test_multi_language_support()
