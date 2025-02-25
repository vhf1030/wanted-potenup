import sys
import cv2
import mediapipe as mp
import csv
import os
import joblib
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

model = joblib.load("practice_DL/OpenCV_tutorial/rock_scissors_paper.pkl")
labels = ["rock", "scissors", "paper"]

vcap = cv2.VideoCapture(0)

while True:
    # ret: 카메라 작동 상태, frame: 카메라 이미지
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다.")
        sys.exit()
        
    # 좌우 반전
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    
    # 손 감지
    results = hands.process(frame)
    
    if results.multi_hand_landmarks:
        one_hand = results.multi_hand_landmarks[0]
        
        # 좌표 모으기(21개)
        landmark_list = []
        for landmark in one_hand.landmark:
            landmark_list.extend([landmark.x, landmark.y, landmark.z])
            cv2.circle(frame, (int(width * landmark.x), int(height * landmark.y)), 2, (0, 0, 225), 2)
            
        # 예측
        pred = model.predict(np.array([landmark_list]))
        cv2.putText(frame, labels[pred[0]], (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                
    cv2.imshow("Webcam", frame)
    
    key = cv2.waitKey(1)
    if key == 27:  # ESC 누르면 종료
        break
    
# 리소스 정리
vcap.release()
cv2.destroyAllWindows()

