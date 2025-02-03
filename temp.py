import cv2
import numpy as np

def balanced_adaptive_vibrance(image, base_factor=1.5, threshold_high=180):
    # BGR을 HSV로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 로컬 영역의 채도 분석을 위한 블러 적용
    local_sat = cv2.GaussianBlur(hsv[:,:,1], (21,21), 0)
    
    # 채도 조정을 위한 마스크 생성
    increase_mask = (local_sat < 128).astype(float)  # 낮은 채도 영역
    decrease_mask = (local_sat > threshold_high).astype(float)  # 높은 채도 영역
    
    # 채도 수준에 따른 조정 계수 계산
    increase_factor = base_factor * (1 - local_sat/255)  # 낮은 채도일수록 더 강하게 증가
    decrease_factor = 0.2 * ((local_sat - threshold_high)/(255 - threshold_high))  # 높은 채도일수록 더 강하게 감소
    
    # HSV 이미지를 실수형으로 변환하여 계산
    hsv_float = hsv.astype(float)
    
    # 채도 조정 적용
    # 낮은 채도 영역은 증가
    hsv_float[:,:,1] += hsv_float[:,:,1] * increase_factor * increase_mask
    # 높은 채도 영역은 감소
    hsv_float[:,:,1] -= hsv_float[:,:,1] * decrease_factor * decrease_mask
    
    # 값의 범위를 0-255로 제한
    hsv_float[:,:,1] = np.clip(hsv_float[:,:,1], 0, 255)
    
    # 다시 BGR로 변환하여 반환
    return cv2.cvtColor(hsv_float.astype(np.uint8), cv2.COLOR_HSV2BGR)

def advanced_balanced_vibrance(image, base_factor=1.5, threshold_high=180):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 로컬 영역 분석을 위한 여러 크기의 블러 적용
    local_sat_small = cv2.GaussianBlur(hsv[:,:,1], (15,15), 0)
    local_sat_medium = cv2.GaussianBlur(hsv[:,:,1], (31,31), 0)
    local_sat_large = cv2.GaussianBlur(hsv[:,:,1], (61,61), 0)
    
    # 멀티스케일 로컬 채도 계산
    local_sat = (local_sat_small + local_sat_medium + local_sat_large) / 3
    
    # 엣지 검출로 디테일 영역 파악
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_mask = cv2.GaussianBlur(edges.astype(float), (21,21), 0) / 255
    
    # 피부톤 보호
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    skin_mask = cv2.GaussianBlur(skin_mask, (21,21), 0) / 255
    
    # 채도 조정 마스크 생성
    increase_mask = (local_sat < 128).astype(float) * (1 - skin_mask)
    decrease_mask = (local_sat > threshold_high).astype(float) * (1 - skin_mask)
    
    # 엣지 영역에서는 조정 강도 감소
    increase_mask *= (1 - edge_mask * 0.5)
    decrease_mask *= (1 - edge_mask * 0.5)
    
    # 채도 수준에 따른 조정 계수 계산
    increase_factor = base_factor * (1 - local_sat/255) 
    decrease_factor = 0.2 * ((local_sat - threshold_high)/(255 - threshold_high))
    
    hsv_float = hsv.astype(float)
    
    # 부드러운 채도 조정 적용
    hsv_float[:,:,1] += hsv_float[:,:,1] * increase_factor * increase_mask
    hsv_float[:,:,1] -= hsv_float[:,:,1] * decrease_factor * decrease_mask
    
    # 값의 범위를 0-255로 제한
    hsv_float[:,:,1] = np.clip(hsv_float[:,:,1], 0, 255)
    
    return cv2.cvtColor(hsv_float.astype(np.uint8), cv2.COLOR_HSV2BGR)
