import cv2
import numpy as np

def draw_equidistant_lines(image, line_spacing):
    height, width = image.shape[:2]  # 이미지의 높이와 너비를 가져옵니다.
    color = (255, 0, 0)  # 선의 색깔을 파란색으로 설정합니다. BGR 포맷입니다.
    thickness = 2  # 선의 두께를 설정합니다.

    # 수평선 그리기
    for y in range(0, height, line_spacing):
        start_point = (0, y)
        end_point = (width, y)
        image = cv2.line(image, start_point, end_point, color, thickness)

    # 수직선 그리기
    for x in range(0, width, line_spacing):
        start_point = (x, 0)
        end_point = (x, height)
        image = cv2.line(image, start_point, end_point, color, thickness)

    return image

# 이미지를 로드합니다. 적절한 경로로 변경하세요.
image_path = 'path/to/your/image.jpg'
image = cv2.imread(image_path)
line_spacing = 50  # 선 간의 간격을 픽셀 단위로 설정합니다.

# 선을 그린 이미지를 생성합니다.
modified_image = draw_equidistant_lines(image, line_spacing)

# 결과 이미지를 보여줍니다.
cv2.imshow('Image with Equidistant Lines', modified_image)
cv2.waitKey(0)  # 윈도우가 키보드 입력을 기다립니다.
cv2.destroyAllWindows()  # 모든 OpenCV 윈도우를 종료합니다.
