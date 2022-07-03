# Pose-Controllable Talking Face Generation by Implicitly Modularized Audio-Visual Representation
## Abstract
임의 인물에 대한 오디오 기반 talking face 생성에 대해 입모양을 정확하게 맞추는것은 성공적으로 연구되어 왔지만 효과적으로 머리의 포즈를 움직이는 방법은 여전히 문제이다.  
과거 연구는 리드미컬한 움직임을 생성하는것을 목표로 landmark나 3D 파라미터와 같은 사전 추정된 구조적 정보에 의존한다.  
그러나 극단적 조건 하에서 부정확한 추정 정보를 활용하는 것은 성능 저하를 야기한다.  
본 논문에서, 깔끔하고 효율적인 pose 제어가능한 talking face 제작 방법을 제안한다.  
Identity reference로 정렬되지 않은 단일 사진을 사용한다.  
핵심은 implicit 저차원의 포즈 code를 고안하여 오디오-시각 표현을 모듈화하는것이다.  

실질적으로, 음성 콘텐츠 & 헤드 포즈는 공동으로 non-identity embedding space에 있다.  
음성 정보는 audio-visual modaliy 간 고유한 동기화를 학습하여 정의할 수 있지만, 우리는 pose code가 modulated convolution 기반 재구성 프레임워크에서 보완적으로 학습될 것임을 확인한다.  
광범위한 실험에 따르면 우리의 방법은 다른 비디오에 의해 포즈를 제어할 수 있는 립싱크 talking face를 정확하게 생성한다.  
또한, 우리 모델은 극단적인 시점의 강인성과 talking face 정면화를 포함한 여러 고급 기능을 가지고 있다.  

