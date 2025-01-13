from typing import List
from PIL import Image

def create_collage_with_margin(images: List[Image.Image], text_length: int, margin: int = 30, fixed_width: int = 1000) -> Image.Image:
    """
    마진이 있는 콜라주를 생성하는 함수
    """
    if not images:
        raise ValueError("이미지 리스트가 비어있습니다.")

    min_image_size = text_length * 10
    collage_width = fixed_width
    
    # 이미지 전처리
    processed_images = []
    for img in images:
        scale = min(collage_width/3/img.width, collage_width/3/img.height)
        if scale < 1:
            new_width = int(0.9*img.width * scale)
            new_height = int(0.9*img.height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        processed_images.append(img)

    class Region:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

        def intersects(self, other):
            return not (self.x + self.width + margin <= other.x or
                       other.x + other.width + margin <= self.x or
                       self.y + self.height + margin <= other.y or
                       other.y + other.height + margin <= self.y)

    placed_regions = []
    current_x = margin
    current_y = margin
    max_row_height = 0
    row_start_x = margin

    for img in processed_images:
        new_region = Region(current_x, current_y, img.width, img.height)
        
        while any(new_region.intersects(placed) for placed in placed_regions):
            current_x += margin
            if current_x + img.width + margin > collage_width:
                current_x = row_start_x
                current_y += max_row_height + margin
                max_row_height = 0
            new_region = Region(current_x, current_y, img.width, img.height)

        placed_regions.append(new_region)
        max_row_height = max(max_row_height, img.height)
        current_x += img.width + margin

    collage_height = max(region.y + region.height for region in placed_regions) + margin
    canvas = Image.new('RGB', (collage_width, collage_height), 'black')

    for img, region in zip(processed_images, placed_regions):
        canvas.paste(img, (region.x, region.y))

    return canvas

def create_collage_compact(images: List[Image.Image], text_length: int, fixed_width: int = 1000) -> Image.Image:
    """
    마진 없이 이미지 간 10픽셀 간격으로 콜라주를 생성하는 함수
    """
    if not images:
        raise ValueError("이미지 리스트가 비어있습니다.")

    SPACING = 10  # 이미지 간 고정 간격
    min_image_size = text_length * 10
    collage_width = fixed_width
    
    # 이미지 전처리
    processed_images = []
    for img in images:
        scale = min(collage_width/3/img.width, collage_width/3/img.height)
        if scale < 1:
            new_width = int(0.95*img.width * scale)  # 더 큰 이미지 허용
            new_height = int(0.95*img.height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        processed_images.append(img)

    class Region:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

        def intersects(self, other):
            return not (self.x + self.width + SPACING <= other.x or
                       other.x + other.width + SPACING <= self.x or
                       self.y + self.height + SPACING <= other.y or
                       other.y + other.height + SPACING <= self.y)

    placed_regions = []
    current_x = 0  # 마진 없음
    current_y = 0
    max_row_height = 0
    row_start_x = 0

    for img in processed_images:
        new_region = Region(current_x, current_y, img.width, img.height)
        
        while any(new_region.intersects(placed) for placed in placed_regions):
            current_x += SPACING
            if current_x + img.width > collage_width:
                current_x = row_start_x
                current_y += max_row_height + SPACING
                max_row_height = 0
            new_region = Region(current_x, current_y, img.width, img.height)

        placed_regions.append(new_region)
        max_row_height = max(max_row_height, img.height)
        current_x += img.width + SPACING

    collage_height = max(region.y + region.height for region in placed_regions) + SPACING
    canvas = Image.new('RGB', (collage_width, collage_height), 'black')

    for img, region in zip(processed_images, placed_regions):
        canvas.paste(img, (region.x, region.y))

    return canvas
