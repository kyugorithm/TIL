## Abstract
단일 입력 오디오에 대해 출력 이미지는 다양할 수 있기 때문에 deterministic mapping을 하면 학습이 모호해지고 이미지 품질이 떨어지게 된다.
이를 해결하기 위해 2-stage(Audio2Expression -> Rendering)로 문제를 분리해도 입력 정보(감정, 주름 등)가 충분치 않으면 결과가 좋을 수 없다.
Two-stage 방식을 따르는 implicit/explicit memory로 부족한 정보를 보완한다.
- Audio2expression : High-level semantics를 포착하기 위해 implicit memory 적용
- Neural-Rendering : Pixel 수준의 합성을 위해 explicit memory 적용 

## 1. Introduction

일반적으로 중간 표현을 활용하는 2stage 방식을 사용한다.
1) Audio2expression : Intermediate representation(2D landmark, blendshape coefficient) 활용
2) neural-renderer : 예측한 representation에 따라 video portrait 생성

위 방법론을 따라 자연스러운 머리의 움직임, 입술싱크 품질, 표정 표현 생성 등이 개선되어 왔다.
Audio2video 데이터로 부터의 deterministic mapping을 학습하는 방식으로 편향되어왔지만 본질적인 문제는 one-to-many mapping 이라는 점에 주목할 가치가 있다.
즉, 입력 오디오 클립에 대해 phoneme context, emotion, illumination 등의 변화로 인해 대상 인물의 가능한 시각적 모습이 여러 개 있음을 의미한다.
이런식으로 deterministic mapping을 학습하면 모호성이 생겨 사실적인 시각 결과를 산출하기가 더 어려워진다.

위 문제는 두 개의 하위 문제로 분해하기 때문에 부분적으로 완화할 수 있지만 각 단계에서 부족한 입력 정보로 예측하도록 최적화되어 있어 예측이 어렵다.  
Audio-to-expression : 습관, 태도 등과 같은 high-level semantic이 없는 입력 오디오와 의미론적으로 일치하는 표정을 생성하는 방법을 학습  
Neural-renderer : 추정된 표정 정보를 입력하여 픽셀 단위의 시각적 모양을 합성  

위 문제를 완화하기 위해 두 단계 방식을 각각 따르는 implicit memory와 explicit memory를 고안하여 missing information을 메모리로 보완하는 방법을 제안한다.  
Implicit memory : 의미적으로 정렬된 정보를 보완하기 위해 audio2expression과 공동으로 최적화  
Explicit memory : non-parametric 방식으로 구성되고 각 대상 인물에 맞게 조정되어 시각적 세부 사항을 보완한다.  
따라서 입력 오디오를 직접 사용하여 표정을 예측하는 대신 Audio-to-expression은 추출된 audio feature를 query로 활용하여 implicit memory에 주의를 기울인다. 의미적으로 정렬된 정보로 제공되는 attention 결과는 audio feature로 보완되어 표현 출력을 생성한다. End-to-end 학습을 가능하게 함으로써 implicit memory는 audio-expression 공유 공간에서 high-level-semantics를 연관시키도록 하여 입력 오디오와 출력 표정 사이의 의미론적 격차를 좁힌다. Neural-renderer를 사용하여 추정된 표정으로 얻은 입 모양을 기반으로 시각적 외모를 합성한다. Pixcel-level 세부 사항을 추가로 보완하기 위해 먼저 3D 얼굴 모델의 vertex와 관련 이미지 patch를 각각 key/value로 간주하여 각 사람에 대한 명시적 메모리를 구성한다. 그런 다음 각 입력 식에 대해 해당 vertex를 query로 사용하여 explicit memory에서 유사한 key를 검색하고 관련 image patch를 Neural-rendering에 대한 pixcel-level 세부 정보로 반환한다.  
직관적으로 모델에 explicit memory를 도입함으로써 모델 자체에서 생성하지 않고 표정이 필요한 세부 사항을 모델이 선택적으로 연관시킬 수 있으므로 생성 프로세스가 쉬워진다.  

## 2. Related Works
### 2.1. Talking Face Generation
Pass
### 2.2. Memorybased Networks
Implicit/Explicit memory와 관련된 작업을 소개한다.  

#### Implicit memory
더 나은 memorization을 위해 읽고 쓸 수 있는 특수한 implicit memory를 도입하려는 시도가 많다. 보통 연속적인 메모리 표현 또는 key-value 쌍을 사용하여 메모리를 읽고 쓰기 때문에 end-to-end 방식으로 메모리를 교육할 수 있다. Implicit memory의 성공과 audio2expression 학습의 1to1 매핑 특성 관찰을 바탕으로, 우리는 의미론적으로 정렬된 정보를 보완하고 일대일 매핑을 다루기 위해 implicit memory를 audio2expression에 통합할 것을 제안한다.

#### Explicit memory
Explicit external memory로 신경망을 증강하는 것은 최근 NLP에서 주목을 받고 있다. 학습 데이터 자체만 활용했던 초기 시도와 달리 검색 기반 시각적 모델의 경우 최근의 발전으로 text-image 생성을 위한 외부 메모리가 도입되었다. 모든 샘플에 대해 통합 메모리를 구축한 이러한 접근 방식과 달리, 우리는 각 id에 대한 Explicit memory를 구축하여 사실적인 talking face 생성을 위한 개인화된 시각적 세부 사항을 보완한다. Yi와 Park은 말하는 talking face generation에 memory를 도입했다다.  

우리의 솔루션은  
1) 메모리 네트워크가 렌더링 프로세스를 개선하기 위해 더 많은 ID 정보를 제공하는 paired spatial features(사전 훈련된 ResNet-18에서 추출)과 identity features(사전 훈련된 ArcFace에서 추출)을 저장한다는 점에서 다르다. 대조적으로, 우리는 Explicit memory로 대상의 비디오에서 입 관련 이미지 패치를 직접 검색하여 메모리 구성을 더 쉽게 하고 모델을 더 시각적인 세부 정보로 보완한다.  
2) SyncTalkFace는 오디오 립 메모리를 활용했다, 여기서 audio feature와 lip feature는 각각 키와 값으로 간주된다. 오디오와 시각적 외관 사이의 큰 차이 때문에, 두 가지 양식을 정렬하기 위해 명시적인 제약 조건을 사용했다. 그러나 하나의 메모리에서 의미론과 시각적 세부 사항을 동시에 정렬하는 것은 여전히 어렵다. 대조적으로, 우리의 MemFace는 의미론적으로 정렬된 정보와 픽셀 수준의 세부 사항을 각각 보완하기 위해 Implicit memory와 explicit memory를 사용하여 예측을 더 쉽게 만든다.
