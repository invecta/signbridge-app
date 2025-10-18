#!/usr/bin/env python3
"""
Hand Detection 3D + SignBridge - Version Simplifiée
Cette version fonctionne sans MediaPipe pour éviter les problèmes d'installation
"""

import cv2
import requests
import json
import socket
import time
import random
import threading
from typing import Dict, List, Optional

class SimpleHandTracker:
    def __init__(self, udp_ip="127.0.0.1", udp_port=5052):
        # Configuration UDP
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Configuration caméra
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # État de la reconnaissance
        self.is_recording = False
        self.recognition_results = []
        self.current_session_id = f"session_{int(time.time())}"
        
        # Signes simulés
        self.simulated_signs = [
            {"name": "Bonjour", "category": "salutation", "confidence": 0.92},
            {"name": "Merci", "category": "politesse", "confidence": 0.88},
            {"name": "Oui", "category": "réponse", "confidence": 0.95},
            {"name": "Non", "category": "réponse", "confidence": 0.90},
            {"name": "Aide", "category": "demande", "confidence": 0.85},
            {"name": "Au revoir", "category": "salutation", "confidence": 0.87},
            {"name": "S'il vous plaît", "category": "politesse", "confidence": 0.89}
        ]
        
    def generate_simulated_landmarks(self):
        """Génère des points de repère simulés pour les mains"""
        landmarks = []
        for i in range(21):  # 21 points MediaPipe
            x = 0.3 + random.random() * 0.4  # Position aléatoire
            y = 0.3 + random.random() * 0.4
            z = 0.1 + random.random() * 0.2
            landmarks.extend([int(x * 1000), int(y * 1000), int(z * 1000)])
        return landmarks
    
    def send_hand_data_to_unity(self, landmarks):
        """Envoie les données de main à Unity via UDP"""
        if landmarks is None:
            return
            
        data_string = str(landmarks).replace('[', '').replace(']', '')
        
        try:
            self.sock.sendto(data_string.encode(), (self.udp_ip, self.udp_port))
            print(f"📤 Données envoyées à Unity: {len(landmarks)} coordonnées")
        except Exception as e:
            print(f"❌ Erreur communication Unity: {e}")
    
    def simulate_recognition(self):
        """Simule la reconnaissance de signes"""
        if not self.is_recording:
            return None
            
        # Simuler un délai de traitement
        time.sleep(0.1)
        
        # Choisir un signe aléatoire
        random_sign = random.choice(self.simulated_signs)
        self.recognition_results.append(random_sign)
        
        print(f"🎯 Signe reconnu: {random_sign['name']} (Confiance: {random_sign['confidence']:.2f})")
        return random_sign
    
    def test_signbridge_api(self):
        """Teste la connexion à l'API SignBridge"""
        try:
            print("🔍 Test de l'API SignBridge...")
            response = requests.get("https://signbridgeproduction-70e5b1074092.herokuapp.com/api/signs", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API SignBridge accessible - {data.get('total', 0)} signes disponibles")
                return True
            else:
                print(f"❌ API SignBridge erreur: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur connexion API: {e}")
            return False
    
    def run_simulation(self):
        """Lance la simulation de détection des mains"""
        print("🚀 Démarrage de la simulation Hand Detection 3D + SignBridge")
        print("Contrôles:")
        print("  'r' - Démarrer/Arrêter reconnaissance")
        print("  's' - Tester SignBridge")
        print("  'd' - Afficher données")
        print("  'q' - Quitter")
        
        # Tester l'API au démarrage
        self.test_signbridge_api()
        
        frame_count = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Impossible de lire la caméra")
                break
                
            # Retourner l'image horizontalement
            frame = cv2.flip(frame, 1)
            
            # Simuler la détection des mains
            if frame_count % 30 == 0:  # Toutes les 30 frames
                landmarks = self.generate_simulated_landmarks()
                
                # Envoyer à Unity
                self.send_hand_data_to_unity(landmarks)
                
                # Simuler la reconnaissance
                recognition_result = self.simulate_recognition()
                
                if recognition_result:
                    # Afficher le résultat sur l'image
                    cv2.putText(frame, f"Signe: {recognition_result['name']}", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Confiance: {recognition_result['confidence']:.2f}", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Afficher le statut
            status = "RECONNAISSANCE" if self.is_recording else "EN ATTENTE"
            cv2.putText(frame, f"Statut: {status}", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Afficher l'image
            cv2.imshow('Hand Detection 3D + SignBridge', frame)
            
            # Gérer les touches
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.is_recording = not self.is_recording
                print(f"🔄 Reconnaissance: {'ACTIVE' if self.is_recording else 'ARRÊTÉE'}")
            elif key == ord('s'):
                self.test_signbridge_api()
            elif key == ord('d'):
                landmarks = self.generate_simulated_landmarks()
                print(f"📊 Données simulées: {landmarks[:9]}...")
            
            frame_count += 1
        
        # Nettoyage
        self.cap.release()
        cv2.destroyAllWindows()
        self.sock.close()
        print("✅ Simulation terminée")

def main():
    print("🤚 Hand Detection 3D + SignBridge - Version Simplifiée")
    print("=" * 60)
    
    try:
        tracker = SimpleHandTracker()
        tracker.run_simulation()
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        print("👋 Au revoir!")

if __name__ == "__main__":
    main()
