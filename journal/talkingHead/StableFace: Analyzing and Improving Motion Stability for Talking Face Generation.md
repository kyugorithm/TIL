## Abstract
과거 speech-driven talking face generation 방법론은 시각 품질과 입술의 싱크 품질 향상에 있어 엄청난 발전을 이뤄왔지만, talking face video의 사실감을 엄청나게 손상시킬 수 있는 lip motion jitter에 관심은 매우 낮았다.  
Motion jitter의 원인과 해결책은 무엇인가? 본 논문에서 우리는 입력 오디오와 출력 비디오를 연결하기 위한 3D 얼굴 표현을 사용하는 SOTA pipeline을 기반하여 motion jittering 문제에 대해 체계적으로 분석을 수행하고 연속적인 효과적 설계를 가지고 motion stability를 향상시킨다.  

Keyword : 이미지 품질 / 입술 싱크 품질 / 떨림 안정성

Jitter가 발생할 수 있는 아래와 같다.  
1) 입력 3D face 표현의 jitter
2) training-inference mismatch
3) 비디오 프레임들 간 dependency 모델링의 부재

따라서 위 문제들을 해결하기 위해 아래 효과적인 해법을 제안한다.  
1) Gaussian-based adaptive smoothing module : 입력의 jitter를 제거하기 위해 3D face representation을 smooth 한다.  
2) Mismatch를 줄이기 위해 intference의 왜곡을 시뮬레이션하기 위해 학습에서 neural renderer의 입력 데이터에 augmented erosion을 추가한다.  
3) 비디오 프레임들 사이에서 dependency를 모델링하기 위해 audio가 혼합된 transformer G를 개발한다.  

추가로, Talking face video에서 motion jitter를 측정하기 위한 기존의 메트릭이 없는것을 고려하여 정량적으로 motion jitter를 가속도 분산 역수를 계산하여 측정하는 objective metric (**Motion Stability Index**, MSI)를 고안한다.  

## 1. Introduction


Talking face video generation은 영화 제작, 만화, TV 쇼, 뉴스 캐스팅, 가상 비서 및 메타버스의 가상 아바타 등과 같은 멀티미디어 응용 프로그램에 대한 유망한 잠재력을 있다. Talking face synthesizing system은 일반적으로 음성을 입력으로 받아 음성의 시각적 내용을 전달하는 사실적인 말하는 얼굴 이미지 시퀀스를 생성한다. 사실적인 talking face video를 생성하는 것은 가치가 높지만 높은 이미지 품질과 립싱크 품질뿐만 아니라 좋은 모션 안정성이 필요하다는 점에서 어렵습니다. 예를 들어, 그림 1과 같이 모션 지터(몇 개의 연속 프레임에서 입이나 머리의 불규칙하거나 부자연스러운 움직임)는 TFV의 현실성을 심각하게 훼손한다. 최근 몇 년 동안 다양한 실제적인 말하는 얼굴 생성 방법이 제안되었지만, 이들 연구는 대부분 합성된 각 이미지의 화질 또는 립싱크 품질을 향상시키는 데 중점을 두는 경향이 있다. 한편, 이러한 작업은 일반적으로 단일 프레임 기반 메트릭(PSNR, SSIM, LMD)으로 비디오 품질을 정량적으로 평가하고 인간 중심의 주관적인 실험을 통해 비디오 현실성을 측정하여 **모션 지터링 문제에 덜 주의를 기울임**으로써 과제를 해결하지 못한 채로 남아 있다.

이 논문에서는 체계적인 분석을 통해 motion jittering 문제를 탐구한 후 효과적인 해법으로 문제를 완화한다. 특히, 우리는 매우 대표적이고 이전 작업에서 널리 사용된 기본적인 talking face 생성 파이프라인을 기본 모델로 선택한다. 이 파이프라인에서 먼저 추출된 오디오 feature에서 **mouth-related expression parameters**를 추정한다. 이후 expression parameters와 shape and pose parameters(배경 이미지에서)가 3D 얼굴 모델의 입력으로 결합되어 애니메이션된 얼굴 모양(이 작업에서 사용된 3D 얼굴 표현)을 rendering한다. Target realistic face image 합성을 위해 nerual renderer를 사용하여 배경 이미지와 애니메이션된 얼굴 모양의 연결 입력이 주어지면 이미지를 예측한다. 그러나 3D 얼굴 표현을 사용하는 것은 혀와 치아의 정보가 손실되어 얼굴 세부 사항을 설명하는 데 비효율적이다. 정보 손실을 보상하기 위해 오디오 feature와 이미지 feature를 융합하는 audio fusion module(AFM)(그림 3(왼쪽 상단) 참조)을 설계했다.  

몇 가지 예비 분석을 통해 모션 지터를 발생시키는 몇 가지 주요 이유를 아래와 같이 찾았다.  
(1) 3D face representation에서 발생하는 지터 :  
3D face representation은 자세한 입 정보와 머리 포즈를 제공하고 neural renderer의 입력 역할을 한다. 인접 프레임 정보를 고려하지 않고 단일 이미지의 3D 얼굴 모델에 의해 추출되기 때문에 프레임 간에 매끄럽지 않고 jitter가 있을 수 있으며 audio-to-expression 예측 네트워크에 불안정한 gt 레이블을 제공한다.  

(2) Neural renderer의 학습-추론 불일치 :  

학습 단계에서 neural renderer는 배경 이미지와 얼굴 모양으로부터 사실적인 이미지를 생성하도록 최적화된다. 그러나 배경 이미지와 얼굴 모양은 동일한 대상 이미지에서 가져온 것이므로 최적화 절차를 완화할 수 있지만 추론에서 불일치가 발생할 수 있다. Inference에서 같은 배경과 일치하지 않는 새로운 오디오로 인해 입 부분이 변경된 얼굴 모양. 함께 concat.할때 모델은 얼굴 모양에서 입 부분이 있는 사실적인 얼굴을 생성하고 나머지는 배경 이미지에서 생성해야 한다. 이것은 모델이 학습에서 한 번도 본 적이 없는 불일치를 처리하기 어렵게 하여 불확실성을 부과하고 렌더링된 이미지에서 motion jitter를 유발한다.  

(3) Neural renderer의 연속 프레임에 대한 종속성 모델링을 고려하지 않는다. 현재 프레임워크의 neural renderer는 연속 프레임 간의 종속성을 모델링하지 않고 각 이미지를 독립적으로 합성하는 방법을 학습하므로 motion stability talking face video 생성에 실패한다.

모션 지터를 유발하는 이러한 문제를 해결하기 위해 몇 가지 효과적인 솔루션을 제안한다.  

(1) 3D face reconstruaction에서 jitter를 제거:  
Smoothing을 위한 간단한 방법은 moving average 혹은 manually designed smoothing weights를 사용하는 것이다. 그러나 둘 다 다양한 속도(빠르거나 느림)로 입의 움직임을 처리할 수 없고, 지나치게 안정적인 움직임의 문제가 발생하고 유사한 발음 간의 차이를 제거하거나 움직임이 덜 안정적인 결과를 생성한다. 이를 방지하기 위해 smoothing weight estimation network를 학습하여 3D 얼굴 표정이 주어지면 각 프레임에 대해 서로 다른 가중치를 적응적으로 예측한다. 

(2) 추론의 불일치를 시뮬레이션하기 위해 학습에서 배경 이미지에 augmented erosion을 도입했다. Augmented Erosion 모듈은 추론의 잠재적 불일치를 시뮬레이션하기 위해 다양한 모양 이미지로 입 영역을 무작위로 erosion했다. Augmented erosion을 통해 neural renderer는 입 영역의 왜곡에 더 강력하고 jitter를 줄인다.  

(3) Talking face generation을 sequence-to-sequence 생성 작업으로 처리하여 transformer 기반 dependency 모델링 모듈을 개발하고 이를 neural renderer에 포함한다. 우리의 종속성 모듈은 temporal relations modeling에서 transformer 이점을 활용하여 motion stability를 개선하는 데 기여한다.

Motion jitter 문제에 대한 연구와 마찬가지로 motion jitter를 정량적으로 평가하는 것은 주관적인 실험에 드는 비용을 줄일 뿐만 아니라 개별 사용자 편견을 도입하지 않고 비디오의 모션 안정성을 평가하는 talking head 생성에 의의가 있다. 그러나 motion jitter는 단일 또는 두 개의 이미지가 아닌 일련의 이미지에서 관찰할 수 있어 모션 안정성의 품질을 정의 및 측정하기 어렵다는 점에서 motion jitter를 평가하기가 어렵다. Talking face 비디오에서 움직임 안정성이나 motion jitter를 측정할 수 있는 기성 메트릭이 없기 때문에 움직임이 안정적인 talking face 생성에 대한 추가 탐색이 지연된다. 이 간극을 메우고 향후 연구를 용이하게 하기 위해 우리는 말하는 얼굴 비디오에서 모션 안정성을 측정하기 위해 MSI(Motion Stability Index)라는 객관적인 메트릭을 고안했다. 특히 얼굴 영상에서 각 키 포인트의 가속도 편차의 역수를 이용하여 움직임의 안정성을 측정하였다. 실험에 따르면 MSI와 동작 안정성에 대한 주관적 점수 사이의 Pearson 상관 계수는 0.438에 도달하여 MSI의 효능을 보여줍니다.  

요약하면, 주요 기여는 다음과 같이 표시할 수 있다.

(1) Motion jitter 문제를 체계적으로 연구하고 원인을 분석한다. 우리가 아는 한, 이것은 talking face generation 작업에서 motion jittering 문제에 초점을 맞춘 첫 번째 작업이다.  
(2) Motion jitter 문제를 해결하기 위해 합성된 talking face 비디오의 motion stability를 개선하기 위해 아래 3가지를 포함하여 여러가지 체계적 설계를 제안한다.  
(1. adaptive smoothing module, 2. augmented erosion, 3. transformer 기반 dependency 모델링 모듈)  
(3) Talking face 생성에 대한 연구를 용이하게 하기 위해 얼굴 동영상에서 motion stability를 정량적으로 평가하는 효과적인 객관적 측정법(MSI)을 제안한다. (Ablation study는 제안된 메트릭의 효율성을 보여준다.)  


##### 2) Augmented Erosion
더 나은 움직임 안정성을 위한 renderer의 훈련-추론 불일치 문제를 해결하기 위해, 추론의 불일치 패턴을 시뮬레이션하기 위해 훈련에서 배경 이미지에 증강 침식을 추가합니다.

1) 입 영역의 원래 얼굴 표정에 무작위 노이즈를 추가한 다음 Deca에서 생성된 입 영역 마스크를 통해 침식된 이미지를 만듭니다.  
2) 추론 단계에서 불일치 패턴을 시뮬레이션하기 위해 마스크를 임의로 침식/확장 및 이동/회전합니다.  

G는 이 작업의 이점을 얻고 다양한 이미지 모양 패턴에서 입 주변의 이미지를 합성하는 방법을 학습하므로 추론 단계에서 더욱 견고해집니다.  
배경 이미지에 대한 증강 침식 결과는 그림 3에서 볼 수 있습니다.

**Implementation Detail.** 
audio2expression과 Neural Rendering이라는 두 단계로 모델을 훈련한다.  

1) **Audio2expression** : (오디오 시퀀스에서 오디오 특징) (비디오 프레임에서 3D 표정 매개변수 추출) - (오디오에서 표정 매개변수로의 매핑이 주요 기여가 아님)  
Transformer-S2A 설정을 따라 audio2expression 모델을 훈련한다.  

2) **Neural Rendering** : 12개의 연속 프레임을 시퀀스로 취급하고 Neural Renderer와 adaptive smoothing 모듈을 훈련시킨다.  
먼저 적응형 스무딩 모듈 없이 신경 렌더러를 100epoch 학습하고 다른 20epoch 동안 공동으로 학습한다.  
적응형 스무딩 모듈은 가볍고 11k 학습 가능한 매개변수만 포함하므로 신경 렌더러(1e-4)보다 작은 학습률(1e-6)로 최적화한다.  
전체 훈련 과정에서 입력 이미지에 대해 증강 침식을 사용하고 침식된 이미지를 얻은 다음 신경 렌더러의 입력으로 부드러운 얼굴 모양과 연결합니다.
