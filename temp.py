from psd_tools import PSDImage
from PIL import Image
from glob import glob
from typing import Optional

def process_layer(layer: PSDImage, canvas_size: tuple, depth: int = 0) -> Optional[Image.Image]:
    """
    레이어를 처리하고 결과를 출력합니다.
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
            # 일반 레이어 처리
            layer_image = layer.composite()
            if layer_image is None:
                print(f"{indent}Failed to composite layer: {layer.name}")
                return None

            # 레이어 정보 출력
            print(f"{indent}Layer Name: {layer.name}")
            print(f"{indent}Kind: {layer.kind}")
            print(f"{indent}Size: {layer.size}")
            print(f"{indent}Position: (left: {layer.left}, top: {layer.top})")
            
            # 투명한 캔버스 생성
            full_image = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
            
            # 레이어 이미지를 올바른 위치에 배치
            if layer_image:
                left = int(layer.left) if layer.left is not None else 0
                top = int(layer.top) if layer.top is not None else 0
                full_image.paste(layer_image, (left, top), layer_image)
            
            return full_image
        
        else:
            # 그룹 레이어 처리
            print(f"{indent}Processing group: {layer.name}")
            group_image = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
            
            # 그룹 내의 각 레이어 처리
            for sublayer in layer:
                sublayer_image = process_layer(sublayer, canvas_size, depth + 1)
                if sublayer_image:
                    # 합성 모드를 고려하여 레이어 합성
                    group_image = Image.alpha_composite(group_image, sublayer_image)
            
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
        
        # 모든 레이어 처리 (역순으로 처리하여 레이어 순서 유지)
        for layer in reversed(list(psd)):
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
            canvas.save(output_path)
            print(f"Successfully saved: {output_path}")
        else:
            print(f"Failed to process: {file_path}")
