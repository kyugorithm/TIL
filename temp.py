def create_diverse_color_pattern(width=25, height=13, line_width=3, 
                                contrast_level=1.0, noise_level=0.05,
                                color_scheme='random', transparency=0.8):
    """
    다양한 색상 조합을 가진 에러 패턴 박스를 생성합니다.
    
    Parameters:
    -----------
    width: 패턴 박스의 가로 픽셀 수
    height: 패턴 박스의 세로 픽셀 수
    line_width: 각 수직선의 픽셀 너비
    contrast_level: 대비 강도 (0.0~1.0)
    noise_level: 추가할 노이즈의 강도 (0.0~1.0)
    color_scheme: 색상 스키마 ('random', 'complementary', 'grayscale', 'highcontrast')
    transparency: 패턴의 투명도 (0.0~1.0)
    
    Returns:
    --------
    pattern: 생성된 패턴 이미지
    mask: 패턴의 투명도 마스크
    """
    # 빈 패턴 이미지 생성
    pattern = np.zeros((height, width, 3), dtype=np.float32)
    
    # 색상 스키마 선택
    if color_scheme == 'random':
        # 랜덤 두 색상 생성
        color1 = np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        color2 = np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
    
    elif color_scheme == 'complementary':
        # 보색 관계의 두 색상 생성
        hue = random.random()
        saturation = random.uniform(0.6, 1.0)
        value = random.uniform(0.7, 1.0)
        
        # HSV -> RGB 변환
        import colorsys
        rgb1 = colorsys.hsv_to_rgb(hue, saturation, value)
        rgb2 = colorsys.hsv_to_rgb((hue + 0.5) % 1.0, saturation, value)
        
        color1 = np.array([int(rgb1[0] * 255), int(rgb1[1] * 255), int(rgb1[2] * 255)])
        color2 = np.array([int(rgb2[0] * 255), int(rgb2[1] * 255), int(rgb2[2] * 255)])
    
    elif color_scheme == 'grayscale':
        # 흑백 색상 (전통적인 에러 패턴)
        bright_level = random.uniform(200, 255)
        dark_level = random.uniform(0, 50)
        color1 = np.array([bright_level, bright_level, bright_level])
        color2 = np.array([dark_level, dark_level, dark_level])
    
    elif color_scheme == 'highcontrast':
        # 높은 대비의 색상 조합
        options = [
            (np.array([255, 255, 0]), np.array([0, 0, 255])),    # 노랑-파랑
            (np.array([255, 0, 255]), np.array([0, 255, 0])),    # 마젠타-초록
            (np.array([255, 0, 0]), np.array([0, 255, 255])),    # 빨강-시안
            (np.array([255, 255, 255]), np.array([0, 0, 0]))     # 흰색-검정
        ]
        color1, color2 = random.choice(options)
    
    # 줄무늬 수 계산
    num_lines = width // line_width
    
    # 줄무늬 생성
    for i in range(num_lines):
        start_x = i * line_width
        end_x = min(start_x + line_width, width)
        
        # 두 색상 교대로 적용
        color = color1 if i % 2 == 0 else color2
        
        # 대비 조정
        if i % 2 == 0:
            adjusted_color = color * contrast_level + 255 * (1 - contrast_level)
        else:
            adjusted_color = color * contrast_level
            
        pattern[:, start_x:end_x, :] = adjusted_color.reshape(1, 1, 3)
    
    # 노이즈 추가
    if noise_level > 0:
        noise = np.random.normal(0, noise_level * 255, pattern.shape).astype(np.float32)
        pattern = np.clip(pattern + noise, 0, 255)
    
    # 패턴을 uint8로 변환
    pattern = pattern.astype(np.uint8)
    
    # 투명도 마스크 생성
    mask = np.ones((height, width), dtype=np.float32) * transparency
    
    return pattern, mask

def apply_diverse_pattern_to_image(image, x, y, background_aware=True, **pattern_params):
    """
    이미지의 지정된 위치에 다양한 색상의 패턴을 적용합니다.
    배경 인식 기능이 활성화된 경우 배경과 구분되는 색상을 선택합니다.
    
    Parameters:
    -----------
    image: 원본 이미지
    x, y: 패턴을 적용할 좌표
    background_aware: 배경색을 고려하여 패턴 색상 선택 여부
    pattern_params: create_diverse_color_pattern에 전달할 추가 파라미터
    
    Returns:
    --------
    result: 패턴이 적용된 이미지
    actual_colors: 실제 사용된 색상 정보 (디버깅용)
    """
    result = image.copy()
    
    # 패턴 크기 설정
    width = pattern_params.get('width', 25)
    height = pattern_params.get('height', 13)
    
    # 이미지 경계 확인
    if y + height > result.shape[0] or x + width > result.shape[1]:
        height = min(height, result.shape[0] - y)
        width = min(width, result.shape[1] - x)
        if height <= 0 or width <= 0:
            return result, None
    
    # ROI 추출
    roi = result[y:y+height, x:x+width]
    
    # 배경 인식 활성화된 경우
    if background_aware:
        # 배경의 평균 색상 계산
        bg_color = np.mean(roi, axis=(0, 1))
        
        # 배경색과 구분되는 색상 스키마 선택
        if np.mean(bg_color) < 128:  # 어두운 배경
            if 'color_scheme' not in pattern_params or pattern_params['color_scheme'] == 'random':
                # 밝은 색상 선호
                pattern_params['color_scheme'] = random.choice(['highcontrast', 'complementary'])
        else:  # 밝은 배경
            if 'color_scheme' not in pattern_params or pattern_params['color_scheme'] == 'random':
                # 어두운 색상 포함 선호
                pattern_params['color_scheme'] = random.choice(['highcontrast', 'complementary'])
    
    # 패턴 생성
    pattern, mask = create_diverse_color_pattern(width=width, height=height, **pattern_params)
    
    # 패턴 적용 (알파 블렌딩)
    for c in range(3):
        result[y:y+height, x:x+width, c] = (roi[:, :, c] * (1 - mask) + 
                                         pattern[:, :, c] * mask).astype(np.uint8)
    
    # 실제 사용된 색상 정보 (디버깅용)
    pattern_info = {
        'position': (x, y),
        'size': (width, height),
        'color_scheme': pattern_params.get('color_scheme', 'random')
    }
    
    return result, pattern_info

def generate_robust_training_data(img_path, num_samples=100, output_dir="./synthetic_data"):
    """
    다양한 색상 패턴을 사용한 강건한 학습용 데이터 생성
    
    Parameters:
    -----------
    img_path: 배경 이미지 경로 (디렉토리 또는 단일 이미지)
    num_samples: 생성할 이미지 샘플 수
    output_dir: 출력 디렉토리
    """
    import os
    import glob
    import json
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "labels"), exist_ok=True)
    
    # 배경 이미지 로드 (디렉토리면 모든 이미지 로드)
    background_paths = []
    if os.path.isdir(img_path):
        for ext in ['jpg', 'jpeg', 'png', 'bmp']:
            background_paths.extend(glob.glob(os.path.join(img_path, f"*.{ext}")))
    else:
        background_paths = [img_path]
    
    if not background_paths:
        raise ValueError(f"No images found in {img_path}")
    
    # 메타데이터 저장을 위한 딕셔너리
    metadata = {}
    
    for i in range(num_samples):
        # 랜덤하게 배경 이미지 선택
        bg_path = random.choice(background_paths)
        background = cv2.imread(bg_path)
        
        if background is None:
            print(f"Warning: Cannot load image from {bg_path}, skipping")
            continue
            
        height, width = background.shape[:2]
        
        # 패턴 개수 랜덤 결정 (2~10개)
        num_patterns = random.randint(2, 10)
        
        # 결과 이미지와 라벨 정보
        result = background.copy()
        labels = []
        pattern_infos = []
        
        # 다양한 색상 스키마
        color_schemes = ['highcontrast', 'complementary', 'grayscale', 'random']
        
        # 각 패턴에 대해
        for j in range(num_patterns):
            # 랜덤 위치 선택 (이미지 가장자리 피하기)
            margin = 10
            x = random.randint(margin, width - 30 - margin)
            y = random.randint(margin, height - 15 - margin)
            
            # 랜덤 패턴 특성
            pattern_width = random.randint(20, 30)
            pattern_height = random.randint(10, 15)
            line_width = random.randint(2, 4)
            contrast = random.uniform(0.7, 1.0)
            noise = random.uniform(0, 0.1)
            
            # 랜덤하게 색상 스키마 선택
            color_scheme = random.choice(color_schemes)
                
            transparency = random.uniform(0.7, 0.95)
            
            # 이미지에 패턴 적용
            result, pattern_info = apply_diverse_pattern_to_image(
                result, x, y, 
                background_aware=True,  # 배경색 인식 활성화
                width=pattern_width, height=pattern_height,
                line_width=line_width, contrast_level=contrast,
                noise_level=noise, color_scheme=color_scheme,
                transparency=transparency
            )
            
            if pattern_info:
                pattern_infos.append(pattern_info)
            
            # 라벨 정보 저장 (YOLO 형식: class x_center y_center width height)
            x_center = (x + pattern_width / 2) / width
            y_center = (y + pattern_height / 2) / height
            norm_width = pattern_width / width
            norm_height = pattern_height / height
            
            labels.append(f"0 {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}")
        
        # 이미지 저장
        img_filename = f"synthetic_{i:04d}.jpg"
        label_filename = f"synthetic_{i:04d}.txt"
        
        cv2.imwrite(os.path.join(output_dir, "images", img_filename), result)
        
        # 라벨 파일 저장
        with open(os.path.join(output_dir, "labels", label_filename), 'w') as f:
            f.write('\n'.join(labels))
        
        # 메타데이터 저장
        metadata[img_filename] = {
            'base_image': os.path.basename(bg_path),
            'patterns': pattern_infos
        }
            
        # 진행 상황 표시
        if (i+1) % 10 == 0:
            print(f"Generated {i+1}/{num_samples} images")
    
    # 메타데이터 저장
    with open(os.path.join(output_dir, "metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=2)

# 추가: 데이터 확인 및 시각화 함수
def visualize_pattern_distribution(metadata_path):
    """
    생성된 패턴 데이터의 분포를 시각화합니다.
    
    Parameters:
    -----------
    metadata_path: 메타데이터 파일 경로
    """
    import json
    import matplotlib.pyplot as plt
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # 색상 스키마 분포
    color_schemes = []
    for img_data in metadata.values():
        for pattern in img_data['patterns']:
            color_schemes.append(pattern['color_scheme'])
    
    # 분포 시각화
    schemes, counts = np.unique(color_schemes, return_counts=True)
    plt.figure(figsize=(10, 6))
    plt.bar(schemes, counts)
    plt.title('Distribution of Color Schemes')
    plt.xlabel('Color Scheme')
    plt.ylabel('Count')
    plt.savefig('color_scheme_distribution.png')
    plt.close()
    
    print("분포 시각화 완료: color_scheme_distribution.png")

# 예시 사용법
# generate_robust_training_data("background_images/", num_samples=500)
# visualize_pattern_distribution("./synthetic_data/metadata.json")
