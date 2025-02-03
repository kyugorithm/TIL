import cv2
import numpy as np

def continuous_vibrance(image, threshold=150, base_factor=1.5):
    # BGR을 HSV로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 채도 채널을 실수형으로 변환하여 작업
    saturation = hsv[:,:,1].astype(float)
    
    # 부드러운 로컬 채도 맵 생성 (큰 커널 사용)
    smooth_local_sat = cv2.GaussianBlur(saturation, (61,61), 0)
    
    # 임계값과의 차이에 기반한 조정 계수 계산
    # threshold를 기준으로 위아래로 연속적으로 변화하는 조정값 생성
    relative_diff = (threshold - smooth_local_sat) / threshold
    
    # 부드러운 전이를 위해 조정 계수에 추가 블러 적용
    adjustment_map = cv2.GaussianBlur(relative_diff, (31,31), 0)
    
    # 최종 조정값 계산 (base_factor로 전체적인 강도 조절)
    final_adjustment = base_factor * adjustment_map
    
    # 채도 조정 적용
    new_saturation = saturation * (1 + final_adjustment)
    new_saturation = np.clip(new_saturation, 0, 255)
    
    # 수정된 채도 값을 HSV 이미지에 적용
    hsv_result = hsv.copy()
    hsv_result[:,:,1] = new_saturation.astype(np.uint8)
    
    return cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
