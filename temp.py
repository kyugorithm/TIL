네, PSD 파일에서는 각 레이어가 순서(zIndex) 정보를 가지고 있습니다. 실제로 PSDImage에서 이 정보를 활용할 수 있습니다.

레이어의 깊이(depth)와 순서를 확인하고 활용하는 코드를 작성해보겠습니다:

```python
def extract_full_size_groups(psd_path):
    psd = PSDImage.open(psd_path)
    
    # 각 레이어의 정보를 수집
    layer_info = []
    for i, layer in enumerate(psd):
        if not layer.is_visible():
            continue
            
        layer_image = layer.composite()
        if layer_image.width >= psd.width and layer_image.height >= psd.height:
            # 레이어의 인덱스, 이름, depth 정보 수집
            depth = getattr(layer, '_index', i)  # 내부 인덱스 활용
            layer_info.append({
                'layer': layer,
                'index': i,
                'depth': depth,
                'name': layer.name
            })
            print(f"배경 레이어 발견: {layer.name}")
            print(f"- Index: {i}")
            print(f"- Depth: {depth}")
            print(f"- Size: {layer_image.size}")
            print("--------------------")
    
    # depth를 기준으로 정렬 (오름차순 - 가장 아래 레이어부터)
    sorted_layers = sorted(layer_info, key=lambda x: x['depth'])
    
    if sorted_layers:
        # 가장 아래에 있는 배경 레이어 사용
        bottom_layer = sorted_layers[0]['layer']
        print(f"선택된 배경 레이어: {bottom_layer.name}")
        print(f"- Depth: {sorted_layers[0]['depth']}")
        
        layer_image = bottom_layer.composite()
        if layer_image.mode == 'CMYK':
            layer_image = layer_image.convert('RGB')
            
        canvas = Image.new('RGB', (psd.width, psd.height), (0, 0, 0, 0))
        left = int(bottom_layer.left) if bottom_layer.left is not None else 0
        top = int(bottom_layer.top) if bottom_layer.top is not None else 0
        canvas.paste(layer_image, (left, top))
        return canvas
    
    return None

# 실행
file_paths = sorted(glob("psd_files/*"))[-1:-1]
h_std = 1024
for file_path in file_paths:
    canvas = extract_full_size_groups(file_path)
    if canvas:
        output_path = file_path.replace("psd_files", "psd_files_extracted").lower().replace(".psd", ".png")
        canvas.save(output_path)
        print(f"{output_path} 저장 완료.")
```

이 코드의 주요 특징:

1. `_index` 속성을 통해 레이어의 실제 depth 정보를 가져옵니다
2. 모든 배경 크기 레이어의 정보를 수집하고 출력합니다
3. depth를 기준으로 정렬하여 가장 아래에 있는 레이어를 선택합니다

만약 더 자세한 레이어 정보를 보고 싶다면:

```python
def print_layer_info(layer, indent=''):
    """레이어의 상세 정보를 출력하는 함수"""
    print(f"{indent}레이어 이름: {layer.name}")
    print(f"{indent}- Index: {getattr(layer, '_index', 'N/A')}")
    print(f"{indent}- 위치: ({layer.left}, {layer.top})")
    print(f"{indent}- 크기: {layer.bbox}")
    print(f"{indent}- 불투명도: {layer.opacity}")
    print(f"{indent}- 보임 여부: {layer.is_visible()}")
    
    if hasattr(layer, 'layers'):  # 그룹 레이어인 경우
        print(f"{indent}- 하위 레이어:")
        for sublayer in layer.layers:
            print_layer_info(sublayer, indent + '  ')

# PSD 파일을 열고 모든 레이어 정보 출력
psd = PSDImage.open(psd_path)
print("=== 전체 레이어 구조 ===")
for layer in psd:
    print_layer_info(layer)
```

이렇게 하면 레이어의 계층 구조와 각 레이어의 상세 정보를 모두 확인할 수 있습니다. 이를 통해:
1. 실제 레이어의 순서 확인
2. 그룹 레이어 내부의 구조 파악
3. 각 레이어의 위치와 크기 정보 확인

이 정보들을 바탕으로 원하는 배경 레이어를 정확하게 선택할 수 있습니다.​​​​​​​​​​​​​​​​
