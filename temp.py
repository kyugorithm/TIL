import cv2
import os

def extract_frames_and_subframes(video_path, output_dir, subframe_scale=4):
    """
    주어진 비디오 파일에서 프레임과 서브프레임을 추출하여 JPG 파일로 저장합니다.

    Args:
        video_path (str): 입력 비디오 파일 경로
        output_dir (str): 출력 디렉토리 경로
        subframe_scale (int, optional): 서브프레임 스케일 (기본값: 4)
    """
    # 비디오 캡처 객체 생성
    cap = cv2.VideoCapture(video_path)

    # 프레임 카운터 초기화
    frame_count = 0

    # 출력 디렉토리가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        if not ret:
            # 더 이상 프레임이 없으면 종료
            break

        # 프레임 저장
        frame_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_path, frame)

        # 서브프레임 추출 및 저장
        height, width, _ = frame.shape
        subframe_height = height // subframe_scale
        subframe_width = width // subframe_scale

        for i in range(subframe_scale):
            for j in range(subframe_scale):
                subframe = frame[i*subframe_height:(i+1)*subframe_height, j*subframe_width:(j+1)*subframe_width]
                subframe_path = os.path.join(output_dir, f"subframe_{frame_count}_{i}_{j}.jpg")
                cv2.imwrite(subframe_path, subframe)

        frame_count += 1

    # 비디오 캡처 객체 해제
    cap.release()

# 사용 예시
video_path = "path/to/your/video.mp4"
output_dir = "path/to/output/directory"
extract_frames_and_subframes(video_path, output_dir)
