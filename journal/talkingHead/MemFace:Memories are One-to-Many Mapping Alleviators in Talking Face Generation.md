## Abstract
Memories are One-to-Many Mapping Alleviators in Talking Face Generation
단일 입력 오디오에 대해 출력 이미지는 다양하므로 기존 deterministic mapping은 모호하게 학습하고 품질이 매우 떨어지게 된다.  
이 문제를 해결하기 위해 과정을 2-stage(Audio2Expression -> Rendering)로 분할하더라도 입력 정보(감정, 주름 등)가 충분치 않으면 결과가 좋을 수 없다.
각각 two-stage 방식을 따르는 implicit/explicit memory로 부재한 정보를 보완한다.
- Audio2expression : High-level semantics를 포착하기 위해 implicit memory 적용
- Neural-Rendering : Pixel 수준의 합성을 위해 explicit memory 적용 

## 1. Introduction

일반적으로 중간 표현을 활용하는 2stage 방식을 사용한다.
1) Audio2expression : Intermediate representation(2D landmark, blendshape coefficient) 활용
2) neural-renderer : 예측한 representation에 따라 video portrait을 생성d

위 방법론을 따라 자연스러운 머리의 움직임, 입술싱크 품질, 표정 표현 생성 등이 개선되어 왔다.
Audio2video 데이터로 부터의 deterministic mapping을 학습하는 방식으로 편향되어왔지만 본질적인 문제는 one-to-many mapping 이라는 점에 주목할 가치가 있다.
즉, 입력 오디오 클립에 대해 음소 문맥, 감정 및 조명 조건 등의 변화로 인해 대상 사람의 가능한 시각적 모습이 여러 개 있음을 의미한다.
이러한 방식으로 deterministic mapping을 학습하면 학습 중에 모호성이 발생하여 현실적인 시각적 결과를 산출하기가 더 어려워진다.

위 문제는 두 개의 하위 문제로 분해하기 때문에 부분적으로 완화할 수 있지만 각 단계에서 부족한 입력 정보로 예측하도록 최적화되어 있어 예측이 어렵다.  
Audio-to-expression : 습관, 태도 등과 같은 high-level semantic이 없는 입력 오디오와 의미론적으로 일치하는 표정을 생성하는 방법을 학습  
Neural-renderer는 픽셀을 데이터가 없는 추정된 표정을 기반으로 시각적 모양을 합성  

이러한 일대다 매핑 문제를 완화하기 위해 본 논문에서는 두 단계 방식을 각각 따르는 implicit memory와 explicit memory를 고안하여 mission information을 메모리로 보완하는 방법을 제안한다.  
implicit memory : 의미적으로 정렬된 정보를 보완하기 위해 audio2expression과 공동으로 최적화  
explicit memory : non-parametric 방식으로 구성되고 각 target person에 맞게 조정되어 시각적 세부 사항을 보완한다.  
따라서 입력 오디오를 직접 사용하여 표정을 예측하는 대신 Audio-to-expression은 추출된 audio feature를 query로 활용하여 implicit memory에 주의를 기울인다.  
의미적으로 정렬된 정보로 제공되는 attention 결과는 audio feature로 보완되어 표현 출력을 생성한다.  
end-to-end 학습을 가능하게 함으로써 implicit memory는 audio-expression 공유 공간에서 high-level-semantics를 연관시키도록 하여 입력 오디오와 출력 표정 사이의 의미론적 격차를 좁힌다.  
표정을 얻은 후 Neural-renderer를 사용하여 표정 추정에서 얻은 입 모양을 기반으로 시각적 외모를 합성한다.  
pixcel-level 세부 사항을 추가로 보완하기 위해 먼저 3D 얼굴 모델의 vertex와 관련 이미지 patch를 각각 key/value로 간주하여 각 사람에 대한 명시적 메모리를 구성한다.  
그런 다음 각 입력 식에 대해 해당 vertex를 query로 사용하여 explicit memory에서 유사한 key를 검색하고 관련 image patch를 Neural-rendering에 대한 pixcel-level 세부 정보로 반환한다.  
직관적으로 모델에 explicit memory를 도입함으로써 모델 자체에서 생성하지 않고 표정이 필요한 세부 사항을 모델이 선택적으로 연관시킬 수 있으므로 생성 프로세스가 쉬워진다.  
