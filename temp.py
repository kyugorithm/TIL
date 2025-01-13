import cv2
from PIL import Image
from PIL.ExifTags import TAGS
import os

def print_image_info(image_path):
    # 파일 기본 정보
    file_size = os.path.getsize(image_path) / (1024 * 1024)  # MB로 변환
    print(f"파일 크기: {file_size:.2f} MB")

    # CV2로 읽어서 확인
    cv_img = cv2.imread(image_path)
    print(f"이미지 크기 (width x height): {cv_img.shape[1]} x {cv_img.shape[0]}")
    print(f"채널 수: {cv_img.shape[2]}")
    print(f"데이터 타입: {cv_img.dtype}")

    # PIL로 추가 정보 확인
    pil_img = Image.open(image_path)
    print(f"이미지 모드: {pil_img.mode}")
    print(f"이미지 형식: {pil_img.format}")
    
    # EXIF 데이터 확인 (있는 경우)
    try:
        exif = pil_img.getexif()
        if exif:
            print("\nEXIF 정보:")
            for tag_id in exif:
                tag = TAGS.get(tag_id, tag_id)
                data = exif.get(tag_id)
                print(f"{tag}: {data}")
    except:
        print("EXIF 데이터 없음")

    # 색상 분포 확인
    print("\n색상 채널별 평균값:")
    b, g, r = cv2.split(cv_img)
    print(f"R 채널 평균: {r.mean():.2f}")
    print(f"G 채널 평균: {g.mean():.2f}")
    print(f"B 채널 평균: {b.mean():.2f}")

# 사용 예
print_image_info('이미지경로.jpg')
