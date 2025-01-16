from psd_tools import PSDImage
from PIL import Image

def find_actual_background(psd_path, size_threshold=0.2):
    psd = PSDImage.open(psd_path)
    canvas_size = (psd.width, psd.height)
    canvas_area = psd.width * psd.height
    print(f"캔버스 크기: {canvas_size}")
    
    def process_layer(layer):
        layer_area = layer.width * layer.height
        if layer_area / canvas_area < size_threshold:
            return None
            
        if layer.is_group():
            visible_layers = []
            for sublayer in layer.descendants():
                if sublayer.visible:
                    sub_area = sublayer.width * sublayer.height
                    if sub_area / canvas_area >= size_threshold:
                        layer_image = sublayer.composite()
                        if layer_image:
                            visible_layers.append({
                                'image': layer_image,
                                'position': (sublayer.left, sublayer.top)
                            })
            return visible_layers if visible_layers else None
        else:
            layer_image = layer.composite()
            return [{'image': layer_image, 'position': (layer.left, layer.top)}] if layer_image else None

    # 캔버스 크기와 동일한 레이어 찾기
    background_candidates = []
    for layer in psd:
        if layer.width == psd.width and layer.height == psd.height:
            print(f"전체 크기 레이어 발견: {layer.name} (그룹: {layer.is_group()})")
            result = process_layer(layer)
            if result:
                background_candidates.extend(result)

    # 결과 이미지 생성
    if background_candidates:
        result = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
        for layer_info in background_candidates:
            if layer_info['image'].mode == 'RGBA':
                result.paste(layer_info['image'], layer_info['position'], layer_info['image'])
            else:
                result.paste(layer_info['image'], layer_info['position'])
        return result
    
    return None

# 사용 예시
background = find_actual_background('example.psd', size_threshold=0.2)
if background:
    background.save('background_only.png')
