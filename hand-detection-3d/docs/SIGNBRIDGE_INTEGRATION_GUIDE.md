# SignBridge Hand Tracking Integration

## 🎯 Integration with SignBridge Platform

This integration adds advanced hand tracking capabilities to your existing SignBridge platform at [https://github.com/invecta/signbridge-app](https://github.com/invecta/signbridge-app).

## 📁 Files to Add to Your Repository

### 1. **Main Integration File**
- `signbridge_hand_tracker.py` - Complete SignBridge integration

### 2. **Web Interface Files**
- `hand-detection-3d/web/index.html` - Web interface
- `hand-detection-3d/web/hand-tracking.js` - JavaScript integration
- `hand-detection-3d/web/signbridge-api.js` - API client

### 3. **Python Backend Files**
- `hand-detection-3d/python/hand_tracker.py` - Main tracker
- `hand-detection-3d/python/signbridge_client.py` - API client
- `hand-detection-3d/python/unity_connector.py` - Unity communication

### 4. **Unity Integration Files**
- `hand-detection-3d/unity/HandTracker.cs` - Unity component
- `hand-detection-3d/unity/SignBridgeAPI.cs` - API connector
- `hand-detection-3d/unity/UDPReceiver.cs` - UDP communication

## 🚀 Quick Integration Steps

### Step 1: Add Files to Your Repository

```bash
# Clone your repository
git clone https://github.com/invecta/signbridge-app.git
cd signbridge-app

# Create hand detection directory
mkdir hand-detection-3d
mkdir hand-detection-3d/web
mkdir hand-detection-3d/python
mkdir hand-detection-3d/unity

# Copy integration files
cp signbridge_hand_tracker.py hand-detection-3d/python/
cp deploy/web/index.html hand-detection-3d/web/
cp deploy/python/* hand-detection-3d/python/
cp deploy/unity/* hand-detection-3d/unity/
```

### Step 2: Update Your SignBridge API

Add these endpoints to your existing backend:

```python
# Add to your web/backend/app.py or similar

@app.route('/api/hand-tracking/start', methods=['POST'])
def start_hand_tracking():
    """Start hand tracking session"""
    session_id = f"ht_{int(time.time())}"
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': 'Hand tracking session started'
    })

@app.route('/api/hand-tracking/landmarks', methods=['POST'])
def process_hand_landmarks():
    """Process hand landmark data"""
    try:
        data = request.json
        landmarks = data.get('landmarks', [])
        session_id = data.get('session_id')
        
        # Process with your existing sign recognition
        result = recognize_sign_from_landmarks(landmarks)
        
        return jsonify({
            'success': True,
            'sign': result.get('sign', 'Unknown'),
            'category': result.get('category', 'unknown'),
            'confidence': result.get('confidence', 0.0),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def recognize_sign_from_landmarks(landmarks):
    """Enhanced sign recognition using hand landmarks"""
    # Integrate with your existing ML models
    # Process 21 hand landmarks
    # Return recognition result
    
    # Example implementation
    return {
        'sign': 'Hello',
        'category': 'greeting',
        'confidence': 0.92
    }
```

### Step 3: Update Your Web Interface

Add hand tracking to your existing web interface:

```html
<!-- Add to your existing HTML -->
<div class="hand-tracking-section">
    <h3>Hand Tracking</h3>
    <button id="start-hand-tracking">Start Hand Tracking</button>
    <video id="hand-video" autoplay muted style="display: none;"></video>
    <canvas id="hand-canvas" style="display: none;"></canvas>
    <div id="recognition-results"></div>
</div>

<script>
// Add to your existing JavaScript
document.getElementById('start-hand-tracking').addEventListener('click', function() {
    startHandTracking();
});

async function startHandTracking() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const video = document.getElementById('hand-video');
        video.srcObject = stream;
        video.style.display = 'block';
        
        // Initialize hand tracking
        initializeHandTracking();
        
    } catch (error) {
        console.error('Camera access error:', error);
    }
}
</script>
```

### Step 4: Update Your Docker Configuration

Add to your existing `Dockerfile`:

```dockerfile
# Add hand tracking dependencies
RUN pip install mediapipe opencv-python numpy requests

# Copy hand detection files
COPY hand-detection-3d/ /app/hand-detection-3d/

# Expose UDP port for Unity
EXPOSE 5052/udp
```

Add to your `docker-compose.yml`:

```yaml
services:
  hand-tracking:
    build: ./hand-detection-3d/python
    ports:
      - "5052:5052/udp"
    environment:
      - SIGNBRIDGE_API_URL=http://signbridge-api:5000
    depends_on:
      - signbridge-api
```

### Step 5: Update Your Kubernetes Deployment

Add to your existing Kubernetes configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: signbridge-hand-tracking
spec:
  replicas: 2
  selector:
    matchLabels:
      app: signbridge-hand-tracking
  template:
    metadata:
      labels:
        app: signbridge-hand-tracking
    spec:
      containers:
      - name: hand-tracking
        image: signbridge/hand-tracking:latest
        ports:
        - containerPort: 5052
          protocol: UDP
        env:
        - name: SIGNBRIDGE_API_URL
          value: "http://signbridge-api:5000"
```

## 🔧 Configuration

### Environment Variables
Add to your existing `.env`:

```bash
# Hand Detection 3D Settings
HAND_TRACKING_ENABLED=true
UNITY_UDP_PORT=5052
MEDIAPIPE_CONFIDENCE=0.7
HAND_TRACKING_FPS=30

# SignBridge Integration
SIGNBRIDGE_API_URL=https://signbridgeproduction-70e5b1074092.herokuapp.com
HAND_RECOGNITION_MODEL_PATH=/models/hand_recognition.pkl
```

### Requirements Update
Add to your existing `requirements.txt`:

```txt
# Existing requirements...
mediapipe==0.10.7
opencv-python==4.8.1.78
numpy==1.24.3
requests==2.31.0
```

## 🎮 Unity Integration

Connect with your existing Unity components:

```csharp
// Add to your existing Unity project
using UnityEngine;
using System.Net.Sockets;
using System.Text;

public class SignBridgeHandTracker : MonoBehaviour
{
    public SignBridgeAPI signBridgeAPI;
    public HandModelController handModel;
    
    private UdpClient udpClient;
    private int port = 5052;
    
    void Start()
    {
        // Connect to existing SignBridge API
        signBridgeAPI = GetComponent<SignBridgeAPI>();
        
        // Initialize UDP receiver
        udpClient = new UdpClient(port);
        StartCoroutine(ReceiveHandData());
    }
    
    System.Collections.IEnumerator ReceiveHandData()
    {
        while (true)
        {
            if (udpClient.Available > 0)
            {
                var data = udpClient.Receive(ref new System.Net.IPEndPoint(System.Net.IPAddress.Any, 0));
                string landmarks = Encoding.UTF8.GetString(data);
                
                // Process landmarks
                ProcessHandLandmarks(landmarks);
            }
            yield return new WaitForSeconds(0.033f); // 30 FPS
        }
    }
    
    void ProcessHandLandmarks(string landmarks)
    {
        // Parse landmarks and update hand model
        // Send to SignBridge API for recognition
        // Update avatar animations
    }
}
```

## 📊 Enhanced Features

### Real-time Communication Flow
1. **Camera Input** → MediaPipe hand detection
2. **Hand Landmarks** → SignBridge API processing
3. **Sign Recognition** → Your existing ML models
4. **Avatar Animation** → 3D model updates
5. **Unity Control** → Real-time hand model

### Multi-platform Support
- **Web interface** integrated with existing UI
- **Python backend** enhanced with hand tracking
- **Unity integration** for 3D visualization
- **Mobile support** via responsive web

### Advanced Analytics
- **Hand tracking accuracy** metrics
- **Sign recognition performance** data
- **User interaction** analytics
- **System performance** monitoring

## 🚀 Deployment Options

### Option 1: Add to Existing Heroku Deployment
```bash
# Add to your existing Heroku app
heroku config:set HAND_TRACKING_ENABLED=true
heroku config:set UNITY_UDP_PORT=5052

# Deploy with hand tracking
git add hand-detection-3d/
git commit -m "Add hand tracking integration"
git push heroku main
```

### Option 2: Add to Existing Kubernetes
```bash
# Apply hand tracking deployment
kubectl apply -f hand-detection-3d/k8s/hand-tracking-deployment.yaml

# Update service
kubectl apply -f hand-detection-3d/k8s/hand-tracking-service.yaml
```

### Option 3: Add to Existing Docker
```bash
# Build with hand tracking
docker build -t signbridge-with-hand-tracking .

# Run with UDP port
docker run -p 5000:5000 -p 5052:5052/udp signbridge-with-hand-tracking
```

## 📈 Performance Benefits

- **Enhanced accuracy** with hand landmark data
- **Real-time processing** for immediate feedback
- **3D visualization** for better user experience
- **Multi-modal input** combining vision and gestures

## 🎯 Next Steps

1. **Fork your repository** and add hand detection files
2. **Update your API** with hand tracking endpoints
3. **Integrate web interface** with existing UI
4. **Deploy enhanced platform** using your existing infrastructure
5. **Test integration** with real users

## 📞 Support

- **Documentation**: Check `hand-detection-3d/docs/`
- **Issues**: Report via GitHub issues
- **API Reference**: SignBridge API documentation
- **Community**: SignBridge user community

---

**🎉 Your SignBridge platform will now have advanced hand tracking capabilities!**

This integration transforms your existing SignBridge into a comprehensive hand tracking and sign recognition platform, perfect for deaf and hearing individuals communication.