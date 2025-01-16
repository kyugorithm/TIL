def increase_vibrance(image, factor=1.3):
    # HSV 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # 낮은 채도 영역에 더 큰 가중치 적용
    mask = (255 - s) / 255.0
    adjustment = s * (1 + factor * mask)
    
    # 범위 제한
    s = np.clip(adjustment, 0, 255).astype('uint8')
    
    hsv = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
