# MSG-GAN: Multi-Scale Gradients for Generative Adversarial Networks

## Abstract
GAN은 학습 중 불안정성과 hyper-parameter 민감성으로 단일 설계로 다양한 데이터 세트에 적용하기 힘들다.  
일반적인 이유는 real과 fake 분포가 충분히 중복되지 않을 때 D에서 G로 흐르는 gradient가 정보가 되지 않기 때문이다.  
이를 해결하기위해 여러 scale에서 D->G로의 gradient 흐름을 허용하는 방법을 사용한다.  
이는 고해상도 합성에 안정성을 제공하며 progressive growing 기술의 대안이 될 수 있다.  
제안 방식이 동일한 고정 hyper-parameter 세트를 사용하여 다양한 크기, 해상도 및 도메인의 다양한 이미지 데이터 세트와  
다양한 유형의 손실 함수 및 아키텍처에서 안정적으로 수렴한다는 것을 보인다.  
SOTA GAN과 비교할 때 우리의 접근 방식은 우리가 시도한 대부분의 경우 성능과 일치하거나 초과한다.  
**key** Multi-scale gradient를 적용하여 학습 안정성을 향상하는 방법  
  
## 1. Introduction
GAN은 수작업으로 최적화를 위한 손실함수를 설계하지 않아도 되기 않고  
명시적인 정의 없이 적대적 방식으로 복잡한 데이터 분포를 생성하는 법을 배울 수 있다. 
flow-based와 autoregressive 모델은 MLE (각각 명시적 및 암시적)을 사용하여 생성 모델을 직접 훈련할 수 있지만  
생성된 이미지의 fidelity는 SOTA GAN 모델에 비해 좋지 못하다.  
그러나 GAN 훈련은 (1) 모드 붕괴와 (2) 훈련 불안정성의 두 가지 두드러진 문제를 겪는다.  
모드 붕괴 문제는 생성기 네트워크가 데이터 분포에 존재하는 분산의 하위 집합만 캡처할 수 있을 때 발생한다.  
본 연구에서는 학습 불안정성의 문제를 다룬다. 
progressive growing 기법에 의존하지 않고 고해상도 이미지(일반적으로 데이터 차원으로 인해 더 까다로움)를 생성하기 위해  
multi-scale gradients를 사용법을 조사하여 이미지 생성 작업에 대한 훈련 불안정성을 해결하는 방법을 제안한다.  
MSG-GAN을 사용하면 D가 G의 최종 출력(최고 해상도)뿐만 아니라 중간 계층의 출력도 볼 수 있다(그림 2).  
  
  
결과적으로 D는 G의 multi-Scale 출력의 함수가 되며 중요하게는 모든 스케일에 gradient를 동시에 전달한다.  
(자세한 내용은 섹션 1.1 및 섹션 2 참조).  
또한 본 방법은 여러 loss function, dataset 및 architecture에서 강인하다.  
progressive growing와 유사하게, multi-scale gradients가 기본 DCGAN 아키텍처에 비해  
FID 점수의 상당한 개선을 설명한다는 점에 주목한다.  
그러나 본 방법은 progressive growing이 도입하는 추가 hyper-parameter, 다양한 생성 단계(해상도)에 대한 학습 일정  
및 을 요구하지 않고 대부분의 기존 데이터 세트에서 SOTA 방법과 비슷한 훈련 시간으로 더 나은 성능을 달성한다.  
이러한 robustness를 통해 MSG-GAN 방식을 새 데이터 세트에서 "즉시" 쉽게 사용할 수 있습니다.  
또한 고해상도 FFHQ 데이터 세트에 대한 ablation study를 통해 여러 세대 단계(coarse, medium, fine)에서  
multi-scale 연결의 중요성을 보여준다.  
요약하면 다음과 같은 기여를 제공한다.  

1. 학습 안정성을 향상하는 multi-scale gradients 도입  
2. 여러 데이터 세트에서 고품질 샘플을 모두 동일한 고정 하이퍼파라미터로 강력하게 생성할 수 있음을 보여줌  
3. 적용하기 쉬움  
4. 
## 1.1 Motivation
## 2. Multi-Scale Gradient GAN
## 3. Experiments
### New Indian Celebs Dataset
### 3.1. Implementation Details
### 3.2. Results
### Stability during training
### Robustness to learning rate
## 4. Discussion
### Limitations and Future Work
### Conclusion
## 5. Acknowledgements
