import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Thresholds
FALL_ANGLE_THRESHOLD = 120
FALL_ANGLE_FRAMES = 5
POSE_CONFIDENCE_THRESHOLD = 0.5
MAX_FALLBACK_FRAMES = 30

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# Initialize video capture
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    low_angle_counter = 0
    fallback_low_conf_counter = 0
    fall_detected = False
    last_fall_time = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            left_shoulder_vis = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility
            left_hip_vis = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility
            left_knee_vis = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility

            avg_vis = (left_shoulder_vis + left_hip_vis + left_knee_vis) / 3
            print(f"DEBUG: Visibility scores - Shoulder: {left_shoulder_vis:.2f}, Hip: {left_hip_vis:.2f}, Knee: {left_knee_vis:.2f}")

            if avg_vis > POSE_CONFIDENCE_THRESHOLD:
                angle = calculate_angle(left_shoulder, left_hip, left_knee)
                print(f"DEBUG: Current angle = {angle:.2f}")

                if angle < FALL_ANGLE_THRESHOLD:
                    low_angle_counter += 1
                    print(f"DEBUG: low_angle_counter = {low_angle_counter}")
                    if low_angle_counter >= FALL_ANGLE_FRAMES:
                        fall_detected = True
                        last_fall_time = datetime.now()
                else:
                    low_angle_counter = 0

                fallback_low_conf_counter = 0  # Reset fallback
            else:
                fallback_low_conf_counter += 1
                print(f"DEBUG: Low confidence fallback counter = {fallback_low_conf_counter}")

                if fallback_low_conf_counter > MAX_FALLBACK_FRAMES:
                    fallback_low_conf_counter = 0  # Reset infinite counter

                if fallback_low_conf_counter >= FALL_ANGLE_FRAMES:
                    fall_detected = True
                    last_fall_time = datetime.now()
        else:
            fallback_low_conf_counter += 1
            print(f"DEBUG: No pose landmarks - fallback_low_conf_counter = {fallback_low_conf_counter}")

            if fallback_low_conf_counter > MAX_FALLBACK_FRAMES:
                fallback_low_conf_counter = 0

            if fallback_low_conf_counter >= FALL_ANGLE_FRAMES:
                fall_detected = True
                last_fall_time = datetime.now()

        # Visual feedback
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if fall_detected:
            cv2.putText(image, f"FALL DETECTED at {last_fall_time.strftime('%H:%M:%S')}",
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            fall_detected = False  # reset flag

        cv2.imshow('Fall Detection', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
