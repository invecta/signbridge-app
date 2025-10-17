# 3D Avatar System
# Animated sign language interpreters using 3D avatars

import json
import time
import math
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class Avatar3DSystem:
    """3D avatar system for animated sign language interpretation"""
    
    def __init__(self):
        """Initialize 3D avatar system"""
        self.avatars = self._create_avatar_library()
        self.animations = self._create_animation_library()
        self.current_avatar = "default"
        self.animation_queue = []
        self.is_playing = False
        
        print("âœ… 3D Avatar System initialized")
        print(f"ðŸ‘¤ Available avatars: {len(self.avatars)}")
        print(f"ðŸŽ¬ Animation library: {len(self.animations)} animations")
    
    def _create_avatar_library(self) -> Dict:
        """Create library of 3D avatars"""
        return {
            "default": {
                "name": "Default Avatar",
                "description": "Standard 3D avatar for sign language",
                "gender": "neutral",
                "skin_tone": "medium",
                "hair_color": "brown",
                "eye_color": "brown",
                "clothing": "casual",
                "accessibility_features": ["high_contrast", "large_hands", "clear_facial_expressions"],
                "file_path": "assets/avatars/default_avatar.glb",
                "texture_path": "assets/textures/default_texture.png"
            },
            "professional": {
                "name": "Professional Avatar",
                "description": "Professional interpreter avatar",
                "gender": "neutral",
                "skin_tone": "medium",
                "hair_color": "black",
                "eye_color": "brown",
                "clothing": "business",
                "accessibility_features": ["professional_appearance", "clear_gestures", "formal_style"],
                "file_path": "assets/avatars/professional_avatar.glb",
                "texture_path": "assets/textures/professional_texture.png"
            },
            "child_friendly": {
                "name": "Child-Friendly Avatar",
                "description": "Friendly avatar for children",
                "gender": "neutral",
                "skin_tone": "light",
                "hair_color": "blonde",
                "eye_color": "blue",
                "clothing": "colorful",
                "accessibility_features": ["bright_colors", "exaggerated_expressions", "playful_style"],
                "file_path": "assets/avatars/child_avatar.glb",
                "texture_path": "assets/textures/child_texture.png"
            },
            "medical": {
                "name": "Medical Avatar",
                "description": "Avatar for medical communication",
                "gender": "neutral",
                "skin_tone": "medium",
                "hair_color": "brown",
                "eye_color": "brown",
                "clothing": "medical",
                "accessibility_features": ["medical_uniform", "calm_expressions", "precise_gestures"],
                "file_path": "assets/avatars/medical_avatar.glb",
                "texture_path": "assets/textures/medical_texture.png"
            },
            "elderly": {
                "name": "Elderly Avatar",
                "description": "Avatar representing elderly interpreter",
                "gender": "neutral",
                "skin_tone": "medium",
                "hair_color": "gray",
                "eye_color": "brown",
                "clothing": "comfortable",
                "accessibility_features": ["slower_movements", "clear_gestures", "respectful_style"],
                "file_path": "assets/avatars/elderly_avatar.glb",
                "texture_path": "assets/textures/elderly_texture.png"
            }
        }
    
    def _create_animation_library(self) -> Dict:
        """Create library of sign language animations"""
        return {
            "hello": {
                "name": "Hello Animation",
                "description": "Wave hand in greeting motion",
                "duration": 2.0,
                "keyframes": [
                    {"time": 0.0, "hand_position": "rest", "expression": "neutral"},
                    {"time": 0.5, "hand_position": "wave_start", "expression": "friendly"},
                    {"time": 1.0, "hand_position": "wave_peak", "expression": "smile"},
                    {"time": 1.5, "hand_position": "wave_end", "expression": "friendly"},
                    {"time": 2.0, "hand_position": "rest", "expression": "neutral"}
                ],
                "hand_movements": [
                    {"joint": "wrist", "rotation": [0, 0, 45]},
                    {"joint": "elbow", "rotation": [0, 0, 0]},
                    {"joint": "shoulder", "rotation": [0, 0, 0]}
                ],
                "facial_expressions": [
                    {"time": 0.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"},
                    {"time": 1.0, "eyebrows": "raised", "eyes": "open", "mouth": "smile"},
                    {"time": 2.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"}
                ]
            },
            "yes": {
                "name": "Yes Animation",
                "description": "Make fist and nod up and down",
                "duration": 1.5,
                "keyframes": [
                    {"time": 0.0, "hand_position": "rest", "expression": "neutral"},
                    {"time": 0.3, "hand_position": "fist", "expression": "neutral"},
                    {"time": 0.6, "hand_position": "nod_up", "expression": "confident"},
                    {"time": 0.9, "hand_position": "nod_down", "expression": "confident"},
                    {"time": 1.2, "hand_position": "nod_up", "expression": "confident"},
                    {"time": 1.5, "hand_position": "rest", "expression": "neutral"}
                ],
                "hand_movements": [
                    {"joint": "wrist", "rotation": [0, 0, 0]},
                    {"joint": "elbow", "rotation": [0, 0, 0]},
                    {"joint": "shoulder", "rotation": [0, 0, 0]}
                ],
                "facial_expressions": [
                    {"time": 0.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"},
                    {"time": 0.6, "eyebrows": "raised", "eyes": "open", "mouth": "slight_smile"},
                    {"time": 1.5, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"}
                ]
            },
            "no": {
                "name": "No Animation",
                "description": "Index finger shakes side to side",
                "duration": 1.0,
                "keyframes": [
                    {"time": 0.0, "hand_position": "rest", "expression": "neutral"},
                    {"time": 0.2, "hand_position": "index_extended", "expression": "neutral"},
                    {"time": 0.4, "hand_position": "shake_left", "expression": "serious"},
                    {"time": 0.6, "hand_position": "shake_right", "expression": "serious"},
                    {"time": 0.8, "hand_position": "shake_left", "expression": "serious"},
                    {"time": 1.0, "hand_position": "rest", "expression": "neutral"}
                ],
                "hand_movements": [
                    {"joint": "wrist", "rotation": [0, 0, -30]},
                    {"joint": "wrist", "rotation": [0, 0, 30]},
                    {"joint": "wrist", "rotation": [0, 0, -30]}
                ],
                "facial_expressions": [
                    {"time": 0.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"},
                    {"time": 0.4, "eyebrows": "furrowed", "eyes": "open", "mouth": "neutral"},
                    {"time": 1.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"}
                ]
            },
            "thank_you": {
                "name": "Thank You Animation",
                "description": "Flat hand touches chin and moves forward",
                "duration": 2.5,
                "keyframes": [
                    {"time": 0.0, "hand_position": "rest", "expression": "neutral"},
                    {"time": 0.5, "hand_position": "chin_touch", "expression": "grateful"},
                    {"time": 1.0, "hand_position": "move_forward", "expression": "grateful"},
                    {"time": 1.5, "hand_position": "extend", "expression": "grateful"},
                    {"time": 2.0, "hand_position": "return", "expression": "grateful"},
                    {"time": 2.5, "hand_position": "rest", "expression": "neutral"}
                ],
                "hand_movements": [
                    {"joint": "wrist", "rotation": [0, 0, 0]},
                    {"joint": "elbow", "rotation": [0, 0, 0]},
                    {"joint": "shoulder", "rotation": [0, 0, 0]}
                ],
                "facial_expressions": [
                    {"time": 0.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"},
                    {"time": 0.5, "eyebrows": "raised", "eyes": "open", "mouth": "slight_smile"},
                    {"time": 1.0, "eyebrows": "raised", "eyes": "open", "mouth": "smile"},
                    {"time": 2.5, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"}
                ]
            },
            "love": {
                "name": "Love Animation",
                "description": "Hands form heart shape",
                "duration": 3.0,
                "keyframes": [
                    {"time": 0.0, "hand_position": "rest", "expression": "neutral"},
                    {"time": 0.5, "hand_position": "heart_start", "expression": "warm"},
                    {"time": 1.0, "hand_position": "heart_form", "expression": "loving"},
                    {"time": 1.5, "hand_position": "heart_hold", "expression": "loving"},
                    {"time": 2.0, "hand_position": "heart_present", "expression": "loving"},
                    {"time": 2.5, "hand_position": "heart_release", "expression": "warm"},
                    {"time": 3.0, "hand_position": "rest", "expression": "neutral"}
                ],
                "hand_movements": [
                    {"joint": "wrist", "rotation": [0, 0, 0]},
                    {"joint": "elbow", "rotation": [0, 0, 0]},
                    {"joint": "shoulder", "rotation": [0, 0, 0]}
                ],
                "facial_expressions": [
                    {"time": 0.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"},
                    {"time": 0.5, "eyebrows": "raised", "eyes": "open", "mouth": "slight_smile"},
                    {"time": 1.0, "eyebrows": "raised", "eyes": "open", "mouth": "smile"},
                    {"time": 1.5, "eyebrows": "raised", "eyes": "open", "mouth": "big_smile"},
                    {"time": 3.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"}
                ]
            },
            "emergency": {
                "name": "Emergency Animation",
                "description": "Hand waves frantically",
                "duration": 1.0,
                "keyframes": [
                    {"time": 0.0, "hand_position": "rest", "expression": "neutral"},
                    {"time": 0.1, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 0.2, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 0.3, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 0.4, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 0.5, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 0.6, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 0.7, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 0.8, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 0.9, "hand_position": "frantic_wave", "expression": "urgent"},
                    {"time": 1.0, "hand_position": "rest", "expression": "neutral"}
                ],
                "hand_movements": [
                    {"joint": "wrist", "rotation": [0, 0, 45]},
                    {"joint": "wrist", "rotation": [0, 0, -45]},
                    {"joint": "wrist", "rotation": [0, 0, 45]},
                    {"joint": "wrist", "rotation": [0, 0, -45]},
                    {"joint": "wrist", "rotation": [0, 0, 45]}
                ],
                "facial_expressions": [
                    {"time": 0.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"},
                    {"time": 0.1, "eyebrows": "furrowed", "eyes": "wide", "mouth": "open"},
                    {"time": 1.0, "eyebrows": "neutral", "eyes": "open", "mouth": "neutral"}
                ]
            }
        }
    
    def set_avatar(self, avatar_id: str) -> bool:
        """Set the current avatar"""
        if avatar_id in self.avatars:
            self.current_avatar = avatar_id
            print(f"âœ… Avatar changed to: {self.avatars[avatar_id]['name']}")
            return True
        else:
            print(f"âŒ Avatar not found: {avatar_id}")
            return False
    
    def get_current_avatar(self) -> Dict:
        """Get current avatar information"""
        return self.avatars.get(self.current_avatar, {})
    
    def get_available_avatars(self) -> Dict:
        """Get all available avatars"""
        return self.avatars
    
    def play_animation(self, animation_id: str) -> bool:
        """Play a specific animation"""
        if animation_id not in self.animations:
            print(f"âŒ Animation not found: {animation_id}")
            return False
        
        animation = self.animations[animation_id]
        print(f"ðŸŽ¬ Playing animation: {animation['name']}")
        print(f"â±ï¸ Duration: {animation['duration']} seconds")
        
        # Simulate animation playback
        self.is_playing = True
        time.sleep(animation['duration'])
        self.is_playing = False
        
        print(f"âœ… Animation completed: {animation['name']}")
        return True
    
    def play_animation_sequence(self, animation_ids: List[str]) -> bool:
        """Play a sequence of animations"""
        print(f"ðŸŽ¬ Playing animation sequence: {len(animation_ids)} animations")
        
        for i, animation_id in enumerate(animation_ids):
            print(f"ðŸ“ Step {i+1}/{len(animation_ids)}: {animation_id}")
            if not self.play_animation(animation_id):
                print(f"âŒ Failed to play animation: {animation_id}")
                return False
        
        print("âœ… Animation sequence completed")
        return True
    
    def create_custom_animation(self, animation_id: str, animation_data: Dict) -> bool:
        """Create a custom animation"""
        try:
            self.animations[animation_id] = animation_data
            print(f"âœ… Custom animation created: {animation_id}")
            return True
        except Exception as e:
            print(f"âŒ Error creating custom animation: {e}")
            return False
    
    def get_animation_info(self, animation_id: str) -> Optional[Dict]:
        """Get information about a specific animation"""
        return self.animations.get(animation_id)
    
    def get_available_animations(self) -> Dict:
        """Get all available animations"""
        return self.animations
    
    def render_avatar(self, position: Tuple[float, float, float], rotation: Tuple[float, float, float]) -> Dict:
        """Render avatar at specific position and rotation"""
        avatar = self.get_current_avatar()
        
        render_data = {
            "avatar_id": self.current_avatar,
            "position": position,
            "rotation": rotation,
            "scale": (1.0, 1.0, 1.0),
            "texture": avatar.get("texture_path", ""),
            "model": avatar.get("file_path", ""),
            "is_playing": self.is_playing,
            "current_animation": self.animation_queue[0] if self.animation_queue else None
        }
        
        return render_data
    
    def export_avatar_data(self, avatar_id: str, file_path: str):
        """Export avatar data to JSON file"""
        try:
            if avatar_id in self.avatars:
                avatar_data = self.avatars[avatar_id]
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(avatar_data, f, indent=2, ensure_ascii=False)
                print(f"âœ… Avatar data exported to {file_path}")
            else:
                print(f"âŒ Avatar not found: {avatar_id}")
        except Exception as e:
            print(f"âŒ Error exporting avatar data: {e}")
    
    def export_animation_data(self, animation_id: str, file_path: str):
        """Export animation data to JSON file"""
        try:
            if animation_id in self.animations:
                animation_data = self.animations[animation_id]
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(animation_data, f, indent=2, ensure_ascii=False)
                print(f"âœ… Animation data exported to {file_path}")
            else:
                print(f"âŒ Animation not found: {animation_id}")
        except Exception as e:
            print(f"âŒ Error exporting animation data: {e}")
    
    def get_system_statistics(self) -> Dict:
        """Get 3D avatar system statistics"""
        return {
            "total_avatars": len(self.avatars),
            "total_animations": len(self.animations),
            "current_avatar": self.current_avatar,
            "is_playing": self.is_playing,
            "animation_queue_length": len(self.animation_queue),
            "system_status": "active"
        }

# Example usage and testing
def test_3d_avatar_system():
    """Test 3D avatar system features"""
    print("ðŸ§ª Testing 3D Avatar System")
    print("=" * 50)
    
    # Initialize avatar system
    avatar_system = Avatar3DSystem()
    
    # Test avatar selection
    print("\nðŸ‘¤ Testing Avatar Selection:")
    avatars = avatar_system.get_available_avatars()
    for avatar_id, avatar_info in avatars.items():
        print(f"âœ… {avatar_id}: {avatar_info['name']}")
    
    # Test avatar switching
    print("\nðŸ”„ Testing Avatar Switching:")
    avatar_system.set_avatar("professional")
    current_avatar = avatar_system.get_current_avatar()
    print(f"âœ… Current avatar: {current_avatar['name']}")
    
    # Test animation playback
    print("\nðŸŽ¬ Testing Animation Playback:")
    animations = avatar_system.get_available_animations()
    for animation_id, animation_info in animations.items():
        print(f"âœ… {animation_id}: {animation_info['name']} ({animation_info['duration']}s)")
    
    # Test single animation
    print("\nðŸŽ­ Testing Single Animation:")
    avatar_system.play_animation("hello")
    
    # Test animation sequence
    print("\nðŸŽª Testing Animation Sequence:")
    sequence = ["hello", "yes", "thank_you"]
    avatar_system.play_animation_sequence(sequence)
    
    # Test custom animation creation
    print("\nðŸ› ï¸ Testing Custom Animation:")
    custom_animation = {
        "name": "Custom Wave",
        "description": "Custom waving animation",
        "duration": 1.0,
        "keyframes": [
            {"time": 0.0, "hand_position": "rest", "expression": "neutral"},
            {"time": 0.5, "hand_position": "wave", "expression": "friendly"},
            {"time": 1.0, "hand_position": "rest", "expression": "neutral"}
        ]
    }
    avatar_system.create_custom_animation("custom_wave", custom_animation)
    
    # Test rendering
    print("\nðŸŽ¨ Testing Avatar Rendering:")
    render_data = avatar_system.render_avatar((0, 0, 0), (0, 0, 0))
    print(f"âœ… Avatar rendered: {render_data['avatar_id']}")
    print(f"âœ… Position: {render_data['position']}")
    print(f"âœ… Playing: {render_data['is_playing']}")
    
    # Test statistics
    print("\nðŸ“Š Testing System Statistics:")
    stats = avatar_system.get_system_statistics()
    print(f"âœ… Total avatars: {stats['total_avatars']}")
    print(f"âœ… Total animations: {stats['total_animations']}")
    print(f"âœ… Current avatar: {stats['current_avatar']}")
    print(f"âœ… System status: {stats['system_status']}")
    
    print("\nðŸŽ‰ 3D Avatar system test completed!")

if __name__ == "__main__":
    test_3d_avatar_system()
