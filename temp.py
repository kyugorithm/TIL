import cv2
import numpy as np
from typing import Tuple, Optional, Union

class ImagePreprocessor:
    def __init__(self):
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    
    def enhance_contrast(self, 
                        image: np.ndarray, 
                        clip_limit: float = 2.0,
                        grid_size: Tuple[int, int] = (8,8)) -> np.ndarray:
        """
        CLAHE를 사용하여 이미지의 대비를 향상시킵니다.
        
        Args:
            image: 입력 이미지
            clip_limit: CLAHE의 클리핑 제한값
            grid_size: CLAHE의 그리드 크기
        
        Returns:
            대비가 향상된 이미지
        """
        if len(image.shape) == 3:
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
            l = clahe.apply(l)
            
            enhanced = cv2.merge((l,a,b))
            return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        else:
            return self.clahe.apply(image)

    def enhance_edges(self, 
                     image: np.ndarray, 
                     blur_size: float = 2.0,
                     alpha: float = 2.0,
                     beta: float = -1.0) -> np.ndarray:
        """
        언샤프 마스킹을 사용하여 엣지를 강화합니다.
        
        Args:
            image: 입력 이미지
            blur_size: 가우시안 블러의 시그마 값
            alpha: 원본 이미지 가중치
            beta: 블러 이미지 가중치
        
        Returns:
            엣지가 강화된 이미지
        """
        gaussian = cv2.GaussianBlur(image, (0,0), blur_size)
        unsharp = cv2.addWeighted(image, alpha, gaussian, beta, 0)
        return unsharp

    def binarize(self, 
                 image: np.ndarray,
                 threshold: Optional[int] = None,
                 max_value: int = 255) -> np.ndarray:
        """
        이미지를 이진화합니다. threshold가 None이면 Otsu 방법을 사용합니다.
        
        Args:
            image: 입력 이미지
            threshold: 임계값 (None이면 Otsu 방법 사용)
            max_value: 최대값
        
        Returns:
            이진화된 이미지
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        if threshold is None:
            return cv2.threshold(gray, 0, max_value, 
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        else:
            return cv2.threshold(gray, threshold, max_value, 
                               cv2.THRESH_BINARY)[1]

    def apply_morphology(self, 
                        image: np.ndarray,
                        operation: str = 'close',
                        kernel_size: int = 3,
                        iterations: int = 1) -> np.ndarray:
        """
        모폴로지 연산을 적용합니다.
        
        Args:
            image: 입력 이미지
            operation: 연산 종류 ('dilate', 'erode', 'open', 'close')
            kernel_size: 커널 크기
            iterations: 반복 횟수
        
        Returns:
            모폴로지 연산이 적용된 이미지
        """
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        if operation == 'dilate':
            return cv2.dilate(image, kernel, iterations=iterations)
        elif operation == 'erode':
            return cv2.erode(image, kernel, iterations=iterations)
        elif operation == 'open':
            return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        elif operation == 'close':
            return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def process_image(self,
                     image: np.ndarray,
                     enhance_contrast: bool = True,
                     enhance_edges: bool = True,
                     binarize: bool = True,
                     morphology: bool = True) -> np.ndarray:
        """
        이미지에 전처리 과정을 순차적으로 적용합니다.
        
        Args:
            image: 입력 이미지
            enhance_contrast: 대비 향상 적용 여부
            enhance_edges: 엣지 강화 적용 여부
            binarize: 이진화 적용 여부
            morphology: 모폴로지 연산 적용 여부
            
        Returns:
            전처리된 이미지
        """
        processed = image.copy()
        
        if enhance_contrast:
            processed = self.enhance_contrast(processed)
            
        if enhance_edges:
            processed = self.enhance_edges(processed)
            
        if binarize:
            processed = self.binarize(processed)
            
        if morphology:
            processed = self.apply_morphology(processed)
            
        return processed

# 사용 예시
def main():
    # 이미지 읽기
    image = cv2.imread('input_image.jpg')
    
    # 전처리기 초기화
    preprocessor = ImagePreprocessor()
    
    # 기본 설정으로 전처리
    processed = preprocessor.process_image(image)
    
    # 커스텀 설정으로 전처리
    custom_processed = preprocessor.process_image(
        image,
        enhance_contrast=True,
        enhance_edges=True,
        binarize=False,  # 이진화 건너뛰기
        morphology=True
    )
    
    # 결과 저장
    cv2.imwrite('processed_image.jpg', processed)
    cv2.imwrite('custom_processed_image.jpg', custom_processed)

if __name__ == "__main__":
    main()
