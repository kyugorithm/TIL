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

(3) 합성된 talking face에 있어 최종 rendering-video 모듈에 대한 보조 eye-attention map에 추가로 포함된 눈 깜빡임의 AU를 예측할 수 있다.
