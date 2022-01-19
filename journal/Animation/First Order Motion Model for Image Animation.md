First Order Motion Model for Image Animation


## 1.Introduction

Still 이미지의 object를 애니메이션으로 만들어 비디오를 생성하는 것은 영화, 사진, 전자 상거래를 비롯해 많은 응용 분야가 있다.  
이미지 애니메이션은 source에서 추출한 appearance와 driving video에서 얻은 모션을 결합하여 동영상을 자동으로 합성하는 작업이다.  
예를 들어, 특정 인물의 얼굴 이미지는 다른 개인의 표정에 따라 애니메이션될 수 있다(그림 1 참조).  
기존 대부분의 방법은 object 표현(예: 3D 모델)에 대한 강력한 우선순위를 가정하고 CG 기술에 의존하여 이 문제를 해결한다.  
이러한 접근 방식은 애니메이션할 특정 object의 모델에 대한 지식을 가정하기 때문에 object-specific 방법이라고 할 수 있다.  
최근에는 이미지 애니메이션 및 비디오 retargetting을 위한 효과적인 기술로 딥 생성 모델이 등장했다.  
특히, GAN및 VAE는 비디오에서 인간 주체 간의 얼굴 표정 또는 동작 패턴을 전송하는 데 사용되었다.  
그럼에도 불구하고 이러한 접근 방식은 일반적으로 keypoint 위치와 같은 object별 표현을 추출하기 위해 사전 학습된 모델에 의존한다.  
그러나 사전 학습된 모델은 값비싼 GT annotation을 사용하여 구축되며 보통 arbitrary object category에 사용할 수 없다.  
이를 해결하기 위해 Siarohin은 이미지 애니메이션을 위한 최초의 object-agnostic 심층 모델인 Monkey-Net을 도입했다.  
Monkey-Net은 self-supervised 방식으로 학습된 keypoint를 통해 motion 정보를 인코딩한다.  
테스트에 source는 driving video에서 추정된 해당 keypoint 궤적에 따라 애니메이션된다.  
Monkey-Net은 0차 모델을 가정하는 keypoint neighborhood에서 object 모양 변환을 제대로 모델링하지 않는다(3.1절).  
이는 큰 물체 포즈 변경의 경우 생성 품질이 저하된다(그림 4 참조).  
이 문제를 해결하기 위해 다음을 제안한다.
1) 1차 모션 모델 : 복잡한 동작을 모델링하기 위해 local affine translation과 함께 self-learned keypoints set 사용  
2) occlusion-aware G : source에서 볼 수 없고 context에서 유추해야 하는 object 부분을 나타내기 위해 자동으로 추정 occlusion 마스크 채택  
(driving 비디오에 큰 움직임 패턴이 포함되고 occlusion이 일반적일 때 특히 필요)  
3) local affine translation의 추정을 개선하기 위해 keypoint detector 학습에 일반적으로 사용되는 equivariance loss 확장  
4) 본 방법이 SOTA를 능가하고 다른 접근 방식이 일반적으로 실패하는 고해상도 데이터 세트를 처리할 수 있음을 실험적으로 보임  
5) 새로운 고해상도 데이터 세트인 Thai-Chi-HD를 출시  
(이미지 애니메이션 및 비디오 생성을 위한 프레임워크 평가를 위한 참조 벤치마크가 될 수 있다.)

## 2 Related work

**Video Generation.**  
Deep video generation에 대한 이전 작업에서는 시공간 NN이 노이즈 벡터에서 video frame을 rendering할 수 있는 방법에 대해 논의했다.  
최근에는 조건부 비디오 생성 문제를 해결하기 위한 여러 접근 방식이 사용되었다.  
Wang은 face 비디오를 생성하기 위해 RNN과 VAE를 결합한다.  
더 넓은 범위의 애플리케이션을 고려하여 Tulyakov는 노이즈, categorical label 또는 static 이미지에서 비디오를 합성하기 위해 적대적으로 학습된 RNN 구조의 MoCoGAN을 도입했다.  
다른 전형적인 경우는 생성된 비디오가 초기 프레임을 조건으로 하는 미래 프레임 예측의 문제이다.  
이 작업에서 초기 비디오 프레임을 단순히 warping하여 현실적인 예측을 얻을 수 있다.  
비디오 시퀀스를 생성하기 위해 warping 공식을 사용하기 때문에 우리의 접근 방식은 이러한 이전 작업과 밀접하게 관련되어 있다.  
그러나 이미지 애니메이션의 경우 적용된 공간적 변형은 예측되지 않고 주행 영상에 의해 주어진다.  
  
**Image Animation.**
이미지 애니메이션 및 비디오 retargeting에 대한 기존 방식은 얼굴, 사람 silhouette 또는 gesture와 같은  
특정 영역을 위해 설계되었으며 애니메이션된 object의 강력한 **prior** 설정이 필요했다.  
예를 들어, Zollhofer은 얼굴의 3D 변형 가능한 모델에 의존하는 대신 사실적인 결과를 생성했다.  
그러나 많은 응용 프로그램에서 이러한 모델을 사용할 수 없다.  
이미지 애니메이션은 하나의 시각 영역에서 다른 영역으로의 **번역 문제**로 취급될 수도 있다.  
예를 들어, Wang은 Isola의 **pix2pix** 프레임워크를 사용하여 인간의 움직임을 전달했다.  
유사하게, Bansal은 두 도메인 간 비디오 번역을 개선하기 위해 **시공간 신호를 통합**하여 cGAN을 확장했다.  
한 사람을 움직이게 하기 위한 이러한 접근 방식은 semantic 정보로 label이 지정된 해당 사람의 비디오를 몇 시간 동안 사용해야 하며  
각 개인에 대해 재학습해야 한다.  
이러한 작업과 대조적으로 우리는 label, animation object에 대한 prior 정보 또는 각 object 인스턴스에 대한 특정 학습 절차에 의존하지 않는다.  
또한 동일한 범주 내의 모든 개체(예: 얼굴, 인체, 로봇 팔 등)에 적용될 수 있다.  
  
Object에 대한 prior 정보가 필요하지 않은 여러 접근 방식이 제안되었다.  
X2Face는 이미지 warping을 통해 출력 비디오를 생성하기 위해 dense motion field를 사용한다.  
우리와 유사하게 object의 표준 표현을 얻는 데 사용되는 reference pose를 사용한다.  
공식에서 explicit reference pose가 필요하지 않으므로 최적화가 훨씬 간단하고 이미지 품질이 향상된다.  
Siarohin는 sparse keypoint trajectory을 사용하여 임의의 object를 애니메이션하기 위한 self-supervised 프레임워크인 Monkey-Net을 도입했다.  
이 작업에서 우리는 또한 self-supervised keypoint에 의해 유도된 sparse trajectory를 사용한다.  
그러나 우리는 local affine transformation에 의해 예측된 각 keypoint 주변의 object motion을 모델링한다.  
또한 source 이미지를 왜곡하여 생성할 수 있는 이미지 영역과 in-paint해야 하는 가려진 영역을 G에 나타내기 위해 occlusion을 명시적으로 모델링한다.

## 3. Method
Source image S의 object를 driving video D의 유사 객체의 motion을 기반하여 움직이도록 하는것에 관심이 있다.  
직접적인 감독은 불가능(유사한 움직임을 가지는 비디오 pair가 없음)하므로 Monkey-Net의 self-supervised 전략을 이용한다.  
학습에 있어, 동일한 object 카테고리의 object를 포함하는 video sequence들의 대규모 모음을 활용한다.  
우리의 모델은 단일 프레임과 비디오의 모션에 대한 학습된 잠재 표현을 결합하여 학습 비디오를 재구성하도록 학습되었다.  

동일 비디오에서 각각 추출된 프레임 pair를 관찰하여 motion-specific keypoint displacement와 local affine transformation의 조합으로  
motion을 encoding하는 방법을 학습한다. 테스트 시 source 이미지와 driving video의 각 프레임으로 구성된 pair에 모델을 적용하고  
source 객체의 이미지 애니메이션을 수행한다.
  
접근 방식에 대한 개요는 그림 2에 나와 있다.  
![image](https://user-images.githubusercontent.com/40943064/150069750-c6fbaf96-6e88-41ee-bd1b-9a1600227f01.png)  
프레임워크는 1) **motion 추정 모듈**과 2) **이미지 생성 모듈**의 두 가지 주요 모듈로 구성된다.  
Motion 추정 모듈의 목적은 구동 video D의 차원 H×W의 프레임 D ∈ R^3×H×W 부터 source 프레임 S ∈ R^3×H×W 까지의 dense motion 필드를 예측하는 것이다.  
Dense motion field는 나중에 S에서 계산된 feature map을 D의 object pose와 정렬하는 데 사용된다.  
Motion field는 D의 각 픽셀 위치를 S의 해당 위치와 mapping하는 TS←D: R2 → R2에 의해 모델링된다.  
TS←D는 종종 backward optical flow이라고 한다.  
이중 선형 샘플링을 사용하여 미분 방식으로 역방향 왜곡을 효율적으로 구현할 수 있기 때문에 forward optical flow보다  
backward optical flow를 사용한다.  
Abstract reference frame R이 있다고 가정한다.  
R에서 S로(TS←R) 및 R에서 D로(TD←R)의 두 가지 변환을 독립적으로 추정한다.  
X2Face와 달리 reference frame은 나중에 파생된 항목에서 취소되는 abstract한 개념이다.  
따라서 명시적으로 계산되지 않으며 시각화할 수 없다. 이 선택을 통해 D와 S를 독립적으로 처리할 수 있다.  
이는 테스트 시간에 모델이 시각적으로 매우 다를 수 있는 다른 video에서 샘플링된 구동 프레임과 source 이미지 pair를 수신하기 때문에 바람직하다.  
TD←R 및 TS←R을 직접 예측하는 대신 motion estimator module은 2단계로 진행한다.  
첫 번째 단계에서는 self-supervised 방식으로 학습된 keypoint를 사용하여 얻은 sparse trajectory 세트에서 두 변환을 모두 근사화한다.  
D와 S의 keypoint 위치는 encoder-decoder 네트워크에 의해 별도로 예측된다.  
Keypoint 표현은 병목 현상으로 작용하여 동작 표현을 간결하게 만든다.  
Siarohin이 보여주듯이 이러한 sparse motion 표현은 테스트 시간에 애니메이션에 매우 적합하며 원본 이미지의 keypoint는  
driving video의 keypoint trajectory를 사용하여 이동할 수 있다.  
Local affine transformation을 사용하여 각 keypoint neighborhood의 motion을 모델링한다.  
Keypoint displacements만 사용하는 것과 비교하여 local affine tranformation을 사용하면 더 큰 변환 패밀리를 모델링할 수 있다.  

우리는 Taylor expansion을 사용하여 keypoint 위치 및 affine transformation 세트로 TD←R을 나타낸다.  
이를 위해 keypoint detector 네트워크는 keypoint 위치와 각 affine transformation의 매개변수를 출력한다.  
  
두 번째 단계에서 dense motion 네트워크는 결과적으로 조밀한 motion 필드 TˆS←D를 얻기 위해 local approximation를 결합한다.  
더욱이, 조밀한 motion 필드에 더하여, 이 네트워크는 D의 어떤 이미지 부분이 소스 이미지의 뒤틀림에 의해 재구성될 수 있고 어떤 부분이 인페인트되어야 하는지,  
즉 context에서 추론해야 하는지를 나타내는 occlusion 마스크 Oˆ S←D를 출력한다.  
마지막으로 생성 모듈은 driving 영상에서 제공하는 대로 움직이는 source object의 이미지를 렌더링한다.  
여기서 TˆS←D에 따라 소스 이미지를 왜곡하고 소스 이미지에서 가려진 이미지 부분을 다시 그리는 G를 사용한다.  
  
다음 섹션에서는 이러한 각 단계와 교육 절차에 대해 자세히 설명한다.  

### 3.1 Local Affine Transformations for Approximate Motion Description
### 3.2 Occlusion-aware Image Generation
### 3.3 Training Losses
### 3.4 Testing Stage: Relative Motion Transfer
