from PIL import Image, ImageCms
import cv2
import numpy as np

def get_icc_profile(image_path):
    # PIL로 이미지 열기
    img = Image.open(image_path)
    
    # ICC 프로파일 확인
    if 'icc_profile' in img.info:
        profile = ImageCms.ImageCmsProfile(BytesIO(img.info['icc_profile']))
        print(f"색 공간: {profile.profile.profile_description}")
        return profile
    else:
        print("ICC 프로파일이 없습니다")
        return None

def convert_colorspace(image_path, target_profile='sRGB'):
    img = Image.open(image_path)
    
    if 'icc_profile' in img.info:
        # 현재 프로파일
        input_profile = ImageCms.ImageCmsProfile(BytesIO(img.info['icc_profile']))
        
        # 대상 프로파일
        output_profile = ImageCms.createProfile(target_profile)
        
        # 색 공간 변환
        img_converted = ImageCms.profileToProfile(img, input_profile, output_profile)
        return np.array(img_converted)
    
    return np.array(img)
