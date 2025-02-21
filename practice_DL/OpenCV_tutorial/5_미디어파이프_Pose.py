import sys
import cv2
import mediapipe as mp
import argparse

# MediaPipe Pose(자세) 인식 모델 초기화
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def init_pose_detection():
    """자세 인식 모델 초기화"""
    return mp_pose.Pose(
        min_detection_confidence=0.5,  # 감지 신뢰도 임계값
        min_tracking_confidence=0.5    # 추적 신뢰도 임계값
    )

def process_frame(frame, pose_detector, flip=True, draw_landmarks=True, draw_points=True):
    """
    자세를 감지하고 랜드마크 및 주요 관절(어깨, 팔꿈치, 무릎 등)을 표시하는 함수.
    - flip: 좌우 반전 옵션
    - draw_landmarks: 랜드마크 연결선 그리기 활성화 여부
    - draw_points: 주요 관절 점 찍기 활성화 여부
    """
    if flip:
        frame = cv2.flip(frame, 1)  # 좌우 반전

    # BGR → RGB 변환 (MediaPipe는 RGB를 사용)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 자세 감지 수행
    results = pose_detector.process(rgb_frame)

    h, w, _ = frame.shape  # 이미지 크기 가져오기

    # 랜드마크 결과 처리
    if results.pose_landmarks:
        # 랜드마크 연결선 그리기 활성화 옵션
        if draw_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

        # 주요 관절 점 찍기 활성화 옵션
        if draw_points:
            key_landmarks = {
                "왼쪽 어깨": 11, "오른쪽 어깨": 12,
                "왼쪽 팔꿈치": 13, "오른쪽 팔꿈치": 14,
                "왼쪽 손목": 15, "오른쪽 손목": 16,
                "왼쪽 엉덩이": 23, "오른쪽 엉덩이": 24,
                "왼쪽 무릎": 25, "오른쪽 무릎": 26,
                "왼쪽 발목": 27, "오른쪽 발목": 28
            }

            for name, idx in key_landmarks.items():
                landmark = results.pose_landmarks.landmark[idx]
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # 빨간 점 표시

    return frame

def main(flip=True, draw_landmarks=True, draw_points=True):
    """웹캠 실행 및 자세 인식"""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 불러오지 못했습니다.")
        sys.exit()

    pose_detector = init_pose_detection()  # 자세 인식 모델 초기화

    while True:
        ret, frame = cap.read()
        if not ret:
            print("카메라에서 프레임을 가져올 수 없습니다.")
            break

        frame = process_frame(frame, pose_detector, flip=flip, draw_landmarks=draw_landmarks, draw_points=draw_points)

        cv2.imshow("Pose Detection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC 키를 누르면 종료
            break
        elif key == ord("l"):  # 'L' 키를 눌러 랜드마크(연결선) 표시 토글
            draw_landmarks = not draw_landmarks
            print(f"자세 랜드마크 표시 변경: {draw_landmarks}")
        elif key == ord("p"):  # 'P' 키를 눌러 주요 관절 점 표시 토글
            draw_points = not draw_points
            print(f"자세 주요 포인트(관절) 표시 변경: {draw_points}")
        elif key == ord("f"):  # 'F' 키를 눌러 좌우 반전 토글
            flip = not flip
            print(f"좌우 반전 상태 변경: {flip}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="자세 인식 및 랜드마크 표시 옵션 설정")
    parser.add_argument("--flip", action="store_true", help="좌우 반전 활성화")
    parser.add_argument("--no-landmarks", action="store_true", help="랜드마크(연결선) 비활성화")
    parser.add_argument("--no-points", action="store_true", help="관절 점 비활성화")
    args = parser.parse_args()

    main(
        flip=args.flip,
        draw_landmarks=not args.no_landmarks,
        draw_points=not args.no_points
    )
