import cv2
import mediapipe as mp
import numpy as np

import Telegram
import Speaker
import Popup
import json
import HighLow

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config('Config.JSON')

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

class CameraHandler:
    def __init__(self, parent, camera_index=config["camera_index"]):
        self.parent = parent
        self.camera_index = camera_index
        self.cap = None
        self.fall_detector = FallDetector()
        self.telegram = Telegram.TelegramBot()
        self.popup = Popup.PopupWindow(parent)
        self.ayo_sound = Speaker.AudioPlayer(config["sounds"]["ayo_sound"], 1000)
        self.sent = False
        self.sixout = HighLow.six_out()

    def open_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise Exception(f"Error: Could not open camera with index {self.camera_index}")

    def close_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None

    def get_frame(self):
        if not self.cap:
            raise Exception("Error: Camera is not opened")

        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Error: Failed to capture image")

        #self.fall_detector.detect_fall()
        success, frame = self.cap.read()
        if not success:
            return
        
        results = detect_landmarks(frame)
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            self.fall_detector.update_landmarks(results.pose_landmarks)
            fallen = self.fall_detector.detect_fall()
            self.sixout.on()
            if fallen and self.fall_detector.fall_message_counter == 0:
                self.fall_detector.fall_message_counter = 30
        else:
            cv2.putText(frame, "Adjust your position", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            self.sixout.off()
            
        if self.fall_detector.fall_message_counter > 0:
            cv2.putText(frame, "Fall detected!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            self.fall_detector.fall_message_counter -= 1
        
        if self.sent == False and self.fall_detector.fall_message_counter > 0:
            self.telegram.send_message("Fall detected! Please check on user NOW!")
            self.ayo_sound.play()
            self.popup.show()
            self.sent = True
        elif self.sent == True and self.fall_detector.fall_message_counter <= 0:
            self.ayo_sound.stop()
            self.sent = False
        
        return frame

    def is_opened(self):
        return self.cap is not None and self.cap.isOpened()


class FallDetector:
    def __init__(self, buffer_size=5):
        self.landmark_buffer = []
        self.buffer_size = buffer_size
        self.fall_message_counter = 0

    def update_landmarks(self, landmarks):
        if landmarks:
            self.landmark_buffer.append(landmarks)
            if len(self.landmark_buffer) > self.buffer_size:
                self.landmark_buffer.pop(0)

    def calculate_velocity(self):
        if len(self.landmark_buffer) < 2:
            return 0
        last = self.landmark_buffer[-1]
        prev = self.landmark_buffer[-2]
        torso_last = np.array([(last.landmark[mp_pose.PoseLandmark.LEFT_HIP].x + last.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x) / 2,
                               (last.landmark[mp_pose.PoseLandmark.LEFT_HIP].y + last.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y) / 2])
        torso_prev = np.array([(prev.landmark[mp_pose.PoseLandmark.LEFT_HIP].x + prev.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x) / 2,
                               (prev.landmark[mp_pose.PoseLandmark.LEFT_HIP].y + prev.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y) / 2])
        velocity = np.linalg.norm(torso_last - torso_prev)
        return velocity

    def calculate_body_angle(self, landmarks):
        shoulder_center = np.array([(landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x +
                                        landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x) / 2,
                                    (landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y +
                                        landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y) / 2])
        hip_center = np.array([(landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x +
                                landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x) / 2,
                                (landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y +
                                landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y) / 2])
        vector = hip_center - shoulder_center
        angle = np.arctan2(vector[1], vector[0]) * 180 / np.pi
        return abs(angle)  

    def detect_fall(self):
        velocity = self.calculate_velocity()
        angle = self.calculate_body_angle(self.landmark_buffer[-1])
        if angle > 45 and velocity > 0.15:
            return True
        return False


def detect_landmarks(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    return results

