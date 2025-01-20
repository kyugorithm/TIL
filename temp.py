def process_layer(layer: PSDImage, canvas_size: tuple, depth: int = 0) -> Optional[Image.Image]:
    """
    레이어를 처리하고 결과를 합성합니다.
    스마트 오브젝트와 텍스트 레이어를 구분하여 처리합니다.
    canvas_size: 전체 PSD 캔버스 크기 (width, height)
    """
    indent = "  " * depth
    print(f"{indent}{'='*30}")

    # 텍스트 레이어 체크
    if not layer.is_group() and layer.kind == 'type':
        print(f"{indent}This is a text layer: {layer.name}")
        return None

    try:
        if not layer.is_group():
            if layer.kind == 'type':
                return None
            
            # 일반 레이어 처리
            layer_image = layer.composite()
            if layer_image is None:
                print(f"{indent}Failed to composite layer: {layer.name}")
                return None

            # 투명한 캔버스 생성
            full_image = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
            
            # 레이어 이미지 위치 설정
            if layer_image:
                left = int(layer.left) if layer.left is not None else 0
                top = int(layer.top) if layer.top is not None else 0
                
                # 알파 채널이 있는 임시 이미지 생성
                temp_image = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
                temp_image.paste(layer_image, (left, top))
                
                # 알파 채널을 고려한 합성
                if layer.opacity != 255:  # 투명도가 있는 경우
                    # 투명도 적용
                    alpha = Image.new('RGBA', canvas_size, (255, 255, 255, int(layer.opacity)))
                    temp_image = Image.composite(temp_image, full_image, alpha)
                
                # 최종 이미지에 합성
                full_image = Image.alpha_composite(full_image, temp_image)
            
            return full_image
            
        else:
            # 그룹 레이어 처리
            print(f"{indent}Processing group: {layer.name}")
            group_image = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
            
            # 그룹 내의 각 레이어 처리
            for sublayer in layer:
                sublayer_image = process_layer(sublayer, canvas_size, depth + 1)
                if sublayer_image:
                    # 알파 채널을 고려한 합성
                    group_image = Image.alpha_composite(group_image, sublayer_image)
            
            # 그룹 전체의 투명도 적용
            if layer.opacity != 255:
                alpha = Image.new('RGBA', canvas_size, (255, 255, 255, int(layer.opacity)))
                blank = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
                group_image = Image.composite(group_image, blank, alpha)
            
            return group_image

    except Exception as e:
        print(f"{indent}Error processing layer {layer.name}: {e}")
        return None

def extract_full_size_groups(psd_path: str) -> Optional[Image.Image]:
    """
    PSD 파일에서 전체 크기의 레이어를 추출하고 합성합니다.
    """
    try:
        psd = PSDImage.open(psd_path)
        print(f"Processing PSD: {psd_path}")
        print(f"Canvas size: {psd.size}")
        
        # 최종 이미지를 위한 투명한 캔버스 생성
        canvas = Image.new('RGBA', psd.size, (0, 0, 0, 0))
        
        # 모든 레이어 처리 (순서대로 처리)
        for layer in list(psd):
            layer_image = process_layer(layer, psd.size)
            if layer_image:
                # 알파 채널을 고려한 합성
                canvas = Image.alpha_composite(canvas, layer_image)
        
        return canvas

    except Exception as e:
        print(f"Failed to process PSD file {psd_path}: {e}")
        return None

if __name__ == "__main__":
    file_paths = sorted(glob("psd_files/*"))
    print(f"Found {len(file_paths)} PSD files")
    
    for file_path in file_paths:
        canvas = extract_full_size_groups(file_path)
        if canvas:
            output_path = file_path.replace("psd_files", "psd_files_extracted").lower().replace(".psd", ".png")
            # PNG 저장 시 알파 채널 유지
            canvas.save(output_path, "PNG")
            print(f"Successfully saved: {output_path}")
        else:
            print(f"Failed to process: {file_path}")
