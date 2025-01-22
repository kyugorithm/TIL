import numpy as np
from PIL import Image

def convert_cmyka_to_rgb(layer_array):
    # layer_array의 shape은 (height, width, 5)
    # 채널별로 분리 (이미 3차원이므로 추가적인 squeeze가 필요 없음)
    c = layer_array[..., 0]  # Cyan 채널
    m = layer_array[..., 1]  # Magenta 채널
    y = layer_array[..., 2]  # Yellow 채널
    k = layer_array[..., 3]  # Key(Black) 채널
    a = layer_array[..., 4]  # Alpha 채널
    
    # CMYK에서 RGB로 변환 (벡터화된 연산 사용)
    # 0~1 범위의 값을 가정
    r = 1.0 - np.minimum(1.0, c + k)
    g = 1.0 - np.minimum(1.0, m + k)
    b = 1.0 - np.minimum(1.0, y + k)
    
    # 알파 채널 적용 (배경은 흰색)
    r = r * a + (1.0 - a)
    g = g * a + (1.0 - a)
    b = b * a + (1.0 - a)
    
    # RGB 채널을 하나의 배열로 합치기
    rgb_array = np.stack([r, g, b], axis=-1)
    
    # 0~1 범위를 0~255 범위로 변환
    rgb_array = (rgb_array * 255).astype(np.uint8)
    
    return rgb_array
