import sys
import cv2
import mediapipe as mp
import argparse
import numpy as np

# MediaPipe 얼굴 감지 및 얼굴 랜드마크 모델 초기화
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def init_face_detection():
    """얼굴 감지 모델 초기화"""
    return mp_face_detection.FaceDetection(
        model_selection=0,  # 0: 근거리, 1: 원거리
        min_detection_confidence=0.5  # 얼굴 감지 신뢰도 임계값
    )

def init_face_mesh():
    """얼굴 랜드마크 모델 초기화"""
    return mp_face_mesh.FaceMesh(
        max_num_faces=1,  # 감지할 최대 얼굴 수
        refine_landmarks=True,  # 눈동자 및 정밀한 랜드마크 포함
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

def process_frame(frame, face_detector, face_mesh, flip=True, draw_landmarks=True, draw_points=True):
    """
    얼굴을 감지하고 바운딩 박스와 랜드마크(눈, 코, 입, 귀)를 표시하는 함수.
    - flip: 좌우 반전 옵션
    - draw_landmarks: 얼굴 메시(랜드마크) 그리기 활성화 여부
    - draw_points: 주요 부위(눈, 코, 입, 귀) 점 찍기 활성화 여부
    """
    if flip:
        frame = cv2.flip(frame, 1)  # 좌우 반전

    # BGR → RGB 변환 (MediaPipe는 RGB를 사용함)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 얼굴 감지 수행
    results_detection = face_detector.process(rgb_frame)

    # 얼굴 랜드마크 감지 수행
    results_mesh = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape  # 이미지 크기 가져오기

    # 얼굴 감지 결과 처리
    if results_detection.detections:
        for detection in results_detection.detections:
            bboxC = detection.location_data.relative_bounding_box

            # 바운딩 박스 좌표 계산
            x_min, y_min = int(bboxC.xmin * w), int(bboxC.ymin * h)
            width, height = int(bboxC.width * w), int(bboxC.height * h)
            x_max, y_max = x_min + width, y_min + height

            # 얼굴 바운딩 박스 그리기
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # 신뢰도 점수 표시
            score = detection.score[0] * 100  # 0~1 값을 100%로 변환
            cv2.putText(
                frame, f"{score:.1f}%", (x_min, y_min - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2
            )

    # 얼굴 랜드마크 결과 처리
    if results_mesh.multi_face_landmarks:
        for face_landmarks in results_mesh.multi_face_landmarks:
            # 얼굴 메시(랜드마크) 그리기 활성화 옵션
            if draw_landmarks:
                mp_drawing.draw_landmarks(
                    frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                
            # 미션: landmark 좌표 중 눈동자의 위치에 사각형 그리기
            h, w, _ = frame.shape  # 이미지 크기 가져오기
            idxes = [(469, 470, 471, 472), (474, 475, 476, 477)]
            eyes_xys = []
            for face in results_mesh.multi_face_landmarks:
                eyes_xys.append([((int(face.landmark[i].x * w), int(face.landmark[i].y * h)) for i in idx) for idx in idxes])
            for eyes_xy in eyes_xys:
                # print([list(xy) for xy in eyes_xy])
                for eye_xy in eyes_xy:
                    cv2.polylines(
                        frame,
                        [np.array(list(eye_xy), np.int32).reshape((-1, 1, 2))],
                        isClosed=True, color=(200, 200, 200), thickness=2
                    )

            # 주요 부위 (눈, 코, 입, 귀) 점 찍기 활성화 옵션
            if draw_points:
                key_landmarks = {
                    "왼쪽 눈": 33, "오른쪽 눈": 263,
                    "코": 1, "입 중앙": 13,
                    "왼쪽 귀": 234, "오른쪽 귀": 454
                }

                for name, idx in key_landmarks.items():
                    x, y = int(face_landmarks.landmark[idx].x * w), int(face_landmarks.landmark[idx].y * h)
                    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # 빨간 점 표시

    return frame

def main(flip=True, draw_landmarks=True, draw_points=True):
    """웹캠 실행 및 얼굴 감지"""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 불러오지 못했습니다.")
        sys.exit()

    face_detector = init_face_detection()  # 얼굴 감지 모델 초기화
    face_mesh = init_face_mesh()  # 얼굴 랜드마크 모델 초기화

    while True:
        ret, frame = cap.read()
        if not ret:
            print("카메라에서 프레임을 가져올 수 없습니다.")
            break

        frame = process_frame(frame, face_detector, face_mesh, flip=flip, draw_landmarks=draw_landmarks, draw_points=draw_points)

        cv2.imshow("Face Detection with Landmarks", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC 키를 누르면 종료
            break
        elif key == ord("l"):  # 'L' 키를 눌러 랜드마크(메시) 표시 토글
            draw_landmarks = not draw_landmarks
            print(f"얼굴 랜드마크 표시 변경: {draw_landmarks}")
        elif key == ord("p"):  # 'P' 키를 눌러 점(눈, 코, 입, 귀) 표시 토글
            draw_points = not draw_points
            print(f"얼굴 주요 포인트(눈, 코, 입, 귀) 표시 변경: {draw_points}")
        elif key == ord("f"):  # 'F' 키를 눌러 좌우 반전 토글
            flip = not flip
            print(f"좌우 반전 상태 변경: {flip}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="얼굴 감지 및 랜드마크 표시 옵션 설정")
    parser.add_argument("--flip", action="store_true", help="좌우 반전 활성화")
    parser.add_argument("--no-landmarks", action="store_true", help="랜드마크(메시) 비활성화")
    parser.add_argument("--no-points", action="store_true", help="눈, 코, 입, 귀 포인트 비활성화")
    args = parser.parse_args()

    main(
        flip=args.flip,
        draw_landmarks=not args.no_landmarks,
        draw_points=not args.no_points
    )
