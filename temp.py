import timm
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import glob
from tqdm import tqdm

# 모델 설정
def get_model():
    model = timm.create_model('tf_efficientnetv2_s', pretrained=True)
    # 마지막 분류 레이어 제거
    model.classifier = nn.Identity()
    model.eval()
    return model

# 이미지 전처리
def get_transforms():
    return transforms.Compose([
        transforms.Resize((384, 384)),  # EfficientNetV2-S 권장 크기
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])

# 특징 추출
def extract_features(model, image_path, transform):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # 배치 차원 추가
    
    with torch.no_grad():
        features = model(image)
    
    return features.squeeze().numpy()

# 이미지 그룹화
def group_similar_images(features_dict, threshold=0.8):
    image_paths = list(features_dict.keys())
    features = np.array(list(features_dict.values()))
    
    # 정규화
    features = features / np.linalg.norm(features, axis=1, keepdims=True)
    
    # 유사도 매트릭스 계산
    similarity_matrix = cosine_similarity(features)
    
    # 그룹화
    groups = []
    used = set()
    
    for i in range(len(image_paths)):
        if i in used:
            continue
            
        current_group = [image_paths[i]]
        used.add(i)
        
        # 유사한 이미지 찾기
        similar_indices = np.where(similarity_matrix[i] > threshold)[0]
        for idx in similar_indices:
            if idx != i and idx not in used:
                current_group.append(image_paths[idx])
                used.add(idx)
                
        if len(current_group) > 1:  # 유사한 이미지가 있는 경우만 그룹 추가
            groups.append(current_group)
    
    return groups

# 메인 실행 코드
def main():
    # 모델과 전처리 설정
    model = get_model()
    transform = get_transforms()
    
    # 이미지 경로 설정 (예: 'images' 폴더 내의 모든 이미지)
    image_paths = glob.glob('images/*.jpg')  # 경로는 실제 환경에 맞게 수정
    
    # 특징 추출
    features_dict = {}
    for img_path in tqdm(image_paths, desc="Extracting features"):
        try:
            features = extract_features(model, img_path, transform)
            features_dict[img_path] = features
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    
    # 유사한 이미지 그룹화
    similar_groups = group_similar_images(features_dict, threshold=0.8)
    
    # 결과 출력
    for i, group in enumerate(similar_groups):
        print(f"\nSimilar Image Group {i+1}:")
        for img_path in group:
            print(f"  - {img_path}")

if __name__ == "__main__":
    main()
