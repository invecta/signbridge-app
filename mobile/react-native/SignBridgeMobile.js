# SignBridge Mobile App - React Native
# Cross-platform mobile application for iOS and Android

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
  Alert,
  Dimensions,
  StatusBar,
  SafeAreaView,
  Modal,
  FlatList
} from 'react-native';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import { request, PERMISSIONS, RESULTS } from 'react-native-permissions';

const { width, height } = Dimensions.get('window');

const SignBridgeMobile = () => {
  // State management
  const [hasPermission, setHasPermission] = useState(false);
  const [isActive, setIsActive] = useState(false);
  const [currentSign, setCurrentSign] = useState(null);
  const [confidence, setConfidence] = useState(0);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [showSignsModal, setShowSignsModal] = useState(false);
  const [availableSigns, setAvailableSigns] = useState([]);
  const [aiEnabled, setAiEnabled] = useState(false);

  // Camera setup
  const devices = useCameraDevices();
  const device = devices.back;
  const cameraRef = useRef(null);

  // Available signs data
  const signsData = [
    { name: 'hello', description: 'Wave hand in greeting motion', confidence: 0.9 },
    { name: 'yes', description: 'Make fist and nod up and down', confidence: 0.9 },
    { name: 'no', description: 'Index finger shakes side to side', confidence: 0.85 },
    { name: 'thank_you', description: 'Flat hand touches chin and moves forward', confidence: 0.85 },
    { name: 'please', description: 'Flat hand circles on chest', confidence: 0.85 },
    { name: 'sorry', description: 'Closed fist circles on chest', confidence: 0.8 },
    { name: 'help', description: 'Closed fist taps on open palm', confidence: 0.85 },
    { name: 'water', description: 'W handshape taps chin', confidence: 0.8 },
    { name: 'food', description: 'Fingertips touch mouth', confidence: 0.85 },
    { name: 'bathroom', description: 'T handshape shakes', confidence: 0.8 },
    { name: 'love', description: 'Hands form heart shape', confidence: 0.9 },
    { name: 'happy', description: 'Both hands move up with smile', confidence: 0.8 },
    { name: 'sad', description: 'Hands move down with frown', confidence: 0.8 },
    { name: 'angry', description: 'Fist shakes', confidence: 0.85 },
    { name: 'surprised', description: 'Hands move up quickly', confidence: 0.8 },
    { name: 'tired', description: 'Hands on face, eyes closed', confidence: 0.8 },
    { name: 'hungry', description: 'Hand moves to mouth', confidence: 0.85 },
    { name: 'thirsty', description: 'Hand moves to throat', confidence: 0.85 },
    { name: 'emergency', description: 'Hand waves frantically', confidence: 0.9 },
    { name: 'stop', description: 'Hand forms stop sign', confidence: 0.95 }
  ];

  useEffect(() => {
    requestCameraPermission();
    setAvailableSigns(signsData);
  }, []);

  const requestCameraPermission = async () => {
    try {
      const result = await request(PERMISSIONS.CAMERA);
      setHasPermission(result === RESULTS.GRANTED);
    } catch (error) {
      console.error('Permission error:', error);
      Alert.alert('Error', 'Could not request camera permission');
    }
  };

  const capturePhoto = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePhoto({
          qualityPrioritization: 'speed',
          flash: 'off',
        });
        
        // Simulate sign recognition (in real app, this would call AI model)
        const randomSign = signsData[Math.floor(Math.random() * signsData.length)];
        setCurrentSign(randomSign);
        setConfidence(randomSign.confidence);
        
        // Add to conversation history
        const newEntry = {
          id: Date.now(),
          timestamp: new Date().toLocaleTimeString(),
          sign: randomSign.name,
          description: randomSign.description,
          confidence: randomSign.confidence
        };
        
        setConversationHistory(prev => [...prev, newEntry]);
        
        Alert.alert(
          'Sign Recognized!',
          ${randomSign.name.toUpperCase()}: ,
          [{ text: 'OK' }]
        );
        
      } catch (error) {
        console.error('Capture error:', error);
        Alert.alert('Error', 'Failed to capture photo');
      }
    }
  };

  const startCamera = () => {
    setIsActive(true);
  };

  const stopCamera = () => {
    setIsActive(false);
  };

  const clearHistory = () => {
    Alert.alert(
      'Clear History',
      'Are you sure you want to clear the conversation history?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Clear', style: 'destructive', onPress: () => setConversationHistory([]) }
      ]
    );
  };

  const renderSignItem = ({ item }) => (
    <View style={styles.signItem}>
      <Text style={styles.signName}>{item.name.toUpperCase()}</Text>
      <Text style={styles.signDescription}>{item.description}</Text>
      <Text style={styles.signConfidence}>Confidence: {(item.confidence * 100).toFixed(1)}%</Text>
    </View>
  );

  if (!hasPermission) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.permissionContainer}>
          <Text style={styles.permissionText}>Camera permission required</Text>
          <TouchableOpacity style={styles.permissionButton} onPress={requestCameraPermission}>
            <Text style={styles.permissionButtonText}>Grant Permission</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  if (!device) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.permissionContainer}>
          <Text style={styles.permissionText}>No camera device found</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#667eea" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>ðŸ¤Ÿ SignBridge</Text>
        <Text style={styles.headerSubtitle}>AI-Enhanced Mobile Communication</Text>
      </View>

      {/* Camera Section */}
      <View style={styles.cameraContainer}>
        {isActive ? (
          <Camera
            ref={cameraRef}
            style={styles.camera}
            device={device}
            isActive={isActive}
            photo={true}
          />
        ) : (
          <View style={styles.cameraPlaceholder}>
            <Text style={styles.cameraPlaceholderText}>ðŸ“¹ Camera Ready</Text>
            <Text style={styles.cameraPlaceholderSubtext}>Tap "Start Camera" to begin</Text>
          </View>
        )}
        
        {/* Detection Overlay */}
        {isActive && (
          <View style={styles.detectionOverlay}>
            <View style={styles.detectionBox} />
            <Text style={styles.detectionText}>AI Detection Area</Text>
          </View>
        )}
      </View>

      {/* Controls */}
      <View style={styles.controls}>
        <TouchableOpacity 
          style={[styles.button, styles.startButton]} 
          onPress={isActive ? stopCamera : startCamera}
        >
          <Text style={styles.buttonText}>
            {isActive ? 'Stop Camera' : 'Start Camera'}
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.button, styles.captureButton]} 
          onPress={capturePhoto}
          disabled={!isActive}
        >
          <Text style={styles.buttonText}>Capture & Recognize</Text>
        </TouchableOpacity>
      </View>

      {/* Current Result */}
      {currentSign && (
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>Last Recognition:</Text>
          <Text style={styles.resultSign}>{currentSign.name.toUpperCase()}</Text>
          <Text style={styles.resultDescription}>{currentSign.description}</Text>
          <Text style={styles.resultConfidence}>
            Confidence: {(confidence * 100).toFixed(1)}%
          </Text>
        </View>
      )}

      {/* Statistics */}
      <View style={styles.statsContainer}>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{availableSigns.length}</Text>
          <Text style={styles.statLabel}>Available Signs</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{aiEnabled ? 'AI' : 'Enhanced'}</Text>
          <Text style={styles.statLabel}>Recognition Mode</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{conversationHistory.length}</Text>
          <Text style={styles.statLabel}>Conversations</Text>
        </View>
      </View>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <TouchableOpacity 
          style={styles.actionButton} 
          onPress={() => setShowSignsModal(true)}
        >
          <Text style={styles.actionButtonText}>View All Signs</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.actionButton} onPress={clearHistory}>
          <Text style={styles.actionButtonText}>Clear History</Text>
        </TouchableOpacity>
      </View>

      {/* Signs Modal */}
      <Modal
        visible={showSignsModal}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <SafeAreaView style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Available Signs</Text>
            <TouchableOpacity onPress={() => setShowSignsModal(false)}>
              <Text style={styles.modalCloseButton}>Close</Text>
            </TouchableOpacity>
          </View>
          
          <FlatList
            data={availableSigns}
            renderItem={renderSignItem}
            keyExtractor={(item) => item.name}
            style={styles.signsList}
          />
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: '#667eea',
    paddingVertical: 20,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 14,
    color: 'white',
    opacity: 0.9,
  },
  cameraContainer: {
    height: height * 0.4,
    margin: 20,
    borderRadius: 15,
    overflow: 'hidden',
    backgroundColor: '#e9ecef',
  },
  camera: {
    flex: 1,
  },
  cameraPlaceholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#e9ecef',
  },
  cameraPlaceholderText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#667eea',
    marginBottom: 5,
  },
  cameraPlaceholderSubtext: {
    fontSize: 14,
    color: '#666',
  },
  detectionOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  detectionBox: {
    width: width * 0.6,
    height: height * 0.3,
    borderWidth: 3,
    borderColor: '#28a745',
    borderRadius: 10,
  },
  detectionText: {
    position: 'absolute',
    top: 10,
    left: 10,
    color: '#28a745',
    fontWeight: 'bold',
    fontSize: 12,
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  button: {
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 25,
    minWidth: 120,
    alignItems: 'center',
  },
  startButton: {
    backgroundColor: '#667eea',
  },
  captureButton: {
    backgroundColor: '#28a745',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 14,
  },
  resultContainer: {
    backgroundColor: 'white',
    marginHorizontal: 20,
    padding: 15,
    borderRadius: 10,
    marginBottom: 20,
    borderLeftWidth: 5,
    borderLeftColor: '#667eea',
  },
  resultTitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  resultSign: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#667eea',
    marginBottom: 5,
  },
  resultDescription: {
    fontSize: 14,
    color: '#333',
    marginBottom: 5,
  },
  resultConfidence: {
    fontSize: 12,
    color: '#28a745',
    fontWeight: 'bold',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginHorizontal: 20,
    marginBottom: 20,
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#667eea',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  actionButton: {
    backgroundColor: '#f8f9fa',
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#667eea',
  },
  actionButtonText: {
    color: '#667eea',
    fontWeight: 'bold',
    fontSize: 12,
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  permissionText: {
    fontSize: 18,
    color: '#666',
    marginBottom: 20,
    textAlign: 'center',
  },
  permissionButton: {
    backgroundColor: '#667eea',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 25,
  },
  permissionButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: 'white',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  modalCloseButton: {
    fontSize: 16,
    color: '#667eea',
    fontWeight: 'bold',
  },
  signsList: {
    flex: 1,
    padding: 20,
  },
  signItem: {
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#667eea',
  },
  signName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#667eea',
    marginBottom: 5,
  },
  signDescription: {
    fontSize: 14,
    color: '#333',
    marginBottom: 5,
  },
  signConfidence: {
    fontSize: 12,
    color: '#28a745',
    fontWeight: 'bold',
  },
});

export default SignBridgeMobile;
