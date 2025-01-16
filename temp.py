from psd_tools import PSDImage
from PIL import Image
import PIL.ImageCms as ImageCms

def composite_with_color_management(psd_path, size_threshold=0.2):
    psd = PSDImage.open(psd_path)
    visible_layers = []
    
    # 최대 면적 계산 (이전과 동일)
    max_area = 0
    for layer in psd:
        if layer.is_group():
            for sublayer in layer.descendants():
                area = sublayer.width * sublayer.height
                max_area = max(max_area, area)
        else:
            area = layer.width * layer.height
            max_area = max(max_area, area)
    
    def process_image(image, area):
        if image is None:
            return None
            
        # ICC 프로파일 확인
        if 'icc_profile' in image.info:
            try:
                # 현재 프로파일 생성
                current_profile = ImageCms.ImageCmsProfile(BytesIO(image.info['icc_profile']))
                profile_name = ImageCms.getProfileName(current_profile).strip()
                
                print(f"발견된 ICC 프로파일: {profile_name}")
                
                # Adobe RGB 프로파일인 경우에만 변환
                if 'Adobe RGB' in profile_name:
                    srgb_profile = ImageCms.createProfile('sRGB')
                    transform = ImageCms.buildTransformFromOpenProfiles(
                        current_profile, srgb_profile,
                        'RGB', 'RGB'
                    )
                    
                    if image.mode == 'RGBA':
                        r, g, b, a = image.split()
                        rgb_image = Image.merge('RGB', (r, g, b))
                        converted_rgb = ImageCms.applyTransform(rgb_image, transform)
                        image = Image.merge('RGBA', (*converted_rgb.split(), a))
                    else:
                        image = ImageCms.applyTransform(image, transform)
                    
                    print("Adobe RGB에서 sRGB로 변환 완료")
            except Exception as e:
                print(f"색공간 변환 중 오류 발생: {e}")
        
        return image if area >= max_area * size_threshold else None
    
    # 레이어 처리
    for layer in psd:
        if layer.is_group():
            for sublayer in layer.descendants():
                if sublayer.kind != 'type' and sublayer.visible:
                    area = sublayer.width * sublayer.height
                    layer_image = sublayer.composite()
                    processed_image = process_image(layer_image, area)
                    if processed_image:
                        visible_layers.append({
                            'image': processed_image,
                            'position': (sublayer.left, sublayer.top)
                        })
        elif layer.kind != 'type' and layer.visible:
            area = layer.width * layer.height
            layer_image = layer.composite()
            processed_image = process_image(layer_image, area)
            if processed_image:
                visible_layers.append({
                    'image': processed_image,
                    'position': (layer.left, layer.top)
                })
    
    # 결과 이미지 생성
    result = Image.new('RGBA', (psd.width, psd.height), (0, 0, 0, 0))
    
    for layer_info in visible_layers:
        if layer_info['image'].mode == 'RGBA':
            result.paste(layer_info['image'], layer_info['position'], layer_info['image'])
        else:
            result.paste(layer_info['image'], layer_info['position'])
    
    return result

# 사용 예시
result_image = composite_with_color_management('example.psd')
result_image.save('result_filtered.png')
