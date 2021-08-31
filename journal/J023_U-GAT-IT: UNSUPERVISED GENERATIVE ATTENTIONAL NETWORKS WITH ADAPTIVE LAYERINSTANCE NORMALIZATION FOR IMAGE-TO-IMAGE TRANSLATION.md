## Abstract
**1) Attention module**과 **2) 학습 가능한 normalization 기능**을 **end-to-end**로 통합하는 unsupervised i2i translation을 제안합니다.  
Attention은 보조 분류기가 획득한 attention map을 기반으로 source/target 을 구분하는 중요영역에 초점을 맞추도록 모델을 안내합니다.  
Geometric 변화가 불가능한 기존 attention 방식과 달리, 전체나 큰 형상의 변화가 필요한 이미지를 모두 변환할 수 있습니다.  
AdaLIN 기능은 attention-guided 모델이 데이터셋에 따라 학습된 매개변수로 모양과 질감의 변화량을 유연하게 제어할 수 있도록 합니다.  
실험 결과는 고정된 네트워크 아키텍처와 하이퍼 매개변수를 가진 기존 SOTA와 비교하여 제안된 방법의 우수성을 보여줍니다.

## 1. Introduction 
I2IT는 서로 다른 도메인 내에서 이미지를 매핑하는 기능을 학습하는 것을 목표로 합니다.  
이 주제는 이미지 인페인팅, super-resolution, colorization 및 style transfer등 분야에서 많은 관심을 받아왔습니다.  
paired 샘플이 주어지면 매핑 모델은 조건부 생성 모델 또는 단순 회귀를 사용하여 지도 방식으로 훈련될 수 있습니다.  
unpaired 비지도학습에서 여러 작업은 **공유 잠재 공간** 및 주기 일관성 가정을 통해 성공적으로 이미지를 번역했습니다.  
이러한 작업은 작업의 multimodal을 처리하기 위해 추가로 개발되었습니다.  
이러한 발전에도 불구하고 기존방법은 영역 간 모양과 질감의 변화량에 따라 성능 차이를 보였습니다.  
예를 들어, local texture를 매핑하는 style transfer에는 성공하지만 일반적으로 wild 이미지에서 더 큰 모양 변경이 있는 이미지 번역 작업에는 성공하지 못합니다.  
따라서 데이터 분포의 복잡성을 제한하여 이러한 문제를 피하기 위해 이미지 cropping 및 alignment 같은 전처리 단계가 종종 필요합니다.  
또한 DRIT 같은 방법은 고정 네트워크와 하이퍼파라미터로 모양 유지/변경 이미지 번역 모두에서 원하는 결과를 얻을 수 없습니다.  
특정 데이터 세트에 대해 네트워크 구조 또는 하이퍼 매개변수 설정을 조정해야 합니다.  
Attention module과 학습 가능한 normalization 기능을 e2e 방식으로 통합하는 unsupervised i2it를 위한 새로운 방법을 제안합니다.  
분류기의 attention map을 기반으로 source/target 도메인을 구분하여 더 중요한 영역에 초점을 맞추고 작은 영역을 무시하도록 안내합니다.  
이러한 어텐션 맵은 의미론적으로 중요한 영역에 초점을 맞추기 위해 G와 D에 포함되어 모양 변환을 용이하게 합니다.  
G의 어텐션 맵은 영역을 구체적으로 구분하는 영역에 초점을 유도하는 반면, D의 어텐션 맵은 대상 영역에서 실제/가짜 차이에 초점을 맞춰 미세 조정을 돕습니다.  
attention mechanism 외에도 normalization 함수의 선택이 모양과 질감의 변화량이 다른 다양한 데이터 세트에 대해 변환된 결과의 품질에 상당한 영향을 미친다는 것을 발견했습니다.  
BIN(Batch-Instance Normalization)에서 영감을 받아 Instance normalization(IN)과 Layer 간의 적절한 비율을 적응적으로 선택하여  
학습동안 데이터 세트에서 매개변수를 학습하는 Adaptive LayerInstance Normal우리의 목표는 각 도메인에서 가져온 짝을 이루지 않은 샘플만 사용하여 소스 도메인 Xs의 이미지를 대상 도메인 Xt로 매핑하는 함수 Gs→t를 훈련하는 것입니다. 우리의 프레임워크는 두 개의 생성기 Gs→t 및 Gt→와 두 개의 판별자 D 및 Dt로 구성됩니다. 주의 모듈을 생성기와 판별기에 통합합니다. 판별기의 주의 모듈은 생성기가 사실적인 이미지를 생성하는 데 중요한 영역에 초점을 맞추도록 안내합니다. 생성기의 Attention 모듈은 다른 도메인과 구별되는 영역에 주의를 기울입니다. 여기서는 Gs→t 및 Dt(그림 1 참조)만 설명합니다. 그 반대의 경우도 간단해야 합니다.ization(AdaLIN)을 제안합니다.  
AdaLIN 기능은 우리의 attention-guided 모델이 모양과 질감의 변화량을 유연하게 제어할 수 있도록 도와줍니다.  
결과적으로 우리 모델은 모델 아키텍처나 하이퍼파라미터를 수정하지 않고도 전체적 변경뿐만 아니라 큰 모양 변경이 필요한 이미지 번역 작업을 수행할 수 있습니다.  
실험을 통해 제안하는 방법이 기존의 최신 모델에 비해 스타일 전이뿐만 아니라 객체 변형에서도 우수함을 보여주었습니다.  
제안된 작업의 주요 기여는 다음과 같이 요약될 수 있습니다.  
  
1. Attention과 AdaLIN을 사용하여 unsupervised i2i 변역의 새로운 방법을 제안합니다.  
  
2. Attention은 보조 분류기에서 얻은 attention 맵을 기반으로 source/target 도메인을 구별하여 집중적으로 변환할 위치를 모델이 알 수 있도록 도와줍니다.  
  
3. AdaLIN 기능은 우리의 attention-guided 모델이 아키텍처나 하이퍼파라미터를 수정하지 않고도 **모양과 질감**의 변화량을 유연하게 제어할 수 있도록 도와줍니다.  

## 2.  UNSUPERVISED GENERATIVE ATTENTIONAL NETWORKS WITH ADAPTIVE LAYER-INSTANCE NORMALIZATION
목표는 각 도메인의 unpaired  샘플을 사용하여 Xs의 이미지를 Xt로 매핑하는 함수 Gs→t를 훈련하는 것입니다.  
우리의 프레임워크는 두 개의 G(Gs→t, Gt→s) 와 두 개의 D(Ds, Dt)로 구성됩니다. Attention 모듈을 G와 D에 통합합니다.  
D의 attention 모듈은 G가 사실적인 이미지를 생성하는 데 중요한 영역에 초점을 맞추도록 안내합니다.  
G의 attention 모듈은 다른 도메인과 구별되는 영역에 주의를 기울입니다.  
여기서는 Gs→t 및 Dt만 설명합니다. 그 반대의 경우도 간단해야 합니다.  
![image](https://user-images.githubusercontent.com/40943064/131239178-075b5971-e1f4-4923-9f6a-0a4e3713aaf2.png)
![image](https://user-images.githubusercontent.com/40943064/131518554-cf970505-2a90-4f4f-b39d-616cb2fd8487.png)
