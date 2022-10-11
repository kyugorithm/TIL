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

이 논문에서는 체계적인 분석을 통해 motion jittering 문제를 탐구한 후 효과적인 으로 문제를 완화합니다. 특히, 우리는 이 방법이 매우 대표적이고 이전 작업에서 널리 사용되었기 때문에 기본 말하는 얼굴 생성 파이프라인을 기본 모델로 선택합니다. 이 파이프라인에서 먼저 추출된 오디오 특징에서 입 관련 표현 매개변수를 추정합니다. 그런 다음 표정 매개변수와 모양 및 포즈 매개변수(배경 이미지에서)가 3D 얼굴 모델의 입력으로 결합되어 애니메이션된 얼굴 모양(이 작업에서 사용된 3D 얼굴 표현)을 렌더링합니다. 대상 현실적인 얼굴 이미지를 합성하기 위해 신경 렌더러를 사용하여 배경 이미지와 애니메이션된 얼굴 모양의 연결 입력이 주어지면 이미지를 예측합니다. 그러나 3D 얼굴 표현을 사용하는 것은 혀와 치아의 정보가 손실되어 얼굴 세부 사항을 설명하는 데 비효율적입니다. 정보 손실을 보상하기 위해 오디오 기능과 이미지 기능을 융합하는 오디오 융합 모듈(그림 3(왼쪽 상단) 참조)을 설계했습니다.
