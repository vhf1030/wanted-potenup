import sys
import cv2
import mediapipe as mp

# MediaPipe 손 인식 모델 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def process_frame(frame, hands, flip=True):
    """
    주어진 프레임에서 손을 감지하고 랜드마크를 표시하는 함수.
    - flip=True일 경우 좌우 반전
    """
    if flip:
        frame = cv2.flip(frame, 1)  # 좌우 반전

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR이므로 RGB로 변환
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:
            # 손 랜드마크 그리기
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

        # # 출력 테스트
        # one_hand = results.multi_hand_landmarks[0]
        # print(len(results.multi_hand_landmarks), len(one_hand.landmark))
        
        # # 미션: landmark 좌표 중 index 12의 위치를 (x, y, z)로 출력
        # idx = 12
        # for i, hand in enumerate(results.multi_hand_landmarks):
        #     finger_tip = hand.landmark[idx]
        #     print(i, finger_tip.x, finger_tip.y, finger_tip.z)
            
        #     # 미션: landmark 좌표 중 index 12의 위치에 동그라미 그리기
        #     x, y = int(hand.landmark[idx].x * w), int(hand.landmark[idx].y * h)
        #     cv2.circle(frame, (x, y), 50, (0, 0, 255), 4, lineType=cv2.LINE_AA)  # 빨간 점 표시
        
        # 미션: landmark 좌표 중 손가락의 마지막 위치에 동그라미 그리기
        h, w, _ = frame.shape  # 이미지 크기 가져오기
        idxes = [4, 8, 12, 16, 20]
        tips_xy = []
        for hand in results.multi_hand_landmarks:
            tips_xy.extend([(int(hand.landmark[idx].x * w), int(hand.landmark[idx].y * h)) for idx in idxes])
        for x, y in tips_xy:
            cv2.circle(frame, (x, y), 50, (0, 0, 255), 4, lineType=cv2.LINE_AA)  # 빨간 원 표시
        
    return frame

def main(flip=True):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 불러오지 못했습니다.")
        sys.exit()

    # MediaPipe Hands 모델 설정
    with mp_hands.Hands(
        model_complexity=1,  # 모델 복잡도 (0~1, 기본값: 1)
        min_detection_confidence=0.5,  # 감지 최소 신뢰도
        min_tracking_confidence=0.5  # 추적 최소 신뢰도
    ) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("카메라에서 프레임을 가져올 수 없습니다.")
                break

            frame = process_frame(frame, hands, flip=flip)  # 손 인식 및 랜드마크 그리기

            cv2.imshow("Hand Tracking", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC 키를 누르면 종료
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(flip=True)  # 좌우 반전 옵션 활성화
