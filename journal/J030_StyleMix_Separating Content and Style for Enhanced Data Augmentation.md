## Abstract
심층신경망의 성능은 성공적으로 향상되어 왔으나 학습된 네트워크는 과적합이나 adversarial task에 취약하다.  
최근 이러한 문제 대비하여 mixup 방법이 활발히 연구되고 있다.  
이러한 방식은 이미지의 content/style을 구분하지 않고 이미지를 혼합하거나 잘라내어 붙여넣는다.  
이미지 쌍의 content/style을 별도로 조작하는 첫 번째 혼합 방법으로 **StyleMix**와 **StyleCutMix**를 제안한다.  
이로써 더 풍부하고 강력한 샘플을 만들어 모델 훈련의 일반화를 개선할 수 있다.  
이미지 쌍의 클래스 거리에 따라 스타일 혼합 정도를 결정하는 자동 체계를 개발하여  
너무 다른 스타일의 쌍으로부터 지저분한 혼합 이미지를 방지한다.  
CIFAR-10, CIFAR-100 및 ImageNet 데이터 세트에 대한 실험은 StyleMix가 SOTA보다 낫거나 유사한 성능을 달성하고  
adversarial task에 대한 보다 강력한 D를 학습한다는 것을 보여준다.

## 1. Introduction
심층 신경망은 많은 분류 작업에서 성과를 달성했지만, 학습된 네트워크는 과적합 및 적대적 공격에 취약하다.  
이러한 문제를 완화하기 위한 가장 유망한 접근법 중 하나로, data augmentation 및 normalization 방법이 활발하게 연구되었다.  
Mixup은 이미지와 라벨의 보간을 통해 두 샘플을 혼합하여 증강한다.  
CutMix는 패치 영역에 비례하여 실측 레이블과 함께 한 이미지에서 다른 이미지로 패치를 잘라내어 붙여 넣는다.  
Manifold Mixup은 네트워크가 은닉 상태를 보간하는 중간 표현에 과적합되는 것을 방지하기 위해 정규화한다.  
이러한 접근 방식은 입력 노이즈 및 공격에 대한 분류 성능과 견고성을 확실히 개선하지만 새로운 혼합 샘플을 생성하기 위한  
이미지의 content/style을 구분하지 않는다. 내용은 일반적으로 이미지의 모양과 형태를 말하며 스타일은 주로 질감과 색상을 포함한다.  
CNN이 content/style의 구분 없이 학습되면 label를 학습하기 위해 정보의 일부분에 초점을 맞추는 경향이 있다.  
(예: 코끼리는 전경이 어떻게 보이든 회색 피부 질감만 사용하여 식별된다.)  

이 작업에서 우리는 두 입력 이미지의 내용과 스타일을 신중하게 혼합하면 더 풍부하고 강력한 샘플을 생성하는 데 도움이 될 수 있으며  
결국 모델 훈련의 일반화를 향상시킬 수 있다고 주장한다.  
스타일 전달 방법은 최근 큰 발전을 보여 딥 네트워크가 content뿐만 아니라 이미지의 style 정보도 인코딩하고  
semantic contents를 보존하면서 이미지의 low-level visual feature 분포를 변경할 수 있는 가능성을 제공함을 입증했다.  

따라서 각 입력 이미지의 content/style을 별도로 고려하여 다양한 style의 contents 보존 이미지 생성,  
동일한 스타일 이미지의 다양한 foreground object 생성 또는 둘 다와 같은 훈련 데이터를 보강하기 위한 두 가지 수준의 옵션이 있다.  
따라서 분류기는 content/style 기능을 모두 인식하여 분류 성능과 노이즈 및 공격에 대한 견고성을 향상시키는 방법을 완전히 학습한다.  
content/style 특성의 convex 조합을 통해 다양한 학습 샘플을 생성할 수 있는 데이터 증대를 위한 새로운 혼합 방법으로 StyleMix를 제안한다.  
![image](https://user-images.githubusercontent.com/40943064/136573448-cca61a0f-81ad-4b31-bd99-12a836077fa4.png)

그런 다음 CutMix의 아이디어를 기반으로 하위 이미지 수준 조작을 허용하는 StyleCutMix로 확장한다.  
마지막으로 주어진 한 쌍의 이미지 사이의 클래스 거리에 따라 스타일 믹싱 정도를 자동으로 결정하는 기법을 개발한다.  
CIFAR-10], CIFAR100 및 ImageNet 데이터 세트에 대한 분류 실험을 통해 우리의 각 제안은 분류 성능을 크게 향상시키고  
궁극적으로 SOTA 혼합 방법과 비교 성능을 달성한다.  
이 작업의 기여는 다음과 같이 요약할 수 있다.  
1. StyleMix를 이미지 pair의 content/style을 별도로 조작하는 mixing 방법을 도입한다.   
2. content/style 입력이 명확하게 식별되는 style transfer 작업과 달리 mixup context에서  
두 개의 입력 이미지는 훈련 세트의 임의의 쌍이다.  
너무 다른 스타일의 쌍으로 인해 지저분한 혼합 이미지가 성능을 크게 손상시키는 것을 방지하기 위해 
쌍의 클래스 거리에 따라 style 혼합 정도를 결정하는 자동 방식을 제안한다.  
3. CIFAR-10/100에서 SOTA 혼합 방법을 능가하며 Cutout, GridMix, Manifold Mixup], CutMix], AugMix 및 ImageNet에서 비교한다. 
4. 퍼즐 믹스 또한 우리의 방법이 최근의 다른 혼합 방법보다 adversarial 공격에 대한 분류기의 견고성을 향상시킨다는 것을 보여준다.  

### Mixup
**Mixup** : 두 개의 무작위 훈련 예제와 해당 레이블을 선형으로 보간하도록 신경망을 훈련한다.  
신경망이 훈련 이미지 사이에서 단순한 선형 동작을 선호하도록 장려하고 결국 일반화 능력을 향상시킨다.  
**Manifold Mixup** : 선형 보간을 feature 수준으로 확장하고 네트워크가 은닉 계층의 보간된 표현에 대한 확신을 떨어뜨린다.  
**CutMix** : 패치를 잘라내어 다른 이미지에 붙여넣고 패치 영역에 비례하여 정답 레이블을 혼합한다.  
**GridMix** : 두 개의 입력 이미지를 그리드 셀로 나누고 두 이미지에서 각 패치를 무작위로 선택한다.  
**PuzzleMix** : 패치를 잘라 붙일 때 전경과 배경을 구분하지 않는 CutMix의 한 가지 문제를 해결하기 위해 돌출 신호를 활용한다.  
**AugMix** : 학습 데이터와 테스트 데이터 간의 도메인 불일치를 처리하기 위해 확률과 다양한 증강을 활용하는 간단한 데이터 처리 기술을 제안한다.  
  
그러나 이전의 접근 방식은 새로운 샘플을 혼합하기 위해 이미지의 content/style을 구분하지 않는다.  
본 방법은 이미지를 content/style의 분리된 표현으로 분해하고 신중하게 혼합하여 더 풍부하고 강력한 샘플을 생성한다.  
  
### Style Transfer
Source 이미지의 semantic한 내용을 유지하면서 스타일을 대상 이미지 스타일로 변경한다. Gatys et al. 는 CNN에서 파생된  
feature 표현이 이미지 내용과 natural 이미지의 스타일을 분리하고 재결합할 수 있음을 보여준다.  
그러나 이 방법은 고품질의 정형화된 이미지를 생성하기 위해 content/style 손실을 최적화하는데 느리다.  
이 단점을 극복하고 실시간으로 임의의 스타일 전달을 가능하게 하기 위해 많은 접근법[14, 26, 7, 12, 20]이 제안되었다.  
그 동안 style transfer 알고리즘을 기반으로 한 data augmentation이 연구되어 왔다.  
Neural augmentation은 CycleGAN을 사용하여 다양한 스타일의 이미지를 생성한다.  
STaDA는 학습 데이터 세트에 더 많은 변형을 추가하기 위해 data augmentaion 방법으로 neural style transfer를 사용한다.  
이 방법들은 스타일마다 transfomer를 개별적으로 훈련하므로 스타일 세트가 제한될 수 있다.  
Style augmentation은 contents를 보존하면서 style transfer 파이프라인을 사용하여 이미지의 질감, 대비 및 색상을 무작위로 지정한다.  
Shape-texture debiased training은 임의의 이미지에 스타일 전송을 적용한 다음 쌍을 이루는 이미지의 레이블을 혼합한다.  
이처럼 이전 작업은 mixup augmentation을 고려하지 않고 학습 이미지의 다양한 스타일에 중점을 두었다.  
반면에 본 접근 방식은 content/style의 convex 조합뿐 아니라  패치 방식의 잘라내기 및 붙여넣기를 사용하여 샘플을 생성한다.  
또한, 본 방법은 prefixed 또는 단순히 임의의 정도가 아닌 쌍의 클래스 거리에 따라 스타일 혼합 정도를 자동으로 결정한다.  

## 3. Approach
두 훈련 샘플(S3.1–3.2)의 content/style를 모두 고려하여 data augmentation을 위해 StyleMix 및 StyleCutMix를 제안한다.  
주어진 쌍에 대한 style mixing 정도를 선택하는 방법을 제시한다(S3.3).  
## 3.1. StyleMix
x1, x2(∈R^W X H X C) 두 입력과 y1, y2 두 label이 있고 두 x를 사용하여 xm을 생성하고자 한다.  
사전학습된 encoder/decoder를 각자 f and g로 정의하며 AdaIN에서 정의된 구조를 사용한다.  
arbitrary style에 대한 실시간 계산과 app. 때문에 AdaIN을 base style transfer로 사용한다.  
Encoder f는 VGG-19 상에서 relu4_1 layer까지 해당한다.  
Decoder g는 checker-board effect를 피하기 위해 pooling을 nearest up-sampling으로 바꾸는것을 제외하고  
f의 역전된 형태이다.  
추가 학습 전에 Imagenet에 대해 encoder와 decoder를 사전학습한다.  
x1, x2의 sytle/content를 분리하여 혼합된 비율로 style mixing된 xm을 생성하고자 한다.  
xm을 선형 보간을 통해 만들기 때문에 아래와 같은 4개 feature map 변수로부터 시작한다.  
![image](https://user-images.githubusercontent.com/40943064/136580993-ace08e5a-7140-44b3-8dc7-df9dbe3fc719.png)  
AdaIN(fii, fjj)는 아래의 수식으로 정의되는 adaptive instance 정규화 layer이다.  
![image](https://user-images.githubusercontent.com/40943064/136581150-d0ccffc7-03a7-4cbb-9c33-c7ca5d7706be.png)  
평균/표준편차 연산은 단일 ch의 단일 샘플의 전체 공간에 대해 수행된다.  
Table 1은 4개의 feature map 변수가 가진 content와 style 요소를 요약한다.  
![image](https://user-images.githubusercontent.com/40943064/136581350-08deb591-009c-44a3-8b26-8e297794fb03.png)  
예를들어, f12는 x1의 content x2의 style을 가진다.  
그림 2는 사전 훈련된 style decoder g를 거쳐 4개의 feature map으로 전달된 출력 이미지를 보여주고 있으며,  
표 1의 분해가 올바른지 확인한다.  
![image](https://user-images.githubusercontent.com/40943064/136581790-6771fb81-677c-40d7-aac9-876dd195de09.png)  
Mixed image를 얻기 위해 이 4개 feature map을 content 비율 rc와 style 비율 rs로 선형 보간한다.  
즉, mixup과 달리 content/style 수준에서 샘플을 생성하므로 더 풍부한 증강 효과를 얻을 수 있다.  
구체적으로, 혼합 이미지 xm은 x1의 content 성분이 rc만큼(즉, x2의 content는 1 - rc),  
x1의 style이 rs만큼(즉, x2의 style이 1 - rs인 경우) 존재하도록 한다.  
자유 변수 max(0, rc + rs − 1) ≤ t ≤ min(rc, rs)을 사용하면 xm이 content/style 구성 요소에서 선형으로 보간된다.  
![image](https://user-images.githubusercontent.com/40943064/136582405-17789a1a-1710-4b55-a9fe-7c29a1ec5465.png)  

그림 3은 Eq4에서 그리드에서 rc 및 rs 값을 조정함으로써 xm을 얻는 방법을 시각화한다.  
![image](https://user-images.githubusercontent.com/40943064/136583140-6a01e498-56cb-4db4-9914-51e650fc7e04.png)

x1(왼쪽 위)과 x2(오른쪽 아래)의 content/style 구성 요소가 선형 보간법으로 잘 분리되어 있음을 보여준다.  
따라서 표 1에 기반하여 Eq.4에서의 mixup은 content/style을 잘 혼합하는 것에 적절하다.  
Eq. 4의 자유 매개변수 t 는 4개의 feature map 사이의 선형 보간을 완성하기 위해 도입되었다.  
예를 들어, xm이 x1의 content의 70%를 가지기를 원한다면(즉, rc = 0.7), x1의 contents를 포함하는 f11과  
f12에서 얼마나 많은 것을 얻을 수 있는지 결정해야 한다.  
t는 f11과 f12 사이의 비율을 결정하며 다행히 t를 설정하는 방법에 관계없이 출력은 거의 변하지 않는다.  
그림 4는 t의 값이 변하더라도 결과적으로 생성되는 혼합 이미지 xm이 거의 변하지 않는 예를 보여준다.  
![image](https://user-images.githubusercontent.com/40943064/136583193-4eeeb8b1-3b21-4704-958f-ba68791a280d.png)  
마지막으로 content/style 구성 요소의 비율에 따라 레이블을 설정한다.  
content 기반 yc와 style 기반 ys를 먼저 계산하고 r의 비율을 가진 ym으로 결합한다.  
![image](https://user-images.githubusercontent.com/40943064/136584745-81bd64ce-b31b-4490-b876-8d49b181b7ea.png)  
학습시에, rc와 rs는 무작위로 Beta(a,a) 분포로부터 추출되어 다양한 조합을 사용한다.  
