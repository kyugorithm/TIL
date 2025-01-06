def create_ocr_friendly_image(image: np.ndarray) -> np.ndarray:
    """
    OCR이 잘 인식할 수 있는 형태로 이미지 변환
    흰 글씨를 검은 글씨로 변환하고, 배경을 흰색으로 만듦
    """
    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 밝기 반전 (흰 글씨를 어두운 글씨로)
    inverted = cv2.bitwise_not(gray)
    
    # 약한 블러로 노이즈 제거
    denoised = cv2.GaussianBlur(inverted, (3,3), 0)
    
    # Otsu 이진화 적용
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 작은 노이즈 제거
    kernel = np.ones((2,2), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    return cleaned



def alternative_ocr_preprocessing(image: np.ndarray) -> np.ndarray:
    """
    대체 전처리 방법
    글자의 엣지를 찾아서 검은색으로 채우는 방식
    """
    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 약한 가우시안 블러
    blurred = cv2.GaussianBlur(gray, (3,3), 0)
    
    # 이미지를 밝게 만들어 그림자 효과 강화
    brightened = cv2.convertScaleAbs(blurred, alpha=1.2, beta=30)
    
    # 적응형 이진화
    binary = cv2.adaptiveThreshold(
        brightened,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, # 블록 크기
        2   # C 상수
    )
    
    # 노이즈 제거
    kernel = np.ones((2,2), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return cleaned
