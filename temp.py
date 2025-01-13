from typing import List, Tuple
from PIL import Image

def adjust_row_images(row_images: List[Tuple[Image.Image, int, int]], target_width: int, spacing: int) -> List[Image.Image]:
    """한 행의 이미지들이 target_width에 맞도록 크기를 조정"""
    total_width = sum(w for _, w, _ in row_images) + (len(row_images) - 1) * spacing
    if total_width <= target_width:
        return [img for img, _, _ in row_images]
    
    # 비율을 유지하면서 전체 너비를 맞추기 위한 스케일 계산
    scale = (target_width - (len(row_images) - 1) * spacing) / sum(w for _, w, _ in row_images)
    resized_images = []
    
    for img, w, h in row_images:
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized_images.append(img.resize((new_w, new_h), Image.Resampling.LANCZOS))
    
    return resized_images

def create_collage_with_margin(images: List[Image.Image], text_length: int, margin: int = 30, fixed_width: int = 1000) -> Image.Image:
    """마진이 있는 콜라주를 생성하는 함수"""
    if not images:
        raise ValueError("이미지 리스트가 비어있습니다.")

    collage_width = fixed_width
    available_width = collage_width - 2 * margin
    
    # 이미지 전처리 및 초기 스케일링
    processed_images = []
    for img in images:
        scale = min(available_width/3/img.width, available_width/3/img.height)
        if scale < 1:
            new_width = int(0.9 * img.width * scale)
            new_height = int(0.9 * img.height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        processed_images.append((img, img.width, img.height))

    # 행별로 이미지 배치
    rows = []
    current_row = []
    current_row_width = 0
    
    for img, width, height in processed_images:
        # 새 이미지를 추가했을 때의 총 너비 계산
        new_row_width = current_row_width + width + (len(current_row) * margin)
        
        if new_row_width <= available_width or not current_row:
            current_row.append((img, width, height))
            current_row_width = new_row_width
        else:
            # 현재 행이 가득 차면, 조정 후 새 행 시작
            rows.append(adjust_row_images(current_row, available_width, margin))
            current_row = [(img, width, height)]
            current_row_width = width
    
    # 마지막 행 처리
    if current_row:
        rows.append(adjust_row_images(current_row, available_width, margin))

    # 전체 높이 계산 및 캔버스 생성
    total_height = margin
    for row in rows:
        total_height += max(img.height for img in row) + margin

    canvas = Image.new('RGB', (collage_width, total_height), 'black')
    
    # 이미지 배치
    current_y = margin
    for row in rows:
        current_x = margin
        row_height = max(img.height for img in row)
        
        for img in row:
            canvas.paste(img, (current_x, current_y))
            current_x += img.width + margin
        
        current_y += row_height + margin

    return canvas

def create_collage_compact(images: List[Image.Image], text_length: int, fixed_width: int = 1000) -> Image.Image:
    """마진 없이 이미지 간 10픽셀 간격으로 콜라주를 생성하는 함수"""
    if not images:
        raise ValueError("이미지 리스트가 비어있습니다.")

    SPACING = 10
    collage_width = fixed_width
    
    # 이미지 전처리 및 초기 스케일링
    processed_images = []
    for img in images:
        scale = min(collage_width/3/img.width, collage_width/3/img.height)
        if scale < 1:
            new_width = int(0.95 * img.width * scale)
            new_height = int(0.95 * img.height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        processed_images.append((img, img.width, img.height))

    # 행별로 이미지 배치
    rows = []
    current_row = []
    current_row_width = 0
    
    for img, width, height in processed_images:
        new_row_width = current_row_width + width + (len(current_row) * SPACING)
        
        if new_row_width <= collage_width or not current_row:
            current_row.append((img, width, height))
            current_row_width = new_row_width
        else:
            # 현재 행이 가득 차면, 조정 후 새 행 시작
            rows.append(adjust_row_images(current_row, collage_width, SPACING))
            current_row = [(img, width, height)]
            current_row_width = width
    
    # 마지막 행 처리
    if current_row:
        rows.append(adjust_row_images(current_row, collage_width, SPACING))

    # 전체 높이 계산 및 캔버스 생성
    total_height = 0
    for row in rows:
        total_height += max(img.height for img in row) + SPACING
    
    if total_height > SPACING:
        total_height -= SPACING  # 마지막 spacing 제거

    canvas = Image.new('RGB', (collage_width, total_height), 'black')
    
    # 이미지 배치
    current_y = 0
    for row in rows:
        current_x = 0
        row_height = max(img.height for img in row)
        
        for img in row:
            canvas.paste(img, (current_x, current_y))
            current_x += img.width + SPACING
        
        current_y += row_height + SPACING

    return canvas
