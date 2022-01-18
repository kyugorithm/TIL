First Order Motion Model for Image Animation


## 1.Introduction

Still 이미지의 object를 애니메이션으로 만들어 비디오를 생성하는 것은 영화 제작, 사진 및 전자 상거래를 비롯한 관심 분야에 걸쳐 셀 수 없이 많은 응용 분야가 있다.  
보다 정확하게는 이미지 애니메이션은 source 이미지에서 추출한 appearance와 driving video에서 파생된 모션 패턴을 결합하여 동영상을 자동으로 합성하는 작업을 의미한다.  
예를 들어, 특정 인물의 얼굴 이미지는 다른 개인의 표정에 따라 애니메이션될 수 있다(그림 1 참조).  
기존 대부분의 방법은 object 표현(예: 3D 모델)에 대한 강력한 우선순위를 가정하고 CG 기술에 의존하여 이 문제를 해결한다.  
이러한 접근 방식은 애니메이션할 특정 object의 모델에 대한 지식을 가정하기 때문에 object-specific 방법이라고 할 수 있다.  
최근에는 이미지 애니메이션 및 비디오 retargetting을 위한 효과적인 기술로 딥 생성 모델이 등장했다.  
특히, GAN및 VAE는 비디오에서 인간 주체 간의 얼굴 표정 또는 동작 패턴을 전송하는 데 사용되었다.  
그럼에도 불구하고 이러한 접근 방식은 일반적으로 keypoint 위치와 같은 object별 표현을 추출하기 위해 사전 학습된 모델에 의존한다.  
불행히도 이러한 사전 학습된 모델은 값비싼 GT annotation을 사용하여 구축되었으며 일반적으로 arbitrary object category에 사용할 수 없다.  
이 문제를 해결하기 위해 최근 Siarohin은 이미지 애니메이션을 위한 최초의 object-agnostic 심층 모델인 Monkey-Net을 도입했다.  
Monkey-Net은 self-supervised 방식으로 학습된 keypoint를 통해 motion 정보를 인코딩한다.  
테스트 시간에 원본 이미지는 주행 비디오에서 추정된 해당 키포인트 궤적에 따라 애니메이션된다.  
Monkey-Net의 주요 약점은 0차 모델을 가정하는 keypoint neighborhood에서 object 모양 변환을 제대로 모델링하지 않는다는 것이다(3.1절).  
이는 큰 물체 포즈 변경의 경우 생성 품질이 저하된다(그림 4 참조).  
이 문제를 해결하기 위해 다음을 제안한다.
1) 1차 모션 모델 : 복잡한 동작을 모델링하기 위해 local affine translation과 함께 self-learned keypoints 세트 사용  
2) occlusion-aware G : source 이미지에서 볼 수 없고 context에서 유추되어야 하는 object 부분을 나타내기 위해 자동으로 추정되는 occlusion 마스크를 채택  
(driving 비디오에 큰 움직임 패턴이 포함되고 occlusion이 일반적일 때 특히 필요)  
3) local affine translation의 추정을 개선하기 위해 keypoint detector 학습에 일반적으로 사용되는 equivariance loss을 확장  
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


Image Animation.  
이미지 애니메이션 및 비디오 retargetting에 대한 전통적인 접근 방식은 얼굴, 사람 silhouettes 또는 gesture와 같은  
특정 영역을 위해 설계되었으며 애니메이션된 object의 강력한 prior 설정이 필요했다.  
예를 들어, 얼굴 애니메이션에서 Zollhofer은 얼굴의 3D 변형 가능한 모델에 의존하는 대신 사실적인 결과를 생성했다.  
그러나 많은 응용 프로그램에서 이러한 모델을 사용할 수 없다.  
이미지 애니메이션은 하나의 시각적 영역에서 다른 영역으로의 번역 문제로 취급될 수도 있다.  
예를 들어, Wang은 Isola의 I2I 번역 프레임워크를 사용하여 인간의 움직임을 전달했다.  
유사하게, Bansal은 주어진 두 도메인 간의 비디오 번역을 개선하기 위해 시공간 신호를 통합하여 cGAN을 확장했다.  
한 사람을 움직이게 하기 위한 이러한 접근 방식은 의미 정보로 label이 지정된 해당 사람의 비디오를 몇 시간 동안 사용해야 하므로  
각 개인에 대해 재교육해야 한다.  
이러한 작업과 대조적으로 우리는 레이블, 애니메이션 개체에 대한 사전 정보 또는 각 개체 인스턴스에 대한 특정 학습 절차에 의존하지 않는다.  
또한 우리의 접근 방식은 동일한 범주 내의 모든 개체(예: 얼굴, 인체, 로봇 팔 등)에 적용될 수 있습니다.  
  
객체에 대한 사전 정보가 필요하지 않은 여러 접근 방식이 제안되었다.  
X2Face는 이미지 warping을 통해 출력 비디오를 생성하기 위해 덴스 모션 필드를 사용한다.  
우리와 유사하게 그들은 object의 표준 표현을 얻는 데 사용되는 참조 pose를 사용한다.  
공식에서 explicit reference pose가 필요하지 않으므로 최적화가 훨씬 간단하고 이미지 품질이 향상된다.  
Siarohin는 sparse keypoint trajectory을 사용하여 임의의 객체를 애니메이션하기 위한 self-supervised 프레임워크인 Monkey-Net을 도입했다.  
이 작업에서 우리는 또한 자가 감독 키포인트에 의해 유도된 희소 궤적을 사용한다.  
그러나 우리는 local affine transformation에 의해 예측된 각 keypoint 주변의 object motion을 모델링한다.  
또한 source 이미지를 왜곡하여 생성할 수 있는 이미지 영역과 in-paint해야 하는 가려진 영역을 G에 나타내기 위해 occlusion을 명시적으로 모델링한다.

## 3. Method
