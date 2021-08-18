# Attribute Manipulation Generative Adversarial Networks for Fashion Images

## Abstract
최근 GAN의 발전으로 단일 G를 사용하여 multi-domain I2I translation이 가능하다.   
Ganimation 및 SaGAN과 같은 최근 방법은 attention을 이용해 attribute 관련 영역에 대한 번역을 수행하지만  
attention mask 학습은 주로 분류 손실에 의존해 attribute 수가 증가하면 성능이 보장되지 않는다.  
관련 문제 해결을 위해 패션 이미지에 AMGAN을 도입한다.  
AMGAN의 G는 attention mechanism을 강화하기 위해 CAM을 사용하지만 attribute similiarity 기반으로 이미지를 할당하여  
perceptual loss를 이용한다. 비현실적인 번역을 감지하기 위해 attribute 관련 영역에 중점을 둔 추가 D를 통합한다.  
소매 또는 몸통 영역과 같은 특정 영역에서 attribute 조작을 수행하도록 제어할 수 있다.  
실험에 따르면 AMGAN은 기존 평가 metric과 이미지 검색을 기반으로 하는 대안을 사용하는 SOTA 보다 성능이 뛰어나다.  
  
## 1. Introduction
Attribute manipulation은 이미지를 목표 attribute 기반하에 변환/조정하는 것이다.  
패션상품에서 관심있는 attribute는 소매길이, 색상, 패턴과 같은 시각적 품질과 관련되고  
attribute value는 긴소매, 빨간색 및 일반 패턴과 같은 특정 레이블에 해당한다.  
이미지의 속성을 조작할 수 있다는 것은 사용자가 일부 속성에 만족하지 못하는 등 다양한 상황에서 유용하다.  
최근 이 작업은 속성 조작을 수행한 후 데이터 세트에서 대상 이미지를 검색하는 것과 관련된 이미지 검색 관점에서 연구되었다.  
그러나 이미지 검색 접근 방식은 데이터 세트 크기와 증가하는 속성 수로 인해 제한된다.  
GAN 도입 이후로 이미지 생성 작업은 많은 관심을 받았다. 많은 컴퓨터 비전 작업과 함께 GAN은 I2I 번역 문제에 적용될 수 있다.  
StarGAN은 단일 생성 네트워크로 multi-domain I2I translation을 수행할 수 있다.  
Ganimation, SaGAN은 생성 네트워크에 attention mechanism을 통합하는 여러 접근 방식이 제안됐다.  
Attention mechanism을 갖는 것은 속성 관련 영역에서 속성 조작을 수행해야 하는 반면 다른 영역은 동일하게 유지해야 할 때 특히 유용하다.  
그러나 속성 수가 증가함에 따라 이러한 attention 기반 방법은 분류 손실을 통해 학습된 attention 영역이 불안정해진다.  
또한, D는 attention mechanism의 이점을 얻을 수 있으며 G가 보다 현실적인 속성 조작을 수행하도록 한다.  
본 논문에서는 속성 조작을 수행할 수 있도록 하는 패션 이미지에 대한 multi-domain I2I translation을 위한 방법블 제안한다.  
I2I translation 네트워크는 대부분 얼굴 이미지 용이지만 AMGAN은 패션 이미지와 같이 덜 딱딱한 개체에 대해 이를 달성한다.  
그림 1은 Deepfashion, Shopping100k 데이터 세트에 대한 속성 조작의 몇 가지 예를 보여준다.  
![image](https://user-images.githubusercontent.com/40943064/129847716-32fedd50-f696-4e73-8f12-0494f17148f0.png)

제안 방법은 AMGAN은 다른 속성을 유지하면서 대상 속성의 변경 사항을 기반으로 입력 이미지를 새 이미지로 변환하는 기능이다.  
제안 방법은 속성 위치에 대한 정보를 활용하지 않고 속성 조작을 위한 attention mechanism을 통합한다.  
**목표는 관심 속성이 있는 영역을 찾아 새로운 영역으로 변환할 수 있도록 하는 것이다**.  
따라서 G가 조작할 속성을 기반으로 영역을 올바르게 지역화하는 것이 중요하다. CAM을 사용하여 속성의 식별 영역을 올바르게 지역화할 수 있다.  
CAM을 attention loss로 사용함으로써 AMGAN의 G는 attention mask를 올바르게 생성하므로 결과적으로 속성 조작 능력이 향상된다.  
다른 연구가 전체 이미지에 대해 단일 D를 사용하는 반면, AMGAN은 속성 관련 영역에 초점을 맞춘 추가 D를 사용하여  
이미지 번역 성능을 개선하기 위해 비현실적인 속성 조작을 감지한다. Unpaired I2I translation의 경우 입력 이미지 및 속성 조작에 따른  
참조(대상) 이미지가 없으므로 지각 손실을 사용할 수 없다. 속성 유사성을 기반으로 참조 이미지를 할당하여 이 문제를 해결한다.  
결과적으로 AMGAN은 CAM을 추출하는 동일한 CNN의 기능을 기반으로 하는 perceptual loss 함수의 이점을 얻는다.  
Perceptual loss로 AMGAN은 속성 조작을 일치시키는 능력이 향상되는 동안 보다 사실적인 이미지를 생성할 수 있다.  
기존의 I2I translation 외에도 AMGAN은 attention mask를 사용하여 특정 영역에 대한 속성 조작을 수행하도록 조정할 수 있다.  
예를 들어, AMGAN은 attention mask를 "sleeveless" attribute manipulation 마스크로 교체하여 소매 영역에서 "빨간색" 속성 조작을 수행하도록 조정할 수 있다.  
이 기능은 지역별 속성 조작을 자동화하는 데 유용하다.  
AMGAN의 주요 기여는 아래와 같다.  

• CAM을 이용한 G의 attention mechanism을 강화 -> attribute similarity 기반 perceptual loss 적용  
• 속성 관련 영역에 중점을 둔 추가 D 통합  
• 특정 영역 속성 조작 활성화  
• 두 가지 패션 데이터 세트에 대한 자세한 실험을 통해 AMGAN이 SOTA임을 증명  
(특성 조작의 성공 여부를 테스트하기 위해 이미지 검색을 기반으로 하는 새로운 방법 소개)

## 2. Related Work
GAN, cGAN : 생략
I2I translation : pix2pix : paried -> cycleGAN : unpaired 1-domain -> StarGAN : Multi-domain -> Attention based architecture  
(Attention based 방법 단점 :  classification loss 의존)

## 3. AMGAN
multi-domain i2i 변환(속성 조작)을 수행할 수 있는 AMGAN에 대해 설명한다. 다음으로 AMGAN을 조정하여 지역별 속성 조작을 수행하는 방법을 이해한다.  
  
**Problem Definition.**  
AMGAN 아키텍처는 그림 2와 같이 G(Enc-Dec 구조:속성 조작 m을 적용하여 입력 이미지 xI를 출력 이미지로 변환 : ![image](https://user-images.githubusercontent.com/40943064/129750323-8f8fd92d-8d99-4fb9-97f6-8df4a89f2ad7.png)))와 DI, DC로 구성하며 가능한 모든 속성 조작 작업은 m = {m1, ...mN , r}로 인코딩될 수 있다.   
N은 속성 값의 수(예: 긴 소매, 빨간색 등)이고 r은 조작 중인 속성(소매, 색상 등)을 나타낸다. G 각 학습 반복에 대한 특정 속성에 초점을 맞추도록 한다.  
r과 m은 모두 원-핫 인코딩으로 표현된다.  

**3.1. Network Construction**
(xI, m)은 G로 입력되어 2개의 출력z(생성이미지), a(attention mask)를 얻는다.  
Attention mask는 입력/출력이미지와 결합되며 특정 영역은 attribute manipulation을 위해 다른 영역은 유지시키도록 한다.   
최종 출력 이미지는 다음과 같이 얻어진다.   
![image](https://user-images.githubusercontent.com/40943064/129838364-e60cdecb-ffaf-44ac-95a1-30cf334588f6.png)  ... (1)  
CAM(X_I, m)을 이용해 얻은 a\*를 G에 넣어 attention loss에 집중할 수 있는 영역을 넣어준다.  
추가로 attribute 유사도를 이용하여 xref(속성조절 이후 얻어질 기대 attribute를 나타내는)가 perceptual loss로 할당된다.   
D는 진짜 가짜 이미지를 구분하기 위해 사용되며 classification loss를 제공한다.  
DI는 전체이미지에 집중하는 반면, DC는 속성 조절영역에 집중한다.  
x\*C, xC로 명시된 DC 입력은 a로 부터 추정된다.  
먼저, 최대값의 50퍼센트가 넘는 a의 pixel값들은 segmented되어 가장 큰 연결 영역을 cover 하는 bonding box를 추정한다.  
그림2와 같이, Bounding box를 사용하여 x\*C, xC는 x\*I, xI로부터 crop된다.  
![image](https://user-images.githubusercontent.com/40943064/129839302-6c35805d-de27-47bf-85d3-e3bdd3fa7016.png)  
  
**3.2. Discriminators**  
DI, DC 둘다 DCNN에 기반하며 adverasrial/classification loss를 가진다.  
**Adversarial Loss.**  
출력이미지 x_d를 ![image](https://user-images.githubusercontent.com/40943064/129839557-a68d85f1-cf36-4b95-bd97-532943525a9a.png)  
d는 x_I, x_C 전체 이미지를 의미한다.  
D의 목적은 ![image](https://user-images.githubusercontent.com/40943064/129839767-7cdf3105-fc29-47e0-86eb-4d7e060b05da.png)를 최대화하고 ![image](https://user-images.githubusercontent.com/40943064/129839830-6cb93980-efe9-4f9c-9c7b-8beae2e8ce4a.png)를 최소화한다.  
따라서, 전체 D에 대한 loss는 다음과 같이 정의된다.  
![image](https://user-images.githubusercontent.com/40943064/129853692-4018c376-74be-47d5-965c-2f844a017e4b.png)  
위 loss의 최종항은 gradient penalty를 lamda_gp(실제와 fake이미지 사이에 직선을 따라 uniform하게 샘플된 x_tilde_d를 패널티하는) Wasserstein GAN 목적함수이다.  
**Classification Loss.**  
적대적 손실이 있는 실제/가짜 샘플을 인식하는 것 외에도 판별자가 실제/가짜 이미지의 속성을 분류할 수 있는 것도 중요하다.  
그러므로, Dd는 Dd_cls(m'|x_d):m'는 원본  attribute에 해당한다. 로 명기된 다른 출력이 있다.  
cross-entropy를 사용하여 전반 classification loss는 다음과 같이 정의된다.  
![image](https://user-images.githubusercontent.com/40943064/129840271-0456607f-3028-472d-a726-04b9e768eca1.png)  
두 loss를 결합하여 목적함수는 다음과같이 정의할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/129840392-5057d9df-6232-437d-b60c-e6a241400b53.png)  

**3.3. Generator**  
AMGAN의 G는 속성조절 m에 따라 새로운 이미지를 만들기 위해 다음의 loss로 구성된다.  

**Adversarial Loss.**  
G가 실제같은 샘플을 생성하기 위해 다음의 adversarival loss가 사용된다.  
![image](https://user-images.githubusercontent.com/40943064/129840895-d5429636-2047-471c-bea4-78985ed0df27.png)  

**Classification Loss.**  
m에 대한 이미지를 생성하기 위해 생성 이미지는 ![image](https://user-images.githubusercontent.com/40943064/129841006-759d43c5-9fd7-42b8-92d1-32fed51c2ad8.png)를 추정하기 위해 입력되고  G를 위한 classification loss는 다음과 같이 정의된다.  
![image](https://user-images.githubusercontent.com/40943064/129841078-54a1cac2-20ff-4a12-bb63-f9419ddd5146.png)  
d = C일 때, 속성 localized 이미지가 입력되어 attended 영역에 올바른 속성값을 가진 더욱 실제같은 샘플을 생성하기 위한 G가 되도록 강제한다.  
**Cycle Consistency Loss.**  
순환 일관성 손실[39]을 사용하여 "관련 없는 영역"이 변경되지 않은 상태에서 입력 내용이 보존되도록 한다.  
속성 조작 m 및 m\*는 xI에 대해 연속적으로 수행될 때 생성된 이미지는 xI와 동일할 것으로 예상된다.  
따라서 주기 일관성 손실은 다음과 같이 정의된다.  
![image](https://user-images.githubusercontent.com/40943064/129841265-ea2845e6-a8f8-4242-84e3-ba369f2a9551.png)  
**Attention Loss.**  
분류 손실이 속성 관련 영역으로 attention mask를 유도하는 경우 위에 정의된 손실 함수로 그럴듯한 attention mask를 가질 수 있다.  
그러나 속성 수가 증가하거나 이미지에 challenging한 포즈 변형이 나타날 때 attention mask가 불안정해져서 속성 조작 결과에 영향을 미칠 수 있다.  
모든 속성에 대해 ground truth mask를 가질 수 없기 때문에 CAM 기법을 사용하여 속성 위치에서 생성기 네트워크를 안내할 것을 제안한다.  
CAM을 사용하면 다음과 같이 주의 손실이 G에 포함됩니다.  
**CAM**  
먼저, 입력 XI는 CNN에 입력되어 convolutional feautre fk를 생성한다. xI의 속성 m'에 대한 (i, j) 위치의 CAM은 다음과 같이 추정된다.  
![image](https://user-images.githubusercontent.com/40943064/129841617-4c452650-2785-4b51-8cfb-8e331804bfe8.png)  
여기서, ![image](https://user-images.githubusercontent.com/40943064/129841687-316cd7a4-0bcf-4b38-835c-1d5e663095ea.png)는 k'th feauture map과 관련된 속성 m'에 대한 weight 변수이다. ![image](https://user-images.githubusercontent.com/40943064/129841764-2c35120c-64d4-43d4-8946-589237af9001.png)에 대한 값들은 0~1로 정규화되어 a\*로 명기된 guidance mask에 상응하도록 된다.  
L1 norm을 채택하고 다음과 같이 attention loss를 정의한다. 
![image](https://user-images.githubusercontent.com/40943064/129841876-5c02b43d-2845-4885-acb0-21b07bbcf979.png)  
α\*가 계산된 후 생성기에서 추가 attention mask 출력 없이 사용하도록 선택할 수 있다.  
(G에서의 출력 a가 a\*를 따라가도록 설계하지 않고 G는 이미지만 출력하고 a는 CAM에서 나온 값을 사용한다는 의미)  
이것은 다음 두 가지 이유 때문에 번거롭다.  
(1) CAM이 classification score 점수의 출처를 찾는 데 사용되는 반면 AMGAN의 작업은 모든 손실의 조합으로부터 이익을 얻을 수 있는 속성 조작을 수행하는 것이다.   
(2) CAM은 때때로 조작할 속성이 전체 의류 항목(예: 색상)을 포함할 때 문제가 되는 작은 영역에 해당할 수 있다.  
우리는 CAM을 직접 "모방"하지 않고 AMGAN의 localization 능력에 기여하기 위해 attention loss를 사용한다.  
**Perceptual Loss.**  
다음과 같이 정의된 CNN의 feature 표현 간의 차이를 기반으로 하는 perceptual loss를 사용한다.  
![image](https://user-images.githubusercontent.com/40943064/129842295-4ef95b7d-ae78-447d-aa3f-38706dcd8dd4.png)  
여기서 j는 CNN의 j번째 레이어에서 추출된 특징을 나타낸다. unpaired i2i translation 작업에서 이 loss를 사용하면  
짝을 이루는 일치 없이 참조 이미지 외부 참조를 선택하는 방법이 불분명하기 때문에 혼동될 수 있다.  
AMGAN에서는 속성 조작 후 속성에 해당하는 이미지로 참조 이미지를 선택할 것을 제안한다.  
따라서 외부 참조를 선택하는 규칙은 그림 2에 제공된 예와 같이 모든 속성이 x^\*I와 일치해야 한다.  
착용자와 포즈가 다르더라도 x\*I 및 xref는 피쳐 공간에서 서로 가깝다.  
생성된 이미지 z의 품질을 향상시키면서 지각 손실도 주의 메커니즘에 기여할 수 있다.  
마지막으로 G를 최적화하는 목적 함수는 다음과 같이 공동으로 작성할 수 있습니다.
![image](https://user-images.githubusercontent.com/40943064/129842526-19aed6ee-076a-4272-bc1a-9864b65f514c.png)  
**Hyper-Parameters**  
![image](https://user-images.githubusercontent.com/40943064/129842549-06233897-0eca-4b17-96cb-45671b99b385.png)  

## 4. Region-specific Attribute Manipulation  
AMGAN이 특정 영역에 대한 속성 조작을 수행하는 능력은 segmentation ground truth를 사용하지 않기 때문에 제한적이다.  
이것은 사용자가 시간 집약적인 AMGAN의 attention mask를 수동으로 편집할 수 있게 함으로써 극복할 수 있다.  
이 과정을 자동화하기 위해 몸통, 소매 등 특정 영역에 대한 속성 조작을 가능하게 하는 방법을 제안한다.  
먼저 G를 이용하여 속성 조작을 수행한다. 예를 들어 사용자가 소매 또는 몸통 영역만 조작하려는 경우 그림 3과 같이 주의 마스크에 개입해야 한다.  
![image](https://user-images.githubusercontent.com/40943064/129847835-b677d723-fc79-4c92-9413-4838e7217224.png)  

영역별 주의 마스크를 생성하기 위해 "소매 없는" 속성 조작이 적용되어 강조 표시 α1로 표시된 슬리브 영역. α1을 직접 적용하기 전에  
임계값 함수를 사용하여 노이즈 값을 제거하기 위해 0.9보다 작은 픽셀 값을 제거한다.  
attention α\*1은 이제 다음과 같이 소매 또는 몸통 영역에서 "주황색" 속성 조작을 수행하는 데 적용할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/129842807-a8740152-9763-479a-8482-5a1da24d8cfc.png)  
이 방법은 attention mask가 속성조작과 관련되어 있음을 표시하는 데 사용할 수도 있다.  
이 방법의 더 많은 변형이 실험에서 조사된다.  

## 5. Implementation Details
**Network Architecture**  
AMGAN의 G에 대해 [39]와 유사한 구조를 사용하고 단일 채널 attention mask를 출력하는 sigmoid activation이 있는 Conv. layer를 추가한다.  
G 입력은 "3+N+M"(N:속성 값의 수, M:속성의 수) 차원의 텐서이다. [7]의 Masking 벡터를 사용하여 속성 간에 교대 훈련 전략을 수행한다.  
PatchGAN 아키텍처는 두개 D에 모두 사용된다. DC의 경우 입력 이미지의 크기가 절반으로 줄어들고 2개의 더 적은 컨볼루션 계층이 사용된다.  
CNN 아키텍처의 경우 ResNet-50을 사용하여 CAM 및 기능을 추출한다.  
각 데이터 세트에 대해 속성 예측을 위해 전이 학습(AMGAN 고정)이 수행된다.  
동일한 네트워크가 conv5 및 avg 풀 레이어를 사용하는 특징 추출에 사용된다.  
**Training**  
Adam(β = 0.5, β = 0.999, lr = 0.0001), mini_batch : 16  
G 업데이트에 대해 D는 5번 업데이트된다. DeepFashion 및 Shopping100k 데이터 세트의 경우 GeForce GTX TITAN X GPU로  
각각 약 1.5 및 2일이 소요되는 각 속성에 대해 80k 및 50k 반복에 대해 AMGAN을 훈련  
훈련의 전반부가 끝나면 학습률은 선형적으로 0으로 감소  

## 6. Experiments
이 섹션에서 AMGAN은 양적 및 정성적 실험을 사용하여 몇 가지 최근 방법과 비교된다.  
새로운 구성 요소의 효과를 조사하기 위해 ablation 실험을 수행한다.  
### 6.1. Competing Methods
다음 SOTA multi-domain i2i translation 방법들과 비교한다.  
#### StarGAN
단일 G로 입력 attribute에 대해 multi-domain i2i translation를 수행한다.
#### Ganimation
StarGAN과 유사하나 attention mechanism을 G에 포함한다.  
우리는 regression loss 대신 classification loss를 사용한다.  
#### SaGAN
역시 Attention mask를 사용하지만 2개의 G가 존재하여 이미지와 attention mask를 생성한다.  
우리는 multi-domain task를 위해 단일 모델에 대해 attribute manipulation을 condition으로 더하였다.  
### 6.2. Datasets
속성 수 측면에서 풍부한 두 가지 패션 데이터 세트가 실험에 사용한다.  
#### DeepFashion-Synthesis
78,979개의 이미지로 상의 이미지로 구성되어 있다. 이 하위 집합은 DeepFashion 데이터 세트의 훨씬 더 깨끗한 버전이며  
21개의 속성 값에 해당하는 color(17), sleeve(4) 속성을 사용하기로 선택했다.  
#### Shopping 100k  
101,021개의 의복 이미지가 포함되어 있으며 70개의 속성 값에 해당하는 칼라(17), 색상(19), 조임(9), 패턴(16), 소매 길이(9)의  
6가지 속성을 사용하도록 선택했습. 이 데이터 세트에 대해 λp = 10인 특징을 추출하기 위해 avg-pool 레이어만 사용한다.  
### 6.3. Evaluation Metrics
모든 이미지는 128x128로 크기가 조정되고 테스트 세트에 대해 2,000개의 이미지가 무작위로 샘플링되고 나머지는 훈련에 사용된다.  
두 데이터 세트의 속성 조작을 위해 대부분 합리적인 속성을 사용하도록 선택한다.  
참조 이미지를 선택할 때 더 정확한 일치를 위해 카테고리 및 성별 속성을 추가로 포함한다.  

#### Classification Accuracy. 
속성 조작이 성공적으로 적용되었는지 테스트하기 위해 조작 중인 속성에 대한 분류 정확도를 확인한다.  
cross-entropy loss가 있는 attribute manipulation를 위해 ResNet-50을 훈련하기로 선택했다.  
모든 경쟁 방법은 동일한 아키텍처로 테스트되었으며 정확도가 높을수록 네트워크에 따라 속성 조작이 더 성공적임을 나타낸다.  
#### Top-k Retrieval Accuracy. 
생성된 이미지의 성공 여부를 평가하기 위해 이미지 검색 기반 방법을 제안한다. Top-k 검색 정확도는 검색 알고리즘이 Top-k 결과에서  
올바른 이미지를 찾는지 여부를 고려한다. 검색된 이미지가 입력 및 속성 조작에서 요구하는 속성으로 구성된 경우 히트 "1"이 되고  
그렇지 않으면 "0"이 누락된다. 이 메트릭은 원하는 이미지를 직접 생성하므로 속성 조작에 적용할 수 있다.  
보다 구체적으로, ResNet-50 네트워크를 사용하여 생성된 이미지(Query)와 실제 이미지(Retrieval Gallery) 모두에 대해  
avg pool layer에서 특성을 추출하고 Query와 Retrieval Gallery를 비교한다.  
#### User Study.
각 경쟁 방법에서 생성된 이미지를 평가하기 위해 20명의 참가자로 구성된 사용자 연구를 수행한다.  
연구 전에 각 참가자는 각 속성 값에 대해 지시를 받는다. 입력 이미지와 속성 조작이 주어지면 참가자들은 4가지 경쟁 방법 중에서  
지각적 사실주의, 속성 조작의 품질 및 이미지의 원래 정체성 보존을 기반으로 가장 잘 생성된 이미지를 선택하도록 요청한다.  
### 6.4. Quantitative Experiments
속성 조작에 대한 분류 정확도 결과는 표 1에 있으며 AMGAN은 각 데이터 세트에 대해 각각 평균 79.48%, 49.49%로 최고의 성능을 달성했다.  
![image](https://user-images.githubusercontent.com/40943064/129847999-3a35d468-2c8b-4e7b-ba6a-4c12125621bc.png)  


세 경쟁 제품 모두 DeepFashion 데이터 세트에서 유사 성능을 보이지만 StarGAN은 Shopping100k 데이터 세트에서 훨씬 더 나은 성능을 가지고 있으며  
그 이유는 대부분 속성 수가 더 많기 때문이다(21 vs 70).  
이는 속성 수가 증가하고 attention mechanism이 있다고 해서 이 평가 메트릭에 추가 성공을 가져오지 않는 attention based 방법의 확장 문제를 지적한다.  
반면 AMGAN은 새로운 구성 요소로 인해 훨씬 더 안정적이다. AMGAN의 구성 요소에 대한 철저한 조사는 ablation 실험에서 이루어진다.  
그림 4에 따르면 AMGAN은 각 데이터 세트에 대해 각각 0.657 및 0.403의 평균 Top30 검색 정확도로 경쟁 모델보다 더 나은 성능을 보인다.  
![image](https://user-images.githubusercontent.com/40943064/129847866-8327111c-878b-4656-9db2-d1d16dfb4f93.png)  


또한 보다 자세한 조사를 위해 표 2에서 각 속성의 상위 30개 검색 정확도를 보고한다.  
![image](https://user-images.githubusercontent.com/40943064/129848034-e5e77b66-c3d3-4236-a546-fbd241de6116.png)  


AMGAN이 속성 조작에 탁월할 뿐만 아니라 변경되지 않은 속성을 동일하게 유지하는 데에도 탁월함을 보여준다.  
또한 속성 조작 없이 입력 이미지에서 특징을 추출한 실제 이미지의 결과를 보고한다.  
실제 이미지가 큰 차이로 최악의 결과를 얻었다는 사실은 속성 조작을 수행하는 능력이 이 메트릭에서 매우 중요하다는 것을 증명한다.  
Ganimation과 SaGAN은 두 평가 메트릭 간의 상관 관계를 보여주는 표 1의 경우인 Shopping100k 데이터 세트에 대해 StarGAN보다 성능이 좋지 않다.  
Top-k 검색 정확도는 생성된 이미지에 대해 "변경되지 않은 속성 유지"와 "속성 조작 활성화"의 균형을 관찰하기 위한 좋은 측정 기준이라고 믿는다.  
이러한 실험은 또한 AMGAN이 향후 연구를 위해 조사할 가치가 있는 이미지 검색을 위한 좋은 모델이 될 수 있음을 시사한다.  
표 3은 선호도에 기반한 사용자 연구의 결과를 보여준다. AMGAN은 다른 경쟁 방법이 두 데이터 세트에서 서로 유사하게 수행되는 모든 속성에 대해 다시 최고의 성능을 달성한다.  
![image](https://user-images.githubusercontent.com/40943064/129848068-531f6335-51e6-4a17-8479-db3c7722c086.png)  


Shopping100k 데이터 세트의 경우 StarGAN은 특히 좋은 성능을 보인 슬리브 속성에서 표 1에 표시된 것처럼 좋지 않다.  
사용자 연구는 분류 정확도가 높다고 해서 모델이 시각적으로 좋은 번역을 수행한다는 의미가 아님을 증명한다.  
Shopping100k 데이터 세트에서 흥미로운 사실은 StarGAN이 특정 영역(칼라, 고정, 소매)에 해당하는 이미지에 비해  
전체 이미지(색상, 패턴)를 포함하는 속성 조작을 수행하는 능력이 더 우수하다는 것이다.  
사용자 연구에 따르면 AMGAN의 주의 메커니즘은 Ganimation 및 SaGAN보다 안정적이며 보다 사실적인 번역을 수행한다.  
고정 속성의 경우 AMGAN은 이 속성 조작이 다른 것보다 더 어렵다는 것을 나타내는 약간 낮은 점수를 받았다.  
#### Ablation Experiments.
Dc, perceptual loss, attention loss, CAM as a에 따른 ablation study를 수행한다.  
#### AMGAN w/o Dc
5.43%, 6.34% drop이 있으며 현실적 이미지를 생성하는데 Attended 영역에 대한 정확한 속성을 주어 도움을 준다.  
#### AMGAN w/o L_p^G, Dc
above + 4.21%, 7.68% drop이 있으며 attribute manipulation에 큰 영향을 줌을 알 수 있다.
#### AMGAN w/o L_a^G, L_p^G, Dc
above + 2.50%, 9.97% drop이 있으며 CAM의 보조가 없어 G에 올바른 영역에 대한 localizing을 주지 못하며 m이 큰 데이터에 영향이 크다.  
새로운 방법 없이 기존 방법론과 결과는 유사하다.  
#### AMGAN, CAM as a
attention mask 출력값 대신 CAM을 넣었다. 비교를 위해 Dc와 perceptual loss를 학습에서 제외하였다.  
CAM을 직접 넣은경우 제안 방법보다 6.97%, 9.34% drop이 있었다.  
즉, 직접적으로 CAM을 사용하기 보다 학습에 사용하는것이 도움이 된다는 사실을 증명한다.  
Attention loss의 목표는 CAM을 복사하는것이 아니라 AMGAN의 localization 능력을 부여하는것이다.  
### 6.5. Qualitative Evaluation
여러 속성 조작의 예를 보여주는 그림 5에서 AMGAN이 속성 조작을 수행하고 원본 이미지의 내용을 유지하는 측면에서 적절한 번역을 수행한다는 것이 분명하다.  
DeepFashion 데이터 세트의 경우 색상 속성 조작을 적용하는 경쟁 방법이 올바른 영역에 초점을 맞추는 데 문제가 있음이 분명하다.  
DNN의 "extra help"를 통해 AMGAN은 보다 정확한 attention mask를 생성하여 보다 사실적인 번역을 제공할 수 있다.  
sleeve 속성을 보면 모든 메소드가 올바른 영역에 번역을 적용하는 것처럼 보인다. 그러나 AMGAN은 생성된 슬리브 영역이 색상 및 패턴 유사성 측면에서  
입력 이미지와 더 상관 관계가 있으므로 보다 사실적으로 수행할 수 있다. Shopping100k 데이터 세트의 경우 그림 5의 오른쪽에 몇 가지 예가 제공된다.  
![image](https://user-images.githubusercontent.com/40943064/129847903-07736118-f417-46d7-87bf-63c07dbe1545.png)

AMGAN에 의한 속성 조작 결과는 다시 더 일관되고 정확하다. 이는 경쟁 방법이 원하는 속성의 실루엣만 제공하는 세 번째 행의 긴팔 속성 조작에서 쉽게 알 수 있다.  
보다 정확하고 사실적인 번역을 수행하는 AMGAN의 능력은 대부분 속성 특정 영역에 참석하기 위해 추가 판별기를 사용하고  
예상 출력에 대해 G를 안내하는 지각 손실에 기인한다.
#### Region-specific Attribute Manipulation:
두 데이터 세트의 예 세트가 그림 6에 제공된다.  
![image](https://user-images.githubusercontent.com/40943064/129847928-b6c1ae23-a1b4-4e5e-8672-bdad91fdf62b.png)  

DeepFashion : "sleeveless" 속성에서 얻은 attention mask를 사용하여 지역별 속성 조작을 수행한다.  
그런 다음 Eq12를 사용하여 소매 마스크에 "빨간색" 및 "주황색" 속성 조작을 수행한다.  
Shopping100k : occlusion으로 인해 의류 제품에 대한 localize가 더 어렵다. 또한, 우리는 hard threshold 방법을 사용하고 있기 때문에  
최적의 값을 찾는 것이 때때로 문제가 될 수 있다. 그럼에도 불구하고 속성 조작은 처음 두 행에 성공적으로 적용된다.  
마지막 두 행의 경우 이 프로세스에 대한 속성만 사용한다는 사실을 감안할 때 괜찮은 결과를 얻는다.  
"sleeveless" 속성 값에서 얻은 attention mask가 소매 영역을 성공적으로 강조 표시할 수 있음을 알 수 있다.  
그런 다음 "파란색" 및 "색 그라데이션 패턴" 속성 조작을 수행한니다. 최종 출력을 보면 마스크 개입의 아이디어가  
지역별 속성 조작 작업에 성공적으로 적용되었다. 이 실험은 또한 G에 의해 생성된 attention mask의 성공을 보여준다.  

## 7. Conclusion
Multi-domain i2i translation을 위한 AMGAN은 향상된 attention mechanism과 속성조절으로 인해 경쟁 방법보다 큰 성능 이점이 있다.  
성능 향상은 CAM 및 perceptual loss의 guide와 추가 D를 통해 가능하다. AMGAN은 attention mask를 활용하여  
특정 영역에 대한 속성 조작을 수행할 수 있다. DeepFashion 및 Shopping100k 데이터 세트에 대해 수행된 실험을 통해  
AMGAN이 이미지 검색을 기반으로 하는 새로운 방법뿐만 아니라 기존 메트릭기반 최신 i2i 변환 방법보다 나은 성능을 발휘할 수 있다.  
향후에는 과제는 AMGAN을 다른 도메인으로 확장하거나 속성 조작 작업 후 이미지 검색을 위한 도구로 사용하는 것이다.
