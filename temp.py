import cv2

def draw_bbox(image, bbox, color=(255, 0, 0), thickness=2):
    # bbox는 [x_min, y_min, width, height] 형태
    x_min, y_min, width, height = bbox
    top_left = (int(x_min), int(y_min))
    bottom_right = (int(x_min + width), int(y_min + height))
    cv2.rectangle(image, top_left, bottom_right, color, thickness)

# 이미지 로드
image = cv2.imread('path_to_image.jpg')

# 바운딩 박스 정보, 예시: [x_min, y_min, width, height]
bbox = [100, 50, 200, 300]  # 실제 사용할 때는 COCO 데이터셋에서 얻은 값으로 대체

# 바운딩 박스 그리기
draw_bbox(image, bbox)

# 이미지 보여주기
cv2.imshow('Image with Bounding Box', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
