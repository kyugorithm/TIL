from typing import List, Tuple
from PIL import Image

def adjust_row_images(row_images: List[Tuple[Image.Image, int, int]], target_width: int) -> List[Image.Image]:
    """한 행의 이미지들이 target_width에 맞도록 크기를 조정"""
    IMAGE_SPACING = 10  # 이미지 간 고정 간격
    
    total_width = sum(w for _, w, _ in row_images) + (len(row_images) - 1) * IMAGE_SPACING
    if total_width <= target_width:
        return [img for img, _, _ in row_images]
    
    # 비율을 유지하면서 전체 너비를 맞추기 위한 스케일 계산
    scale = (target_width - (len(row_images) - 1) * IMAGE_SPACING) / sum(w for _, w, _ in row_images)
    resized_images = []
    
    for img, w, h in row_images:
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized_images.append(img.resize((new_w, new_h), Image.Resampling.LANCZOS))
    
    return resized_images

def create_collage_from_pil(images: List[Image.Image], text_length: int, margin: int = 30, fixed_width: int = 1000) -> Image.Image:
    """
    PIL Image 객체들의 리스트를 받아 자동으로 콜라주를 생성하는 함수
    
    Args:
        images: PIL Image 객체들의 리스트
        text_length: 텍스트 길이
        margin: 바깥쪽 여백 (픽셀)
        fixed_width: 고정 가로 크기 (픽셀)
    """
    if not images:
        raise ValueError("이미지 리스트가 비어있습니다.")

    IMAGE_SPACING = 10  # 이미지 간 고정 간격
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
        new_row_width = current_row_width + width + (len(current_row) * IMAGE_SPACING)
        
        if new_row_width <= available_width or not current_row:
            current_row.append((img, width, height))
            current_row_width = new_row_width
        else:
            # 현재 행이 가득 차면, 조정 후 새 행 시작
            rows.append(adjust_row_images(current_row, available_width))
            current_row = [(img, width, height)]
            current_row_width = width
    
    # 마지막 행 처리
    if current_row:
        rows.append(adjust_row_images(current_row, available_width))

    # 전체 높이 계산 및 캔버스 생성
    total_height = margin
    for row in rows:
        total_height += max(img.height for img in row) + IMAGE_SPACING
    total_height += margin - IMAGE_SPACING  # 마지막 spacing 대신 margin 사용

    canvas = Image.new('RGB', (collage_width, total_height), 'black')
    
    # 이미지 배치
    current_y = margin
    for row in rows:
        current_x = margin
        row_height = max(img.height for img in row)
        
        for img in row:
            canvas.paste(img, (current_x, current_y))
            current_x += img.width + IMAGE_SPACING
        
        current_y += row_height + IMAGE_SPACING

    return canvas
