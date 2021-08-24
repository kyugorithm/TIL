# Not just Compete, but Collaborate: Local Image-to-Image Translation via Cooperative Mask Prediction

## Abstract 
Facial attribute editing은 원하는 속성으로 이미지를 조작하면서 다른 디테일은 보존하는 것을 목표로 한다.  
최근, GAN, Encoder-Decoder architecture가 현실적인 이미지를 만들 수 있는 능력 때문에 이 작업에 활용되고 있다.  
그러나 unpaired dataset에 대한 기존 방법은 ground truth image가 없기 때문에 attribute-irrelevant regions를 제대로 보존할 수 없다.  
본 연구는 CAM-consistensy loss라는 새롭고 직관적인 손실 함수를 제안하며, 이는 이미지 변환에서 입력 이미지의 일관성을 향상시킨다.  
기존의 cycle consistency loss는 이미지를 다시 변환할 수 있도록 보장하지만, 우리의 접근방식은 모델이 판별기에서 계산한 Grad-CAM 
출력을 사용하여 다른 도메인에 대한 단일 변환에서도 속성 무관 영역을 더욱 보존하도록 한다.  
우리의 CAM-consistensy loss는 다른 영역을 변경하지 않으면서 발전기가 변경해야 하는 로컬 영역을 적절히 캡처하기 위해 학습 중에  
판별기에서 이러한 Grad-CAM 출력을 직접 최적화한다.  
이러한 방식으로, 우리의 접근방식은 이미지 변환 품질을 향상시키기 위해 생성자와 판별자가 서로 협력할 수 있도록 한다.  
실험에서는 StarGAN, AttGAN, STGAN과 같은 대표적인 얼굴 이미지 편집 모델에 CAM 일관성 손실 제안의 효과와 다용성을 검증한다.

## 1. Introduction

**Unpaired I2I translation 사례**
1) CycleGAN : cycle consistency loss를 통해 unpaired dataset을 사용하여 도메인 간 이미지 번역을 할 수 있는 CycleGAN을 도입  
2) StarGAN/AttGA : 단일 G를 사용하여 multi-domain translation을 달성하면서 face attribute 편집을 위해 제안  

주어진 이미지의 원하는 속성을 변경하면서 속성과 무관한 영역을 보존하는 것은 어렵다.
예를들어 금발 속성을 부여할 때 이미지의 전체 색상을 황금색으로 변경하는 경우가 많다.  

**속성과 무관한 영역을 보존하기 위해 추가 모듈이 제안된 사례**  
1) SaGAN : 추정된 segmentation mask를 기반으로 이미지 일부 영역만 변경  
다만, global attribute(예: 성별, 연령) translation은 이러한 로컬 조작이 적용되지 않을 수 있다.  
2) CAFEGAN : Attention Branch Network을 사용하여 픽셀 수준이 아닌 feature map에서 속성 관련 정보를 예측하여  
속성 관련 없는 영역을 보존  
3) RelGAN : relative attribute를 사용하고 이미지 변환을 위해 수정된 속성의 벡터와 두 개의 이미지로 구성된 삼중항을 사용하여  
조건부 적대적 손실을 활용  

위 방식은 특정 모듈이 필요하고 픽셀 수준 보존을 위해 명시적 손실을 사용하지 않기 때문에 일반 아키텍처에 쉽게 적용할 수 없다.  

이 문제해결을 위해 본 논문은 adversarial 학습에서 Grad-CAM을 활용하여 I2I translation을 위한  
**CAM consistency loss**라는 새롭고 직관적인 손실 함수를 제안한다.  
본 방법은 아키텍처를 수정하지 않고 StarGAN, AttGAN, STGAN과 같은 기존 이미지 변환 접근 방식에 광범위하게 적용할 수 있다.  
CAM consistency loss는 D가 특징 수준에서 속성 관련 정보에 주의를 기울이도록 하는 동안 이미지의 관련 없는 영역을  
픽셀 수준에서 보존하도록 G를 강제하기 때문에 기존 방법의 다양한 한계를 극복할 수 있다.  
이를 통해 모델은 그림 1과 같이 속성과 무관한 영역을 유지하면서 이미지를 한 번에 생성할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/130634632-ecb49ad8-fb87-4b47-b209-c85da7274d14.png)

**요약**

• **새로운 loss 제안 : CAM consistency loss**
D가 속성 관련 영역을 처리하는 동안 속성과 관련 없는 영역을 보존하도록 G를 직접 적용  
각 속성의 segmentation map이나 네트워크 아키텍처의 수정과 같은 추가 정보 없이도 작동하며 G와 D가  
더 나은 성능을 위해 서로 협력할 수 있음  
  
• D가 Attribute와 무관한 영역을 보존하여 기존 I2I 변환 접근 방식의 한계를 극복  
  
• GradCAM을 시각화 도구가 아닌 학습 목표로 직접 사용할 수 있는 가능성을 보여줌  

## 3. Proposed Method
얼굴 이미지를 조작할 때 세부 정보를 유지하지 못하는 기존 cycle-consistency-loss의 한계를 고려한다.  
이를 해결하기 위해 real과 fake를 비교하는 간단한 접근 방식을 제안한다.  
real과 fake를 직접 비교하는 것은 일반적으로 비현실적이므로 두 이미지를 비교할 때  
배경과 같이 속성과 관련이 없는 영역에만 모델이 표시되도록 하는 CAM 일관성 손실을 제안한다.  
구체적으로, 보조 분류기의 Grad-CAM 출력을 활용하여 사용자가 변경하고자 하는 속성에 해당 영역을 마스킹한다.  
**그림 2** : Cycle consistency vs CAM consistency  
![image](https://user-images.githubusercontent.com/40943064/130637975-7b743836-6d40-49a7-8834-61cd82daa35c.png)

CAM consistency loss는 기존 네트워크 구조를 수정하지 않고도 Grad-CAM 모듈을 유연하게 추가할 수 있으므로  
보조 분류기를 사용하는 다양한 아키텍처에 광범위하게 적용할 수 있다.  
이러한 직관을 달성하기 위해 우리는 그림 3과 같이 훈련 과정에서 GAN 모델의 G와 D 모두에 대해 CAM consistency loss를 적용한다.  
흥미롭게도 단순히 훈련 목표에 CAM 일관성 손실을 추가함으로써 우리는 다음을 관찰한다.  
G와 D는 서로 협력한다. GAN에서 이름에서 알 수 있듯이 판별자와 생성자는 기본적으로 서로 경쟁하는 방식으로 훈련된다.  
그러나 CAM consistency loss을 최적화하려면 서로 협력해야 한다. 즉, G 관점에서, D는 attribute 관련 영역을 보존하기 위해  
속성 관련 영역에 적절하게 주의를 기울이는 것이 필수적이다.  
반면에 D는 G에 의해 조작된 영역을 따르기 위해 주어진 속성에 해당하는 Grad-CAM 영역을 적절하게 업데이트해야 한다.  
따라서 G는 판별자가 특성을 올바르게 분류할 수 있도록 특성 관련 영역에 해당하는 최소한의 필요한 변경을 수행해야 한다.  
학습이 진행됨에 따라  
1) G는 D가 주어진 속성과 상관관계가 높다고 생각하는 부분을 변경할 수 있고  
2) D는 G가 변경한 영역에 초점을 맞춰 속성 관련 영역을 캡처할 수 있다.  
물론 학습 목표는 CAM consistency loss의 적용이 생성이미지의 품질에 해를 끼치지 않도록 이미지 조작의 원래 목적과 완전히 일치한다.  
