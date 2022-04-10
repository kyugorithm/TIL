## Towards Open-Set Identity Preserving Face Synthesis

## Abstract

1) 서로다른 얼굴의 id와 attr를 합성하기 위해 GAN 기반의 id, attr 분리 프레임워크를 제안  
2) 기존에는 학습 데이터에 대한 합성만 가능했으나 본 방법론에서는 임의 얼굴 변환을 위한 방법론을 제안  
- ID벡터를 만들기 위한 얼굴의 입력 이미지와 포즈, 감정, 조명, 배경등을 포착하는 att. vector를 추출할 다른 입력 이미지를 사용하고 ID 벡터와 att. 벡터를 재결합하여 새로운 얼굴을 합성  
3) 얼굴 att.에 대한 주석이 필요하지 않음
4) ID를 더 잘 보존하고 학습 과정을 안정화하기 위해 비대칭적 loss function을 이용하여 학습  
5) 레이블이 지정되지 않은 많은 양의 학습 얼굴 이미지를 효과적으로 활용하여 레이블이 지정된 학습 세트에 표시되지 않는 subject에 대해 합성된 얼굴의 fidelity를 더욱 향상 
6) Face forntalization, face att. morphing 및 face adversarial example등 다양한 활용 사례를 제시
