# SimSwap: An Efficient Framework For High Fidelity Face Swapping

## Abstract
일반화된 고성능의 face swapping을 목적으로 하는 효율적 framework를 제안  
임의 ID를 일반화하는 능력이 부족하거나 표정/시선등의 특성들을 보존하지 못하는 과거 연구결과와 달리  
임의의 source face의 **ID**를 전달하면서 target face의 attribute를 보존할 수 있다.  
다음의 두가지 방법으로 문제를 해결한다.  
  
1) ID Injection Module (IIM) : feature level의 source ID 정보를 target으로 전송  
- 특정 ID 한정으로 학습되는 방식을 임의 ID 적용 방식으로 확장할 수 있다.  

2) Weak Feature Matching Loss : Implicit하게 target attribute 보존  
  
여러 wild face set에 대한 다양한 실험은 SOTA 대비 attribute 보존/ID 적용 성능의 경쟁력을 보여준다.  
![image](https://user-images.githubusercontent.com/40943064/143544606-8516eb6f-982c-402c-9f6e-f631a53ea930.png)  
  
## Introduction
Face swapping은 target attribute(표정, 자세, 조명)는 보존하면서 source ID를 전달하는 유망한 기술이다.  
이 기술은 존재하지 않는 twin을 생성하는 영화산업에서 광범위하게 사용된다.  
산업에서의 face swapping 방식은 배우의 얼굴모델을 재현하기 위한 최신 장비를 이용하고  
대부분의 사람이 접근할 수 없는 장면의 조명조건을 재구성한다.  
최근, 최신 장비 없이 face swapping을 수행하는 방식은 연구자들의 관심을 끌어왔다.  

face swapping에서 고려되는 주요 어려움들은 다음과 같다.  
1) 강력한 일반화 능력을 가진 face swap 프레임워크를 임의의 페이스에 맞게 조정해야 한다.  
2) 결과 face의 ID는 source의 것과 가까워야 한다.  
3) 결과 face의 attribute(표정, 자세, 조명)는 target의 것과 가까워야 한다.  

swapping 방법은 주로 두가지로 나뉜다.  
1) Source-oriented : image level로 source에서 작업  
target에서 source로 attribute(표정/자세)를 전달하고 source를 target에 섞는다.  
Source의 자세와 조명에 영향을 크게 받고 target의 표정을 정확하게 재생성할 수 없다.  

2) Target-oriented : feature level로 target에서 작업  
Target의 feature를 수정하고 source의 변화에 잘 적응 할 수 있다.  
  
open-source 알고리즘은 두 특정 ID 사이에서의 face swapping을 생성할 수 있지만 일반화는 부족하다.  
GAN 기반의 작업은 source의 ID와 target의 attribute를 feature 수준에서 결합하고 임의의 ID에 대해 확장된다.  
최근 작접은 2단계의 framework를 활용하며 고품질 결과를 달성한다.  
그러나 이 방법론들은 ID 수정에 과도하게 집중한다.  
또한 attribute 보존에 약한 제약을 가하고 종종 표정이나 포즈의 불일치에 직면한다.  
일반화 및 속성 보존의 결함을 극복하기 위해 SimSwap이라는 효율적인 페이스 스왑 프레임워크를 제안한다.  
ID별 얼굴 교환 알고리즘의 아키텍처를 분석하고, Decoder가 하나의 특정 ID에만 적용될 수 있도록 ID를 디코더에 통합함으로써  
일반화 부족이 발생한다는 것을 알아냈다.  

이러한 통합을 방지하기 위해 ID 주입 모듈을 제시한다.  
우리 모듈은 source의 ID를 내장하여 target의 attribute를 수정하므로, ID와 decoder의 weight 사이의 관련성을 제거하고  
임의 ID에 아키텍처를 적용할 수 있다.  
또한 ID와 attribute 정보는 feature 수준에서 크게 결합되어 있다.  
전체 feature를 직접 수정하면 attribute 성능이 저하되므로 영향을 완화하기 위해 training loss를 사용해야 한다.  
target의 attribute를 match하기 위해 결과 이미지의 attribute를 각각 명시적으로 제한하는 대신 Weak Feature Matching Loss를 제안한다.  
Weak Feature Matching Loss는 생성된 결과를 high semantic level에서 입력 대상에 정렬하고 아키텍처가 대상의 속성을 보존하는 데 암시적으로 도움이 된다.  
이 loss를 통해 SimSwap은 이전의 SOTA보다 나은 attribute 보존 기술을 보유하면서 경쟁력 있는 IT 성능을 달성할 수 있다.  

## 2 Related Work

Face Swapping은 오랫동안 연구되어 왔다.
방법은 크게 이미지 level에서 source에서 작동하는 source 지향 방법과 feature level에서 target 페이스에서 작동하는 target 지향 방법의 두 가지로 나눌 수 있다.

**Source-oriented Methods.**  
Attribute를 target에서 source로 전송한 다음 source를 target 이미지로 혼합한다.  
초기 방법은 3D 모델을 사용하여 자세와 조명을 전송했지만 수동 작업이 필요했다.  
자동 방법이 제안되었지만 특정 얼굴 라이브러리의 ID만 얼굴을 교환할 수 있었다.  
니르킨은 3D 얼굴 데이터 세트를 사용하여 표정과 자세를 전송한 다음 포아송 블렌딩을 사용하여 source 얼굴을 target 이미지에 병합했다.
그러나 3D 얼굴 데이터 세트의 표현력이 제한적이기 때문에 3D 모델에 응답하는 방법은 표정을 정확하게 재현하지 못하는 경우가 많다.
최근 FSGAN은 face reenactment network로 표정 및 자세 전송을 먼저 수행한 다음  
다른 face inpainting network를 사용하여 source 얼굴을 target 이미지에 혼합하는 2단계 아키텍처를 제안했다.  
source 지향 방법의 일반적인 문제는 입력 source 이미지에 민감하다는 것이다.
source의 과장된 표정이나 큰 자세는 페이스 swapping 결과의 성능에 강한 영향을 미친다.

**Target-oriented Methods.**  
NN을 사용하여 target의 feature를 추출한 다음 feature를 수정하고 feature를 출력 face swap 이미지로 복원한다.  
코르수노바은 G를 학습시키고 하나의 특정 ID으로 얼굴을 교환할 수 있었다.  
유명한 알고리즘 DeepFakes는 encoder-decoder 구조를 활용했다.  
일단 학습하면 두 개의 특정 ID 사이에서 얼굴을 교환할 수 있었지만 일반화 능력은 부족했다.  
다른 방법은 source 얼굴영역과 target 얼굴 외 영역의 latent representation을 결합하여 결과를 산출했지만  
target의 표현을 유지하지는 못했다.  
IPGAN는 source 이미지에서 identity 벡터를 추출하고 target 이미지에서 attribute 벡터를 추출한 후 decoder로 전송한다.  
생성된 출력은 source의 ID 전달에는 좋았지만 target 페이스의 표정이나 자세를 유지하지 못하는 경우가 많았다.
최근에 제안된 FaceShifter 방법은 높은 충실도의 페이스 swap 결과를 생성할 수 있었다.
FaceShifter는 정교한 2단계 프레임워크를 활용하여 최첨단 신원 성능을 달성했다.
그러나 이전 방법과 마찬가지로 FaceShifter는 attribute에 너무 약한 제약을 가하여 결과가 종종 표정 불일치로 어려움을 겪었다.  

## 3 Method

Source와 target이 주어지면, target 얼굴의 속성을 변경하지 않고 source ID를 target으로 전송하는 프레임워크를 제시한다.  
프레임워크는 ID별 face swap 아키텍처에서 확장되며 임의의 ID에 맞게 조정될 수 있다.  
먼저 원본 아키텍처의 한계에 대해 논의한다(Sec 3.1).  
임의의 ID를 위한 프레임워크로 확장하는 방법을 보여준다(Sec 3.2).  
그런 다음 target의 attribute를 보존하는 데 도움이 되는 Weak Feature Matching Loss를 제시한다(Sec 3.3).  
마지막으로 loss function을 제공한다(Sec 3.4).  

### 3.1 Limitation of the DeepFakes
DeepFakes의 구조는 2개 파트(일반 Encoder Enc, 2개의 ID 특정 Decoder Decs, EncT)로 구성되어있다.  
학습 단계에서 𝐸𝑛𝑐-𝐷𝑒𝑐𝑆 아키텍처는 왜곡된 소스 이미지를 가져와 원래의 왜곡되지 않은 소스 이미지로 복원한다.  
동일 과정이 target에 대해서도 𝐸𝑛𝑐-𝐷𝑒𝑐𝑇 구조에 대해 적용된다.  
테스트 단계에서 target은 𝐸𝑛𝑐-𝐷𝑒𝑐𝑆에 넘겨질 것이다.  
이 구조는 왜곡된 소스 이미지로 오인하여 소스의 정체성과 대상의 속성을 가진 이미지를 생성할 것이다.  
이러한 과정동안, Enc는 target의 ID, attribute 정보를 포함하는 feature를 추출한다.  
디코더 𝐷𝑒𝑐𝑆 가 target의 feature를 source의 ID가 있는 이미지로 변환하므로 source의 ID 정보가 𝐷𝑒𝑐𝑆 의 weight에 통합되어야 한다.  
그러므로 Deepface의 Decoder는 특정 ID에만 적용될 수 있다.  


### 3.2 Generalization to Arbitrary Identity
이러한 한계를 극복하기 위해 Decoder에서 ID를 분리하여 전체 아키텍처를 임의의 ID으로 일반화할 수 있는 방법을 찾는다.  
인코더와 디코더 사이에 추가 ID 주입 모듈을 추가하여 아키텍처를 개선한다.  
프레임워크는 그림 2에 나와 있다.  
![image](https://user-images.githubusercontent.com/40943064/146665904-cb10cfd4-91d3-4c6f-a7a1-357b10a48739.png)  
  
Target 𝐼𝑇 가 주어지면 인코더를 통해 전달하여 특징 𝐹𝑒𝑎𝑇 을 추출한다.  
Target 얼굴을 원본 얼굴로 바꾸는 것이므로 𝐹𝑒𝑎𝑇의 attribute를 변경하지 않고 유지하면서 𝐹𝑒𝑎𝑇의 ID를 원본 얼굴의 ID로 교체해야 한다.  
그러나 𝐹𝑒𝑎𝑇의 ID와 attribute은 매우 결합되어 구별하기 어렵다.  
그래서 우리는 𝐹𝑒𝑎𝑇 전체에 대해 직접 수정을 수행하고 학습 손실을 사용하여 네트워크가 𝐹𝑒𝑎𝑇의 어느 부분을 변경해야 하고  
어떤 부분을 보존해야 하는지 암묵적으로 학습하도록 권장한다.  
ID 주입 모듈은 𝐹𝑒𝑎𝑇의 ID를 원본 얼굴의 ID로 변경하는 작업을 한다.  
모듈은 ID 추출 부분과 임베딩 부분의 두 부분으로 구성된다.  
ID 추출 부분에서는 source 얼굴의 ID 및 attribute를 모두 포함하는 입력 source 이미지 𝐼𝑆를 처리한다.  
전자만 필요하므로 얼굴 인식 네트워크를 사용하여 𝐼𝑆 에서 식별 벡터 𝑣𝑆를 추출한다.  
임베딩 부분에서는 ID 블록을 사용하여 기능에 ID를 삽입한다.  
우리의 ID-Block은 Residual Block의 수정된 버전이며 원래 Batch Normalization을 대체하기 위해 AdaIN을 사용하고 있다.  
우리 작업에서 AdaIN의 공식은 다음과 같이 작성할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/146665925-61673027-db47-4fc7-83d4-162910b81487.png)  

여기서 𝜇(𝐹𝑒𝑎) 및 𝜎(𝐹𝑒𝑎)는 입력 특성 𝐹𝑒𝑎의 채널별 평균 및 표준편차이다.  
𝜎𝑆 및 𝜇𝑆는 완전 연결 계층을 사용하여 𝑣𝑆에서 생성된 두 개의 변수이다.  
충분한 ID 임베딩을 보장하기 위해 총 9개의 ID 블록을 사용한다.  
ID 정보를 주입한 후 Decoder를 통해 수정된 기능을 전달하여 최종 결과 𝐼𝑅를 생성한다.  
다른 ID의 source 이미지가 훈련에 포함되므로 디코더의 가중치는 특정 ID와 관련이 없어야 한다.  
디코더는 기능에서 이미지를 복원하는 데만 집중하고 ID 수정 임무는 ID 주입 모듈에 맡기므로 아키텍처를 임의의 ID에 적용할 수 있다.  
학습 과정에서 생성된 결과 𝐼𝑅에서 항등 벡터 𝑣𝑅를 추출하고 항등 손실을 사용하여 𝑣𝑅 과 𝑣𝑆 사이의 거리를 최소화한다.  
그러나 ID 손실을 최소화하면 네트워크가 과적합되어 source의 ID가 있는 전면 이미지만 생성되고 target의 모든 속성은 손실될 수 있다.  
이러한 현상을 피하기 위해 우리는 adversarial training[10, 16, 21, 28]이라는 개념을 활용하고 Discriminator를 사용하여 명백한 오류가 있는 결과를 구별한다.  
Adversarial Loss는 또한 생성된 결과의 품질을 향상시키는 데 중요한 역할을 한다.  
우리는 D의 patchGAN 버전을 사용한다.  



### 3.3 Preserving the Attributes of the Target

Face swapping 작업에서 수정은 ID만 수행되어야 하며 target attribute(예: 표정, 자세, 조명 등)은 유지되어야 한다.  
하지만 target ID와 attribute 정보를 모두 포함하는 𝐹𝑒𝑎𝑇 전체에 대해 직접 수정을 진행하고 있기 때문에  
attribute 정보는 ID 임베딩에 영향을 받을 가능성이 높다.  
Attribute 불일치를 방지하기 위해 학습 loss를 사용하여 제한한다.  
그러나 모든 attribute을 명시적으로 제한하기로 선택한 경우 각 attribute에 대해 하나의 네트워크를 학습해야 한다.  
Attribute이 너무 많이 고려되어야 하므로 전체 프로세스는 비실용적이어야 한다.  
그래서 암시적 방식으로 제약을 수행하기 위해 Weak Feature Matching Loss를 제안한다.  
Feature Matching의 아이디어는 D를 사용하여 GT 이미지와 생성된 출력에서  feature의 여러 레이어를 추출하는 pix2pixHD에서 시작되었다.  
원래 Feature Matching Loss는 다음과 같이 작성된다.  
  
𝐿𝑜𝐹𝑀 (𝐷) = ∑︁ 𝑀 𝑖=1 1 𝑁𝑖 ∥𝐷 (𝑖) (𝐼𝑅) − 𝐷 (𝑖) (2)  
  
여기서 𝐷(𝑖)는 𝐷의 𝑖번째 레이어 feature 추출기를 나타내고 𝑁𝑖는 𝑖번째 레이어의 요소 수를 나타낸다.  
𝑀는 총 레이어 수이다.  
𝐼𝑅은 생성된 출력이고 𝐼𝐺𝑇은 해당 GT 이미지이다.  
아키텍처에서는 얼굴 교체 작업에 GT가 없기 때문에 입력 target 𝐼𝑇를 사용하여 위치를 대체한다.  
처음 몇 개의 레이어를 제거하고 마지막 몇 개의 레이어만 사용하여 Weak Feature Matching Loss를 계산한다.  
이는 다음과 같이 작성할 수 있다.  
  
𝐿𝑤𝐹𝑀 (𝐷) = ∑︁ 𝑀 𝑖=𝑚 1 𝑁𝑖 ∥𝐷 (𝑖) (𝐼𝑅) − 𝐷 (𝑖) (𝐼) (𝑖) (3)  
  
여기 𝑚는 Weak Feature Matching Loss를 계산하기 시작하는 레이어이다.  
원래 Feature Matching Loss와 Weak Feature Matching Loss는 유사한 공식을 공유하지만 목적이 완전히 다르다.  
학습을 안정화하기 위해 원래의 Feature Matching Loss가 제안되었으며 여러 수준에서 자연 통계를 생성하려면 G가 필요한다.
얕은 레이어의 feature는 주로 텍스처 정보를 포함하고 픽셀 수준에서 결과를 제한할 수 있기 때문에 핵심 역할을 한다.  
그러나 face swapping 작업에서 입력 target 이미지에서 너무 많은 텍스처 정보를 도입하면 target 얼굴과 유사한 결과가 만들어지고  
ID 수정이 어려워 원래 기능 일치 용어에서 처음 몇 개의 레이어를 제거한다.  
목표는 attribute 성능을 제한하는 것이다.  
Attribute는 주로 깊은 feature에 있는 높은 의미 정보이므로 깊은 수준에서 결과 이미지를 입력 target과 정렬해야 하며  
Weak Feature Matching Loss는 D의 마지막 몇 레이어만 사용하여 Feature Matching term을 계산한다.  
이러한 손실 함수를 사용하면 특정 attribute에 대해 네트워크를 명시적으로 제한하지 않더라도  
입력 target 얼굴의 attribute을 유지하는 방법을 암시적으로 학습한다.  

### 3.4 Overall Loss Function
Loss 함수는 아래 5가지 구성요소를 가지고 있다.  
1) Identity Loss
2) Reconstruction Loss
3) Adversarial Loss
4) Gradient Penalty
5) Weak Feature Matching Loss

**Identity Loss**  
𝑣𝑅 과 𝑣𝑆 사이의 거리를 제한하는 데 사용된다.  
거리를 계산하기 위해 cosine similarity를 사용하고 있으며 다음과 같이 쓸 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/146666163-8e7a678c-b07d-4876-b856-dcd3f4048674.png)  
  
**Reconstruction Loss**   
Source face와 target face가 동일한 ID에서 나온 경우 생성된 결과는 target face와 같아야 한다.  
Reconstruction Loss를 다음과 같이 쓸 수 있는 정규화항으로 사용한다.  
![image](https://user-images.githubusercontent.com/40943064/146666187-0b403dd6-0e87-4a27-b2e3-adb5dec32687.png)  
(Source와 target이 서로 다른 ID에서 온 경우 이 항을 0으로 설정한다.)  
  
**Adversarial Loss and Gradient Penalty**  
Adversarial Loss의 힌지 버전을 사용한다.  
큰 자세에서 더 나은 성능을 위해 다중 스케일 Discriminator를 사용한다.  
또한 Gradient Penalty 항을 사용하여 D가 gradient explosion을 방지한다.  
  
**Weak Feature Matching Loss**  
다중 스케일 판별기를 사용하기 때문에 Weak Feature Matching Loss는 다음과 같이 쓸 수 있는 모든 D를 사용하여 계산해야 한다.  
![image](https://user-images.githubusercontent.com/40943064/146666246-e0a39635-ea04-418e-b6aa-14d41f60fdb9.png)  

전체 손실은 다음과 같이 쓸 수 있다.
λ𝐼𝑑*𝐿𝐼𝑑 + λ𝑅𝑒𝑐𝑜𝑛*𝐿𝑅𝑒𝑐𝑜𝑛 + 𝐿𝐴𝑑𝑣 + λ𝐺𝑃*𝐿𝐺𝑃 + λ𝑤𝐹𝑀𝐿𝑤𝐹𝑀𝑠𝑢𝑚 (7)  
(λ𝐼𝑑 = 10, 10 = λ𝑅𝑒𝑐𝑜𝑛, λ𝐺𝑃 = 10-5, λ𝑤𝐹𝑀 = 10)  
  
## 4 Experiments
**Implementation Detail**  
임의 ID에 대한 face swapping이므로 대량 얼굴 데이터 세트 VGGFace2를 사용한다.  
학습 세트의 품질을 개선하기 위해 250 × 250보다 작은 크기의 이미지를 제거한다.  
이미지를 224 × 224 크기의 표준 위치에 정렬하고 자른다.  
ID 주입 모듈의 얼굴 인식 모델은에서 사전 학습된 Arcface를 사용한다.  
𝛽1 = 0 및 𝛽2 = 0.999인 Adam optimizer를 사용하여 네트워크를 학습한다.  
동일한 ID를 가진 이미지 쌍에 대해 하나의 배치를 훈련하고 다른 ID를 가진 이미지 쌍에 대해 다른 배치를 교대로 학습한다.  
500 이상의 Epoch 학습을 수행한다.  
  
### 4.1 Qualitative Face Swapping Results
결과를 보여주기 위해 face matrix를 제시한다.  
영화 장면에서 8개의 얼굴 이미지를 target 이미지로 선택한다.  
인터넷에서 10개의 얼굴 이미지를 source 이미지로 다운로드한다.  
원본 이미지는 ID 벡터만 사용하기 때문에 정면 자세나 중립적인 표정이 필요하지 않다.  
이 모든 이미지는 학습 세트에서 제외된다.  
모든 source 및 target 쌍에 대해 face swapping을 수행한다.  
그림 3과 같이 SimSwap은 target의 attribute(표정, 시선 방향, 자세 및 조명 조건 등)을 유지하면서  
source 얼굴의 ID를 target 얼굴로 전송할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/146669032-9a70271f-bf77-4975-a58c-e4fb63a88eb1.png)  
  
방법은 다양한 ID를 잘 처리할 수 있다.  
과장된 표현(행 4), 얼굴 줄무늬(행 4), 큰 얼굴 회전(행 7)과 같은 어려운 대상 조건이 주어지더라도  
SimSwap은 여전히 높은 충실도의 face swapping 결과를 생성한다.  

### 4.2 Comparison with Other Methods
최근 몇 년 동안 많은 얼굴 교환 방법이 제안되었다.  
소스 지향 방법 FSGAN과 대상 지향 방법 DeepFakes, FaceShfiter를 포함하여 세 가지를 선택한다.  
이러한 방법과 SimSwap 간의 비교를 보여준다.  

**FaceForensics++에서의 비교**  
FaceForensics++는 인터넷에서 다운로드한 1,000개의 얼굴 동영상과  
DeepFakes에서 생성한 1,000개의 face swap 동영상이 포함되어 있다.  
FaceForensics++에서 SimSwap을 DeepFakes 및 FaceShifter와 비교한다.  
FaceShifter는 코드를 공개하지 않기 때문에 공정한 비교를 위해 paper에서 이미지를 직접 자른다.  
그림 4에서 볼 수 있듯이 DeepFakes의 결과는 심각한 조명과 자세 불일치로 어려움을 겪는다.  
![image](https://user-images.githubusercontent.com/40943064/146669041-a659c23d-1900-45b4-a354-697a9d49c5f4.png)  
  
FaceShifter는 적절한 face swapping 결과를 생성하지만 결과 얼굴의 표정과 시선 방향은  
대상 얼굴의 표정과 시선 방향을 완전히 존중하지 않는다.  
SimSwap은 attribute 보존에서 더 나은 성능을 달성하면서 그럴듯한 face swapping 결과를 생성한다.  
  
**FaceShifter와의 추가 비교**  
더 많은 결과를 그림 5에서 FaceShifter와 비교한다.  
우리가 볼 수 있듯이 FaceShifter는 강력한 ID 수정 기능을 나타내며  
결과의 얼굴 모양을 원본 얼굴의 얼굴 모양으로 변경할 수 있다.  
하지만 ID 부분에 너무 치중해 표정이나 시선 방향과 같은 속성을 유지하지 못하는 경우가 많다.  
그림 5 행 2에서 대상 얼굴이 눈을 가늘게 하고 있다.  
SimSwap은 FaceShifter가 실패하는 동안 이러한 미묘한 표현을 재현하는 결과를 생성할 수 있다.  
또한 FaceShifter가 두 번째 네트워크를 사용하여 얼굴 교체 결과를 배경과 결합하지만  
여전히 FaceShifter보다 약간 더 나은 조명 조건(3&4행)을 생성한다.  
![image](https://user-images.githubusercontent.com/40943064/146669045-258ff2ee-e8de-4348-a5bd-f652b75adb9d.png)  


**FSGAN과의 비교**  
그림 6에서 FSGAN과 비교한다.  
![image](https://user-images.githubusercontent.com/40943064/146669053-7b11f78f-631c-41bf-9e58-852a63484687.png)  
  
FSGAN의 결과는 대상 얼굴의 표정(row 1), 시선 방향(row 1&4)을 재현하지 못했으며  
결과와 대상 이미지 사이의 조명 조건에 명백한 차이가 있다.  
SimSwap은 속성 보존에서 더 나은 성능을 달성한다.  
또한 FSGAN은 입력 소스 이미지에 매우 민감하다.  
행 2에서 볼 수 있듯이 대상 얼굴은 깨끗한 눈 영역을 갖지만 FSGAN은 원본 얼굴의 그림자를 가져온다.  
코 주변의 4열에서도 비슷한 문제가 발생한다.  
SimSwap은 입력 소스 이미지에 대해 훨씬 더 강력하고 더 설득력 있는 결과를 생성한다.  


### 4.3 Analysis of SimSwap
ID 수정 능력에 대한 분석을 제공할 것이다.  
그런 다음 face swapping 작업에서 ID와 attribute 성능 사이의 균형을 유지하는 방법을 보여주기 위해  
몇 가지 ablation 테스트를 수행한다.  

**효율적인 ID 임베딩**  
SimSwap의 아키텍처는 ID 삽입 모듈을 사용하여 ID 임베딩을 수행하므로  
Decoder의 가중치에서 ID 정보를 분리하고 아키텍처를 임의의 ID로 일반화할 수 있다.  
아키텍처 효율성을 검증하기 위해 타 연구에서 제안한 기준을 사용하여  
FaceForensics++ 에 대해 동일한 quantitative 실험을 수행한다.  
FaceForensics++의 각 얼굴 비디오에서 무작위로 10개의 프레임을 선택한다.  
FaceForensics++에서 동일한 source 및 target 쌍을 따라 SimSwap을 사용하여 face swapping을 수행한다.  
생성된 프레임과 원본 프레임의 id 벡터를 추출하기 위해 다른 얼굴 인식 네트워크를 사용한다.  
생성된 각 프레임에 대해 원본 프레임에서 가장 가까운 얼굴을 검색하고 해당 얼굴이 올바른 소스 비디오에서 나온 것인지 확인한다.  
정확도 비율은 ID 검색이라고 하며 메서드의 ID 성능을 나타내는 역할을 한다.  
또한 포즈 추정기를 사용하여 생성된 프레임과 원본 프레임의 자세를 추정하고 평균 L2 거리를 계산한다.  
유효한 재현을 찾을 수 없기 때문에 표정 부분을 무시한다.  

추가 비교를 위해 원래 Feature Matching formula를 사용하는 SimSwap-oFM과 Feature Matching term을  
사용하지 않는 SimSwap-nFM이라는 또 다른 2개의 네트워크를 훈련한다.  
우리는 이 2개의 네트워크에 대해 동일한 양적 실험을 수행한다.  
DeepFakes에서 생성된 프레임도 테스트한다.  
비교 결과를 표 1에 나타내었다.  
우리가 볼 수 있듯이 SimSwap-oFM은 얕은 수준에서 결과를 정렬하기 때문에 낮은 세트 ID 검색이 있다.  
한편 SimSwap-nFM은 모든 수준에서 제약을 제거함으로써 Faceshifter와 매우 유사한 정체성 성능을 갖는다.  
SimSwap은 정체성이 약간 뒤처져 있지만 비교적 좋은 자세 성능을 보인다.  
그림 4 및 5의 결과와 결합하여 SimSwap은 FaceShifter보다 약간 약한 ID 성능을 나타내지만 더 나은 속성 보존 능력을 가지고 있다.  

**Keeping a Balance between Identity and Attribute**  
IIM은 target 이미지에서 추출한 𝐹𝑒𝑎𝑇 전체 feature에 대해 직접 작업하기 때문에  
ID의 삽입은 필연적으로 attribute 보존 성능에 영향을 미친다.  
따라서 ID 수정과 attribute 보존 사이의 균형을 찾아야 한다.  
우리의 프레임워크에는 ID와 attribute 사이의 균형을 조정하는 두 가지 방법이 있다.  
첫 번째는 더 강력한 수정 기술을 장려하기 위해 𝜆𝐼𝑑에 대해 더 높은 가중치를 명시적으로 설정하는 것이다.  
두 번째는 feature matching term에서 더 많거나 적은 feature를 선택하는 것이다.  
이 두 가지 접근 방식을 조합하면 광범위한 결과를 얻을 수 있다.  
  
SimSwap-oFM 및 SimSwap-nFM 외에도 SimSwap-𝑤𝐹𝑀, SimSwap-oFM-FM-, SimSwap-oFMid+ 및 SimSwap-wFM-id+라는  
다른 4개의 네트워크를 학습한다.  
𝑤𝐹𝑀 : Feature Matching term + 초반 몇 개의 레이어를 유지하고 마지막 몇 개를 제거  
oFM-FM- : Feature Matching term +  𝜆𝑜𝐹𝑀 = 5  
oFM-id+ : Feature Matching term + 𝜆𝐼𝑑 = 20  
wFM-id+ :Weak Feature Matching Loss를 SimSwap으로 사용 + 𝜆𝐼𝑑 = 20  
SimSwap과 동일한 전략에 따라 위의 모든 네트워크를 학습한다.  
모든 네트워크의 ID 검색을 테스트한다.  
CelebAMaskHQ에 대한 추가 정량 실험을 수행한다.  
먼저, 서로 다른 ID를 가진 1,000개의 source 및 target 쌍을 무작위로 선택하고 face swapping 결과를 생성한다.  
ID 수정 기술을 측정하기 위해 결과와 source 간의 평균 ID loss를 사용한다.  
그런 다음 무작위로 1,000개의 이미지를 선택하고 각 이미지를 source와 target으로 사용하여 자체 교체를 수행한다.  
우리는 평균 Reconstruction Loss를 사용하여 face swapping 프로세스 동안 target에서 손실된 attribute 정보의 양을 측정한다.  
비교 결과는 그림 7에 나와 있다.  
![image](https://user-images.githubusercontent.com/40943064/146669418-6228fd56-135c-4d1e-9109-276bd6fcd1cb.png)  
우리가 볼 수 있듯이 oFM, 𝑤𝐹𝑀, oFM-FM- 및 oFM-id+는 모두 SimSwap보다 ID 검색이 낮다.  
이는 Feature Matching에서 마지막 몇 개의 레이어를 유지하는 것이 ID 성능에 미치는 영향이 적다는 것을 나타낸다.  
nFM은 ID 검색이 가장 높지만 Reconstruction Loss가 가장 높아 수정 능력이 강하면 attribute 보존에 어려움이 있음을 알 수 있다.  
SimSwap은 ID와 attribute 성능 사이의 균형을 잘 유지하는 중간 수준의 재구성 손실을 유지하면서 비교적 높은 ID 검색을 달성하고 있다.  
Weak Feature Matching Loss의 효과를 더 검증하기 위해 다른 네트워크에서 생성된 결과가 그림 8에 나와 있다.  
![image](https://user-images.githubusercontent.com/40943064/146669862-f2dd5f5b-2e6d-4627-8514-0c123889d699.png)  
동일한 Feature Matching loss를 사용한 결과(col 3&4, col 5&6)가 상대적으로 작은 차이를 나타냄을 알 수 있다.  
의 𝜆𝐼𝑑은 시각적인 외모에 대한 영향이 제한적이다.  
SimSwap(col 5)과 SimSwap-oFM(col 3)의 결과를 비교하면 SimSwap은 많은 attribute을 잃지 않고 더 나은 식별 성능을 제공한다.  
SimSwap-nFM(col 7)의 결과는 최고의 식별 성능을 가지며 결과 얼굴의 모양이 source 얼굴의 모양으로 수정되었다.  
그러나 시선 방향이 target 얼굴의 방향에서 벗어나는 경향이 있기 때문에 SimSwap-nFM은 분명히 attribute을 잃어가고 있다.  
SimSwap 및 wFM-id+의 경우 대부분 매우 유사한 시각적 출력을 생성한다.  
그러나 그림 7의 wFM-id+ 및 nFM 값과 그림 8의 결과를 비교할 때 wFM-id+의 Identity Loss가 더 적지만  
ID 검색 및 시각적 보기를 통해 nFM이 실제로 더 나은 ID 성능을 달성함을 알 수 있다.  
이는 wFM-id+가 Identity Loss에 대해 과적합되었음을 나타낸다.  
게다가, wFM-id+는 source 얼굴에서 머리카락에 도입될 가능성이 더 높다(그림 9 참조).  
![image](https://user-images.githubusercontent.com/40943064/146669874-99cddf5c-da15-4046-8cd0-b6d27bde50dc.png)  

우리는 face만 교체하기 때문에 이것은 필요하지 않다.  
따라서 보다 안정적인 결과를 위해 SimSwap을 선택한다.  
  

## 5 Conclusion
일반화되고 충실도가 높은 face swapping을 목표로 하는 효율적인 프레임워크인 SimSwap을 제안한다.  
ID 주입 모듈은 feature 수준에서 ID를 전송하고 ID별 face swapping을 임의의 face swapping으로 확장한다.  
Weak Feature Matching Loss는 프레임워크가 우수한 attribute 보존 능력을 갖도록 도와준다.  
광범위한 결과에 따르면 시각적으로 매력적인 결과를 생성할 수 있으며 우리 방법은 이전 방법보다 attribute를 더 잘 보존할 수 있다.
