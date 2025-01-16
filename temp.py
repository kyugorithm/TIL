from psd_tools import PSDImage
from PIL import Image

def extract_full_size_groups(psd_path):
    psd = PSDImage.open(psd_path)
    canvas_size = (psd.width, psd.height)
    print(f"캔버스 크기: {canvas_size}")
    
    # 캔버스 크기와 동일한 그룹/레이어 찾기
    full_size_layers = []
    
    for layer in psd:
        if layer.width == psd.width and layer.height == psd.height:
            print(f"전체 크기 레이어 발견: {layer.name} (그룹: {layer.is_group()})")
            # 그룹이든 일반 레이어든 composite() 사용
            layer_image = layer.composite()
            if layer_image:
                full_size_layers.append({
                    'name': layer.name,
                    'image': layer_image,
                    'is_group': layer.is_group()
                })

    # 각 그룹/레이어를 개별 파일로 저장
    for layer_info in full_size_layers:
        filename = f"{layer_info['name']}.png"
        # 파일명에 사용할 수 없는 문자 처리
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))
        print(f"저장 중: {filename}")
        layer_info['image'].save(filename)
        
    return len(full_size_layers)

# 사용 예시
num_saved = extract_full_size_groups('example.psd')
print(f"총 {num_saved}개의 전체 크기 레이어/그룹을 저장했습니다.")
