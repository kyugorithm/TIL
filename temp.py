import numpy as np
from PIL import Image

def convert_5d_cmyka_to_3d_rgb(layer_array):
    # 5차원 배열을 사용하기 쉽게 압축
    # (1, h, w, 5, 1) -> (h, w, 5)
    working_array = np.squeeze(layer_array)
    
    height, width, _ = working_array.shape
    
    # 새로운 RGB 배열 생성
    rgb_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # CMYK 채널과 알파 채널 분리
    c = working_array[:, :, 0]
    m = working_array[:, :, 1]
    y = working_array[:, :, 2]
    k = working_array[:, :, 3]
    alpha = working_array[:, :, 4]
    
    # CMYK에서 RGB로 변환하면서 알파 채널 고려
    # 알파 채널이 0인 부분은 배경색(흰색)으로 처리
    for i in range(height):
        for j in range(width):
            if alpha[i, j] > 0:  # 투명하지 않은 부분만 처리
                # CMYK 값이 높을수록 어둡기 때문에 255에서 뺌
                r = 255 - np.minimum(255, (c[i,j] + k[i,j]))
                g = 255 - np.minimum(255, (m[i,j] + k[i,j]))
                b = 255 - np.minimum(255, (y[i,j] + k[i,j]))
                
                # 알파 채널을 고려한 블렌딩
                alpha_ratio = alpha[i,j] / 255
                rgb_array[i,j,0] = int(r * alpha_ratio + 255 * (1 - alpha_ratio))
                rgb_array[i,j,1] = int(g * alpha_ratio + 255 * (1 - alpha_ratio))
                rgb_array[i,j,2] = int(b * alpha_ratio + 255 * (1 - alpha_ratio))
            else:
                # 완전 투명한 부분은 흰색으로
                rgb_array[i,j] = [255, 255, 255]
    
    return rgb_array

# 사용 예시
converted_rgb = convert_5d_cmyka_to_3d_rgb(layer_array)
rgb_image = Image.fromarray(converted_rgb)
