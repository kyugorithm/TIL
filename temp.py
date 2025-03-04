import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import glob

def process_image(image_path):
    # 이미지 로드 (흑백 변환)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return None, None, None
    
    # Sobel 필터 적용 (수평 + 수직 경계 검출)
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    sobel_edges = cv2.magnitude(sobel_x, sobel_y)
    sobel_edges = np.uint8(255 * (sobel_edges / np.max(sobel_edges)))  # 정규화

    # 이진화 (Threshold 적용)
    _, binary_edges = cv2.threshold(sobel_edges, 50, 255, cv2.THRESH_BINARY)

    # 윤곽선 검출
    contours, _ = cv2.findContours(binary_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 박스 크기 필터링 (20x9 크기 내외)
    min_w, min_h = 10, 5  # 너무 작은 노이즈 제거
    max_w, max_h = 50, 25  # 너무 큰 박스 제거
    detected_boxes = []
    
    image_with_boxes = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # 원본 이미지에 박스 표시
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if min_w < w < max_w and min_h < h < max_h:
            detected_boxes.append((x, y, w, h))
            cv2.rectangle(image_with_boxes, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return image, sobel_edges, image_with_boxes, len(detected_boxes)

def process_folder(folder_path, output_folder="output_results"):
    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)

    # 폴더 내 모든 이미지 처리
    image_paths = glob.glob(os.path.join(folder_path, "*.jpg")) + glob.glob(os.path.join(folder_path, "*.png"))

    results = []
    for image_path in image_paths:
        image_name = os.path.basename(image_path)
        original, sobel, boxed, count = process_image(image_path)

        if original is None:
            continue

        # 결과 시각화
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        axs[0].imshow(original, cmap='gray')
        axs[0].set_title("Original Image")
        axs[1].imshow(sobel, cmap='gray')
        axs[1].set_title("Sobel Edge Detection")
        axs[2].imshow(boxed)
        axs[2].set_title(f"Detected Boxes ({count})")

        for ax in axs:
            ax.axis("off")

        # 결과 저장
        save_path = os.path.join(output_folder, f"result_{image_name}")
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()

        results.append((image_name, count))

    return results

# 폴더 경로 지정 후 실행
folder_path = "/path/to/your/image/folder"  # 이미지 폴더 경로 설정
output_results = process_folder(folder_path)

# 결과 출력
for img_name, count in output_results:
    print(f"Image: {img_name}, Detected Small Boxes: {count}")
