using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;
using System;

[System.Serializable]
public class SignBridgeSign
{
    public string name;
    public string category;
    public float confidence;
    public string description;
}

[System.Serializable]
public class SignBridgeResponse
{
    public bool success;
    public string message;
    public SignBridgeSign[] signs;
    public SignBridgeSign recognized_sign;
}

[System.Serializable]
public class AvatarRequest
{
    public string text;
    public string gesture_type;
    public float confidence;
}

public class SignBridgeConnector : MonoBehaviour
{
    [Header("SignBridge Configuration")]
    public string signBridgeURL = "https://signbridgeproduction-70e5b1074092.herokuapp.com";
    public string apiKey = ""; // Add your API key if required
    
    [Header("Hand Tracking Integration")]
    public HandTracking handTracking;
    public UDPReceive udpReceive;
    
    [Header("UI Elements")]
    public UnityEngine.UI.Text statusText;
    public UnityEngine.UI.Text recognizedSignText;
    public UnityEngine.UI.Button startRecognitionButton;
    public UnityEngine.UI.Button getSignsButton;
    
    private bool isRecognizing = false;
    private string currentSessionId = "";
    private List<SignBridgeSign> availableSigns = new List<SignBridgeSign>();
    
    void Start()
    {
        // Initialize UI
        if (statusText != null)
            statusText.text = "Ready";
            
        if (recognizedSignText != null)
            recognizedSignText.text = "No sign recognized";
            
        // Setup button listeners
        if (startRecognitionButton != null)
            startRecognitionButton.onClick.AddListener(ToggleRecognition);
            
        if (getSignsButton != null)
            getSignsButton.onClick.AddListener(GetAvailableSigns);
        
        // Start learning session
        StartCoroutine(StartLearningSession());
    }
    
    void Update()
    {
        // Check for hand tracking data
        if (handTracking != null && udpReceive != null)
        {
            if (!string.IsNullOrEmpty(udpReceive.data))
            {
                // Process hand tracking data for SignBridge
                ProcessHandTrackingData();
            }
        }
    }
    
    public void ToggleRecognition()
    {
        isRecognizing = !isRecognizing;
        UpdateStatus();
        
        if (isRecognizing)
        {
            Debug.Log("🎯 Started SignBridge recognition");
        }
        else
        {
            Debug.Log("⏹️ Stopped SignBridge recognition");
        }
    }
    
    private void UpdateStatus()
    {
        if (statusText != null)
        {
            statusText.text = isRecognizing ? "Recognizing..." : "Ready";
        }
    }
    
    private void ProcessHandTrackingData()
    {
        if (!isRecognizing) return;
        
        try
        {
            // Parse hand tracking data
            string data = udpReceive.data;
            data = data.Remove(0, 1);
            data = data.Remove(data.Length - 1, 1);
            string[] points = data.Split(',');
            
            if (points.Length >= 63) // 21 landmarks * 3 coordinates
            {
                // Convert to SignBridge format
                StartCoroutine(SendHandDataToSignBridge(points));
            }
        }
        catch (Exception e)
        {
            Debug.LogError($"Error processing hand data: {e.Message}");
        }
    }
    
    private IEnumerator SendHandDataToSignBridge(string[] handPoints)
    {
        // Create hand data structure for SignBridge
        var handData = new
        {
            landmarks = new List<object>(),
            session_id = currentSessionId,
            timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()
        };
        
        // Convert points to landmark format
        for (int i = 0; i < 21; i++)
        {
            if (i * 3 + 2 < handPoints.Length)
            {
                var landmark = new
                {
                    x = float.Parse(handPoints[i * 3]),
                    y = float.Parse(handPoints[i * 3 + 1]),
                    z = float.Parse(handPoints[i * 3 + 2])
                };
                handData.landmarks.Add(landmark);
            }
        }
        
        // Send to SignBridge
        string jsonData = JsonUtility.ToJson(handData);
        yield return StartCoroutine(SendToSignBridge("/api/recognize/advanced", jsonData));
    }
    
    private IEnumerator StartLearningSession()
    {
        string url = $"{signBridgeURL}/api/learning/start-session";
        
        using (UnityWebRequest request = UnityWebRequest.Post(url, ""))
        {
            request.SetRequestHeader("Content-Type", "application/json");
            
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                var response = JsonUtility.FromJson<SignBridgeResponse>(request.downloadHandler.text);
                if (response.success)
                {
                    currentSessionId = response.message; // Assuming session ID is in message
                    Debug.Log($"✅ Learning session started: {currentSessionId}");
                }
            }
            else
            {
                Debug.LogError($"❌ Failed to start session: {request.error}");
            }
        }
    }
    
    public void GetAvailableSigns()
    {
        StartCoroutine(GetSignsCoroutine());
    }
    
    private IEnumerator GetSignsCoroutine()
    {
        string url = $"{signBridgeURL}/api/signs";
        
        using (UnityWebRequest request = UnityWebRequest.Get(url))
        {
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                var response = JsonUtility.FromJson<SignBridgeResponse>(request.downloadHandler.text);
                if (response.success && response.signs != null)
                {
                    availableSigns.Clear();
                    availableSigns.AddRange(response.signs);
                    Debug.Log($"📋 Loaded {availableSigns.Count} available signs");
                    
                    // Display first few signs
                    string signsText = "Available Signs:\n";
                    for (int i = 0; i < Mathf.Min(5, availableSigns.Count); i++)
                    {
                        signsText += $"• {availableSigns[i].name}\n";
                    }
                    
                    if (recognizedSignText != null)
                        recognizedSignText.text = signsText;
                }
            }
            else
            {
                Debug.LogError($"❌ Failed to get signs: {request.error}");
            }
        }
    }
    
    private IEnumerator SendToSignBridge(string endpoint, string jsonData)
    {
        string url = $"{signBridgeURL}{endpoint}";
        
        using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
        {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                var response = JsonUtility.FromJson<SignBridgeResponse>(request.downloadHandler.text);
                if (response.success && response.recognized_sign != null)
                {
                    OnSignRecognized(response.recognized_sign);
                }
            }
            else
            {
                Debug.LogError($"❌ SignBridge request failed: {request.error}");
            }
        }
    }
    
    private void OnSignRecognized(SignBridgeSign sign)
    {
        Debug.Log($"🎯 Sign Recognized: {sign.name} (Confidence: {sign.confidence:F2})");
        
        if (recognizedSignText != null)
        {
            recognizedSignText.text = $"Recognized: {sign.name}\nConfidence: {sign.confidence:F2}";
        }
        
        // Trigger avatar animation
        StartCoroutine(CreateAvatarFromSign(sign));
    }
    
    private IEnumerator CreateAvatarFromSign(SignBridgeSign sign)
    {
        var avatarRequest = new AvatarRequest
        {
            text = sign.name,
            gesture_type = sign.category,
            confidence = sign.confidence
        };
        
        string jsonData = JsonUtility.ToJson(avatarRequest);
        yield return StartCoroutine(SendToSignBridge("/api/avatar/process-text", jsonData));
    }
    
    // Public methods for external control
    public void SetRecognitionState(bool state)
    {
        isRecognizing = state;
        UpdateStatus();
    }
    
    public List<SignBridgeSign> GetAvailableSignsList()
    {
        return availableSigns;
    }
    
    public string GetCurrentSessionId()
    {
        return currentSessionId;
    }
}
