from psd_tools import PSDImage
from PIL import Image
import PIL.ImageCms as ImageCms
from io import BytesIO

def composite_with_color_management(psd_path, size_threshold=0.2):
    psd = PSDImage.open(psd_path)
    
    # PSD 파일의 색공간 정보 확인
    color_mode = psd.color_mode
    print(f"PSD 색상 모드: {color_mode}")
    
    # 색공간 관련 추가 정보 확인
    if hasattr(psd, 'image_resources'):
        for resource in psd.image_resources:
            print(f"리소스 ID: {resource.resource_id}")
            if resource.name:
                print(f"리소스 이름: {resource.name}")
    
    # 디버깅을 위한 정보 출력
    print("PSD 속성:")
    for attr in dir(psd):
        if not attr.startswith('_'):  # 내부 속성 제외
            try:
                value = getattr(psd, attr)
                if not callable(value):  # 메서드 제외
                    print(f"{attr}: {value}")
            except Exception as e:
                print(f"{attr}: 접근 불가 ({e})")
    
    # 나머지 코드는 이전과 동일...
    # 여기서 색공간 정보를 기반으로 처리 로직 추가 가능

# 테스트
psd_path = 'example.psd'
result_image = composite_with_color_management(psd_path)
