import sys
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import logging
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 한글 폰트
font_manager.fontManager.addfont(font_path)
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지

# PaddleOCR 로그 숨기기 (DEBUG 및 WARNING 제거)
logging.getLogger("ppocr").setLevel(logging.ERROR)

# OCR 모델 초기화 (한국어 인식)
ocr = PaddleOCR(lang="korean")

def draw_text_with_pil(frame, text, position, font_path="C:/Windows/Fonts/malgun.ttf", font_size=20):
    """
    OpenCV 이미지에 한글 텍스트를 표시하기 위해 PIL을 사용.
    """
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=(255, 0, 0, 255))  # 빨간색 텍스트
    return np.array(img_pil)

def process_frame(frame, ocr_model, flip=True, confidence_threshold=0.8):
    """
    실시간으로 OCR을 수행하고 인식된 텍스트를 표시하는 함수.
    - flip=True일 경우 좌우 반전
    """
    if flip:
        frame = cv2.flip(frame, 1)  # 좌우 반전

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV BGR → RGB 변환
    results = ocr_model.ocr(rgb_frame, cls=True)  # OCR 수행

    extracted_texts = []  # OCR로 추출된 텍스트 저장

    if results and results[0] is not None:
        for res in results[0]:  
            if len(res) < 2:  
                continue  # 데이터가 올바르지 않은 경우 스킵

            try:
                box, (text, score) = res  # 바운딩 박스, 인식된 텍스트, 신뢰도 점수
            except ValueError:
                continue  # 데이터가 비정상적인 경우 스킵
            
            # 신뢰도 필터링 (0.8 이상만 저장)
            if score < confidence_threshold:
                continue  # 신뢰도가 낮으면 스킵

            x_min, y_min = int(box[0][0]), int(box[0][1])
            x_max, y_max = int(box[2][0]), int(box[2][1])

            # OCR 텍스트 박스 그리기
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # 한글이 깨지지 않도록 PIL을 사용하여 텍스트 그리기
            frame = draw_text_with_pil(frame, text, (x_min, y_min - 25))

            extracted_texts.append(text)  # 터미널 출력용 리스트에 추가

    return frame, extracted_texts  # OCR로 추출한 텍스트 반환

def main(flip=True):
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("카메라를 불러오지 못했습니다.")
        sys.exit()

    last_print_time = time.time()  # 마지막 터미널 출력 시간 저장
    last_texts = []  # 이전 OCR 결과 저장

    while True:
        ret, frame = cap.read()
        if not ret:
            print("카메라에서 프레임을 가져올 수 없습니다.")
            break

        # OCR 수행
        frame, extracted_texts = process_frame(frame, ocr, flip=flip)

        # 1초마다 OCR 결과 출력 (같은 내용이면 출력하지 않음)
        current_time = time.time()
        if current_time - last_print_time >= 1:
            if extracted_texts and extracted_texts != last_texts:
                print(f"OCR 인식된 텍스트: {', '.join(extracted_texts)}")
                last_texts = extracted_texts[:]  # 이전 텍스트 업데이트
            last_print_time = current_time  # 마지막 출력 시간 업데이트

        cv2.imshow("Korean OCR", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC 키를 누르면 종료
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(flip=False)  # 좌우 반전 옵션 활성화
