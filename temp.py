from PIL import Image
import numpy as np
from typing import List, Tuple
import math

def create_collage_from_pil(images: List[Image.Image], output_path: str, margin: int = 10) -> None:
    """
    PIL Image 객체들의 리스트를 받아 자동으로 콜라주를 생성하는 함수
    
    Args:
        images: PIL Image 객체들의 리스트
        output_path: 결과 이미지를 저장할 경로
        margin: 이미지 간 여백 (픽셀)
    
    주요 동작 과정:
    1. 전체 이미지 영역을 계산하여 적절한 캔버스 크기 결정
    2. 큰 이미지부터 차례로 배치하여 공간 활용도를 높임
    3. 각 이미지별로 겹치지 않는 최적의 위치를 탐색
    4. 필요한 경우 이미지 크기를 자동으로 조정
    """
    if not images:
        raise ValueError("이미지 리스트가 비어있습니다.")
    
    # 전체 이미지 영역 계산
    total_area = sum(img.width * img.height for img in images)
    
    # 전체 이미지의 가로/세로 비율 계산 (16:9 기본값)
    n = len(images)
    aspect_ratio = 16/9
    
    # 콜라주 캔버스 크기 계산 
    # math.sqrt를 사용하여 전체 면적을 기반으로 적절한 크기 도출
    collage_width = int(math.sqrt(total_area * aspect_ratio))
    collage_height = int(collage_width / aspect_ratio)
    
    # 흰색 배경의 캔버스 생성
    canvas = Image.new('RGB', (collage_width, collage_height), 'white')
    
    # 면적 기준 내림차순 정렬 (큰 이미지부터 배치)
    sorted_images = sorted(images, key=lambda x: x.width * x.height, reverse=True)
    
    def find_best_position(img: Image.Image, used_areas: List[Tuple[int, int, int, int]]) -> Tuple[int, int]:
        """
        새 이미지를 위한 최적의 위치를 찾는 내부 함수
        
        Args:
            img: 배치할 이미지
            used_areas: 이미 사용된 영역들의 좌표 리스트 [(x1,y1,x2,y2),...]
            
        Returns:
            (x, y): 이미지를 배치할 최적의 좌상단 좌표
        """
        best_x, best_y = 0, 0
        min_overlap = float('inf')
        
        # 10픽셀 간격으로 가능한 모든 위치 검사
        for x in range(0, collage_width - img.width, 10):
            for y in range(0, collage_height - img.height, 10):
                current_area = (x, y, x + img.width, y + img.height)
                overlap = 0
                
                # 기존 이미지들과의 겹침 영역 계산
                for used_area in used_areas:
                    x1 = max(current_area[0], used_area[0])
                    y1 = max(current_area[1], used_area[1])
                    x2 = min(current_area[2], used_area[2])
                    y2 = min(current_area[3], used_area[3])
                    
                    if x1 < x2 and y1 < y2:
                        overlap += (x2 - x1) * (y2 - y1)
                
                # 더 작은 겹침 영역을 가진 위치 발견 시 업데이트
                if overlap < min_overlap:
                    min_overlap = overlap
                    best_x, best_y = x, y
                
                # 겹치지 않는 완벽한 위치를 찾으면 즉시 반환
                if overlap == 0:
                    return x, y
        
        return best_x, best_y
    
    # 이미지가 차지하는 영역을 추적하기 위한 리스트
    used_areas = []
    
    # 각 이미지를 최적의 위치에 배치
    for img in sorted_images:
        # 너무 큰 이미지는 적절히 축소
        # 캔버스의 1/3을 넘지 않도록 제한
        scale = min(collage_width/3/img.width, collage_height/3/img.height)
        if scale < 1:
            new_width = int(img.width * scale)
            new_height = int(img.height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 최적의 배치 위치 찾기
        x, y = find_best_position(img, used_areas)
        
        # 이미지를 캔버스에 붙이기
        canvas.paste(img, (x, y))
        
        # 사용된 영역 기록
        used_areas.append((x, y, x + img.width, y + img.height))
    
    # 여백 추가를 위해 캔버스 크기 약간 확장
    final_canvas = Image.new('RGB', 
                           (collage_width + margin*2, collage_height + margin*2), 
                           'white')
    final_canvas.paste(canvas, (margin, margin))
    
    # 결과 저장
    final_canvas.save(output_path, quality=95)

# 사용 예시
# pil_images = [이미지1, 이미지2, 이미지3]  # PIL Image 객체들의 리스트
# create_collage_from_pil(pil_images, 'collage_result.jpg')
