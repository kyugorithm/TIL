def enhance_text_visibility(image: np.ndarray) -> np.ndarray:
    """
    원본 이미지의 특성을 유지하면서 텍스트의 가시성을 높이는 함수
    """
    # BGR -> LAB 변환 (밝기 채널을 따로 다루기 위해)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # L 채널에서 대비 향상
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    
    # 밝기 및 대비 미세 조정
    l = cv2.convertScaleAbs(l, alpha=1.15, beta=5)
    
    # 채널 다시 합치기
    enhanced_lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # 전체적인 선명도 향상
    kernel = np.array([[-1,-1,-1],
                      [-1, 9,-1],
                      [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    # 최종 결과에서 밝기와 대비 미세 조정
    final = cv2.convertScaleAbs(sharpened, alpha=1.1, beta=0)
    
    return final




# 이미지 읽기
image = cv2.imread('input.jpg')

# 기본 설정으로 처리
result = enhance_text_visibility(image)

# 또는 더 강한 대비를 위한 설정
def enhance_text_visibility_stronger(image: np.ndarray) -> np.ndarray:
    # BGR -> LAB 변환
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # L 채널 처리 강화
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    l = cv2.convertScaleAbs(l, alpha=1.25, beta=8)
    
    # 채널 합치기
    enhanced_lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # 더 강한 선명화
    kernel = np.array([[-1,-1,-1],
                      [-1, 11,-1],
                      [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    # 최종 조정
    final = cv2.convertScaleAbs(sharpened, alpha=1.15, beta=0)
    
    return final

# 더 강한 설정 적용
stronger_result = enhance_text_visibility_stronger(image)
