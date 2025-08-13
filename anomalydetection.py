import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import requests

# Setup Pose detection
mp_pose = mp.solutions.pose

# Constants
FALL_ANGLE_THRESHOLD = 90  # Typical angle threshold for fall detection
FALL_ANGLE_FRAMES = 10     # Number of consecutive frames to confirm fall
POSE_CONFIDENCE_THRESHOLD = 0.6  # Minimum average landmark confidence

# Function to calculate the angle between three points (a, b, c)
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

# Send fall event to your FastAPI backend
def send_fall_event_to_api(latitude, longitude, timestamp, severity=0.9):
    payload = {
        "latitude": latitude,
        "longitude": longitude, #Simulated by get_watch_data()
        "timestamp": timestamp,
        "event_type": "fall",
        "severity": severity
    }
    try:
        response = requests.post("http://localhost:8000/fall_event/", json=payload)
        if response.status_code == 200:
            print("Fall event sent to API successfully.") 
        else:
            print("Failed to send fall event:", response.status_code, response.text)
    except Exception as e:
        print("Error sending fall event:", e)

# Simulated GPS data (replace with actual device GPS input if available)
def get_watch_data():
    now = datetime.now()
    return {
        "timestamp": now.isoformat(),
        "lat": -33.865143,
        "lon": 151.209900,
    }

def run_fall_detection():
    """
    Runs fall detection on the webcam feed and returns a message when a fall is detected.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    print("Fall detection started. Press 'q' to quit.")

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        low_angle_counter = 0
        fall_detected = False
        last_fall_time = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera")
                break

            # Show the camera frame
            #cv2.imshow('Fall Detection', frame)

            # Convert to RGB for Mediapipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Extract left shoulder, hip, and knee (x,y)
                l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                # Average visibility confidence of key landmarks
                avg_vis = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility +
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility +
                           landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility) / 3

                if avg_vis > POSE_CONFIDENCE_THRESHOLD:
                    angle = calculate_angle(l_shoulder, l_hip, l_knee)
                    # Debug print
                    print(f"DEBUG: Angle={angle:.2f}, Counter={low_angle_counter}")

                    if angle < FALL_ANGLE_THRESHOLD:
                        low_angle_counter += 1
                        if low_angle_counter >= FALL_ANGLE_FRAMES:
                            fall_detected = True
                            last_fall_time = datetime.now()
                    else:
                        low_angle_counter = 0
                else:
                    low_angle_counter = 0
            else:
                low_angle_counter = 0

            # If fall detected, send API event and return message
            if fall_detected:
                data = get_watch_data()
                send_fall_event_to_api(data["lat"], data["lon"], last_fall_time.isoformat())
                cap.release()
                cv2.destroyAllWindows()
                return f"Fall detected at {last_fall_time.strftime('%H:%M:%S')}!"

            # Break loop if user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return None  # No fall detected

