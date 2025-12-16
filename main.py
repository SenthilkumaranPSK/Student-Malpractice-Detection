"""
Student Malpractice Detection System - Flask Application (Advanced AI Version)
Integrates YOLO for objects, and MediaPipe for Gaze, Pose, and Hand Gestures.
"""
import os
import cv2
import json
import logging
import numpy as np
import math
from datetime import datetime, timedelta
from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
import mediapipe as mp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

# --- MediaPipe Initializations ---
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

class MalpracticeDetector:
    def __init__(self, yolo_model_path='yolov8n.pt'):
        self.camera = None
        self.is_monitoring = False
        self.detection_log = []
        self.alert_trackers = {} # Unified tracker for time-based alerts
        self.load_configurations()
        
        logger.info("Initializing AI Models...")
        
        # Auto-download YOLOv8 model if not present
        if not os.path.exists(yolo_model_path):
            logger.info(f"YOLOv8 model not found. Downloading {yolo_model_path}...")
            # YOLO will automatically download the model on first use
        
        self.object_model = YOLO(yolo_model_path)
        self.pose_detector = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.hand_detector = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5)
        logger.info("AI Models Initialized.")

    def load_configurations(self):
        try:
            with open("models/detection_parameters.json", 'r') as f:
                self.params = json.load(f)
            logger.info("Detection parameters loaded.")
        except Exception as e:
            logger.error(f"Failed to load configurations: {e}. Using defaults.")
            self.params = {"object_detection": {"enabled": True, "confidence_min": 0.55}, "gaze_detection": {"enabled": True, "threshold_seconds": 3.0, "sensitivity": 0.8}, "pose_detection": {"enabled": True, "hand_near_head_threshold_seconds": 2.0}, "gesture_detection": {"enabled": True}, "multiple_people_detection": {"enabled": True, "max_people": 1}}

    # --- Core AI Detection Modules ---
    def detect_objects(self, frame):
        detections = []
        if not self.params['object_detection']['enabled']: return detections
        results = self.object_model(frame, verbose=False, classes=[0, 67, 73, 76]) # person, cell phone, book, clock
        for res in results:
            for box in res.boxes:
                conf = float(box.conf[0])
                if conf >= self.params['object_detection']['confidence_min']:
                    x1, y1, x2, y2 = [int(c) for c in box.xyxy[0]]
                    class_name = self.object_model.names[int(box.cls[0])]
                    detections.append({'type': 'object', 'class': class_name, 'bbox': [x1, y1, x2-x1, y2-y1], 'confidence': conf})
        return detections

    def analyze_pose_and_gestures(self, frame, persons):
        detections = []
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process each person
        for i, person in enumerate(persons):
            person_id = f"person_{i}"
            px, py, pw, ph = person['bbox']
            
            # 1. Gaze Detection
            if self.params['gaze_detection']['enabled']:
                gaze_ratio = self._get_gaze_ratio(rgb_frame[py:py+ph, px:px+pw])
                if gaze_ratio and abs(gaze_ratio) > self.params['gaze_detection']['sensitivity']:
                    detections.append({'type': 'behavior', 'class': 'Suspicious Gaze', 'person_id': person_id})

            # 2. Pose Detection
            pose_results = self.pose_detector.process(rgb_frame)
            if self.params['pose_detection']['enabled'] and pose_results.pose_landmarks:
                landmarks = pose_results.pose_landmarks.landmark
                # Check for hand near head
                left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                nose = landmarks[mp_pose.PoseLandmark.NOSE]
                if (left_hand.visibility > 0.5 and left_hand.y < nose.y) or \
                   (right_hand.visibility > 0.5 and right_hand.y < nose.y):
                    detections.append({'type': 'behavior', 'class': 'Hand Near Head', 'person_id': person_id})

            # 3. Hand Gesture Detection
            hand_results = self.hand_detector.process(rgb_frame)
            if self.params['gesture_detection']['enabled'] and hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    gesture = self._classify_gesture(hand_landmarks.landmark)
                    if gesture != "Unknown":
                        detections.append({'type': 'behavior', 'class': gesture, 'person_id': person_id})
        return detections

    # --- Helper methods for analysis ---
    def _get_gaze_ratio(self, person_roi):
        if person_roi.size == 0: return None
        h, w, _ = person_roi.shape
        results = self.face_mesh.process(person_roi)
        if results.multi_face_landmarks:
            face = results.multi_face_landmarks[0].landmark
            nose_x = face[1].x * w
            reye_x = face[33].x * w
            leye_x = face[263].x * w
            eye_center_x = (reye_x + leye_x) / 2
            return (eye_center_x - nose_x) / (w * 0.1)
        return None

    def _classify_gesture(self, landmarks):
        # Simple rule-based gesture classifier
        thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
        # Peace sign
        if index_tip.y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and \
           middle_tip.y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and \
           ring_tip.y > landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y and \
           pinky_tip.y > landmarks[mp_hands.HandLandmark.PINKY_PIP].y:
            return "Peace Sign Gesture"
        return "Unknown"

    def process_alerts(self, detections):
        """Generates descriptive alerts based on detections."""
        now = datetime.now()
        persons = [d for d in detections if d.get('class') == 'person']
        
        active_alerts = set()
        for det in detections:
            alert_key = det['class']
            description = ""
            
            if det['type'] == 'object' and det['class'] != 'person':
                description = f"Prohibited Object Detected: A '{det['class']}' is visible near the student."
                active_alerts.add(alert_key)
            
            elif det['type'] == 'behavior':
                if det['class'] == 'Suspicious Gaze':
                    if self.check_duration(alert_key, self.params['gaze_detection']['threshold_seconds']):
                        description = "Suspicious Gaze Detected: The student is looking away from their desk for an extended period."
                        active_alerts.add(alert_key)
                elif det['class'] == 'Hand Near Head':
                    if self.check_duration(alert_key, self.params['pose_detection']['hand_near_head_threshold_seconds']):
                        description = "Suspicious Pose Detected: The student has their hand raised near their head, which could be used to obscure actions."
                        active_alerts.add(alert_key)
                elif "Gesture" in det['class']:
                    description = f"Suspicious Action Detected: A '{det['class']}' was made, which is unusual for an exam environment."
                    active_alerts.add(alert_key)
        
        # Rule: Multiple People
        if self.params['multiple_people_detection']['enabled'] and len(persons) > self.params['multiple_people_detection']['max_people']:
            description = "Potential Collusion Detected: More than one person is visible in the frame."
            active_alerts.add("Multiple People")

        # Log new alerts
        for key in active_alerts:
            if not self.alert_trackers.get(key, {}).get('logged', False):
                self.detection_log.append({'timestamp': now.isoformat(), 'description': description})
                self.alert_trackers[key] = {'start_time': now, 'logged': True}

        # Reset trackers that are no longer active
        for key in list(self.alert_trackers.keys()):
            if key not in active_alerts:
                del self.alert_trackers[key]

        self.detection_log = self.detection_log[-100:]

    def check_duration(self, key, threshold):
        """Helper to check if a behavior has persisted for a duration."""
        now = datetime.now()
        if key not in self.alert_trackers:
            self.alert_trackers[key] = {'start_time': now, 'logged': False}
        
        if now - self.alert_trackers[key]['start_time'] > timedelta(seconds=threshold):
            return True
        return False
    
    def generate_frames(self):
        camera_index = 0
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            # (Camera error handling code as before)
            return

        while self.is_monitoring:
            success, frame = self.camera.read()
            if not success: break
            
            # --- Main AI Pipeline ---
            object_detections = self.detect_objects(frame)
            persons = [d for d in object_detections if d['class'] == 'person']
            behavior_detections = self.analyze_pose_and_gestures(frame, persons)
            all_detections = object_detections + behavior_detections
            
            self.process_alerts(all_detections)
            
            # Draw detections
            for det in all_detections:
                if 'bbox' in det:
                    x, y, w, h = det['bbox']
                    color = (0, 255, 255) if det['class'] != 'person' else (0, 255, 0)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, det['class'], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        self.camera.release()

# --- Flask Routes and App Initialization ---
detector = MalpracticeDetector()

@app.route('/')
def landing():
    """Landing page with features and pricing"""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Monitoring dashboard"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(detector.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_monitoring')
def start_monitoring():
    """Start the monitoring session"""
    if not detector.is_monitoring:
        detector.is_monitoring = True
        detector.detection_log.clear()
        detector.alert_trackers.clear()
    return jsonify({'status': 'started'})

@app.route('/stop_monitoring')
def stop_monitoring():
    """Stop the monitoring session"""
    if detector.is_monitoring: 
        detector.is_monitoring = False
    return jsonify({'status': 'stopped'})

@app.route('/get_alerts')
def get_alerts():
    """Get all alerts for the current session"""
    formatted_alerts = []
    for alert in reversed(detector.detection_log):
        dt = datetime.fromisoformat(alert['timestamp'])
        formatted_alerts.append({
            'time': dt.strftime('%b %d, %Y, %I:%M:%S %p'),
            'description': alert['description']
        })
    return jsonify({'alerts': formatted_alerts})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)