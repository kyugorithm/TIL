def preprocess_light_text(image: np.ndarray) -> np.ndarray:
    """
    밝은 배경의 흰색 텍스트를 위한 특화된 전처리
    """
    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 로컬 히스토그램 평활화 적용 (작은 블록 사이즈로)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(4,4))
    enhanced = clahe.apply(gray)
    
    # 부드러운 블러로 노이즈 제거
    blurred = cv2.GaussianBlur(enhanced, (3,3), 0)
    
    # 배경 제거를 위한 차연산
    background = cv2.GaussianBlur(enhanced, (31,31), 0)
    removed_bg = cv2.addWeighted(blurred, 1.5, background, -0.5, 0)
    
    # 텍스트 주변의 그림자 강조
    kernel = np.ones((3,3), np.float32)/25
    shadow_enhanced = cv2.filter2D(removed_bg, -1, kernel)
    
    # 최종 이진화 (Otsu 대신 적응형 임계값 사용)
    final = cv2.adaptiveThreshold(
        shadow_enhanced,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )
    
    return final
