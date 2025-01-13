from PIL import Image, ImageCms
from io import BytesIO
import numpy as np
import cv2

def convert_to_adobe_rgb(image_path):
    # PIL로 이미지 열기
    img = Image.open(image_path)
    
    # Adobe RGB 프로파일 생성
    adobe_rgb_profile = ImageCms.createProfile('AdobeRGB1998')
    
    # 현재 이미지의 프로파일 확인
    if 'icc_profile' in img.info:
        # 현재 프로파일이 있는 경우
        current_profile = ImageCms.ImageCmsProfile(BytesIO(img.info['icc_profile']))
    else:
        # 프로파일이 없으면 sRGB로 가정
        current_profile = ImageCms.createProfile('sRGB')
    
    # 색 공간 변환
    transform = ImageCms.buildTransformFromOpenProfiles(
        current_profile, adobe_rgb_profile, 'RGB', 'RGB')
    img_adobe = ImageCms.applyTransform(img, transform)
    
    # 프로파일 포함해서 저장
    img_adobe.save('output_adobe.png', icc_profile=adobe_rgb_profile.tobytes())
    
    return "변환 완료"

# 사용 예
result = convert_to_adobe_rgb('input.jpg')
print(result)
