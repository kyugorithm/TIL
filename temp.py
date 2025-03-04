import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from tqdm import tqdm

def detect_small_boxes(image_path, visualize=False):
    """
    이미지에서 소벨 필터를 적용하고 작은 박스들을 검출하는 함수
    
    Args:
        image_path (str): 이미지 파일 경로
        visualize (bool): 중간 처리 결과 시각화 여부
        
    Returns:
        tuple: (검출된 박스 개수, 처리된 결과 이미지)
    """
    # 이미지 로드
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"이미지를 로드할 수 없습니다: {image_path}")
        return 0, None
    
    # 원본 이미지 저장 (시각화용)
    original_image = image.copy()
    
    # 이미지 전처리 (대비 향상)
    image = cv2.equalizeHist(image)
    
    # 소벨 필터 적용
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    
    # 그라디언트 크기 계산
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # 이진화
    _, binary = cv2.threshold(gradient_magnitude, 50, 255, cv2.THRESH_BINARY)
    
    # 노이즈 제거를 위한 모폴로지 연산
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # 윤곽선 검출
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 작은 박스 필터링
    small_boxes = []
    min_area = 10  # 최소 면적
    max_area = 500  # 최대 면적
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            # 사각형과 유사한지 확인
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
            
            if len(approx) >= 4:  # 4개 이상의 꼭지점을 가진 경우 (사각형에 가까운 형태)
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                
                # 종횡비가 적절한 경우만 선택 (너무 길쭉하지 않은 경우)
                if 0.5 < aspect_ratio < 2.0:
                    small_boxes.append(contour)
    
    # 결과 시각화를 위한 컬러 이미지
    result_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
    
    # 검출된 작은 박스 표시
    cv2.drawContours(result_image, small_boxes, -1, (0, 255, 0), 2)
    
    # 박스 개수 표시
    box_count = len(small_boxes)
    cv2.putText(result_image, f"Box Count: {box_count}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    if visualize:
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 3, 1)
        plt.title("Original Image")
        plt.imshow(original_image, cmap='gray')
        
        plt.subplot(2, 3, 2)
        plt.title("Sobel Gradient Magnitude")
        plt.imshow(gradient_magnitude, cmap='gray')
        
        plt.subplot(2, 3, 3)
        plt.title("Binary")
        plt.imshow(binary, cmap='gray')
        
        plt.subplot(2, 3, 4)
        plt.title(f"Detected Boxes: {box_count}")
        plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        
        plt.tight_layout()
        plt.show()
    
    return box_count, result_image

def process_folder(folder_path, output_folder=None):
    """
    폴더 내의 모든 이미지 파일을 처리하는 함수
    
    Args:
        folder_path (str): 처리할 이미지들이 있는 폴더 경로
        output_folder (str, optional): 결과 저장 폴더 경로
    
    Returns:
        dict: 파일명과 검출된 박스 개수를 담은 딕셔너리
    """
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 이미지 파일 찾기
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob(os.path.join(folder_path, ext)))
    
    results = {}
    
    for image_path in tqdm(image_files, desc="Processing images"):
        filename = os.path.basename(image_path)
        box_count, result_image = detect_small_boxes(image_path)
        
        results[filename] = box_count
        
        # 결과 저장
        if output_folder and result_image is not None:
            output_path = os.path.join(output_folder, f"result_{filename}")
            cv2.imwrite(output_path, result_image)
    
    return results

def visualize_results(results):
    """
    검출 결과를 시각화하는 함수
    
    Args:
        results (dict): 파일명과 검출된 박스 개수를 담은 딕셔너리
    """
    filenames = list(results.keys())
    box_counts = list(results.values())
    
    plt.figure(figsize=(12, 6))
    
    # 막대 그래프
    plt.subplot(1, 2, 1)
    plt.bar(filenames, box_counts, color='skyblue')
    plt.title('Box Count per Image')
    plt.xlabel('Image File')
    plt.ylabel('Number of Boxes')
    plt.xticks(rotation=45, ha='right')
    
    # 파이 차트
    plt.subplot(1, 2, 2)
    plt.pie(box_counts, labels=filenames, autopct='%1.1f%%')
    plt.title('Box Count Distribution')
    
    plt.tight_layout()
    plt.savefig("box_detection_results.png")
    plt.show()

def main():
    # 사용 예시
    folder_path = input("이미지 폴더 경로를 입력하세요: ")
    output_folder = input("결과 저장 폴더 경로를 입력하세요 (빈칸은 저장 안함): ")
    
    if not output_folder.strip():
        output_folder = None
    
    # 단일 이미지 테스트 (시각화 옵션 활성화)
    test_image = None
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
        test_files = glob(os.path.join(folder_path, ext))
        if test_files:
            test_image = test_files[0]
            break
    
    if test_image:
        print(f"테스트 이미지로 {test_image}를 사용합니다.")
        detect_small_boxes(test_image, visualize=True)
    
    # 폴더 내 모든 이미지 처리
    results = process_folder(folder_path, output_folder)
    
    # 결과 출력
    print("\n검출 결과:")
    for filename, count in results.items():
        print(f"{filename}: {count}개의 작은 박스 검출")
    
    # 결과 시각화
    if results:
        visualize_results(results)
    else:
        print("처리할 이미지가 없습니다.")

if __name__ == "__main__":
    main()
