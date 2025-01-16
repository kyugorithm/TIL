from psd_tools import PSDImage
from PIL import Image

def composite_without_text(psd_path):
    # PSD 파일 열기
    psd = PSDImage.open(psd_path)
    
    # 모든 레이어를 순회하면서 텍스트가 아닌 레이어만 저장
    visible_layers = []
    
    for layer in psd:
        if layer.is_group():
            # 그룹의 경우 하위 레이어들을 확인
            for sublayer in layer.descendants():
                if sublayer.kind != 'type' and sublayer.visible:
                    # 텍스트가 아니고 보이는 레이어만 저장
                    layer_image = sublayer.composite()
                    if layer_image:
                        visible_layers.append({
                            'image': layer_image,
                            'position': (sublayer.left, sublayer.top)
                        })
        elif layer.kind != 'type' and layer.visible:
            # 텍스트가 아니고 보이는 레이어만 저장
            layer_image = layer.composite()
            if layer_image:
                visible_layers.append({
                    'image': layer_image,
                    'position': (layer.left, layer.top)
                })
    
    # 최종 이미지 생성 (PSD 크기와 동일하게)
    result = Image.new('RGBA', (psd.width, psd.height), (0, 0, 0, 0))
    
    # 저장된 레이어들을 순서대로 합성
    for layer_info in visible_layers:
        if layer_info['image'].mode == 'RGBA':
            result.paste(layer_info['image'], layer_info['position'], layer_info['image'])
        else:
            result.paste(layer_info['image'], layer_info['position'])
    
    return result

# 사용 예시
result_image = composite_without_text('example.psd')
result_image.save('result_without_text.png')
