def process_layer(layer: PSDImage, depth: int = 0) -> Optional[Image.Image]:
    """
    레이어를 처리하고 결과를 출력합니다.
    스마트 오브젝트와 텍스트 레이어를 구분하여 처리합니다.
    """
    indent = "  " * depth
    print(f"{indent}{'='*30}")
    
    try:
        layer_image = layer.composite()
        w, h = layer_image.size
        h_new = 384
        w_new = int(w * (h_new / h))
        layer_image = layer_image.resize((w_new, h_new))
        layer_image.save(f"layers/{layer.name}.png")
    except Exception as e:
        print(f"{indent}Failed to composite layer {layer.name}: {e}")
        return None

    # 텍스트 레이어 체크
    if not layer.is_group() and layer.kind == 'type':
        print(f"{indent}This is a text layer.")
        return None
    
    # 스마트 오브젝트 체크 및 처리
    if not layer.is_group() and hasattr(layer, 'smart_object'):
        print(f"{indent}Smart Object detected: {layer.name}")
        try:
            # 스마트 오브젝트 내부의 텍스트 레이어 확인
            if check_smart_object_for_text(layer.smart_object):
                print(f"{indent}Smart Object contains text layers")
                return None
            else:
                print(f"{indent}Processing Smart Object as image")
                return process_smart_object(layer)
        except Exception as e:
            print(f"{indent}Failed to process Smart Object: {e}")
            return None

    # 일반 레이어 정보 출력
    if not layer.is_group():
        print(f"{indent}Layer Name: {layer.name}")
        print(f"{indent}Is Group: {layer.is_group()}")
        print(f"{indent}Kind: {layer.kind}")
        print(f"{indent}Visible: {layer.is_visible()}")
        print(f"{indent}Opacity: {layer.opacity}")
        print(f"{indent}Blend Mode: {layer.blend_mode}")
        print(f"{indent}Size: {layer.size}")
        print(f"{indent}Position: (left: {layer.left}, top: {layer.top}, right: {layer.right}, bottom: {layer.bottom})")
        return layer_image

    # 그룹 레이어 처리
    if layer.is_group():
        group_image = Image.new('RGBA', (layer.width, layer.height), (0, 0, 0, 0))
        for sublayer in layer:
            sublayer_image = process_layer(sublayer, depth + 1)
            if sublayer_image:
                left = int(sublayer.left) if sublayer.left is not None else 0
                top = int(sublayer.top) if sublayer.top is not None else 0
                group_image.paste(sublayer_image, (left, top), sublayer_image)
        return group_image

    print(f"{indent}{'='*30}")
    return layer_image

def check_smart_object_for_text(smart_object) -> bool:
    """
    스마트 오브젝트 내부에 텍스트 레이어가 있는지 확인합니다.
    """
    try:
        # 스마트 오브젝트의 내부 구조를 확인
        for layer in smart_object.layers:
            if layer.kind == 'type':
                return True
            if layer.is_group():
                if check_smart_object_for_text(layer):
                    return True
        return False
    except Exception:
        return False

def process_smart_object(layer) -> Optional[Image.Image]:
    """
    스마트 오브젝트를 처리하고 이미지를 반환합니다.
    """
    try:
        return layer.smart_object.composite()
    except Exception:
        return None

def extract_full_size_groups(psd_path: str) -> Optional[Image.Image]:
    """
    PSD 파일에서 전체 크기의 레이어 추출합니다.
    """
    try:
        psd = PSDImage.open(psd_path)
    except Exception as e:
        print(f"Failed to open PSD file {psd_path}: {e}")
        return None

    canvas = Image.new('RGBA', (psd.width, psd.height), (0, 0, 0, 0))
    for layer in psd:
        layer_image = process_layer(layer)
        if layer_image:
            left = int(layer.left) if layer.left is not None else 0
            top = int(layer.top) if layer.top is not None else 0
            canvas.paste(layer_image, (left, top), layer_image)

    return canvas

if __name__ == "__main__":
    file_paths = sorted(glob("psd_files/*"))
    print(file_paths)
    
    for file_path in file_paths:
        canvas = extract_full_size_groups(file_path)
        if canvas:
            output_path = file_path.replace("psd_files", "psd_files_extracted").lower().replace(".psd", ".png")
            canvas.save(output_path)
            print(f"Saved: {output_path}")
