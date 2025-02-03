import cv2
import numpy as np

def smooth_adaptive_vibrance(image, base_factor=1.5):
    # BGR을 HSV로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 채도 채널 추출
    saturation = hsv[:,:,1].astype(float)
    
    # 매우 큰 커널로 부드러운 로컬 채도 맵 생성
    # 큰 커널을 사용하여 점진적인 변화 유도
    smooth_local_sat = cv2.GaussianBlur(saturation, (71,71), 0)
    
    # 부드러운 조정 계수 맵 생성
    adjustment_map = np.zeros_like(saturation)
    
    # 낮은 채도 영역에서는 점진적으로 증가
    low_sat_mask = smooth_local_sat < 128
    adjustment_map[low_sat_mask] = base_factor * (1 - smooth_local_sat[low_sat_mask]/128)
    
    # 높은 채도 영역에서는 점진적으로 감소
    high_sat_mask = smooth_local_sat > 180
    adjustment_map[high_sat_mask] = -0.3 * ((smooth_local_sat[high_sat_mask] - 180)/(255 - 180))
    
    # 조정 맵에 추가 블러 적용하여 더욱 부드럽게 만들기
    adjustment_map = cv2.GaussianBlur(adjustment_map, (31,31), 0)
    
    # 채도 조정 적용
    new_saturation = saturation * (1 + adjustment_map)
    new_saturation = np.clip(new_saturation, 0, 255)
    
    # 수정된 채도 값을 HSV 이미지에 적용
    hsv_result = hsv.copy()
    hsv_result[:,:,1] = new_saturation.astype(np.uint8)
    
    # BGR로 변환하여 반환
    return cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)

def advanced_smooth_vibrance(image, base_factor=1.5):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = hsv[:,:,1].astype(float)
    
    # 여러 스케일의 가우시안 블러를 적용하여 부드러운 전이 보장
    blur_sizes = [(31,31), (61,61), (91,91)]
    blur_weights = [0.4, 0.35, 0.25]  # 작은 커널에 더 큰 가중치
    
    smooth_local_sat = np.zeros_like(saturation)
    for size, weight in zip(blur_sizes, blur_weights):
        smooth_local_sat += weight * cv2.GaussianBlur(saturation, size, 0)
    
    # 채도 변화의 그래디언트를 계산하여 급격한 변화 감지
    gradient_x = cv2.Sobel(smooth_local_sat, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(smooth_local_sat, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    # 그래디언트가 큰 영역에서는 조정 강도를 줄임
    gradient_weight = 1 / (1 + gradient_magnitude/30)
    gradient_weight = cv2.GaussianBlur(gradient_weight, (31,31), 0)
    
    # 조정 계수 맵 생성
    adjustment_map = np.zeros_like(saturation)
    
    # 채도에 따른 점진적 조정
    low_range = smooth_local_sat < 128
    adjustment_map[low_range] = base_factor * (1 - smooth_local_sat[low_range]/128)
    
    high_range = smooth_local_sat > 180
    adjustment_map[high_range] = -0.3 * ((smooth_local_sat[high_range] - 180)/(255 - 180))
    
    # 그래디언트 가중치를 적용하여 급격한 변화 방지
    adjustment_map *= gradient_weight
    
    # 최종 조정 맵에 큰 커널의 가우시안 블러 적용
    final_adjustment = cv2.GaussianBlur(adjustment_map, (61,61), 0)
    
    # 채도 조정 적용
    new_saturation = saturation * (1 + final_adjustment)
    new_saturation = np.clip(new_saturation, 0, 255)
    
    # 결과 생성
    hsv_result = hsv.copy()
    hsv_result[:,:,1] = new_saturation.astype(np.uint8)
    
    return cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
