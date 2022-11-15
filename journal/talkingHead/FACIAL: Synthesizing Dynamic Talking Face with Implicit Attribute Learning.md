## Abstract

오디오 신호를 입력으로, 짧은 target 동영상을 기준으로 삼아 입력 음성과 동기화된 (자연스러운 입술 동작, 헤드 포즈, 눈 깜빡임)으로 target 얼굴의 실제같은 영상을 합성하는 talking face 생성 방법 제안  
합성얼굴의 속성에는 음성과 상관관계가 높은 **명시적 속성**(입술동작)과 **암시적 속성**(헤드포즈, 눈 깜빡임)이 모두 포함됨을 주목한다.  

입력 오디오를 사용하여 여러 얼굴 속성 간의 복잡한 관계를 모델링하기 위해 (음성 인식, 컨텍스트 인식 및 id 인식) 정보를 통합하여 속성들(입술, 헤드 포즈,눈 깜빡임)의 현실적인 움직임으로 3D 얼굴 애니메이션을 합성하는 FACIAL-GAN을 제안한다.  
그런 다음 Rendering-to-Video 네트워크는 렌더링된 얼굴 이미지와 눈 깜빡임 attention map을 입력으로 사용하여 사실적인 출력 비디오 프레임을 생성한다.  
실험 결과와 사용자 연구에 따르면 우리의 방법은 동기화된 입술 동작뿐만 아니라 자연스러운 머리 움직임과 눈 깜빡임으로 현실적인 말하는 얼굴 비디오를 생성할 수 있다.

## 1. Introduction

Synthesizing dynamic talking faces driven by input audio has become an important technique in computer vision, computer graphics, and virtual reality. There have been steady research progresses, however, it is still very challenging to generate photorealistic talking faces that are indistinguishable from real captured videos, which not only contain synchronized lip motions, but also have personalized and natural head movements and eye blinks, etc.   
입모양 동기화에 더불어 (개인화되고 자연스러운 머리 움직임과 눈 깜빡임)을 가진 실제와 구별할 수 없는 사실적인 결과를 생성하는 것은 매우 어렵다.  

The information contained in dynamic talking faces can be roughly categorized into two different levels: 1) the attributes that need to be synchronized with the input audio, e.g., the lip motion that has strong correlations with the signals of auditory phonetics; 2) the attributes that have only weak correlations with the phonetic signal, e.g., the head motion that is related to both the context of speech and the personalized talking style and the eye blinking whose rate is mainly decided by personal health condition as well as external stimulus. Here we call the first type of attributes to be explicit attributes, and the second type to be implicit attributes.  
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
(1) Head pose 학습자를 사용하여 암시적 속성을 예측하는 이전 작업과 달리, 적대적 학습의 정규화와 함께 암시적 및 명시적 속성을 공동으로 학습  
눈 깜빡임, 헤드 포즈, 표정, 정체성, 텍스처 및 조명의 Action Unit(AU)를 포함한 모든 속성을 협업 방식으로 포함시켜 대화 얼굴 생성을 위한 잠재적 상호 작용을 동일한 프레임워크에서 모델링할 수 있도록 제안한다.  
(2) 음성, context를 공동으로 학습하기 위해 이 프레임워크에서 특별한 FACIAL-GAN을 설계한다.  
개인화된 정보를 제공한다. 그것은 그룹화된 입력으로 프레임 시퀀스를 취하고 개별 프레임 기반 생성기에 의해 각 프레임의 음성 정보와 함께 추가로 인코딩되는 상황별 잠재 벡터를 생성한다.  
FACIAL-GAN은 처음에 전체 데이터 세트에 대해 훈련된다(4장). 대상 피사체의 짧은 참조 비디오(2~3분)가 주어지면, FACIAL-GAN은 이 짧은 비디오로 미세 조정되어 그 안에 포함된 개인화된 정보를 캡처할 수 있다.  
따라서 우리의 FACIAL-GAN은 헤드 포즈와 같은 암시적 속성의 모든 음성, 상황 및 개인화된 정보를 잘 포착할 수 있습니다.  
(3) 최종 rendering-video 모듈에 대한 보조 눈 깜빡임 맵에 포함되어 합성에서 현실적인 눈 깜빡임을 생성할 수 있다.말 많은 얼굴입니다.

To tackle these challenges, we propose a FACIAL framework for synthesizing dynamic talking faces, as shown in Fig. 2. (1) Unlike the previous work predicting implicit attributes using an individual head pose learner, our FACIAL framework jointly learns the implicit and explicit attributes with the regularization of adversarial learning. We propose to embed all attributes, including Action Unit (AU) of eye blinking, head pose, expression, identity, texture and lighting, in a collaborative manner so their potential interactions for talking face generation can be modeled under the same framework. (2) We design a special FACIAL-GAN in this framework to jointly learn phonetic, contextual, and personalized information. It takes a sequence of frames as a grouped input and generates a contextual latent vector, which is further encoded together with the phonetic information of each frame, by individual frame-based generators. FACIAL-GAN is initially trained on our whole dataset (Sec. 4). Given a short reference video (2 ∼ 3 minutes) of the target subject, FACIAL-GAN will be fine-tuned with this short video, so it can capture the personalized information contained in it. Hence our FACIAL-GAN can well-capture all phonetic, contextual, and personalized information of the implicit attributes, such as head poses. (3) Our FACIAL-GAN can also predict the AU of eye blinks, which is further embedded into an auxiliary eye-attention map for the final Rendering-to-Video module, to generate realistic eye blinking in the synthesized talking face.  

With the joint learning of explicit and implicit attributes, our end-to-end FACIAL framework can generate photorealistic dynamic talking faces as shown in Fig. 1, superior to the results produced by the state-of-the-art methods. The contribution of this paper is threefold: (1) We propose a joint explicit and implicit attribute learning framework to synthesize photo-realistic talking face videos with audiosynchronized lip motion, personalized and natural head motion, and realistic eye blinks. (2) We design a FACIALGAN module to encode the contextual information with the phonetic information of each individual frame, to model the implicit attributes needed for synthesizing natural head motions. (3) We embed the FACIAL-GAN generated AU of eye blinking into an eye-attention map of rendered faces, which achieves realistic eye blinks in the resulting video produced by the Rendering-to-Video module.
