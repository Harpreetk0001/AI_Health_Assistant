import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import folium

# Setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Constants
FALL_ANGLE_THRESHOLD = 100
FALL_ANGLE_FRAMES = 10
POSE_CONFIDENCE_THRESHOLD = 0.6
MAX_FALLBACK_FRAMES = 60
COOLDOWN_SECONDS = 30

ALTITUDE_DROP_THRESHOLD = 15  # meters
NO_MOVEMENT_DURATION = 60     # seconds
HEART_RATE_THRESHOLD = 100    # bpm
STEP_THRESHOLD = 0

# Helper: Calculate angle
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

# Simulate Apple Watch data (replace with real input in production)
def get_watch_data():
    now = datetime.now()
    return {
        "timestamp": now.isoformat(),
        "lat": -33.865143,
        "lon": 151.209900,
        "altitude": 50,
        "prev_altitude": 70,
        "steps": 0,
        "heart_rate": 110
    }

# Apple Watch-based fallback detection
def detect_fall_from_watch(data):
    t2 = datetime.fromisoformat(data["timestamp"])
    alt_drop = data["prev_altitude"] - data["altitude"]
    no_steps = data["steps"] <= STEP_THRESHOLD
    high_hr = data["heart_rate"] >= HEART_RATE_THRESHOLD
    if alt_drop >= ALTITUDE_DROP_THRESHOLD and no_steps and high_hr:
        return True, (data["lat"], data["lon"]), data["timestamp"]
    return False, None, None

# Start camera
cap = cv2.VideoCapture(0)
print(" Fall detection started. Press 'q' to quit.")

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    low_angle_counter = 0
    fallback_low_conf_counter = 0
    fall_detected = False
    fall_location = None
    last_fall_time = None
    last_alert_time = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        # No person detected → skip
        if not results.pose_landmarks:
            fallback_low_conf_counter += 1
            if fallback_low_conf_counter >= FALL_ANGLE_FRAMES:
                watch_data = get_watch_data()
                detected, location, timestamp = detect_fall_from_watch(watch_data)
                if detected:
                    fall_detected = True
                    last_fall_time = datetime.fromisoformat(timestamp)
                    fall_location = location
                fallback_low_conf_counter = 0
            cv2.imshow("Fall Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        fallback_low_conf_counter = 0  # reset

        # Extract landmarks
        lm = results.pose_landmarks.landmark
        l_shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                      lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        l_hip = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                 lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        l_knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                  lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        visibilities = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility,
                        lm[mp_pose.PoseLandmark.LEFT_HIP.value].visibility,
                        lm[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility]
        avg_vis = sum(visibilities) / 3

        if avg_vis > POSE_CONFIDENCE_THRESHOLD:
            angle = calculate_angle(l_shoulder, l_hip, l_knee)
            if angle < FALL_ANGLE_THRESHOLD:
                low_angle_counter += 1
                if low_angle_counter >= FALL_ANGLE_FRAMES:
                    now = datetime.now()
                    if not last_alert_time or (now - last_alert_time).total_seconds() > COOLDOWN_SECONDS:
                        fall_detected = True
                        last_fall_time = now
                        fall_location = get_watch_data()["lat"], get_watch_data()["lon"]
                        last_alert_time = now
            else:
                low_angle_counter = 0

        # Draw pose landmarks
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # If fall detected
        if fall_detected:
            cv2.putText(frame, f"FALL DETECTED at {last_fall_time.strftime('%H:%M:%S')}",
                        (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)

            # Save map
            fmap = folium.Map(location=fall_location, zoom_start=18)
            folium.Marker(
                fall_location,
                popup=f"Fall at {last_fall_time.strftime('%H:%M:%S')}",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(fmap)
            fmap.save("fall_map.html")
            print("️ Fall saved to fall_map.html")

            fall_detected = False

        # Show window
        cv2.imshow("Fall Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print(" Exiting fall detection.")
cap.release()
cv2.destroyAllWindows()
