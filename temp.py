def enhance_text_clarity(image: np.ndarray) -> np.ndarray:
    """
    엣지 강화와 CLAHE를 사용해 텍스트를 더 선명하게 만드는 함수
    """
    # CLAHE로 대비 향상
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        l = clahe.apply(l)
        
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    else:
        enhanced = clahe.apply(image)
    
    # 언샤프 마스크로 엣지 강화
    gaussian = cv2.GaussianBlur(enhanced, (0,0), 2.0)
    sharpened = cv2.addWeighted(enhanced, 1.5, gaussian, -0.5, 0)
    
    return sharpened

# 사용 예시:
result = enhance_text_clarity(image)

# 더 강한 효과를 원하는 경우:
def enhance_text_clarity_stronger(image: np.ndarray) -> np.ndarray:
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = clahe.apply(l)
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    else:
        enhanced = clahe.apply(image)
    
    gaussian = cv2.GaussianBlur(enhanced, (0,0), 2.0)
    sharpened = cv2.addWeighted(enhanced, 2.0, gaussian, -1.0, 0)
    
    return sharpened
