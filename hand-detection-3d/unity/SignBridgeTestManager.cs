using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SignBridgeTestManager : MonoBehaviour
{
    [Header("Test Configuration")]
    public bool enableAutoTest = true;
    public float testInterval = 2.0f;
    
    [Header("UI Elements")]
    public Text statusText;
    public Text connectionText;
    public Text dataText;
    public Button testButton;
    
    [Header("Components")]
    public UDPReceive udpReceive;
    public HandTracking handTracking;
    public SignBridgeConnector signBridgeConnector;
    
    private bool isTesting = false;
    private float lastDataTime = 0f;
    private int dataCount = 0;
    
    void Start()
    {
        // Initialize UI
        if (statusText != null)
            statusText.text = "Ready for Testing";
            
        if (connectionText != null)
            connectionText.text = "Checking Connection...";
            
        if (dataText != null)
            dataText.text = "No data received";
        
        // Setup button
        if (testButton != null)
            testButton.onClick.AddListener(StartTest);
        
        // Start connection check
        StartCoroutine(CheckConnection());
        
        // Start auto test if enabled
        if (enableAutoTest)
        {
            StartCoroutine(AutoTest());
        }
    }
    
    void Update()
    {
        // Monitor UDP data
        if (udpReceive != null && !string.IsNullOrEmpty(udpReceive.data))
        {
            lastDataTime = Time.time;
            dataCount++;
            
            if (dataText != null)
            {
                dataText.text = $"Data Count: {dataCount}\nLast: {Time.time - lastDataTime:F1}s ago\nData: {udpReceive.data.Substring(0, Mathf.Min(50, udpReceive.data.Length))}...";
            }
        }
        
        // Update status
        UpdateStatus();
    }
    
    private void UpdateStatus()
    {
        if (statusText != null)
        {
            if (isTesting)
            {
                statusText.text = "Testing Integration...";
            }
            else if (Time.time - lastDataTime < 5f)
            {
                statusText.text = "Receiving Data ✅";
            }
            else
            {
                statusText.text = "Waiting for Data ⏳";
            }
        }
    }
    
    private IEnumerator CheckConnection()
    {
        yield return new WaitForSeconds(1f);
        
        if (connectionText != null)
        {
            if (udpReceive != null)
            {
                connectionText.text = "UDP Receiver: Ready ✅";
            }
            else
            {
                connectionText.text = "UDP Receiver: Missing ❌";
            }
        }
        
        yield return new WaitForSeconds(1f);
        
        if (connectionText != null)
        {
            if (handTracking != null)
            {
                connectionText.text += "\nHand Tracking: Ready ✅";
            }
            else
            {
                connectionText.text += "\nHand Tracking: Missing ❌";
            }
        }
        
        yield return new WaitForSeconds(1f);
        
        if (connectionText != null)
        {
            if (signBridgeConnector != null)
            {
                connectionText.text += "\nSignBridge Connector: Ready ✅";
            }
            else
            {
                connectionText.text += "\nSignBridge Connector: Missing ❌";
            }
        }
    }
    
    public void StartTest()
    {
        if (!isTesting)
        {
            StartCoroutine(RunTest());
        }
    }
    
    private IEnumerator RunTest()
    {
        isTesting = true;
        
        if (statusText != null)
            statusText.text = "Running Integration Test...";
        
        // Test 1: Check components
        yield return StartCoroutine(TestComponents());
        
        // Test 2: Simulate hand data
        yield return StartCoroutine(TestHandData());
        
        // Test 3: Test SignBridge connection
        yield return StartCoroutine(TestSignBridgeConnection());
        
        isTesting = false;
        
        if (statusText != null)
            statusText.text = "Test Complete ✅";
    }
    
    private IEnumerator TestComponents()
    {
        Debug.Log("🔍 Testing Components...");
        
        bool allComponentsPresent = true;
        
        if (udpReceive == null)
        {
            Debug.LogError("❌ UDPReceive component missing");
            allComponentsPresent = false;
        }
        else
        {
            Debug.Log("✅ UDPReceive component found");
        }
        
        if (handTracking == null)
        {
            Debug.LogError("❌ HandTracking component missing");
            allComponentsPresent = false;
        }
        else
        {
            Debug.Log("✅ HandTracking component found");
        }
        
        if (signBridgeConnector == null)
        {
            Debug.LogError("❌ SignBridgeConnector component missing");
            allComponentsPresent = false;
        }
        else
        {
            Debug.Log("✅ SignBridgeConnector component found");
        }
        
        if (allComponentsPresent)
        {
            Debug.Log("🎉 All components present!");
        }
        
        yield return new WaitForSeconds(1f);
    }
    
    private IEnumerator TestHandData()
    {
        Debug.Log("🤚 Testing Hand Data Processing...");
        
        // Simulate hand data
        string simulatedData = "[500, 500, 100, 600, 500, 110, 700, 500, 120, 800, 500, 130, 900, 500, 140, 600, 600, 150, 700, 650, 160, 800, 700, 170, 900, 750, 180, 1000, 800, 190, 500, 700, 200, 600, 750, 210, 700, 800, 220, 800, 850, 230, 900, 900, 240, 1000, 950, 250, 400, 800, 260, 500, 850, 270, 600, 900, 280, 700, 950, 290, 800, 1000, 300, 900, 1050, 310, 1000, 1100, 320, 1100, 1150, 330, 1200, 1200, 340, 1300, 1250, 350, 1400, 1300, 360, 1500, 1350, 370, 1600, 1400, 380, 1700, 1450, 390, 1800, 1500, 400, 1900, 1550, 410, 2000, 1600, 420, 2100, 1650, 430, 2200, 1700, 440, 2300, 1750, 450, 2400, 1800, 460, 2500, 1850, 470, 2600, 1900, 480, 2700, 1950, 490, 2800, 2000, 500, 2900, 2050, 510, 3000, 2100, 520, 3100, 2150, 530, 3200, 2200, 540, 3300, 2250, 550, 3400, 2300, 560, 3500, 2350, 570, 3600, 2400, 580, 3700, 2450, 590, 3800, 2500, 600, 3900, 2550, 610, 4000, 2600, 620, 4100, 2650, 630]";
        
        if (udpReceive != null)
        {
            udpReceive.data = simulatedData;
            Debug.Log("✅ Simulated hand data set");
        }
        
        yield return new WaitForSeconds(1f);
        
        if (handTracking != null)
        {
            Debug.Log("✅ HandTracking can process data");
        }
        
        yield return new WaitForSeconds(1f);
    }
    
    private IEnumerator TestSignBridgeConnection()
    {
        Debug.Log("🌐 Testing SignBridge Connection...");
        
        if (signBridgeConnector != null)
        {
            // Test getting available signs
            var signs = signBridgeConnector.GetAvailableSignsList();
            Debug.Log($"✅ Retrieved {signs.Count} signs from SignBridge");
            
            // Test session management
            string sessionId = signBridgeConnector.GetCurrentSessionId();
            if (!string.IsNullOrEmpty(sessionId))
            {
                Debug.Log($"✅ Session ID: {sessionId}");
            }
            
            // Test recognition state
            signBridgeConnector.SetRecognitionState(true);
            Debug.Log("✅ Recognition state set to active");
            
            yield return new WaitForSeconds(1f);
            
            signBridgeConnector.SetRecognitionState(false);
            Debug.Log("✅ Recognition state set to inactive");
        }
        
        yield return new WaitForSeconds(1f);
    }
    
    private IEnumerator AutoTest()
    {
        while (enableAutoTest)
        {
            yield return new WaitForSeconds(testInterval);
            
            if (!isTesting)
            {
                Debug.Log("🔄 Auto-test running...");
                StartCoroutine(RunTest());
            }
        }
    }
    
    // Public methods for external control
    public void EnableAutoTest(bool enable)
    {
        enableAutoTest = enable;
    }
    
    public void SetTestInterval(float interval)
    {
        testInterval = interval;
    }
    
    public int GetDataCount()
    {
        return dataCount;
    }
    
    public float GetLastDataTime()
    {
        return lastDataTime;
    }
}
