## Abstract
과거 speech-driven talking face generation 방법론은 시각 품질과 입술의 싱크 품질 향상에 있어 엄청난 발전을 이뤄왔지만, talking face video의 사실감을 엄청나게 손상시킬 수 있는 lip motion jitter에 관심은 매우 낮았다.  
Motion jitter의 원인과 해결책은 무엇인가? 본 논문에서 우리는 입력 오디오와 출력 비디오를 연결하기 위한 3D 얼굴 표현을 사용하는 SOTA pipeline을 기반하여 motion jittering 문제에 대해 체계적으로 분석을 수행하고 연속적인 효과적 설계를 가지고 motion stability를 향상시킨다.  

Jitter가 발생할 수 있는 아래와 같다.  
1) 입력 3D face 표현의 jitter
2) training-inference mismatch
3) 비디오 프레임들 간 dependency 모델링의 부재

따라서 위 문제들을 해결하기 위해 아래 효과적인 해법을 제안한다.  
1) Gaussian-based adaptive smoothing module : 입력의 jitter를 제거하기 위해 3D face representation을 smooth 한다.  
2) Mismatch를 줄이기 위해 intference의 왜곡을 시뮬레이션하기 위해 학습에서 neural renderer의 입력 데이터에 augmented erosion을 추가한다.  
3) 비디오 프레임들 사이에서 dependency를 모델링하기 위해 audio가 혼합된 transformer G를 개발한다.  
추가로, Talking face video에서 motion jitter를 측정하기 위한 기존의 메트릭이 없는것을 고려하여 정량적으로 motion jitter를 reciprocal of variance acceleration을 계산하여 측정하기 위해 objective metric (**Motion Stability Index**, MSI)를 고안한다.  
