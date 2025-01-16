네, 이미지의 특성에 따라 각 필터의 강도를 자동으로 조절하는 방법을 제안드립니다:

```python
def analyze_image(image):
    # 이미지 분석
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # 평균 밝기와 표준편차
    mean_brightness = np.mean(v)
    std_brightness = np.std(v)
    
    # 평균 채도
    mean_saturation = np.mean(s)
    
    return {
        'brightness': mean_brightness,
        'brightness_std': std_brightness,
        'saturation': mean_saturation
    }

def adaptive_enhance(image):
    # 이미지 분석
    stats = analyze_image(image)
    
    # 1. 감마 값 적응적 조정
    # 어두운 이미지(밝기 < 128)는 더 강한 감마 보정
    gamma = 1.0
    if stats['brightness'] < 128:
        # 어두울수록 감마값을 낮춤 (더 밝게)
        gamma = 0.8 + (stats['brightness'] / 128) * 0.4
    else:
        # 밝은 이미지는 감마 보정 약하게
        gamma = 1.0
    img1 = adjust_gamma(image, gamma)
    
    # 2. CLAHE 강도 적응적 조정
    # 대비(표준편차)가 낮은 이미지는 더 강한 CLAHE
    clip_limit = 0.3
    if stats['brightness_std'] < 50:
        clip_limit = 0.4  # 대비가 낮으면 더 강하게
    img2 = apply_clahe(img1)
    
    # 3. Vibrance 강도 적응적 조정
    # 채도가 낮은 이미지는 더 강한 vibrance
    vibrance_factor = 0.3
    if stats['saturation'] < 128:
        # 채도가 낮을수록 더 강한 vibrance
        vibrance_factor = 0.4
    else:
        # 채도가 높으면 약한 vibrance
        vibrance_factor = 0.2
    img3 = increase_vibrance(img2, factor=vibrance_factor)
    
    return img3

# 사용 예시
for img_path in img_paths:
    img = cv2.imread(img_path)
    enhanced = adaptive_enhance(img)
    
    # 결과 비교
    res = np.hstack((img, enhanced))
    Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB)).show()
```

이 방식의 장점:
1. 각 이미지의 특성에 따라 자동으로 파라미터 조정
2. 불필요한 처리 최소화 (밝은 이미지는 감마 보정 약하게)
3. 기존 코드의 구조를 유지하면서 적응형 처리 추가

필요하다면 파라미터 범위나 조건을 더 세밀하게 조정할 수 있습니다. 어떻게 생각하시나요?​​​​​​​​​​​​​​​​
