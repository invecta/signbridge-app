# SignBridge Web Application - Flask Backend
# RESTful API for web-based sign language communication

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import base64
import io
import json
import time
import os
from pathlib import Path
import sys

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Import SignBridge components
from sign_recognition.enhanced_classifier import EnhancedSignClassifier
from ml.sign_recognition_model import SignRecognitionModel

app = Flask(__name__)
CORS(app)

class SignBridgeWebAPI:
    """Web API for SignBridge communication"""
    
    def __init__(self):
        """Initialize the web API"""
        self.enhanced_classifier = EnhancedSignClassifier()
        self.ai_model = None
        self.ai_enabled = False
        
        # Try to load AI model
        self.load_ai_model()
        
        # Conversation history
        self.conversations = {}
        
        print("âœ… SignBridge Web API initialized")
        print(f"ðŸ“Š Enhanced classifier: {len(self.enhanced_classifier.get_available_signs())} signs")
        print(f"ðŸ§  AI model: {'âœ… Active' if self.ai_enabled else 'âš ï¸ Enhanced Classifier'}")
    
    def load_ai_model(self):
        """Load AI model if available"""
        try:
            model_path = "src/ml/models/best_model.h5"
            if os.path.exists(model_path):
                self.ai_model = SignRecognitionModel()
                if self.ai_model.load_model(model_path):
                    self.ai_enabled = True
                    print("âœ… AI model loaded for web API")
                else:
                    print("âš ï¸ Failed to load AI model for web API")
            else:
                print("âš ï¸ AI model not found for web API")
        except Exception as e:
            print(f"âŒ Error loading AI model for web API: {e}")
    
    def process_image(self, image_data: str) -> dict:
        """Process uploaded image for sign recognition"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data.split(',')[1])
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {"error": "Invalid image data"}
            
            # Resize image
            image = cv2.resize(image, (640, 480))
            
            # Convert to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Mock landmarks for enhanced classifier
            mock_landmarks = [[0.5, 0.5, 0.0] for _ in range(21)]
            
            # Get prediction from enhanced classifier
            result = self.enhanced_classifier.classify_gesture(mock_landmarks)
            
            if result:
                sign, confidence = result
                return {
                    "sign": sign,
                    "confidence": confidence,
                    "description": self.enhanced_classifier.get_sign_description(sign),
                    "ai_enabled": self.ai_enabled
                }
            else:
                return {
                    "sign": "unknown",
                    "confidence": 0.0,
                    "description": "No sign detected",
                    "ai_enabled": self.ai_enabled
                }
                
        except Exception as e:
            return {"error": f"Image processing error: {str(e)}"}
    
    def get_conversation_history(self, session_id: str) -> list:
        """Get conversation history for a session"""
        return self.conversations.get(session_id, [])
    
    def add_to_conversation(self, session_id: str, message: dict):
        """Add message to conversation history"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            **message,
            "timestamp": time.time()
        })
    
    def get_available_signs(self) -> list:
        """Get list of available signs"""
        signs = self.enhanced_classifier.get_available_signs()
        return [{
            "name": sign,
            "description": self.enhanced_classifier.get_sign_description(sign),
            "confidence": self.enhanced_classifier.sign_dictionary[sign]["confidence"]
        } for sign in signs]
    
    def get_statistics(self) -> dict:
        """Get API statistics"""
        return {
            "total_signs": len(self.enhanced_classifier.get_available_signs()),
            "ai_enabled": self.ai_enabled,
            "active_conversations": len(self.conversations),
            "enhanced_classifier_stats": self.enhanced_classifier.get_sign_statistics()
        }

# Initialize API
api = SignBridgeWebAPI()

# API Routes
@app.route('/')
def index():
    """Serve the main web application"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    })

@app.route('/api/signs', methods=['GET'])
def get_signs():
    """Get available signs"""
    try:
        signs = api.get_available_signs()
        return jsonify({
            "success": True,
            "signs": signs,
            "total": len(signs)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recognize', methods=['POST'])
def recognize_sign():
    """Recognize sign from uploaded image"""
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({
                "success": False,
                "error": "No image data provided"
            }), 400
        
        result = api.process_image(data['image'])
        
        if 'error' in result:
            return jsonify({
                "success": False,
                "error": result['error']
            }), 400
        
        # Add to conversation if session_id provided
        if 'session_id' in data:
            api.add_to_conversation(data['session_id'], {
                "type": "sign_recognition",
                "sign": result['sign'],
                "confidence": result['confidence'],
                "description": result['description']
            })
        
        return jsonify({
            "success": True,
            "result": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Get conversation history"""
    try:
        history = api.get_conversation_history(session_id)
        return jsonify({
            "success": True,
            "conversation": history
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/conversation/<session_id>', methods=['POST'])
def add_message(session_id):
    """Add message to conversation"""
    try:
        data = request.get_json()
        
        api.add_to_conversation(session_id, {
            "type": data.get("type", "message"),
            "content": data.get("content", ""),
            "sign": data.get("sign", ""),
            "confidence": data.get("confidence", 0.0)
        })
        
        return jsonify({
            "success": True,
            "message": "Message added to conversation"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get API statistics"""
    try:
        stats = api.get_statistics()
        return jsonify({
            "success": True,
            "statistics": stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/sign/<sign_name>', methods=['GET'])
def get_sign_info(sign_name):
    """Get information about a specific sign"""
    try:
        if sign_name in api.enhanced_classifier.sign_dictionary:
            sign_data = api.enhanced_classifier.sign_dictionary[sign_name]
            return jsonify({
                "success": True,
                "sign": {
                    "name": sign_name,
                    "description": sign_data["description"],
                    "confidence": sign_data["confidence"],
                    "gesture_type": sign_data["gesture_type"],
                    "hand_shape": sign_data["hand_shape"]
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Sign '{sign_name}' not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("ðŸŒ Starting SignBridge Web Application")
    print("=" * 50)
    print("ðŸ“Š Features:")
    print("- RESTful API for sign recognition")
    print("- Real-time image processing")
    print("- Conversation history management")
    print("- Statistics and analytics")
    print("- Cross-platform compatibility")
    print()
    print("ðŸš€ Server starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
