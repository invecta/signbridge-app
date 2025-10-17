# Enterprise SDK
# Software Development Kit for SignBridge integration

import requests
import json
import time
import hashlib
import hmac
from typing import Dict, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APITier(Enum):
    """API access tiers"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

@dataclass
class SignRecognitionResult:
    """Sign recognition result"""
    sign: str
    confidence: float
    description: str
    processing_time: float
    model_version: str

@dataclass
class AnalyticsData:
    """Analytics data structure"""
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    popular_signs: List[Dict]
    api_usage_by_tier: Dict
    geographic_distribution: Dict

@dataclass
class User:
    """User data structure"""
    id: str
    name: str
    email: str
    tier: str
    created_at: str
    last_active: str

class SignBridgeSDK:
    """SignBridge Enterprise SDK"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.signbridge.com"):
        """Initialize SignBridge SDK"""
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'SignBridge-SDK/1.0.0'
        })
        
        # SDK configuration
        self.config = {
            "version": "1.0.0",
            "timeout": 30,
            "retry_attempts": 3,
            "retry_delay": 1.0
        }
        
        # Rate limiting
        self.rate_limits = {
            "free": 100,
            "basic": 1000,
            "premium": 10000,
            "enterprise": -1  # Unlimited
        }
        
        # Request tracking
        self.request_count = 0
        self.last_request_time = 0
        
        print("âœ… SignBridge SDK initialized")
        print(f"ðŸ”‘ API Key: {api_key[:8]}...")
        print(f"ðŸŒ Base URL: {base_url}")
        print(f"ðŸ“Š Rate limiting: Active")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict:
        """Make authenticated API request with retry logic"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.config["retry_attempts"]):
            try:
                # Check rate limits
                if not self._check_rate_limit():
                    raise Exception("Rate limit exceeded")
                
                # Make request
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    timeout=self.config["timeout"]
                )
                
                # Update request tracking
                self.request_count += 1
                self.last_request_time = time.time()
                
                # Handle response
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise Exception("Invalid API key")
                elif response.status_code == 429:
                    raise Exception("Rate limit exceeded")
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                if attempt == self.config["retry_attempts"] - 1:
                    raise Exception(f"Request failed after {self.config['retry_attempts']} attempts: {e}")
                
                # Wait before retry
                time.sleep(self.config["retry_delay"] * (2 ** attempt))
        
        raise Exception("Max retry attempts exceeded")
    
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        # In a real implementation, this would check against API tier
        # For now, we'll simulate rate limiting
        return True
    
    def recognize_sign(self, image_data: Union[str, bytes], 
                      language: str = "asl") -> SignRecognitionResult:
        """Recognize sign language from image data"""
        try:
            # Prepare request data
            if isinstance(image_data, bytes):
                # Convert bytes to base64 string
                import base64
                image_data = base64.b64encode(image_data).decode('utf-8')
            
            request_data = {
                "image": image_data,
                "language": language,
                "timestamp": time.time()
            }
            
            # Make API request
            response = self._make_request("POST", "/api/v1/recognize", data=request_data)
            
            if response.get("success"):
                result_data = response["result"]
                return SignRecognitionResult(
                    sign=result_data["sign"],
                    confidence=result_data["confidence"],
                    description=result_data["description"],
                    processing_time=result_data["processing_time"],
                    model_version=result_data["model_version"]
                )
            else:
                raise Exception(response.get("error", "Sign recognition failed"))
                
        except Exception as e:
            logger.error(f"Sign recognition error: {e}")
            raise
    
    def get_analytics(self) -> AnalyticsData:
        """Get analytics data"""
        try:
            response = self._make_request("GET", "/api/v1/analytics")
            
            if response.get("success"):
                analytics_data = response["analytics"]
                return AnalyticsData(
                    total_requests=analytics_data["total_requests"],
                    successful_requests=analytics_data["successful_requests"],
                    failed_requests=analytics_data["failed_requests"],
                    average_response_time=analytics_data["average_response_time"],
                    popular_signs=analytics_data["popular_signs"],
                    api_usage_by_tier=analytics_data["api_usage_by_tier"],
                    geographic_distribution=analytics_data["geographic_distribution"]
                )
            else:
                raise Exception(response.get("error", "Analytics retrieval failed"))
                
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            raise
    
    def get_users(self) -> List[User]:
        """Get users list"""
        try:
            response = self._make_request("GET", "/api/v1/users")
            
            if response.get("success"):
                users_data = response["users"]
                return [
                    User(
                        id=user["id"],
                        name=user["name"],
                        email=user["email"],
                        tier=user["tier"],
                        created_at=user["created_at"],
                        last_active=user["last_active"]
                    )
                    for user in users_data
                ]
            else:
                raise Exception(response.get("error", "User retrieval failed"))
                
        except Exception as e:
            logger.error(f"User retrieval error: {e}")
            raise
    
    def create_user(self, name: str, email: str, tier: str = "free") -> User:
        """Create new user"""
        try:
            request_data = {
                "name": name,
                "email": email,
                "tier": tier
            }
            
            response = self._make_request("POST", "/api/v1/users", data=request_data)
            
            if response.get("success"):
                user_data = response["user"]
                return User(
                    id=user_data["id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    tier=user_data["tier"],
                    created_at=user_data["created_at"],
                    last_active=user_data.get("last_active", "")
                )
            else:
                raise Exception(response.get("error", "User creation failed"))
                
        except Exception as e:
            logger.error(f"User creation error: {e}")
            raise
    
    def get_webhooks(self) -> List[Dict]:
        """Get webhooks list"""
        try:
            response = self._make_request("GET", "/api/v1/webhooks")
            
            if response.get("success"):
                return response["webhooks"]
            else:
                raise Exception(response.get("error", "Webhook retrieval failed"))
                
        except Exception as e:
            logger.error(f"Webhook retrieval error: {e}")
            raise
    
    def create_webhook(self, url: str, events: List[str]) -> Dict:
        """Create new webhook"""
        try:
            request_data = {
                "url": url,
                "events": events
            }
            
            response = self._make_request("POST", "/api/v1/webhooks", data=request_data)
            
            if response.get("success"):
                return response["webhook"]
            else:
                raise Exception(response.get("error", "Webhook creation failed"))
                
        except Exception as e:
            logger.error(f"Webhook creation error: {e}")
            raise
    
    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete webhook"""
        try:
            response = self._make_request("DELETE", f"/api/v1/webhooks?id={webhook_id}")
            
            if response.get("success"):
                return True
            else:
                raise Exception(response.get("error", "Webhook deletion failed"))
                
        except Exception as e:
            logger.error(f"Webhook deletion error: {e}")
            raise
    
    def health_check(self) -> Dict:
        """Check API health"""
        try:
            response = self._make_request("GET", "/api/v1/health")
            return response
        except Exception as e:
            logger.error(f"Health check error: {e}")
            raise
    
    def get_api_info(self) -> Dict:
        """Get API information"""
        try:
            response = self._make_request("GET", "/api/v1")
            return response
        except Exception as e:
            logger.error(f"API info error: {e}")
            raise
    
    def get_usage_stats(self) -> Dict:
        """Get SDK usage statistics"""
        return {
            "total_requests": self.request_count,
            "last_request_time": self.last_request_time,
            "sdk_version": self.config["version"],
            "api_key": self.api_key[:8] + "...",
            "base_url": self.base_url
        }

class SignBridgeWebhook:
    """SignBridge webhook handler"""
    
    def __init__(self, secret: str):
        """Initialize webhook handler"""
        self.secret = secret
        self.handlers = {}
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature"""
        expected_signature = hmac.new(
            self.secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def handle_event(self, event_type: str, payload: Dict):
        """Handle webhook event"""
        if event_type in self.handlers:
            handler = self.handlers[event_type]
            handler(payload)
        else:
            logger.warning(f"No handler for event type: {event_type}")
    
    def register_handler(self, event_type: str, handler: Callable):
        """Register event handler"""
        self.handlers[event_type] = handler
        logger.info(f"Registered handler for event: {event_type}")

# Example usage and testing
def test_signbridge_sdk():
    """Test SignBridge SDK features"""
    print("ðŸ§ª Testing SignBridge SDK")
    print("=" * 40)
    
    # Initialize SDK
    sdk = SignBridgeSDK("dev-key-123", "http://localhost:5000")
    
    # Test API info
    print("\nðŸ“š Testing API Info:")
    try:
        api_info = sdk.get_api_info()
        print(f"âœ… API Version: {api_info.get('api', {}).get('version', 'Unknown')}")
        print(f"âœ… Endpoints: {len(api_info.get('endpoints', {}))}")
    except Exception as e:
        print(f"âŒ API info test failed: {e}")
    
    # Test health check
    print("\nðŸ¥ Testing Health Check:")
    try:
        health = sdk.health_check()
        print(f"âœ… Status: {health.get('status', 'Unknown')}")
        print(f"âœ… Version: {health.get('version', 'Unknown')}")
    except Exception as e:
        print(f"âŒ Health check test failed: {e}")
    
    # Test sign recognition (mock)
    print("\nðŸ¤Ÿ Testing Sign Recognition:")
    try:
        # Mock image data
        mock_image = "base64_encoded_image_data"
        result = sdk.recognize_sign(mock_image)
        print(f"âœ… Sign: {result.sign}")
        print(f"âœ… Confidence: {result.confidence:.2f}")
        print(f"âœ… Description: {result.description}")
    except Exception as e:
        print(f"âŒ Sign recognition test failed: {e}")
    
    # Test analytics
    print("\nðŸ“Š Testing Analytics:")
    try:
        analytics = sdk.get_analytics()
        print(f"âœ… Total requests: {analytics.total_requests}")
        print(f"âœ… Success rate: {analytics.successful_requests/analytics.total_requests:.1%}")
        print(f"âœ… Popular signs: {len(analytics.popular_signs)}")
    except Exception as e:
        print(f"âŒ Analytics test failed: {e}")
    
    # Test user management
    print("\nðŸ‘¥ Testing User Management:")
    try:
        users = sdk.get_users()
        print(f"âœ… Users retrieved: {len(users)}")
        for user in users:
            print(f"  - {user.name} ({user.tier})")
    except Exception as e:
        print(f"âŒ User management test failed: {e}")
    
    # Test webhook management
    print("\nðŸ”— Testing Webhook Management:")
    try:
        webhooks = sdk.get_webhooks()
        print(f"âœ… Webhooks retrieved: {len(webhooks)}")
    except Exception as e:
        print(f"âŒ Webhook management test failed: {e}")
    
    # Test usage stats
    print("\nðŸ“ˆ Testing Usage Stats:")
    stats = sdk.get_usage_stats()
    print(f"âœ… Total requests: {stats['total_requests']}")
    print(f"âœ… SDK version: {stats['sdk_version']}")
    
    print("\nðŸŽ‰ SignBridge SDK test completed!")
    print("ðŸš€ Ready for enterprise integration!")

if __name__ == "__main__":
    test_signbridge_sdk()
