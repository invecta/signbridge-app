import cv2
import speech_recognition as sr
import pyttsx3

print('SignBridge - Computer Vision Communication Assistant')
print('Initializing camera...')

cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('Camera working!')
    cap.release()
else:
    print('Camera not accessible')

print('Testing speech recognition...')
try:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print('Speech recognition ready!')
except Exception as e:
    print(f'Speech recognition error: {e}')

print('Testing text-to-speech...')
try:
    tts_engine = pyttsx3.init()
    tts_engine.say('SignBridge is working!')
    tts_engine.runAndWait()
    print('Text-to-speech working!')
except Exception as e:
    print(f'Text-to-speech error: {e}')

print('All tests completed!')
