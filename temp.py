from psd_tools import PSDImage
from PIL import Image

def composite_without_text_and_small(psd_path, size_threshold=0.2):
    psd = PSDImage.open(psd_path)
    visible_layers = []
    
    # 먼저 가장 큰 레이어의 크기를 찾습니다
    max_area = 0
    for layer in psd:
        if layer.is_group():
            for sublayer in layer.descendants():
                area = sublayer.width * sublayer.height
                max_area = max(max_area, area)
        else:
            area = layer.width * layer.height
            max_area = max(max_area, area)
    
    # 레이어를 순회하면서 조건에 맞는 것만 저장
    for layer in psd:
        if layer.is_group():
            for sublayer in layer.descendants():
                # 텍스트가 아니고, 보이며, 크기가 충분히 큰 레이어만 선택
                area = sublayer.width * sublayer.height
                if (sublayer.kind != 'type' and 
                    sublayer.visible and 
                    area >= max_area * size_threshold):
                    layer_image = sublayer.composite()
                    if layer_image:
                        visible_layers.append({
                            'image': layer_image,
                            'position': (sublayer.left, sublayer.top),
                            'area': area  # 디버깅을 위해 면적 정보도 저장
                        })
        elif layer.kind != 'type' and layer.visible:
            area = layer.width * layer.height
            if area >= max_area * size_threshold:
                layer_image = layer.composite()
                if layer_image:
                    visible_layers.append({
                        'image': layer_image,
                        'position': (layer.left, layer.top),
                        'area': area
                    })
    
    # 디버깅을 위한 정보 출력
    print(f"최대 이미지 크기: {max_area} px²")
    print(f"크기 임계값: {max_area * size_threshold} px²")
    print(f"선택된 레이어 수: {len(visible_layers)}")
    for i, layer in enumerate(visible_layers):
        print(f"레이어 {i+1} 크기: {layer['area']} px²")
    
    # 최종 이미지 생성
    result = Image.new('RGBA', (psd.width, psd.height), (0, 0, 0, 0))
    
    # 저장된 레이어들을 순서대로 합성
    for layer_info in visible_layers:
        if layer_info['image'].mode == 'RGBA':
            result.paste(layer_info['image'], layer_info['position'], layer_info['image'])
        else:
            result.paste(layer_info['image'], layer_info['position'])
    
    return result

# 사용 예시
# size_threshold는 0.2 (20%)로 설정되어 있지만 필요에 따라 조절 가능
result_image = composite_without_text_and_small('example.psd', size_threshold=0.2)
result_image.save('result_filtered.png')
