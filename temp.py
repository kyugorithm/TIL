def alternative_preprocess(image: np.ndarray) -> np.ndarray:
    """
    대체 전처리 방법
    """
    # Lab 컬러스페이스로 변환
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # L 채널에서 엣지 검출
    edges = cv2.Canny(l, 50, 150)
    
    # 엣지 팽창으로 텍스트 영역 강화
    kernel = np.ones((2,2), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # 원본 밝기 정보와 결합
    result = cv2.bitwise_and(l, l, mask=dilated)
    
    return result
