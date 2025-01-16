이 문제를 해결하기 위해 몇 가지 부분을 체크하고 수정해보겠습니다.

1. CMYK 이미지 처리 관련:
- 현재 코드에서 CMYK를 RGB로 변환하는 부분은 있지만, 레이어별로 처리할 때 색상 공간이 올바르게 유지되지 않을 수 있습니다.
- 각 레이어의 변환 과정에서 색상 정보가 왜곡될 수 있습니다.

2. 좌표 계산 관련:
- `left`와 `top` 좌표 계산 부분에서 문제가 있을 수 있습니다. 현재는 단순히 layer.left와 layer.top을 사용하고 있는데, 이는 PSD 파일의 특성에 따라 부정확할 수 있습니다.

다음과 같이 코드를 수정해보세요:

```python
def extract_full_size_groups(psd_path):
    psd = PSDImage.open(psd_path)
    
    # CMYK 모드 처리를 명시적으로
    composite_image = psd.composite()
    if composite_image.mode == 'CMYK':
        composite_image = composite_image.convert('RGB')
    
    canvas_size = (psd.width, psd.height)
    canvas = Image.new('RGB', (psd.width, psd.height), (0, 0, 0, 0))
    
    print(f"캔버스 크기: {canvas_size}")
    
    for layer in psd:
        if not layer.is_visible():
            continue
            
        layer_image = layer.composite()
        
        # CMYK 모드 처리를 더 엄격하게
        if layer_image.mode == 'CMYK':
            layer_image = layer_image.convert('RGB')
        elif layer_image.mode != 'RGB':
            layer_image = layer_image.convert('RGB')
            
        # 레이어 위치 보정
        left = int(layer.left) if layer.left is not None else 0
        top = int(layer.top) if layer.top is not None else 0
        
        # 레이어 크기가 캔버스보다 큰 경우 체크
        if layer_image.width >= psd.width and layer_image.height >= psd.height:
            print(f"- 원본 사이즈 레이어 발견: {layer.name} (그룹: {layer.is_group()})")
            
            # 레이어 위치가 음수인 경우 보정
            if left < 0:
                layer_image = layer_image.crop((-left, 0, layer_image.width, layer_image.height))
                left = 0
            if top < 0:
                layer_image = layer_image.crop((0, -top, layer_image.width, layer_image.height))
                top = 0
                
            # 레이어 크기가 캔버스를 벗어나는 경우 크롭
            if left + layer_image.width > canvas.width:
                layer_image = layer_image.crop((0, 0, canvas.width - left, layer_image.height))
            if top + layer_image.height > canvas.height:
                layer_image = layer_image.crop((0, 0, layer_image.width, canvas.height - top))
            
            canvas.paste(layer_image, (left, top))
            
    return canvas
```

주요 수정사항:
1. CMYK -> RGB 변환을 더 엄격하게 처리
2. 레이어 위치 값을 정수로 변환하여 오차 방지
3. 음수 좌표 보정
4. 캔버스 크기를 벗어나는 경우 처리

또한, 문제가 되는 특정 PSD 파일에 대해 다음을 확인해보세요:
1. `print(layer.left, layer.top)` 을 추가하여 각 레이어의 실제 위치 값 확인
2. `print(layer_image.size)` 로 각 레이어의 크기 확인
3. `print(layer_image.mode)` 로 각 레이어의 색상 모드 확인

이렇게 하면 문제의 원인을 더 정확히 파악할 수 있을 것입니다.​​​​​​​​​​​​​​​​

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
