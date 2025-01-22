import numpy as np
from PIL import Image

def convert_5d_cmyka_to_3d_rgb_optimized(layer_array):
    # 5차원 배열을 3차원으로 압축 (1, h, w, 5, 1) -> (h, w, 5)
    working_array = np.squeeze(layer_array)
    
    # CMYK 채널과 알파 채널을 한번에 분리
    c, m, y, k, alpha = np.moveaxis(working_array, -1, 0)
    
    # CMYK to RGB 변환을 벡터화된 연산으로 처리
    # 255를 곱하기 전에 먼저 계산하여 정밀도 유지
    r = 1.0 - np.minimum(1.0, c + k)
    g = 1.0 - np.minimum(1.0, m + k)
    b = 1.0 - np.minimum(1.0, y + k)
    
    # 알파 블렌딩을 벡터화된 연산으로 처리
    alpha = alpha.clip(0, 1)  # 알파값을 0~1 범위로 제한
    
    # 이미지 선명도를 위한 대비 향상
    contrast_factor = 1.2  # 대비 증가 factor
    r = ((r - 0.5) * contrast_factor + 0.5).clip(0, 1)
    g = ((g - 0.5) * contrast_factor + 0.5).clip(0, 1)
    b = ((b - 0.5) * contrast_factor + 0.5).clip(0, 1)
    
    # alpha 블렌딩 적용 (배경은 흰색)
    r = r * alpha + (1.0 - alpha)
    g = g * alpha + (1.0 - alpha)
    b = b * alpha + (1.0 - alpha)
    
    # 최종 RGB 배열 생성
    rgb_array = np.stack([r, g, b], axis=-1)
    
    # 0~1 범위의 float를 0~255 범위의 uint8로 변환
    rgb_array = (rgb_array * 255).astype(np.uint8)
    
    return rgb_array

# 노이즈 제거와 선명도 향상을 위한 후처리 함수
def enhance_image(rgb_array):
    # 이진화를 위한 임계값 설정 (적응형)
    threshold = np.mean(rgb_array) * 0.9  # 평균값의 90%를 임계값으로 사용
    
    # 채널별로 이진화 적용
    binary_mask = np.mean(rgb_array, axis=2) < threshold
    enhanced = np.zeros_like(rgb_array)
    
    # 마스크를 기반으로 값 설정
    enhanced[binary_mask] = 0  # 어두운 부분은 완전한 검정
    enhanced[~binary_mask] = 255  # 밝은 부분은 완전한 흰색
    
    return enhanced

# 사용 예시
converted_rgb = convert_5d_cmyka_to_3d_rgb_optimized(layer_array)
enhanced_rgb = enhance_image(converted_rgb)
rgb_image = Image.fromarray(enhanced_rgb)
