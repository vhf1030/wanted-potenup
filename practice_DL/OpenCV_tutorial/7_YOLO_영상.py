
from ultralytics import YOLO
import sys
import cv2
import logging

# PaddleOCR 로그 숨기기 (DEBUG 및 WARNING 제거)
logging.getLogger("ppocr").setLevel(logging.ERROR)

vcap = cv2.VideoCapture(0)

model = YOLO("yolo11n.pt")

print(model.names)

while True:
    # ret: 카메라 작동 여부, frame: 이미지
    ret, frame = vcap.read()
    # print(type(frame))
    
    # 좌우 반전
    frame = cv2.flip(frame, 1)
    
    # 모델에 input하여 예측값 얻기
    results = model(frame, stream=True)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            print(box.cls)
            print(model.names[int(box.cls)])
            print(box.xyxy)
            
            x1, y1, x2, y2 = (int(xy) for xy in box.xyxy[0])
            # print(x1, y1, x2, y2)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            
            # 신뢰도 점수 표시
            cls_idx = int(box.cls.item())
            cls_name = model.names[cls_idx]
            
            score = box.conf.item() * 100  # 0~1 값을 100%로 변환
            cv2.putText(
                frame, f"{cls_name} {score:.1f}%", (x1, y2 - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2
            )
    
    cv2.imshow("Webcam", frame)
    
    key = cv2.waitKey(1)
    if key == 27:  # ESC를 누르면 break되도록 설정
        break
    
    
    
vcap.release()  # 카메라 장치 해제
cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기
    
    