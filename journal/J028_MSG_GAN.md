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
  
## 1.1 Motivation
Arjovsky는 GAN의 학습 불안정성의 이유 중 하나는 실제 분포와 fake 분포의 support 사이에 실질적이지 않은 중첩이 있을 때  
D에서 G로 무작위(정보가 없는) 그라디언트가 흐르기 때문이라고 지적했다.  
1. Arjovsky / Support가 최소한으로 겹치도록 실제 이미지와 가짜 이미지에 **노이즈를 추가**  
  
2. Peng / variational D bottleneck 입력 이미지와 D의 가장 깊은 표현 사이의 **상호 정보 병목**  
(D가 분류를 위해 이미지의 가장 식별 가능한 특징에만 집중하도록 하며, 인스턴스 노이즈의 adaptive 변형으로 볼 수 있다.  
본 작업은 VDB 기술과 직교하며 MSG-GAN과 VDB의 조합에 대한 조사는 향후 작업에 남겨둔다.)  
  
3. Karras / 해상도 **레이어를 점진적으로 추가**  
(해상도를 점진적으로 두 배로 늘려 계층별로 학습함으로써 불안정성 문제를 해결한다.  
레이어가 학습에 추가될 때마다 이전 레이어의 학습이 유지되도록 천천히 페이드인 된다.  
직관적으로, 이 기술은 데이터 차원이 더 낮은 저해상도에서 먼저 양호한 분포 일치를 달성한 다음,  
이러한 기술을 사용하여 고해상도 학습을 부분적으로 초기화(실제 분포와 가짜 분포 사이에 상당한 지원 중복 포함)하기 때문에  
직관적으로 support 중첩 문제에 도움이 된다. 학습된 가중치, 세부 사항 학습에 중점을 둔다.  
이 접근 방식은 SOTA를 생성할 수 있지만 다른 반복 횟수, 학습률(G에 따라 다를 수 있음)을 포함하여  
해상도별로 조정할 하이퍼파라미터가 추가되기 때문에 학습하기 어려울 수 있다.  
또한 생성된 특정 기능이 특정 공간 위치에 연결되는 위상 아티팩트가 발생한다는 사실을 발견했다.  )  
  



본 논문의 주요 동기는 고품질 결과와 안정적인 교육으로 이어지는 간단한 대안을 제공하여 문제를 해결하는 데 있다.  
Imagenet 데이터 세트, 즉 BigGAN에 대한 조건부 이미지 생성의 SOTA는 다중 스케일 이미지 생성을 사용하지 않지만  
작동하는 최고 해상도는 512x512이다.  
모든 고해상도 SOTA는 **다중 스케일 이미지 합성의 일부 또는 다른 형태**를 사용한다.  
다중 스케일 이미지 생성은 이 작업에 대해 심층 네트워크가 대중화되기 훨씬 전에 존재하는 방법으로 잘 확립된 기술이다.  
보다 최근에는 많은 GAN 기반 방법이 고해상도 이미지 합성 프로세스를 더 작은 하위 작업으로 나눈다.  

1. **LRGAN** : 최종 이미지의 배경, 전경 및 합성 마스크를 합성하기 위해 별도의 G 사용  
2. **GMAN 및 StackGAN** : 티칭 및 다중 스케일 생성의 변형을 위해 단일 G, 다중 D 사용  
3. **MAD-GAN** : 여러 G를 사용하여 학습 데이터 세트에서 다른 modality를 캡처하는 방식으로  
다중 에이전트 설정을 학습하여 mode-collapse 해결  
4. **LapGAN** : 다른 scale에 대해 단일 G와 다중 D를 사용하여 이미지의 라플라시안 피라미드에서 생성된  
다중 축척 구성요소 간의 차이를 모델링  
5. **Pix2PixHD** : 실제 이미지와 생성된 이미지를 다운샘플링하여 얻은 이미지의 세 가지 다른 해상도에 따라  
작동하는 세 가지 구조적으로 유사한 D를 사용  

제안 방법은 위 방법에서 구조적 영감을 얻고 가르침과 이데올로기를 기반으로 하지만 몇 가지 중요한 차이점이 있다.  
다중 스케일 연결이 있는 단일 D와 단일 G를 사용하여 gradient가 여러 해상도에서 동시에 흐를 수 있도록 한다.  
이에는 몇 가지 장점이 있다(대부분 단순성에 의해 주도됨).  
각 해상도에서 여러 D가 사용되는 경우 반복되는 다운샘플링 레이어가 필요하기 때문에 전체 매개변수가 규모에 따라  
기하급수적으로 증가하지만 MSG-GAN에서는 관계가 선형이다.  
또한 서로 다른 effective field를 가진 여러 D는 규모 간에 정보를 공유할 수 없으므로 작업을 더 쉽게 만들 수 있다.  
StackGAN에서 더 적은 수의 매개변수와 디자인 선택이 필요한 것 외에도 우리의 접근 방식은 여러 스케일에서 생성된  
이미지 전반에 걸쳐 명시적인 색상 일관성 정규화 조건이 필요하지 않다. 

## 2. Multi-Scale Gradient GAN
ProGAN과 StyleGAN에 적용된 MSG-GAN 프레임워크로 실험을 수행하며 MSG-ProGAN 및 MSG-StyleGAN이라 표현한다.  
MSG 변종에는 점진적 성장이 없으며 따라서 본질적으로 DCGAN 아키텍처이다.  
그림 2는 MSG-ProGAN 아키텍처를 보여주며, 이 섹션에서 더 자세히 정의하고 보충 자료에 MSGStyleGAN 모델 세부 정보를 설명한다.  
![image](https://user-images.githubusercontent.com/40943064/135482041-630cd0ff-1481-411a-8ad2-6f7585b88159.png)  

**G 정의**  
ggen(초기 블록) : Z(=R^512) → Abegin(=R^4x4x512)  
g^i(기본 블록)  : 구현에서 업샘플링과 두 개의 conv 레이어로 구성  
![image](https://user-images.githubusercontent.com/40943064/135480369-e5ac29b7-6490-4aa4-9c9e-79c6eb65bada.png)  
c_i = 채널수, i = G의 activation 순서  
위 설명에 따라 GEN(z)인 전체 G는 아래와 같이 표준 포맷을 따르고 아래와 같이 표현할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/135481591-048521e0-8c16-4f5e-9230-cdc303812a80.png)  
  
**r 정의**  
최종 출력 이미지의 서로다른 downsampled 버전에 해당하는 G의 다른 stage이다.  
r을 중간 conv 활성화를 RGB(=3ch)로 변환하는 (1x1) conv.로 정의한다.  
![image](https://user-images.githubusercontent.com/40943064/135482510-3793b3f1-238b-4753-aeb1-5fe67e57d517.png)  
즉, oi는 ai의 i번째 중간 레이어의 출력으로부터 합성된 이미지이다.  
PGGAN과 유사하게 r은 학습된 feature map들이 RGB 공간으로 매핑되게 학습되도록 함으로써  
regularizer 역할을 하는것으로도 여겨질 수 있다. D의 모든 구성요소를 **d**로 표현한다.  

**D 정의**
D의 최종 critic loss는 g의 최종 이미지에 대해서만 계산되는것이 아닌 oi로도 계산되기 때문에  
D가 넘기는 gradient는 G의 중간 레이어로도 흘러들어갈 수 있다.  
**d_critic(z')** : critic score를 만드는 D의 최종 레이어  
**d^0(y), d^0(y')**: 첫번째 레이어(y=real, y'=fake)  
**d^j** : 중간 레이어  
![image](https://user-images.githubusercontent.com/40943064/135483939-4160b4e3-c317-44dd-8f18-63154626377c.png)  
실험에서 아래 세가지 버전을 검토한다.  
![image](https://user-images.githubusercontent.com/40943064/135484213-a752da03-f3f6-41ff-9fae-29a7a384b820.png)  
r'는 r과 유사하지만 다른 (1x1) conv. 이다.  
![image](https://user-images.githubusercontent.com/40943064/135484709-91c46598-73de-4af0-8bdb-ea41e409d447.png)

d_critic loss : WGAN-GP(ProGAN) and Non-saturating GAN loss(1-sided GPStyleGAN)  


## 3. Experiments
CIFAR10에는 IS를 나머지에는 FID를 사용하며 사용자실험도 추가한다.  
### New Indian Celebs Dataset  
### 3.1. Implementation Details  
1. CIFAR10 : 60K @ 32x32  
2. Oxford flowers : 8K @ 256x256  
3. LSUN churches : 126K @ 256x256  
4. Indian Celebs : 3K @ 256x256  
5. CelebA-HQ : 30K @ 1024x1024  
6. FFHQ : 70K @ 1024x1024  
- same dim of Z = 512(N(0, I)  
- hypersphere normalization  
- RMSprop(lr=0.003)
- Initialize parameters N(0, I)
  
또한 샘플 다양성을 개선하기 위해 활성화 배치의 평균 표준 편차가 D에 공급되는  
MinBatchStdDev 기술을 다중 스케일 설정으로 확장한다.  
이를 위해 D의 각 블록 시작 부분에 별도의 MinBatchStdDev 레이어를 추가한다.  
이러한 방식으로 D는 각 스케일에서 직선 경로 활성화와 함께 생성된 샘플의 배치 통계를 얻고  
G의 모드 붕괴의 어느 정도를 감지할 수 있다.  
모델을 직접 훈련할 때 훈련 시간과 사용된 GPU를 보고한다.  
직접 훈련 시간을 비교할 수 있도록 해당 실험 세트에 동일한 하드웨어를 사용한다.  
표시된 실제 이미지 수와 교육 시간의 차이는 일반적인 관행과 같이 고정된 반복 횟수로 얻은  
최상의 FID 점수와 해당 점수를 달성하는 데 걸린 시간을 보고하기 때문이다.

### 3.2. Results
### Stability during training
### Robustness to learning rate
## 4. Discussion
### Limitations and Future Work
### Conclusion
## 5. Acknowledgements
