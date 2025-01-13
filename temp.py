def create_collage_from_pil(images: List[Image.Image], text_length: int, margin: int = 30, fixed_width: int = 1000) -> Image.Image:
    """
    PIL Image 객체들의 리스트를 받아 자동으로 콜라주를 생성하는 함수
    
    Args:
        images: PIL Image 객체들의 리스트
        text_length: 텍스트 길이
        margin: 이미지 간 여백 (픽셀)
        fixed_width: 고정 가로 크기 (픽셀)
    """
    if not images:
        raise ValueError("이미지 리스트가 비어있습니다.")

    # 텍스트 길이와 최소 허용 이미지 크기 설정
    min_image_size = text_length * 10  # 텍스트 길이의 10배를 최소 크기로 설정

    # 고정 가로 크기 설정
    collage_width = fixed_width
    
    # 이미지들의 크기를 조정하고 최적의 배치를 찾기
    processed_images = []
    for img in images:
        # 이미지 스케일 계산 (가로 기준 1/3)
        scale = min(collage_width/3/img.width, collage_width/3/img.height)
        if scale < 1:
            new_width = int(0.9*img.width * scale)
            new_height = int(0.9*img.height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        processed_images.append(img)

    # 이미지 배치를 위한 그리드 시스템 구현
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

    # 이미지 배치 정보 저장
    placed_regions = []
    current_x = margin
    current_y = margin
    max_row_height = 0
    row_start_x = margin

    # 이미지 배치 알고리즘
    for img in processed_images:
        # 새로운 위치 시도
        new_region = Region(current_x, current_y, img.width, img.height)
        
        # 다른 이미지들과 겹치는지 확인
        while any(new_region.intersects(placed) for placed in placed_regions):
            current_x += margin
            # 행이 너무 길어지면 새로운 행 시작
            if current_x + img.width + margin > collage_width:
                current_x = row_start_x
                current_y += max_row_height + margin
                max_row_height = 0
            new_region = Region(current_x, current_y, img.width, img.height)

        # 이미지 위치 확정
        placed_regions.append(new_region)
        max_row_height = max(max_row_height, img.height)
        current_x += img.width + margin

    # 전체 캔버스 높이 계산
    collage_height = max(region.y + region.height for region in placed_regions) + margin

    # 최종 캔버스 생성
    canvas = Image.new('RGB', (collage_width, collage_height), 'black')

    # 이미지들 캔버스에 배치
    for img, region in zip(processed_images, placed_regions):
        canvas.paste(img, (region.x, region.y))

    return canvas
