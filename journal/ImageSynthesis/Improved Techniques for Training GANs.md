# Improved Techniques for Training GANs

## Abstract
GAN framework에 적용하는 새로운 구조적 특성과 학습과정에 대한 다양한 방법을 제시한다.  
제안 방법을 통해 각 데이터셋 대한 semi-supervised classification의 SOTA결과를 달성한다.  
생성이미지는 시각 튜링 테스트로 확인한 고품질이다. (MNIST, CIFAR-10 : human error 21.3%  
전례없는 해상도의 ImageNet 생성샘플 그리고 ImageNet class에 대한 인식가능한 feature를 배우는 모델을 가능하도록 한다.  

## 1 Introduction
GAN은 게임이론에 기반하여 생성모델을 학습하기 위한 방법에 해당한다.  
GAN의 목표는 데이터 분포 pdata(x)로부터 z as x = G(z; θ(G))를 변형하여 샘플을 생성하는 G(z; θ(G))를 학습하는 것이다.  
G 학습을 위해서는 G의 생성샘플과 실제 데이터 분포를 구분하도록 학습하는 D(x)를 통해 신호가 주어진다.
G는 차례를 이어받아 D가 G의 가짜 샘플이 진짜라고 받아들이도록 속이는 방향으로 학습된다.
최근 연구는 높은 품질의 샘플을 생성할 수 있음을 보였지만 GAN학습은 연속적인 고차원 파라미터의 non-convex Nash 평형을 찾아야 한다.  
GAN은 게임의 Nash 평형을 찾기 보다는 전형적으로 cost function의 값이 낮게 되도록 설계된 gradient descent 기법들을 사용하여 학습된다.  
Nash 평형을 추구하도록 한다면 이 알고리즘들은 수렴되지 못할 것이다.  
이 연구에서,GAN의 게임에 대한 수렴을 장려하는 여러가지 기법을 소개한다.  
소개 방법들은 수렴되지 않는 문제에 대한 경험적 이해에 의해 시작되었다.  
이 문제들은 semi-supervised 학습 성능을 향상시켰고 샘플의 품질을 향상하도록 했다.  
방법중 일부가 수렴의 공식적인 보장을 제공하면서 미래 연구의 기초가 되길 바란다.  

## 2 Related work
몇몇 최근 논문은 훈련의 안정성 및 GAN 샘플의 결과 perceptual quality를 개선하는 데 집중하고 있다.  
이 작업에서는 이러한 기술 중 일부를 기반으로 한다. 예를 들어, Radford 등에 제안된 "DCGAN" 아키텍처 혁신의 일부를 사용한다.  
[3]에서 설명한 바와 같습니다. 3.1절에서 논의된 우리가 제안한 기법 중 하나인 **feature matching**는 G를 학습시키기 위해  
maximum mean discrepancy를 사용하는 접근법과 본질적으로 유사하다[10, 11].  
minibatch features는 부분적으로 배치 정규화에 사용된 아이디어[12]에 기반을 두고 있으며, 제안된 가상 배치 정규화는 배치 정규화의 직접 확장이다.  
본 연구의 주요 목표 중 하나는 semi-supervised 학습을 위한 GAN의 효과를 개선하는 것이다  
(이 경우 라벨이 부착되지 않은 추가 예제에 대한 학습을 통해 감독된 과제의 성능을 향상시키는 것이다).  
많은 심층 생성 모델과 마찬가지로, GAN도 이전에 semi-supervised[13, 14]에 적용되었으며, 우리의 연구는 이러한 노력의 지속과 개선으로 볼 수 있다.  
Odena[15]는 동시에 GAN을 확장하여 5절에서와 같이 이미지 레이블을 예측할 것을 제안하지만,  
feature matching 확장 기능(섹션 3.1)을 사용하지 않고 SOTA를 얻는 데 중요한 것으로 밝혀졌다.  

## 3 Toward Convergent GAN Training
GAN 학습은 2인용 비협조 게임에 대한 내쉬 평형을 찾는 것이다. G/D는 각자 비용 함수를 최소화한다.  
각 참가자는 각자 loss, D 경우 J(D)(θ(D), θ(G)), G의 경우J(G)(θ(D), θ(G) )를 최소화하고자 한다.  
내쉬 평형은 J(D)가 θ(D)에 대해 최소, J(G)가 θ(G)에 대해 최소인 점(θ(D), θ(G))을 찾는것이다.  
불행하게도 내쉬 평형을 찾는 것은 매우 어려운 문제이다.  
알고리즘은 특수한 경우를 위해 존재하지만 비용 함수가 non-convex하고 매개 변수가 연속적이며  
매개 변수 공간이 극도로 고차원적인 GAN 게임에 적용할 수 있는 어떤 것도 알지 못한다.  
  
Nash 균형은 각 플레이어가 최소 loss을 가질 때 발생한다는 생각은 직관적으로 각 플레이어의 비용을 동시에 최소화하기 위해  
전통적인 gradient-based minimization 기술을 사용하는 아이디어에 동기를 부여하는 것으로 보인다.  

불행하게도 J(D)를 최소화하는 θ(D)의 수정은 J(G)를 높힐 수 있고 J(G)를 최소화하는 θ(G)의 수정은 J(D)를 높힐 수 있다.  
따라서 gradient descent는 많은 게임에서 수렴되지 않는다. 예를 들어, 한 플레이어가 xy를 xy로 최소화하고 다른 플레이어가 y에 대해 -xy를 최소화하면,  
gradient descent는 원하는 평형점인 x = y = 0으로 수렴되지 않고 안정된 궤도에 진입한다[16].  
따라서 GAN 훈련에 대한 이전의 접근방식은 이 절차가 수렴될 것이라는 보장이 없음에도 불구하고 각 참가자의 loss에 gradient descent를 동시에 적용했다.  
우리는 수렴을 장려하기 위해 경험적으로 동기부여된 다음 기법을 소개한다.  
  
### 3.1 Feature matching
Feature matching은 현재 D에 대한 오버트레이닝을 방지하는 G에 대한 새로운 목표를 지정하여 GAN의 불안정성을 해결한다.  
D의 출력을 직접 최대화하는 대신, 새로운 목표는 G가 실제 데이터의 통계와 일치하는 데이터를 생성하도록 요구한다.  
여기서 D는 일치시킬 가치가 있다고 생각되는 통계를 지정하기 위해서만 D를 사용한다.  
특히, 우리는 D의 중간 레이어에 있는 feature의 예상 값과 일치하도록 G를 훈련한다.  
이것은 D를 학습함으로써 현재 모델에 의해 생성된 데이터와 실제 데이터를 가장 구별하는 특성을 찾도록 요청하기 때문에 G가 일치시킬 통계의 자연스러운 선택이다.  
f(x)가 D의 중간 계층에 대한 actiation을 나타내도록 하면 G에 대한 새로운 목적은 다음과 같이 정의됩니다.  
||Ex∼pdata f(x) − Ez∼pz(z) f(G(z))||^2_2 . D와 f(x)는 일반적인 방식으로 학습된다. 일반 GAN 훈련과 마찬가지로  
목표는 G가 훈련 데이터의 분포와 정확히 일치하는 고정 소수점을 갖는다.  
실제로 이 고정점에 도달한다는 보장은 없지만 경험적 결과는 일반 GAN이 불안정해지는 상황에서 feature matching이 실제로 효과적임을 나타낸다.  
