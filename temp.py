import cv2
import av
import numpy as np
import time
import os
import argparse
from tqdm import tqdm

def cv2_process(video_path, num_frames=2000):
    """
    OpenCV(cv2)를 사용하여 비디오 프레임을 추출하고 NumPy로 평균값 계산
    """
    # 결과를 저장할 리스트
    frame_means = []
    
    # OpenCV로 비디오 파일 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: OpenCV에서 {video_path} 파일을 열 수 없습니다.")
        return None, 0
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_to_process = min(num_frames, total_frames)
    
    start_time = time.time()
    
    # 프레임 추출 및 처리
    for _ in tqdm(range(frames_to_process), desc="OpenCV 처리"):
        ret, frame = cap.read()
        if not ret:
            break
            
        # BGR에서 RGB로 변환 (PyAV와 동일한 형식 유지)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # NumPy로 평균값 계산
        mean_value = np.mean(frame_rgb)
        frame_means.append(mean_value)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    cap.release()
    
    return frame_means, processing_time

def pyav_process(video_path, num_frames=2000):
    """
    PyAV를 사용하여 비디오 프레임을 추출하고 NumPy로 평균값 계산
    """
    # 결과를 저장할 리스트
    frame_means = []
    
    # PyAV로 비디오 파일 열기
    try:
        container = av.open(video_path)
        video_stream = container.streams.video[0]
    except Exception as e:
        print(f"Error: PyAV에서 {video_path} 파일을 열 수 없습니다: {e}")
        return None, 0
    
    start_time = time.time()
    
    # 프레임 추출 및 처리
    frame_count = 0
    for frame in tqdm(container.decode(video_stream), total=num_frames, desc="PyAV 처리"):
        # 최대 프레임 수에 도달하면 중단
        if frame_count >= num_frames:
            break
            
        # 프레임을 numpy 배열로 변환
        img = frame.to_ndarray(format='rgb24')
        
        # NumPy로 평균값 계산 (GPU 사용 X)
        mean_value = np.mean(img)
        frame_means.append(mean_value)
        
        frame_count += 1
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    container.close()
    
    return frame_means, processing_time

def save_results(cv2_means, pyav_means, cv2_time, pyav_time, output_dir="results"):
    """
    결과를 파일로 저장
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 평균값 저장
    if cv2_means is not None:
        np.save(f"{output_dir}/cv2_means.npy", np.array(cv2_means))
    if pyav_means is not None:
        np.save(f"{output_dir}/pyav_means.npy", np.array(pyav_means))
    
    # 처리 시간 기록
    with open(f"{output_dir}/processing_times.txt", "w") as f:
        f.write(f"OpenCV(cv2) 처리 시간: {cv2_time:.4f}초\n")
        if pyav_time > 0:
            f.write(f"PyAV 처리 시간: {pyav_time:.4f}초\n")
            speed_ratio = cv2_time / pyav_time if pyav_time > 0 else 0
            f.write(f"PyAV 속도 향상: {speed_ratio:.2f}배\n")

def main():
    parser = argparse.ArgumentParser(description="OpenCV vs PyAV 비디오 처리 성능 비교 (모두 NumPy 사용)")
    parser.add_argument("video_path", type=str, help="비디오 파일 경로")
    parser.add_argument("--frames", type=int, default=2000, help="처리할 프레임 수 (기본값: 2000)")
    parser.add_argument("--output", type=str, default="results", help="결과 저장 디렉토리 (기본값: results)")
    parser.add_argument("--cv2-only", action="store_true", help="OpenCV만 사용")
    parser.add_argument("--pyav-only", action="store_true", help="PyAV만 사용")
    
    args = parser.parse_args()
    
    # OpenCV 처리
    cv2_means, cv2_time = None, 0
    if not args.pyav_only:
        print(f"\n{'='*50}\nOpenCV(cv2)로 비디오 처리 시작\n{'='*50}")
        cv2_means, cv2_time = cv2_process(args.video_path, args.frames)
        print(f"OpenCV 처리 완료: {cv2_time:.4f}초")
    
    # PyAV 처리
    pyav_means, pyav_time = None, 0
    if not args.cv2_only:
        print(f"\n{'='*50}\nPyAV로 비디오 처리 시작\n{'='*50}")
        pyav_means, pyav_time = pyav_process(args.video_path, args.frames)
        print(f"PyAV 처리 완료: {pyav_time:.4f}초")
    
    # 결과 저장
    save_results(cv2_means, pyav_means, cv2_time, pyav_time, args.output)
    
    # 결과 출력
    print(f"\n{'='*50}\n결과 요약\n{'='*50}")
    print(f"처리한 프레임 수: {args.frames if cv2_means is not None else 'N/A' if pyav_means is None else len(pyav_means)}")
    
    if cv2_means is not None:
        print(f"OpenCV 처리 시간: {cv2_time:.4f}초")
    if pyav_means is not None:
        print(f"PyAV 처리 시간: {pyav_time:.4f}초")
    
    if cv2_means is not None and pyav_means is not None:
        speed_ratio = cv2_time / pyav_time if pyav_time > 0 else 0
        print(f"PyAV 속도 향상: {speed_ratio:.2f}배")
        
        # 결과 정확도 확인 (충분한 프레임을 처리했을 경우)
        min_frames = min(len(cv2_means), len(pyav_means))
        if min_frames > 0:
            cv2_mean_all = np.mean(cv2_means[:min_frames])
            pyav_mean_all = np.mean(pyav_means[:min_frames])
            mean_diff = abs(cv2_mean_all - pyav_mean_all)
            print(f"OpenCV vs PyAV 전체 평균값 차이: {mean_diff:.6f}")
            
            # 첫 N개 프레임에 대해 프레임별 차이 계산
            n_frames = min(10, min_frames)
            print(f"\n첫 {n_frames}개 프레임의 평균값 비교:")
            for i in range(n_frames):
                print(f"프레임 {i}: OpenCV={cv2_means[i]:.2f}, PyAV={pyav_means[i]:.2f}, 차이={abs(cv2_means[i]-pyav_means[i]):.6f}")

if __name__ == "__main__":
    main()
