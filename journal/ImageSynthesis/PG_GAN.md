# Progressive growing of gans for improved quality, stability, and variation

## Abstract
GAN의 새로운 학습방법론 제시  
낮은 해상도에서부터 학습이 진전됨에 따라 세밀한 디테일들을 **점진적으로 모델링하는 새로운 layer**를 G, D 모두에 더해간다.  
**높은 품질**의 이미지를 생성하게 되면서 **학습속도가 증가**하고 **안정적**으로 학습을 수행한다.  
생성 이미지에서의 **variation을 증가**시키는 간단한 방법도 제안하며 CIFAR10 데이터셋에 대해서 8.8의 inception score를 기록한다.  
추가로 G와 D 사이의 학습에 부정적인 원치않는 경쟁에 있어 중요한 여러 구현 디테일들을 설명한다.  
마지막으로 결과를 평가하기 위한 **새로운** 이미지 품질과 variation **지표**를 소개한다.  
추가로, 고품질의 CELEBA 데이터셋 버전을 구성한다.  
  
1) 점진적 layer 추가 학습방식으로 이미지 품질, 학습속도, 안정성 증가  
2) Variation을 증가시키는 방법론 제안  
3) G와 D 학습시 잘못된 경쟁이 되는것을 피하는 테크닉 제안  
4) 새로운 데이터셋 공유  

## 1. INTRODUCTION 
대표적인 방법론은 autoregressive, VAE 및 GAN이 있으며 각자 장단점을 가지고 있다.   
Autoregressive models : sharp images, slow to evaluate, no latent space  
VAE : fast to train, blurry images  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150899232-7a6bb5f6-e4b9-40f7-8ade-140fda0d8896.png" width = 350></p>  

GANs : sharp images, low resolutioin, limited variation, unstabble training  
(세가지 방법의 장점을 결합한 방법도 있으나 품질에서는 GAN에 뒤쳐짐)  
  
### GAN의 구성에 내재하는 잠재 문제

### Distance metric 
실제 분포와 생성 분포 사이의 거리를 측정 할 때 분포가 겹쳐지지 않는 경우 기울기는 임의의 방향을 가리킬 수 있다.  
JS divergence는 거리 메트릭으로 사용되었으며 최근에는 least square, margin을 포함하는 절대편차, Wasserstein 거리를 포함하여  
여러 안정적인 방법론이 제안되었다.  
본 논문은 진행중인 논의에 대체로 독립적이며 **향상된 Wasserstein loss**를 주로 사용하지만 least-squre loss를 실험한다.  

### 학습 안정성 문제
고해상도 이미지는 실제/생성이미지 구분이 쉽기 때문에 gradient가 증폭되는 문제가 있어 이미지 생성이 어렵다.  
해상도가 커지면 batch-size(GPU 메모리)를 상대적으로 낮춰야하는데 이 때문에 학습 안정성이 저하되기도 한다.  
본 논문의 아이디어는 저해상도 이미지부터 시작하여 G와 D를 점진적으로 학습시키고 학습 진행에 따라  
고해상도 세부 정보를 도입하는 새로운 layer를 추가 하는 것이다.  
이는 학습 속도를 크게 높이고 고해상도 안정성을 향상시킨다.  

### Variation
이미지 품질과 variation 사이에 trade-off 관계가 있다는것이 일반적인 지식이나 최근 이에대한 해결책이 제시되고 있다.  
보존된 diversity 수준은 관심을 받고 있으며, inception score, multi-scale structural similarity (MS-SSIM), birthday paradox,  
explicit tests for the number of discrete modes discovered 등이 측정하기 위한 방법들로 제안되었다.  
S3 : variation을 장려하는 방법 제안

### 학습속도
S4.1 : 미세한 네트워크 초기화를 통한 여러 layer의 균형 잡힌 학습 속도를 제공  

### 네트워크 비정상적 경쟁학습
Mode collapses 현상은 전통적으로 작은 mini-batch에서 매우 빠르게 발생하여 GAN의 학습을 저해한다.  
일반적으로 D가 overshoot하여 과도한 기울기로 이어질 때 시작되며  
두 네트워크에서 신호 크기가 증가하는 비정상적인 경쟁이 뒤 따른다.  
G가 이러한 문제에 참여하지 못하도록하여 문제를 극복하는 메커니즘을 제안한다.  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150898217-53824ddc-c873-4fb3-85f3-ff133c12969f.png" width = 400></p>  


### 품질 평가 메트릭
S5 : 품질과 variation을 평가하기 위한 새로운 메트릭  

### 데이터 세트의 적용 
CELEBA, LSUN, CIFAR10 데이터 세트를 사용하여 논문의 기여를 평가한다. 특히, CIFAR10에 대해 최고의 IS를 제시한다.  
생성 방법을 벤치마킹하는 데 일반적으로 사용되는 데이터 세트는 상당히 낮은 해상도로 제한되어 있으므로  
최대 1024 × 1024 픽셀의 출력 해상도로 실험 할 수있는 CELEBA 데이터 세트의 고품질 버전도 생성한다.  
  
## 2 Progressive growing of GANs  
핵심 아이디어는 저해상도부터 시작해서 layer를 추가하여 해상도를 점진적으로 높이는 GAN 학습 방법론이다.  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150899658-32d2bf0b-0874-4939-af75-33a13a63cde9.png" width = 600></p>  


점진적 특성을 통해 최초로 큰 스케일의 구조를 학습한다.  
모든 스케일을 동시에 학습 하지 않고 점점 더 미세한 스케일 세부 사항으로 확장한다.  
서로의 거울 이미지이며 항상 동기화되어 성장하는 G 및 D를 사용한다.  
각 네트워크는 학습과정에서 모든 계층이 학습가능 상태로 유지된다.  
새로운 layer가 네트워크에 추가되면서 그림2와 같이 부드럽게 페이드인 된다.  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150899790-895192d1-036f-445a-aa22-23c075881bf8.png" width = 600></p>  
이를통해 잘 훈련 된 더 작은 해상도 layer에 대한 갑작스러운 충격을 방지 할 수 있다.  
Appendix A는 다른 훈련 매개 변수와 함께 G 및 D의 구조를 자세히 설명한다.  
점진적 학습이 몇 가지 이점이 있음을 관찰한다.  
초기에 더 작은 이미지의 생성은 클래스 정보가 적고 모드가 적기 때문에 훨씬 더 **안정적**이다.  
해상도를 조금씩 늘림으로써 latent 벡터에서 예를 들어 매핑을 발견하는 **최종 목표에 비해 훨씬 더 간단한 질문을 지속**한다.  
WGAN-GP 손실 및 LSGAN 손실을 사용하여 mega-pixel 스케일 이미지를 안정적으로 합성 할 수 있도록 학습을 충분히 안정화한다.  
  
또 다른 이점은 학습시간 단축이다. 점진적으로 증가하는 GAN으로 인해 대부분의 반복은 더 낮은 해상도에서 수행되며  
최종 출력 해상도에 따라 비슷한 품질을 최대 **2 ~ 6 배 더 빠르게** 얻을 수 있다.  
점진적으로 GAN을 성장시키는 아이디어는 pix2pixHD에서 여러 해상도에 서로다른 D를 사용하는 방식과 관련이 있다.  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150685549-c4df7455-c9a0-42b1-8507-3743f8c6be32.png" width = 400></p>  
위 아이디어는 하나의 G와 여러 D를 사용하는 Durugkar의 연구나 여러개의 G와 하나의 D를 사용하는 Ghosh의 연구에서 참고하였다.  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150685714-eb356a06-9700-4194-aaa1-e9e52aa41d17.png" width = 400></p>  
Hierarchical GAN은 이미지 피라미드의 각 수준에 대해 G와 D를 정의한다.  
<p align="center"><img src = https://user-images.githubusercontent.com/40943064/150685939-a5d5db36-a553-4cad-a838-56a5b4189666.png width = 400></p>  
  
이러한 방법은 latent에서 고해상도 이미지로의 복잡한 매핑이 단계적으로 학습하기 더 쉽다는 우리 작업과  
동일한 관찰을 기반으로하지만 중요한 차이점은 계층 구조 대신 단일 GAN 만 있다는 것이다.  
Adaptive하게 성장하는 네트워크에 대한 초기 작업,  
예를 들어 성장하는 neural gas 및 네트워크를 탐욕스럽게 성장시키는 증강 토폴로지의 neuro evolution과는 대조적으로,  
단순히 미리 구성된 layer의 도입을 사용한다. 그런 의미에서 AE의 layer 별 학습과 유사하다.  

<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150679673-06591815-a7cc-4f5c-b8cc-1405f5c17818.png" width = 500></p>  

https://github.com/happy-jihye/happy-jihye.github.io/blob/master/_posts/images/gan/pggan1.gif?raw=1

## 3. Increasing Variation using Minibatch Standard Deviation
GAN은 학습 데이터에서 발견되는 variation의 하위 집합만 포착하는 경향이 있으며  
Salimans는 솔루션으로 "minibatch discrimination"을 제안한다.  
개별 이미지뿐만 아니라 mini-batch 전체에서 feature statistics를 계산하므로  
생성된 이미지와 학습 이미지의 mini-batch가 유사한 statistics를 표시하도록 유도한다.  
이것은 D의 끝 부분에 mini-batch layer를 추가하여 구현된다. 여기서 layer는 입력 activation을  
statistics 배열에 projection하는 큰 tensor를 학습한다.  
mini-batch의 각 샘플에 대해 별도의 statistics 세트가 생성되고 layer 출력에 연결되므로 D가 내부적으로 statistics를 사용할 수 있다.  
Variation을 개선하는 동시에 이 접근 방식을 크게 단순화한다.  
  
이 단순화된 방법은, 학습 가능한 parameter나 새로운 hyperparameter가 없다.  
우선 mini-batch에 대한 각 공간 위치의 각 feature 대한 표준 편차를 계산한다.  (B X CH X W X H) → (CH X W X H)
그런 다음 모든 feature(채널) 및 공간 위치에 대해 이러한 추정치(표준 편차)를 평균화하여 단일 값을 얻는다.  
값을 복제하고 모든 공간 위치와 mini-batch에 연결하여 하나의 추가(상수) feature map을 생성한다.  
이 layer는 D의 아무 곳에나 삽입할 수 있지만 끝에 추가하는 것이 가장 좋다(appendix A.1 참조).  
풍부한 statistics 세트로 실험했으나 variation을 더 이상 개선할 수 없었다.  
병렬 작업에서 Lin은 D에게 여러 이미지를 표시할 때의 이점에 대한 이론적 통찰력을 제공한다.  
  
Variation 문제에 대한 대안에는 업데이트를 정규화하기 위한 D unrolling과 G에 새로운 loss 항을 추가하여 mini-batch에서  
feature 벡터를 orthogonalize화하도록 권장하는 " repelling regularizer"가 포함된다.  
Ghosh의 여러 G도 비슷한 목표를 달성한다.  
(이러한 솔루션이 제안 방식보다 훨씬 더 variation을 증가시킬 수 있다.)  

<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150685549-c4df7455-c9a0-42b1-8507-3743f8c6be32.png" width = 800></p>  
reference : https://engineer-mole.tistory.com/89

## 4. Normalization in Generator and Discriminator
GAN은 두 네트워크 간의 비정상적 경쟁의 결과로 **신호 크기가 확대**되는 경향이 있다.  
과거에는 G 혹은 D에서 batch normalization의 변형을 사용하여 문제를 막으려 했다.  
이 방식은 원래 covariance shift를 제거하기 위해 도입되었다.  
그러나 우리의 경우 GAN에서 문제가 되는것은 아니며 진짜 필요한 것은 **신호의 크기와 경쟁을 제한**하는 것이라고 믿는다.  
이를위해 학습 가능한 parameter를 포함하지 않는 두 가지 접근 방식을 사용한다.  

### 4.1 Equalized learning rate
가중치를 초기화하는 트렌드에서 벗어나 N(0, 1) 초기화를 사용하고 런타임에 가중치를 명시적으로 scale 한다.  
정확히는 wˆi = wi/c로 설정한다. (wi : weight, c : He의 초기화에서 가져온 layer별 정규화 상수)  
초기화 대신 동적으로 수행하는 이점은 다소 미묘하며 RMSProp 및 Adam과 같이 일반적으로 사용되는  
adaptive stochastic gradient descent의 scale 불변성과 관련이 있다.  
이러한 방법은 추정된 표준 편차로 gradient 업데이트를 정규화하므로 업데이트를 parameter scale과 무관하게 만든다.  
결과적으로 일부 parameter의 동적 범위가 다른 parameter보다 크면 조정하는 데 시간이 더 오래 걸린다.  
이것은 최신 initializer가 유발하는 시나리오이므로 학습률이 동시에 너무 크고 너무 작을 수 있다.  
우리의 접근 방식은 동적 범위와 이에 따른 학습 속도가 모든 weight에 대해 동일함을 보장한다.  
유사한 추론이 van Laarhoven(2017)에 의해 독립적으로 사용되었다.  
(StyleGAN1, StyleGAN2에도 사용)  

<img src = 'https://user-images.githubusercontent.com/40943064/150788084-9b2d1318-da30-4a3e-af47-31a76373170d.png' width = 600>  
<img src = 'https://user-images.githubusercontent.com/40943064/150789896-2fb80ec3-d6b2-416a-8e15-03d95952454c.png' width = 600>  

### 4.2 Pixelwise feature vector normalization in generator

G 및 D의 크기가 경쟁의 결과로 통제불능하게 되는것을 막기 위해  
각 conv. 레이어 이후 G의 단위 길이로 픽셀의 feature 벡터를 정규화한다.  
다음과 같이 구성된 "local response normalization"의 변형을 사용하여 이 작업을 수행한다.  
<img src = 'https://user-images.githubusercontent.com/40943064/150680873-d69d60d3-ef40-4ebd-a867-cf0294b0468c.png' width = 400>  
(epsilon: 10^-8, N : feature map 개수, ax,y 및 bx,y : 픽셀(x, y)의 원본 및 정규화된 feature vector)  
우리는 이 무거운 제약이 어떤 식으로도 G에 해를 끼치지 않는 것처럼 보이며  
실제로 대부분의 데이터 세트에서 결과를 많이 변경하지 않는다는 것이 놀랍다는 것을 알게 되었지만  
필요할 때 신호 크기의 상승을 매우 효과적으로 방지한다.

## 5. Multi-Scale Statistical Similarity for Assessing GAN Results
**MS-SSIM의 한계**  
한 GAN의 결과를 다른 GAN과 비교하려면 지루하고 어렵고 주관적일 수 있는 많은 이미지를 조사해야 한다.  
따라서 대규모 이미지 컬렉션에서 일부 지표를 계산하는 자동화된 방법에 의존하는 것이 바람직하다.  
MS-SSIM과 같은 기존 방법은 대규모 mode-collapse를 안정적으로 찾았지만 색상/질감의 변화 손실같은 작은 효과에는 반응하지 않으며  
학습세트와 유사성 측면에서 이미지 품질을 직접 평가하지 않는다.  
**Laplacian Pyramid 표현을 이용한 local patch 추출**
성공적인 G가 모든 스케일에 대한 학습 세트와 유사한 로컬 이미지 구조를 갖는 샘플을 생성할 것이라는 직관을 기반으로 한다.  
16 × 16의 low-pass 해상도에서 시작하여 생성된 이미지와 대상 이미지의 Laplacian 피라미드(Burt & Adelson, 1987)  
표현에서 가져온 로컬 이미지 패치의 분포 사이의 다중 스케일 statistics 유사성을 고려하여 이를 연구할 것을 제안한다.  
표준 관행에 따라 피라미드는 전체 해상도에 도달할 때까지 점진적으로 두 배가 되며,  
각 연속 레벨은 차이를 이전 레벨의 업샘플링된 버전으로 인코딩한다.  
단일 라플라시안 피라미드 레벨은 특정 공간 주파수 대역에 해당한다.  

![image](https://user-images.githubusercontent.com/40943064/150793904-5e8b2114-ee55-4f8e-9726-80aa355cd48d.png)

1) 16384개의 이미지를 무작위로 샘플링  
2) Laplacian 피라미드의 각 레벨에서 128개 descriptor(x ∈ R^7×7×3(147)로 표시되는 3개의 색상 채널이 있는 7 × 7 픽셀 이웃) 추출  
3) Level당 2^7 * 2^14 = 2^21(2.1M)개의 descriptor를 제공  
  
학습 세트와 생성 세트의 레벨 l에서 패치 :
<img src = 'https://user-images.githubusercontent.com/40943064/150804429-98cd82bb-cfbd-452b-a6a9-054834bec9b9.png' width = 150>  

1) 각 색상 채널의 평균 및 표준 편차에 대해 {xli} 및 {yli}를 정규화  
2) sliced Wasserstein distance(SWD)를 계산하여 통계적 유사성을 추정  
  
직관적으로 작은 Wasserstein 거리는 패치의 분포가 유사함을 나타낸다.  
즉, 학습 이미지와 생성기 샘플이 이 공간 해상도에서 **모양**과 **변형** 모두에서 유사하게 나타난다.  
특히, 가장 낮은 해상도의 16 × 16 이미지에서 추출한 패치 세트 간의 거리는 대규모 이미지 **구조**에서 유사성을 나타내는 반면,  
가장 정밀한 패치는 가장자리의 **선명도 및 노이즈와 같은 픽셀 수준 속성**에 대한 정보를 인코딩한다.  

## 6 Experiments

### 6.1 Statistical similarity 측면에서 개별 기여의 중요성
1) SWD와 MSSSIM의 지표를 이용하여 개별적 기여도 평가  
2) 지각적으로 지표 자체를 검증  

Benchmark : WGAN-GP  
Dataset(128x128) :  
1) CelebA(학습 이미지 자체가 관측가능한 artifact(aliasing, compression, blur)를 가지므로 검증하기 좋음)  
2) LSUN bedroom   
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150807402-725bd490-ab96-4eed-9708-902190bab98e.png"></p>  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150807662-d136d024-3b67-4e53-b2b0-eb1ca299a6cf.png"></p>  
**실험조건**
(a) Batchnorm in G, Layernorm in D, minibatch = 64  
(b) + progressive growing  
(c) + mini-batch size 감소 (64 → 16)  
(d) + hyperparameter 조절 + batchnorm/layernorm 제거를 통한 학습 안정화(A.2)  
(e*)+ minibatch discriminations of Salimans  
(e) + proposed minibatch discriminations  
(f) + Equalized learning rate  
(g) + Pixelwise normalization  
(h) + 모두 포함 & 충분한 학습시간

**MS-SSIM의 무효성**  
(a) vs (h) : 시각적 품질은 (h)가 훨씬 좋지만 MS-SSIM 차이가 없거나 (a)가 더 좋음  
(MS-SSIM은 학습셋과의 유사성 보다는 출력간 variation만 평가하기 때문)  

**Progressive Growing 성능**  
(b)가 (a)에 비해 훨씬 선명하고 신뢰할 수 있는 결과를 얻는다.  
SWD는 학습셋과의 유사성 측면에서 더 잘 나타낸다.  

**모듈 추가에 따른 성능**  
(고해상도 학습시에는 GPU의 memory 한계로 minibatch 사이즈를 줄여야함)
(c) : 이미지가 망가지며 평가 척도에서도 값이 매우 나쁨  
(d) : (c)에 비해 상대적으로 학습 안정화 확보에 성공  
(e*): 두개의 평가 척도에서 성능 향상을 이끌어내지 못함
(e) : 대체로 시각적 품질과 SWD 향상  
(f) & (g) : 대체로 시각적 품질과 SWD 향상  
(h) : 전반적으로 가장 좋음  

### 6.2 수렴과 학습속도
(a) : Baseline / (b) : PG 방식 추가  / (c) : 고해상도에서의 시간에 따른 이미지 노출수
  
(b)의 최종 성능이 더 좋으며 동일 성능 기준 학습시간이 두배 빠름  

개선된 수렴은 점진적으로 증가하는 네트워크 용량에 의해 부과되는 암묵적인 형태의 커리큘럼 학습으로 설명할 수 있다.  
1) PG 없이  없이 G와 D의 모든 레이어는 대규모 변형과 소규모 세부 사항 모두에 대한 간결한 중간 표현을 동시에 찾는 작업을 수행한다.  
2) PG 방식의 경우 기존 저해상도 레이어는 이미 초기에 수렴되었을 가능성이 있으므로 네트워크는 새 레이어가 도입됨에 따라  
점점 더 작은 규모의 효과로 표현을 수정하는 작업만 수행한다.  
실제로, (b)에서 16이 최적의 값에 매우 빠르게 도달하고 나머지 시간 동안 유지된다는 것을 알 수 있다.  
32, 64, 128은 해상도가 증가함에 따라 하나씩 평평해 지지만 각 곡선의 수렴은 동일하게 일관된다.  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150812244-ab538e0a-3199-4485-a30a-ebab4164082b.png"></p>  
(a)에서 SWD의 각 scale은 예상대로 대략 일치하게 수렴한다.  
(b)의 속도 향상은 출력 해상도가 증가함에 따라 증가한다.   

(c)는 학습이 1024x1024 까지 진행될 때 시간의 함수로 D에 표시되는 실제 이미지 수로 측정한 학습 진행 상황을 보여준다.  
네트워크가 얕고 초기에 평가하기가 빠르기 때문에 점진적 성장이 상당한 우위를 점하고 있음을 알 수 있다.  
전체 해상도에 도달하면 이미지 처리량은 두 가지 방법 간에 동일하다.  
PG가 96시간 동안 약 640만 이미지에 도달하는 것을 보여주지만, 기본은 동일한 지점에 도달하는 데 약 520시간이 소요될 것으로 추정할 수 있다.  
이 경우 PG는 대략 5.4배의 속도 향상을 제공한다.  

### 6.3 CelebA-HQ를 이용한 고해상도 이미지 생성

높은 해상도에서의 성능을 평가하기 위해는 다양한 고품질 데이터가 필요하다.  
낮은해상도(32 ~ 480) 데이터만 존재했기 때문에 1024의 30k개로 구성된 고품질 CelebA 데이터 새트를 만들었다.  
(부록 C 참조)  

그림 5는 생성된 선택된 1024 × 1024 이미지를 보여준다.  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150816981-a8c14a49-640d-4d75-abc6-c6cc64426023.png"></p>  
1024 해상도에 대한 GAN 결과는 다른 데이터 세트(Marchesi, 2017)에서 이전에 표시되었지만  
본 결과는 훨씬 더 다양하고 더 높은 지각 품질을 제공한다.  

**Appendix F1 : 학습 데이터에서 찾은 가장 가까운 이웃**  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150818249-8bc6cc54-f413-402c-a030-23259f2f46ff.png"></p>  
**Appendix F2 : CelebA-HQ에 대한 추가 결과**  
(설명 비디오에 interpolation 결과 확인가능)  
SWD : 16: 7.48, 7.24, 6.08, 3.51, 3.55, 3.02, 7.22, (average is 5.44)  
FID : 7.3 (50k 샘플)  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150818943-0bf1f95a-17ec-4d9c-9a9a-8e4ca270def3.png"></p>  
loss function의 선택(LS or WGAN-GP)에 관계없이 고품질을 얻을 수 있으며 figure. 1의 결과가 LS loss로부터 얻은 결과이다.  
LS를 적용하기 위해 몇가지 추가 작업이 필요하다.(Appendix B.)

### 6.4 LSUN 결과
Figure 6 : 초기 결과와 본 방법의 시각적 비교  
Figure 7 : 다양한 category의 256 해상도 샘플에 대한 결과 
(G에 30개의 LSUN category의 더 크고 무작위 결과 확인 가능)    

<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150820578-8f17bd22-9067-479f-a8b7-40336236c25c.png"></p>  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150820746-1f1833fd-f8d0-448e-bf26-708325e765c3.png"></p>  



## 6.5 CIFAR10 Inception scores
CIFAR10(32 × 32 RGB 이미지의 10개 범주) SOTA(Grinblat, 2017) 
1) Unsupervised : 7.90  
2) Labeled      : 8.87 
두 숫자 사이의 큰 차이는 주로 unsupervised 환경에서 class 사이에 나타나는 "ghost"에 의해 발생하지만  
label 조절은 이러한 많은 전환을 제거할 수 있다.  
본 연구의 모든 contribution을 적용하면 unsupervised setting에서 8.80을 얻는다.(Labeled 학습과 거의 유사)  
<p align="center"><img src = "https://user-images.githubusercontent.com/40943064/150822751-004db170-4f02-4639-9657-1608af49f646.png"></p>  
