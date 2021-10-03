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
**Quality** 
**Mid-level resolution**(Table 1)
해상도 데이터셋에 대한 우리 방식의 양적결과를 보여준다.  
두 모델에 대해 FID 향상을 얻었다.
![image](https://user-images.githubusercontent.com/40943064/135553413-ed75128d-21ae-4aa5-8a62-35541c9f3bd2.png)  
위 결과를 얻기 위해서 PGGAN에 비해 저해상도의 성능 향상은 느리지만 본 방법은 전체를 한번에 학습하기 때문에 결과적으로는 훨씬  
적은 시간이 소요된다. Figure 3은 특정 latent에 대해 생성된 이미지를 보여준다.  
![image](https://user-images.githubusercontent.com/40943064/135553633-c8cfc73c-a464-4e48-a321-f5eae18e3797.png)  
  
**High-level resolution**(Table 2)
두 모델에 대해 유사한 결과가 나왔지만 성능이 더 낫지는 않았고 해당 이유에 대한 가설을 Sec.4에 기술한다.  
그러나 안정화및 일반화하는 관점에서는 이점이 있으며 phase artifact는 발생하지 않는 결과가 나온다.  

**Stability during training**
모델 안정성을 평가하기 위해 고정 latent point에서 학습 진행사항을 확인해본다.  
(The unusual effectiveness of averaging in GAN training 연구 참조)  
연속된 Epochs끼리의 이미지의 MSE를 계산하여 평가한다.  
그림 6을 보면 저해상도의 이미지에서만 수렴하며 MSG추가 모델에 대해서는 모든 해상도에 대해 수렴하는것을 알 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/135554138-8f90df5d-4fa7-4315-8107-ad3f999fb558.png)  
학습 epoch는 기존의 경우 순차적으로 발생하지만 MSG는 동시에 발생한다.  
좋은 결과를 생성하는 데 반드시 필요한 것은 아니지만, 안정성이 높은 방법은 훈련 중 스냅샷을 시각화하여 최종 결과가 어떻게 보일지에 대한  
합리적인 추정을 더 쉽게 얻을 수 있다는 이점이 있으며 학습 작업이 며칠에서 몇주까지 걸릴 때 도움이 될 수 있다. 
  
**Robustness to learning rate**
훈련 중 GAN의 수렴이 하이퍼파라미터, 특히 학습률의 선택에 매우 크게 의존한다는 것이 관찰되었다.  
MSG-ProGAN의 견고성을 검증하기 위해 CIFAR-10 데이터에 대해 (0.001, 0.003, 0.005 및 0.01)로 학습했다(표 3).  
![image](https://user-images.githubusercontent.com/40943064/135554947-a4405526-242a-4ef3-b3e5-c19879be7467.png)  
  CIFAR-10에 대한 lr에 대한 robustness 실험. 모든 lr에 대해 유사한 lr로 수렴함을 알 수 있다.  
  
학습 속도의 큰 변화에도 불구하고 네 가지 모델이 모두 수렴하여 합리적인 이미지와 유사한 시작 점수를 생성하는 것을 볼 수 있다.  
강력한 훈련 scheme은 unssen 데이터 세트에 얼마나 쉽게 일반화될 수 있는지를 나타내기 때문에 중요하다.  

## 4. Discussion
**Ablation Studies**  
MSG-ProGAN에서 두 가지 ablation을 진행했다. 표4는 MultiScale Gradients의 ablated 버전을 적용하는 실험을 요약한다.  
![image](https://user-images.githubusercontent.com/40943064/135554729-6cdd9063-cc7e-480d-b680-4660b23e3c87.png)  
(1024x1024) FFHQ 데이터 세트에서 다양한 정도의 다중 스케일 그라디언트 연결에 대한 절제 실험.  
Coarse : (4x4) & (8x8) / Middle : (16x16) & (32x32) / Fine : (64x64) ~ (1024x1024)  

여기서 서로 다른 규모의 G->D로 연결의 하위 집합만 추가한다. ProGAN(DCGAN) 아키텍처에 모든 수준에서  
다중 스케일 그라디언트를 추가하면 FID 점수가 향상된다는 것을 알 수 있다.  
흥미롭게도 middle 연결만 추가하면 coarse 또는 fine 연결만 추가하는 것보다 약간 더 나은 성능을 보이지만  
모든 수준의 연결에서 전반적인 최상의 성능을 얻을 수 있다.  

표 5는 MSG-ProGAN 및 MSG-StyleGAN 아키텍처에서 결합 기능 φ의 다양한 변형에 대한 실험을 보여준다.  
![image](https://user-images.githubusercontent.com/40943064/135555211-1617439d-2258-438e-b8c1-894b22b693c1.png)  
φsimple은 MSG-ProGAN 아키텍처에서 가장 잘 수행된 반면 φcat lin은 MSGStyleGAN 아키텍처에서  
최고의 FID 점수를 얻었다. 이 작업에 표시된 모든 결과는 이러한 각각의 결합 기능을 사용한다.  
이러한 실험을 통해 결합 기능이 모델의 생성 성능에 중요한 역할을 함을 알 수 있으며,  
multi-layer densenet이나 AdaIN과 같은 고급 결합 기능이 결과를 더욱 향상시킬 수 있다.  
  
### Limitations and Future Work  
본 방법에는 제한이 없다. PG방법을 사용하면 낮은 해상도에서 학습 빠르게 수행되는 반면 MSG-GAN의 각 반복에는 동일한 시간이 걸린다.  
그러나 MSG-GAN이 동일한 FID에 도달하기 위해 더 적은 iteration이 필요하다.  
또한 MSG-StyleGAN의 multi-scale 수정으로 인해 다중 latent 벡터가 혼합되고 결과 이미지가 D에 의해 현실적이어야 하는  
mixing regularization 트릭을 사용할 수 없다.  
이는 테스트 시간에 다양한 수준에서 다양한 스타일을 혼합할 수 있도록 하기 위해 수행되지만 전반적인 품질도 향상된다.  
흥미롭게도 혼합 정규화를 명시적으로 시행하지 않더라도 우리 방법은 여전히 그럴듯한 혼합 결과를 생성할 수 있다(보충 자료 참조).  
## 6.1. Architecture Details
**MSG-ProGAN**  
MSG-ProGAN의 G, D 구조 : Table 6, 7  
D로 넘기는 conv(in_ch, 3, kernel_size=1, stride=1, padding=0)를 매 G의 block 마다 사용한다.  
위의 RGB 이미지는 D에서 combine 함수 φ를 통해 D의 activation 출력과 결합된다.  
1. φsimple : channelwise concat.  
2. φlin_cat : RGB를 다시 D출력 channel의 반의 channel을 가지는 conv.를 통과시켜 channelwise concat.  
3. φcat_lin : channelwise concat. 후에 1x1 conv.를 수행 이때 channel은 앞선 블럭의 수와 같음  
  
Model 1, Model 2, Model 3 블럭은 32x32, 128 x 128, 256x256을 합성하는데 사용된다.  
G에서의 매 3x3 conv 이후에는 PixNorm 방식으로 정규화한다.  

## 6.3. Observation
생성된 결과의 차이(vs StyleGAN)에 대한 몇 가지 관찰과 가설을 제시한다.  
그림 7에서 두 모델에서 무작위로 선택된 샘플의 개요를 보여준다. 결과 분석에서 실제 결과 이미지 품질은 매우 비슷하지만  
StyleGAN 샘플은 **포즈 측면에서 약간 더 높은 변화**를 나타냅니다. 대조적으로 MSGStyleGAN 결과는 약간 더 **전체적으로 일관되고 더 현실적**이다.  
다양성과 결과 품질 간의 이러한 균형은 널리 보고되고, FID 점수의 일부 차이를 설명할 수 있다.  
두 축(현실성 대 다양성)을 제어하는 방법과 이것이 FID 점수에 미치는 영향에 대한 추가 조사는 향후 작업을 위한 흥미로운 방법이 될 것이다.  
또한 StyleGAN G의 각 블록에 추가된 픽셀 단위 noise가 이미지 생성에서 수행하는 역할을 조사하는 실험을 수행했다.  
얼굴이 아닌 데이터에서 노이즈 레이어가 확률적 변화뿐만 아니라 이미지의 의미론적 측면을 모델링한다는 것을 발견했다(그림 8 참조).  
![image](https://user-images.githubusercontent.com/40943064/135555995-c0b8979c-ad42-40c3-bf10-140de1113b0d.png)
(StyleGAN vs MSG-StyleGAN / z를 유지하면서 픽셀당 노이즈를 다르게 구현)  

MSG-StyleGAN도 이러한 유형의 효과를 나타내지만 정도는 약간 낮다는 것을 관찰했다.  
확률적 특징과 의미론적 특징 사이의 이러한 분리가 얼굴 모델링 작업(예: CelebA-HQ 및 FFHQ 데이터 세트에서)에 대해 더 간단하고  
노이즈에 대한 서로 다른 모델 민감도가 우리가 관찰한 성능 차이의 일부에 기여할 수 있다고 추측한다.  
얼굴 vs 비얼굴 데이터 세트에서도 마찬가지이다. 본 논문의 discussion 부분에서 언급했듯이 StyleGAN 작업에서 설명한  
mix.reg. 기술을 사용하지 않는다. 그러나 모델은 제안방법으로 인해 높은 수준의 의미론적 특징을 분리하는 방법을 여전히 학습한다(그림 9 참조).  
![image](https://user-images.githubusercontent.com/40943064/135556238-8b532150-981e-43cb-9854-1e2002a9569e.png)  
그림에서 알 수 있듯이 높은 수준의 믹싱은 훨씬 더 일관성 있고 시각적으로 사실적인 결과를 생성한다.  
낮은 수준의 믹싱은 종종 부적절한 조명 및 불균형한 머리카락과 같은 잘못된 시각적 신호를 생성한다.  
이것은 생성의 coarse 수준에서 적절한 스타일 기반 믹싱을 보장함으로써 성능 향상이 가능할 수 있음을 보여준다.  
