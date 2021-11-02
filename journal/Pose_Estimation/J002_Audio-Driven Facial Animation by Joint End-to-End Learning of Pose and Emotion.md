# Audio-Driven Facial Animation by Joint End-to-End Learning of Pose and Emotion

## Abstract 
낮은 latency의 실시간 오디어 입력을 통해 3D 얼굴 애니메이션을 만드는 ML 기법을 제시한다.  
DL은 입력 음성파형을 얼굴 모델의 3D vertex 좌표축으로 mapping을 한다.  
동시에 오디오 만으로는 설명할 수 없는 얼굴 표정 변화를 모호하게 하는 compact하고 latent한 code를 찾아낸다.  
추론 과정에서 latent 코드는 얼굴 모델의 감정 상태를 직관적으로 제어하는데 사용된다. 
전통적인 비전기반의 performance capture method를 사용하여 3-5분의 고품질 애니메이션 데이터를 얻어 네트워크를 학습한다.
우선적인 목표가 단일 actor의 말하기 스타일을 모델링하는것이지만  
우리 모델은 심지어 다른 성별, 강쇠, 언어등의 변화를 가진 오디오를 이용할 때에도 합리적인 결과를 만들어 낸다.  
