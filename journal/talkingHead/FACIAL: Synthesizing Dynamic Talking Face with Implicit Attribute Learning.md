## Abstract

오디오 신호를 입력으로, 짧은 target 동영상을 기준으로 삼아 입력 음성과 동기화된 (자연스러운 입술 동작, 헤드 포즈, 눈 깜빡임)으로 target 얼굴의 실제같은 영상을 합성하는 talking face 생성 방법 제안  
합성얼굴의 속성에는 음성과 상관관계가 높은 **명시적 속성**(입술동작)과 **암시적 속성**(헤드포즈, 눈 깜빡임)이 모두 포함됨을 주목한다.  

입력 오디오를 사용하여 여러 얼굴 속성 간의 복잡한 관계를 모델링하기 위해 (음성 인식, 컨텍스트 인식 및 id 인식) 정보를 통합하여 속성들(입술, 헤드 포즈,눈 깜빡임)의 현실적인 움직임으로 3D 얼굴 애니메이션을 합성하는 FACIAL-GAN을 제안한다.  
그런 다음 Rendering-to-Video 네트워크는 렌더링된 얼굴 이미지와 눈 깜빡임 attention map을 입력으로 사용하여 사실적인 출력 비디오 프레임을 생성한다.  
실험 결과와 사용자 연구에 따르면 우리의 방법은 동기화된 입술 동작뿐만 아니라 자연스러운 머리 움직임과 눈 깜빡임으로 현실적인 말하는 얼굴 비디오를 생성할 수 있다.

## 1. Introduction

입모양 동기화에 더불어 (개인화되고 자연스러운 머리 움직임과 눈 깜빡임)을 가진 실제와 구별할 수 없는 사실적인 결과를 생성하는 것은 매우 어렵다.  

Dynamic talking face에 포함된 정보는 크게 두 가지 수준으로 분류될 수 있다.  
1) Explicit attribute(입력 오디오와 동기화되어야 하는 속성) : 청각 음성학의 신호와 강한 상관관계를 갖는 입술 움직임  
2) Implicit attribute(음성 신호와 약한 상관관계만을 갖는 속성) : 말의 맥락과 개인화된 대화 스타일과 눈 깜빡임과 관련된 머리 동작은 주로 외부 자극뿐만 아니라 개인적인 건강 상태에 의해 결정된다.  

기존 연구의 대부분은 입력 오디오와 입술 동작을 동기화하여 명시적인 속성에만 초점을 맞추려 한다.  
1) Zhou : 음성을 인물 관련 정보와 음성 관련 정보로 분리하여 선명한 입술 패턴을 생성 
2) Chen : ATVG 네트워크는 오디오를 landmark로 전송하고 랜드마크를 조건으로 한 비디오 프레임을 생성  

Implicit attribute(헤드 포즈)와 입력 오디오 사이의 상관관계를 탐구하는 노력은 아래와 같이 적다.  
Chen : 각 입력 프레임의 변환 행렬을 예측하기 위해 헤드 포즈 학습자로 MLP를 사용했지만 다음 질문에 대해 불분명 하다.  
- 명시적이고 암묵적인 속성이 잠재적으로 서로에게 어떤 영향을 미칠 수 있는가?  
- 음성 신호뿐만 아니라 말의 context 정보와 개인화된 대화 스타일에 의존하는 머리 자세와 눈 깜빡임과 같은 암시적 속성을 모델링하는 방법은 무엇인가?  

위 과제를 해결하기 위해, 그림 2와 같은 프레임워크를 제안한다.  

(1) Head pose learner로 implicit attribute를 예측하는 이전 작업과 달리, adversarial learning의 regularization과 함께 implicit/explicit attribute를 공동으로 학습  
Action Unit(AU)(눈 깜빡임, 헤드 포즈, 표정, id, 텍스처 및 조명)을 포함한 모든 속성을 협업 방식으로 포함시켜 talking face generation을 위한 잠재적 상호 작용을 동일한 프레임워크에서 모델링할 수 있도록 제안한다.  

(2) 음성, 문맥, 개인화 정보를 함께 학습하기 위해 FACIAL-GAN을 설계한다.  
그룹화된 입력(프레임 시퀀스)을 취하고 개별 프레임 기반 G에 의해 각 프레임의 음성 정보와 함께 추가로 인코딩되는 상황별 잠재 벡터를 생성한다.  
처음에 전체 데이터 세트에 대해 훈련되고(4장) 짧은 비디오(2~3분)가 주어지면, 이 짧은 비디오로 미세 조정되어 그 안에 포함된 개인화된 정보를 캡처할 수 있다.  
따라서 헤드 포즈와 같은 암시적 속성의 모든 음성, 상황 및 개인화된 정보를 잘 포착할 수 있다.  

(3) 최종 rendering-video 모듈에 대한 보조 eye-attention map에 embedding으로 포함된 눈 깜빡임의 AU를 예측할 수 있다.  

excplicit/implicit attribute 공동 학습을 통해, SOTA결과를 얻는다.  
이 논문의 기여는 세 가지이다.  

(1) 오디오에 동기화된 (lip motion, 개인화되고 자연스러운 head motion 및 현실적인 눈 깜빡임)과 함께 사실적인 talking face video를 합성하기 위한 공동 explicit/implcit attribute 학습 프레임워크 제안  
(2) 자연스러운 머리 움직임을 합성하는 데 필요한 implicit attribute를 모델링하기 위해 각 프레임의 음성 정보로 contenxt 정보를 인코딩하는 모듈을 설계  
(3) 렌더링된 얼굴의 eye-attention map에 FACIAL-GAN 생성 눈 깜빡임 AU를 포함시켜 Rendering-to-Video 모듈에 의해 생성된 결과 비디오에서 현실적인 눈 깜빡임을 달성

## 2. Related Work
### Audio-driven talking face generation

기존 방법은 입력 오디오와 동기화된 비디오를 생성하는 데 중점을 두었다.

Chung : 얼굴과 오디오의 공동 임베딩을 사용하는 인코더-디코더 CNN 모델 제안  
Chen : 오디오를 랜드마크로 전송하고 랜드마크를 조건으로 한 비디오 프레임을 생성하는 계층 구조를 제안  

하지만 연설하는 동안 머리 자세는 거의 고정되어 있다. 헤드 모션을 사용하여 사실적인 비디오를 얻기 위해, 몇 가지 기술은 먼저 입력 오디오와 동기화된 입술 영역을 생성하고 원본 비디오로 구성한다.  

Suwajanakorn: 오바마의 오디오 스트림을 사용하여 그의 연설의 사실적인 비디오를 합성했다. 그러나 이 방법은 많은 양의 비디오 영상이 필요하기 때문에 다른 캐릭터에도 적용할 수 있다.  

Thies: latent 3D 모델 공간을 사용하여 다양한 사람들이 사용할 수 있는 말하는 얼굴 비디오를 생성하지만 본질적인 한계로 인해 머리 움직임과 얼굴 표정을 분리할 수 없고 머리 동작이 입력 오디오와 무관하다는 것을 의미한다.  

Chen과 Yi : 입력 오디오에서 직접 머리 움직임을 생성하는 데 초점을 맞추었다.  
Yi : 개인화된 머리 포즈로 사실적 영상을 생성하기 위해 memory-augmented GAN 모듈을 제안했다. 그러나 네트워크와 3D 모델의 한계로 인해 생성된 얼굴 표정(예: 눈 깜빡임)과 머리 움직임은 정지하는 경향이 있다.  

그에 비해, 우리는 FACIAL GAN 모듈을 도입하여 발화의 (음성, 상황 및 개인화된 정보)를 통합하고 합성된 3D 모델을 AU attention-map과 결합하여 (동기화된 입술 움직임, 개인화된 자연스러운 머리 자세 및 눈 깜빡임)과 함께 사실적인 영상을 생성한다.

### Video-driven talking face generation

소스 비디오 프레임에서 대상 비디오 프레임으로 (표정/자세)를 전송한다.  

Zakharov : 보지 않은 neural talking head model의 몇 번의 원샷 학습을 고용량 GAN 문제로 프레임화하는 시스템을 제시했다.  
Kim : 생성된 3D 모델을 기반으로 (헤드 포즈, 얼굴 표정, 시선, 깜박임)을 소스에서 타겟 으로 전송하는 generative neural network을 도입했다. 그러나 머리 움직임과 얼굴 표정은 소스 비디오에 의해 안내되기 때문에, 이러한 방법은 소스 비디오와 일치하는 미리 결정된 talking head 움직임과 표정만 생성할 수 있다.

## 3. Approach
### 3.1. Problem Formulation

![image](https://user-images.githubusercontent.com/40943064/202853604-3117f56e-7b1f-457f-b3fb-8e3039f0dc6d.png)

## Dataset Collection
Explicit & implicit을 joint하게 통합하기 위해 Zhang의 talking head dataset을 이용한다. (dynamic head poses, eye motions, lip syncronization 등의 풍부한 정보를 지님)  
#### Audio preprocessing.
Speech feature(초당 50 프레임으로 문자의 log 확률을 정규화하여 출력)를 추출하기 위해 DeepSpeech를 사용한다. Feature dimention은 29이므로 50 X 29의 array 사이즈를 가진다.  
이 데이터를 비디오 프레임과 맞추기 위해 30프레임으로 resample하여 30 X 29의 사이즈로 만든다.

#### Head pose & eye moiton field.
각 비디오 프레임에 대한 얼굴 파라미터 생성을 하기 위한 eye motion과 head pose를 수집하기 위해, OpenFace를 선택한다.  
Rigid head pose와 3D translation vector는 각각 오일러 각도로 표현되어 6개 차원(pitch xy, yaw xy, roll xy)와 3차원 정보를 가진다.  
Eye motion을 묘사(눈영역 주변의 근육에 대한 움직임 강도를 표현하기 위해 )하기 위해 AU를 사용한다.  

#### 3D face reconstruction.
Deng의 3D recon. 방법을 사용하여 3DMM파라미터 ID(80), 표정(64), 텍스쳐(80), 조도(27) 정보를 추출하도록 한다.

#### Dataset statistics.
제안한 데이터셋은 Agarwal에 의해 사용된 450개 이상의 풍부한 비디오 클립을 포함한다. 각 피디오 클립은 30fps에 1분(1800 frames) 가량 지속되어 총 535,400 frames의 양을 가진다.  
이 데이터를 5-1-4(train/val/test)로 분할한다. 각 비디오 클립들은 안정적인 얼굴 생성을 위해 안정적으로 고정된 파라미터, 적절한 조명, 그리고 단일 화자의 환경이 유지된다.  


## 5. Experiments
### 5.1. Network Learning

#### Training.
(1) FACIAL-GAN 일반 학습 : 전체 학습 데이터(Zhang) 기반 L_facial 최적화 - audio와 생성된 attribute사이의 일반적인 mapping 고려  
(2) 파라미터 추출 : 레퍼런스 비디오 V가 주어지면 파라미터 추출 - a(audio feature), 3D face model, p(head pose), e(깜빡임 AU)  
(3)-1 FACIAL-GAN 개별학습 : L_facial를 fine-tune 하여 개별 스타일에 일반화 된 표현 학습  
(3)-2 render2video 학습 : L_render를 통해 attention map과 redering을 이용  

#### Testing.
1) 파라미터 추출 : fine-tuned FACIAL-GAN을 이용해 audio feature로 V의 개인화된 화법을 가지는 (표정-f, 포즈-p, 깜빡임-e) 추출  
2) Render    : 얼굴이미지와 eye attention map render  
3) render2video : V로 개인화된 스타일의 사실적 비디오로 변환  

#### Experiment details.
T(sliding window size) = 128. & Sliding distance = 5  
General training : 50 epochs * batchSize 64  
Fine training    : 10 epochs * batchSize 16
R2V training     : 50 epochs * batchSize 1 (lr decay from 30 epochs)
parameters : w(2, 1, 5, 10, 10, 0.1) / lambda(2, 10, 50)


