## Abstract
Score-based 생성모델은 GAN과 비교할만한 고품질의 이미지를 적대적 최적화 없이 생성할 수 있다.  
그러나 현존 학습 과정들은 저해상도에 제한되어 있으며 일부 세팅 하에서는 불안정할 수 있다.  
고차원 공간의 score-based 모델에서 학습 및 샘플링에 대한 새로운 이론적 분석을 제공하여 기존 failure-mode를 설명하고 데이터 세트 전반을 일반화하는 새로운 솔루션에 동기를 부여한다.  
안정성을 향상하기 위해 우리는 모델 weigth의 EMA를 유지하는것을 제안한다.  
이러한 개선을 통해 score-based 생성 모델을 64 × 64에서 256 × 256 × 256까지 다양한 해상도로 다양한 이미지 데이터 세트로 확장할 수 있다.  
우리의 score-based 모델은 다양한 이미지 데이터 세트(CelebA, FFHQ, LSUN)에서 GAN과 견줄 수 있는 높은 충실도의 샘플을 생성할 수 있다.  

## 1. Introduction
Score-based 생성 모델은 score를 통한 확률 분포를 나타낸다. 놀랍게도, 이러한 score 함수는 적대적 최적화를 요구하지 않고 데이터에서 학습할 수 있으며, CIFAR-10과 같은 간단한 데이터 세트에서 GAN과 견줄만한 현실적인 이미지 샘플을 생성할 수 있다. 이러한 성공에도 불구하고 기존 score-based 생성 모델은 몇 가지 제한 요인으로 인해 저해상도 이미지(32x32)에서만 작동한다.  
  
1) Denoising Score matching을 통해 score function을 학습한다. 직관적으로, 이것은 score network가 Gaussian noise로 blur되어진 이미지의 노이즈를 제거하도록 학습된다는 것을 의미한다. NCSN의 핵심 통찰력은 score network가 coarse하고 fine-grained한 이미지 feature를 모두 캡처할 수 있도록 multiple noise scale을 사용하여 데이터를 perturb하는 것이다. 그러나 이러한 noise scale을 어떻게 선택해야 하는지는 미결 문제이다. NCSN의 권장 설정은 32x32 이미지에서는 잘 작동하지만 해상도가 높아지면 성능이 저하된다.  
2) Sampling은 Langevin dynamics를 실행하여 생성된다. 이 방법은 white noise에서 시작하여 score network를 사용하여 이미지로 점진적으로 노이즈를 제거한다. 그러나 이 절차는 고차원 및 필연적으로 불완전한(학습된) score network에서 사용될 때 실패하거나 수렴하는 데 매우 오랜 시간이 걸릴 수 있다. 우리는 score-based 생성 모델을 고해상도 이미지로 스케일링하는 일련의 기술을 제안한다. 단순화된 혼합 모델에 대한 새로운 이론적 분석을 기반으로, 훈련 데이터에서 효과적인 Gaussian noise scale 세트를 분석적으로 계산하는 방법을 제공한다. 또한 단일 신경망을 사용하여 많은 수의(아마도 무한) noise scale에 걸쳐 score estimation 작업을 상각하는 효율적인 아키텍처를 제안한다. 기본 Langevin dynamics sampling 절차의 수렴 특성에 대한 단순 분석을 기반으로, 우리는 또한 noise scale의 함수로서 성능을 대략적으로 최적화하는 기술을 도출한다. 이러한 기술을 EMA와 결합하면 샘플 품질을 크게 향상시킬 수 있으며, 이전에는 score-based 생성 모델에서 불가능했던 64x64에서 256x256 범위의 해상도의 이미지로 성공적으로 확장할 수 있다. Fig. 1에 도시된 바와 같이, 샘플은 sharp & diverse 하다.  
![image](https://user-images.githubusercontent.com/40943064/174436349-5a503f08-c87d-4280-8432-df58ad7982d3.png)

## 2. Background
### 2.1 Langevin dynamics
연속적으로 미분 가능한 확률 밀도 p(x)에 대해, 우리는 del ▽log p(x)를 score function이라 부른다. 많은 상황에서 score function은 원래 확률 밀도 함수보다 모델링하고 추정하기가 더 쉽다. 예를 들어, 정규화되지 않은 density의 경우 partition 함수에 의존하지 않을 수 있다. Score function이 알려지면 Langevin dynamics를 사용하여 해당 분포에서 표본을 sampling 할 수 있다. Step size ⍺ > 0, 총 반복 횟수 T 및 prior pi(x)의 초기 샘플 x0이 주어졌을 때, Langevin dynamics는 다음을 반복적으로 평가한다.  
<img src ='https://user-images.githubusercontent.com/40943064/174436618-6d63cd12-e30f-432a-a027-2bacdb936045.png' width = 400>  
z(t) ~ N(0, I).  
⍺가 충분히 작고 T가 충분히 크면 XT는 몇가지 regularity condition 하에 p(x)에 근접할 것이다.  
θ에 의해 파라미터화된 네트워크 sθ(x)가 있을때, sθ(x) ~ ▽log p(x)되도록 학습되어진다고 가정한다.  
▽log p(x_t-1)을 sθ(x_t-1)로 대체하여 Langevin dynamics를 사용함으로써 p(x)로부터 근사적으로 샘플을 생성할 수 있다.  
Eq(1)은 log density log p(x)에 대한 noisy gradient ascent로 해석될 수 있음을 주목하자.  

### 2.2 Score-based generative modeling
데이터에서 score function을 추정하고 Langevin dynamics를 사용하여 새로운 샘플을 생성할 수 있다. 이 아이디어는 NCSN에 의해 score-based 생성 모델링으로 명명되었다. 학습 데이터가 없는 영역에서 추정된 score function이 부정확하기 때문에, sampling trajectory가 해당 데이터 저밀도 영역에 맞닥뜨릴 때 Langevin dynamics는 올바르게 수렴되지 않을 수 있다. 해결책으로서, NCSN은 서로 다른 강도의 Gaussian noise를 사용하여 데이터를 perturb하고 모든 noise purterb 데이터 분포의 score function 공동으로 추정할 것을 제안한다. 추론하는 동안, 그들은 Langevun dynamics를 사용하여 순차적으로 각 노이즈 교란 분포에서 샘플링하여 모든 noise scale의 정보를 결합한다.  

좀 더 구체적으로, 기초적인 데이터 분포 pdata(x)가 있다고 가정하고 α1 > α2 > αL 을 만족하는 일련의 노이즈 스케일 {σ}i=(1>L)을 고려해보자.  
입력에 대한 전이확률(perturbation 확률)을 아래와 같이 정의하고,  
<img src = 'https://user-images.githubusercontent.com/40943064/174437349-0eea8efa-6a8e-4fe3-9764-6cf2cd79d185.png' width=350>   
그에 상응하는 perturbed 데이터 분포를 다음과 같이 정의한다.  
<img src = 'https://user-images.githubusercontent.com/40943064/174437367-70c7ba80-a120-49fe-841f-8ca9a829109d.png' width=400>   
NCSN에서는 아래 loss항을 가지고 sθ(x, σ)인 joint neural network를 학습하여 각 pσi(x)에 대한 score function을 추정하는 것을 제안한다.  
<img src = 'https://user-images.githubusercontent.com/40943064/174437494-60321bbd-1219-48b1-af2d-e12d6c2c7c08.png' width=500>   
여기서 모든 기대값연산은 empirical average를 사용하여 효과적으로 추정할 수 있다.  
sθ*(x,σ)로 명시되는 optimum으로 학습이 되면 NCSN은 (충분한 데이터 그리고 모델용량이 충분하다고 가정하에) 모든 i에 대하여 sθ*(x,σ) = ▽x log pσi(x)를 만족한다.  

우리는 데이터에서 score function를 추정하고 Langevin dynamics를 사용하여 새로운 샘플을 생성할 수 있다.  
이 아이디어는 NCSN에 의해 score-based 생성 모델링으로 명명되었다. 
학습 데이터가 없는 영역에서 추정된 점수 함수가 부정확하기 때문에, 샘플링 궤적이 해당 영역에 맞닥뜨릴 때 랑주뱅 역학은 올바르게 수렴되지 않을 수 있다.  
해결책으로 NCSN은 서로 다른 강도의 Gaussian noise를 사용하여 데이터를 perturb하고 모든 noise perturbed 데이터 분포의 score function을 공동으로 추정할 것을 제안한다. 
Sampling 동안, 그들은 Langevin dynamics를 사용하여 순차적으로 각 noise perturbed distribution에서 샘플링하여 모든 noise scale의 정보를 결합한다.

DSM-ALS은 NCSN에서 제안한 annealed Langevin dynamics이후 추가 denoising을 추가하는이 때로 시각적 샘플의 외형을 바꾸지 않고 FID를 엄청나게 올린다는것을 관측했다.  
직접적으로 XT를 얻는것이 아니라 이 denoising step은 XT + σT ** 2 sθ(XT,σT)를 얻으며 그것은 본질적으로 Tweedie의 공식을 사용하여 XT로부터 원치않는 noise N(0, σT ** 2)를 본질적으로 제거한다.  
그러므로우 우리는 본 논문에서 denoising trick을 통합하여 업데이트 했으며, 일부 원 논문의 결과를 유지했다.  

아래와 같이 NCSN의 성공적은 학습과 추론에 매우 중요한 설계적 선택사항들이 존재한다.  
1) Noise scales 
2) sθ(x, σ)가 σ에 대한 정보를 통합하는 방식
3) step size 파라미터 ϵ
4) scale T에 대한 sampling step number

아래에서는 수동 튜닝 없이 이를 구성할 수 있는 이론적인 방법을 제공하여 고해상도 이미지에서 NCSN의 성능을 크게 향상시킨다.

## 3 Choosing noise scales
Noise scale은  NCSN 성능에 매우 중요하다. NCSN에서 볼 수 있듯이, 단일 노이즈로 학습된 score network는 큰 이미지에 대해 신뢰할 수 있는 샘플을 생성할 수 없다. 직관적으로 높은 noise는 score function의 추정을 용이하게 하지만 corrupted sample로 이어진다. 반면 낮은 노이즈는 깨끗한 샘플을 제공하지만 score function을 추정하기 어렵게 만든다. 따라서 서로 다른 noise scale을 함께 활용하여 두 세계를 모두 활용해야 한다.  
NCSN에서 pixel값의 범위가 0~1이면 L=10, σ1=1, σL=0.01로 선택하는것을 추천한다. σL은 1보다 매우 작은 0.01로 설정 하는것은 합리적이다. (noise scale을 감소시켜 perturbed distribution으로부터 샘플을 하고 종단에는 낮은 noise를 더하므로)  

그러나, 일부 중요한 질문들은 대답되지 않은 채 남아 있는데, 이는 고해상도 이미지에서 NCSN의 성공에 중요한 것으로 드러난다:  
1) σ1 = 1이 적절한가? 그렇지 않다면, 서로 다른 데이터 세트에 대해 1을 어떻게 조정해야 하는가?
2) geometric progression이 좋은 선택인가? 
3) L = 10은 서로 다른 데이터 세트에 걸쳐 유효한가? 만약 그렇지 않다면, 몇 개의 noise scale이 이상적인가?

아래에서는 간단한 수학 모델에 대한 이론적 분석에 의해 위의 질문에 대한 답변을 제공한다. 우리의 통찰력은 섹션 6의 실험 결과에 의해 입증되었듯이 실제로 score-based 생성 모델링을 구성하는 데 효과적이다.

### 3.1 Initial noise scale
Annealed Langevin dynamics(Algorithm 1) 알고리즘은 작은 노이즈에서 변동이 적은 미세한 샘플로 수렴하기 전에 큰 노이즈에서 변화가 많은 coarse 샘플을 생성하는 반복적인 refining 절차이다. 초기 noise scale δ1은 최종 표본의 **diversity**를 크게 제어한다. 샘플 다양성을 증진시키기 위해, 우리는 가능한 한 크게 σ1을 선택할 수 있다. 그러나 σ1이 지나치게 크면 더 많은 noise scales가 필요하며(섹션 3.2에서 다룸) annealed Langevin dynamics는 더 계산량이 많아진다. 아래에서는 σ1의 선택을 안내하고 올바른 균형을 맞추기 위한 기술을 제공하기 위한 분석을 제시한다.

실제 데이터 분포는 복잡하고 분석하기 어려우므로 경험적 분포로 근사치를 구한다. pdata(x)에서 샘플링된 i.i.d. 데이터 세트 {x(1)}, ...x(N)}가 있다고 가정해보자.  

N이 충분히 크다고 가정하면 <img src ='https://user-images.githubusercontent.com/40943064/174442981-2d2f7817-8239-4f39-8167-4336314e509d.png' width = 300>는 점 질량 분포를 나타낸다.(경험적 분포근사로 샘플이 충분히 많을때 점질량 분포를 근사할 수 있는 사실에 대해 검색)  
초기화와 관계없이 다양한 샘플을 생성하기 위해, 우리는 자연스럽게 Langevin 역학이 다른 구성 요소 p(j)(x)에서 초기화될 때 모든 구성 요소 p(i)(x)를 탐색할 수 있다고 예상한다. 여기서 i!= j.
Langevin dynamics의 성능은 <img src = 'https://user-images.githubusercontent.com/40943064/174443085-6f63e236-a1c9-4e16-b201-cedfd5b5a208.png' width = 200> score function에 의해 제어된다.

<img src = 'https://user-images.githubusercontent.com/40943064/174443125-4eb288ba-7e62-47ce-a7b5-d7ea2e14dc45.png' width = 800>  
Langevin dynamics가 i!=j 조건에서 p(i)(x)로부터 p(j)(x)로 변이하기 위해, <img src ='https://user-images.githubusercontent.com/40943064/174443592-9f7725a0-8644-4df1-9b46-7d71e67e4b61.png' width=200>가 상대적으로 커야한다.  
(그렇지 않으면 <img src = 'https://user-images.githubusercontent.com/40943064/174443516-30c7538e-0c33-403f-9ad4-70f9deee3106.png' width = 300> p(j)(x)를 무시할 것이다. : p(i)(x)로 초기화 되면 p(j)(x)는 존재하지 않는것 처럼 행동)  
Eq(3)의 bound는 다음을 명시한다. :  만약 σ1가 <img src = 'https://user-images.githubusercontent.com/40943064/174443701-a08b2ef6-634d-4862-8135-84963f052efe.png' width = 150> 에 상대적으로 작다면 <img src ='https://user-images.githubusercontent.com/40943064/174443592-9f7725a0-8644-4df1-9b46-7d71e67e4b61.png' width=200> 는 지수적으로 감쇠할 수 있다.  

결과적으로, σ1은 Langjuvin dynamics의 transition을 용이하게 하고 따라서 샘플 다양성을 향상시키기 위해 데이터의 최대 pairwise distance와 수치적으로 비교될 수 있어야 한다. 특히 다음과 같이 제안한다.

**Technique1** (Initial noise sclle).  
모든 학습 data point pair 사이의 최대 유클리드 거리만큼 큰 σ1를 선택한다.  
CIFAR-10에 대하여 적절하게 선택하는경우 아래와 같은 결과를 얻을 수 있다.(GT(a)와 Propose(c)의 샘플 다양성이 유사함)  
<img src = 'https://user-images.githubusercontent.com/40943064/174444181-3c1aa797-ea1a-409b-acf4-f582db48ced2.png' width=600>


### 3.1 Initial noise scale
