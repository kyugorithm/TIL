import av
import numpy as np
import time
import torch
import os
import argparse
from tqdm import tqdm

def cpu_process_video(video_path, num_frames=2000):
    """
    CPU를 사용하여 비디오에서 프레임을 추출하고 평균값 계산
    """
    # 결과를 저장할 리스트
    frame_means = []
    
    # 비디오 파일 열기
    container = av.open(video_path)
    video_stream = container.streams.video[0]
    
    start_time = time.time()
    
    # 프레임 추출 및 처리
    frame_count = 0
    for frame in tqdm(container.decode(video_stream), total=num_frames, desc="CPU 처리"):
        # 최대 프레임 수에 도달하면 중단
        if frame_count >= num_frames:
            break
            
        # 프레임을 numpy 배열로 변환
        img = frame.to_ndarray(format='rgb24')
        
        # 평균값 계산
        mean_value = np.mean(img)
        frame_means.append(mean_value)
        
        frame_count += 1
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    container.close()
    
    return frame_means, processing_time

def gpu_process_video(video_path, num_frames=2000):
    """
    GPU를 사용하여 비디오에서 프레임을 추출하고 평균값 계산
    """
    # GPU 사용 가능 여부 확인
    if not torch.cuda.is_available():
        print("CUDA를 사용할 수 없습니다. GPU 처리를 건너뜁니다.")
        return None, 0
    
    # 결과를 저장할 리스트
    frame_means = []
    
    # 비디오 파일 열기
    container = av.open(video_path)
    video_stream = container.streams.video[0]
    
    start_time = time.time()
    
    # 프레임 추출 및 처리
    frame_count = 0
    for frame in tqdm(container.decode(video_stream), total=num_frames, desc="GPU 처리"):
        # 최대 프레임 수에 도달하면 중단
        if frame_count >= num_frames:
            break
            
        # 프레임을 numpy 배열로 변환
        img = frame.to_ndarray(format='rgb24')
        
        # numpy 배열을 GPU로 전송
        img_tensor = torch.from_numpy(img).to('cuda')
        
        # GPU에서 평균값 계산
        mean_value = torch.mean(img_tensor.float()).item()
        frame_means.append(mean_value)
        
        frame_count += 1
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    container.close()
    
    return frame_means, processing_time

def save_results(cpu_means, gpu_means, cpu_time, gpu_time, output_dir="results"):
    """
    결과를 파일로 저장
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 평균값 저장
    if cpu_means:
        np.save(f"{output_dir}/cpu_means.npy", np.array(cpu_means))
    if gpu_means:
        np.save(f"{output_dir}/gpu_means.npy", np.array(gpu_means))
    
    # 처리 시간 기록
    with open(f"{output_dir}/processing_times.txt", "w") as f:
        f.write(f"CPU 처리 시간: {cpu_time:.4f}초\n")
        if gpu_time > 0:
            f.write(f"GPU 처리 시간: {gpu_time:.4f}초\n")
            f.write(f"속도 향상: {cpu_time/gpu_time:.2f}배\n")

def main():
    parser = argparse.ArgumentParser(description="비디오 프레임 추출 및 평균값 계산 (CPU vs GPU)")
    parser.add_argument("video_path", type=str, help="비디오 파일 경로")
    parser.add_argument("--frames", type=int, default=2000, help="처리할 프레임 수 (기본값: 2000)")
    parser.add_argument("--output", type=str, default="results", help="결과 저장 디렉토리 (기본값: results)")
    parser.add_argument("--cpu-only", action="store_true", help="CPU만 사용")
    parser.add_argument("--gpu-only", action="store_true", help="GPU만 사용")
    
    args = parser.parse_args()
    
    # CPU 처리
    cpu_means, cpu_time = None, 0
    if not args.gpu_only:
        print(f"\n{'='*50}\nCPU로 비디오 처리 시작\n{'='*50}")
        cpu_means, cpu_time = cpu_process_video(args.video_path, args.frames)
        print(f"CPU 처리 완료: {cpu_time:.4f}초")
    
    # GPU 처리
    gpu_means, gpu_time = None, 0
    if not args.cpu_only and torch.cuda.is_available():
        print(f"\n{'='*50}\nGPU로 비디오 처리 시작\n{'='*50}")
        gpu_means, gpu_time = gpu_process_video(args.video_path, args.frames)
        print(f"GPU 처리 완료: {gpu_time:.4f}초")
    
    # 결과 저장
    save_results(cpu_means, gpu_means, cpu_time, gpu_time, args.output)
    
    # 결과 출력
    print(f"\n{'='*50}\n결과 요약\n{'='*50}")
    print(f"처리한 프레임 수: {args.frames}")
    if cpu_means:
        print(f"CPU 처리 시간: {cpu_time:.4f}초")
    if gpu_means:
        print(f"GPU 처리 시간: {gpu_time:.4f}초")
    
    if cpu_means and gpu_means:
        print(f"속도 향상: {cpu_time/gpu_time:.2f}배")
        
        # 결과 정확도 확인
        cpu_mean_all = np.mean(cpu_means)
        gpu_mean_all = np.mean(gpu_means)
        mean_diff = abs(cpu_mean_all - gpu_mean_all)
        print(f"CPU vs GPU 평균값 차이: {mean_diff:.6f}")

if __name__ == "__main__":
    main()
