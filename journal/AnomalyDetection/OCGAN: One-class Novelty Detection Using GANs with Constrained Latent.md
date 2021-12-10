# OCGAN: One-class Novelty Detection Using GANs with Constrained Latent

## Abstract
One class novelty detection의 고전적인 문제에 대해 OCGAN이라는 새로운 모델을 제시한다.  
목표는 특정 class의 example이 동일한 클래스의 것인지 여부를 확인하는 것이다.  

해법 : Denoising AE를 사용한 in-class의 latent representation 학습 방식 활용  
  
본 방법의 key contribution은 주어진 class를 배타적(독점적)으로 표현하기 위해 **latent space를 명시적으로 제약** 하는것이다.  

이를 달성하기 위해 다음과 같이 설계한다.
1) Encoder output 레이어에 tanh를 적용하여 latent space의 값이 제약되도록 한다. 
2) 적대적으로 학습된 latent 공간에서 D를 사용함으로써 in-class 샘플의 encoding된 표현이 동일한 bounding space로부터 uniform random distribution을 모사하도록 한다. 
(개인생각 : 보통은 이미지 공간에서 사용하나 latent 에 대한 Discrimination을 사용하는것이 novelty가 있으나 학습시 D가 over-training 될 위험이 존재함)
3) 추가 D를 정의하여 image 공간에서의 discrimination을 수행하도록 하고 이를통해 생성된 이미지가 실제처럼 보이도록 한다.
(개인생각 : 기존 방식)
4) 잠재적인 out-of-class 샘플을 생성하는 latent space의 point를 탐색하는 gradient-descent 기반 sampling은 네트워크에 피드백되어 해당 지점에서 클래스 내 example을 생성하도록 추가 학습한다.


두 개의 1-class novelty detection 프로토콜을 사용하여 네개의 데이터 세트에 걸쳐 성능을 증명한다.


## 1. Introduction
## 2. Related Work
## 3. Proposed Method: OCGAN
### 3.1. Motivation
Introudction에서 주어진 클래스를 나타내도록 학습된 네트워크가 다른 클래스의 이미지에 대한 표현을 나타내는 예를 보여줬다.  
주어진 클래스의 이미지가 충분히 다양할 때 latent space의 한 클래스 내 이미지의 projection을 다른 클래스의 이미지로 원활하게 전환하는 것은  
무한히 다양한 경로를 따라 수행될 수 있다. 이는 특히 높은 차원의 latent space의 경우이다.  
AE를 학습할 때 우리는 관찰된 예만 latent space로 projection을 모델링한다.
해당 latent point 사이의 모든 가능한 경로는 아니다.  
그림 2에서 주어진 클래스8 의 서로 다른 두 이미지에 해당하는 두 지점 사이의 latent space에서 추적된 경로를 시각화한다.  
![image](https://user-images.githubusercontent.com/40943064/145534081-a68d76e9-99fc-431b-a787-38e3f3927fe7.png)

좌측은 지정된 경로를 따라 latent space 한 point에서 다른 point로 전환할 때 특정 중간 latent 샘플이 숫자 1인 것이 확인된다.  
네트워크에서 숫자 1의 인스턴스를 관찰하면 해당 샘플에 projection된다.  
네트워크 학습시 숫자 1은 표현되기 쉽기 때문에 비록 클래스를 벗어나더라도 reconstruction error가 낮을 것이고  
이 때문에 이러한 문제가 발생하기 쉬울 것이다.

제안의 핵심 아이디어는 이러한 문제점에 대한 관찰을 기반으로 한다.  
(전체 latent space가) (주어진 클래스의 이미지만을 나타내기 위해 제한하면) (클래스를 벗어난 샘플의 표현이 최소화될 것)이며  
높은 재구성 오류가 발생한다고 주장하는 것이다.  

이 전략을 염두에 두고 명시적으로 전체 latent space가 주어진 클래스만 나타내도록 강제한다.  
이 아이디어를 그림 2(b)의 예에 적용하면 두개의 8 사이의 경로에 있는 모든 latent 샘플이 숫자 8 이미지 세트로 표현될 수 있다.  

결과적으로 8이 아닌 1이 모델에 표시되면 reconstruction error가 커지는 것이다. 
제안된 방법은 우수한 novelty detection 성능을 얻을 수 있다.  

### 3.2. Proposed Strategy
OCGAN은 denoising AE, 두 개의 D(latent & original) 및 classifier 네 가지로 구성된다.  
제안된 네트워크는 adversarial 원칙을 사용하여 학습한다.  
아래에서 이러한 각 구성 요소에 대해 자세히 설명한다.  

**Denoising auto-encoder:**  
AE는 입력과 출력 사이의 거리를 최소화하기 위해 훈련된 인코더(En) - 디코더(De) 구조이다.  
입력보다 작은 차원 사이에 병목 현상이 있는 latent space가 있는 것이 일반적이다.  
이러한 병목으로인해 AE는 reconstruction에 필요한 latent space에 필수 정보만 유지하게된다.  
Denoising AE에서 노이즈가 입력 이미지에 추가되고 네트워크는 이미지의 노이즈 제거 출력을 reconstruct할 것으로 기대한다.  
Denoising AE가 일반 AE에 비해 overfitting을 줄이고 네트워크의 generalizabilty를 향상시키는 것으로 알려져있다.  
결과적으로 Denoising AE는 입력 이미지 차원보다 더 큰 latent space를 가질 가능성을 열어준다.  
또한, 우리 전략은 latent space에서 dense하게 샘플링하는 것을 중심으로 이루어진다.  
이 작업을 용이하게 하기 위해  latent space를 제한적으로 support 하기 위해 encoder의 출력 레이어에 tanh 활성화를 적용한다.  
따라서 잠재 공간의 support는 (−1, 1)d 이다. (d :  latent space 차원)  
구현에서 입력 이미지에 0.2의 분산을 갖는 제로 평균 gauss white noise를 추가하고 아래와 같이 MSE loss를 사용하여 AE를 학습한다.  
![image](https://user-images.githubusercontent.com/40943064/145535904-35b79d2e-0a68-4ff0-8088-b126009aeaa3.png)  
(x : 입력 이미지 / n ~ N(0, 0.2))
또한 다음 섹션에서 소개하는 적대적 손실 항은 AE의 parameter 학습에도 사용된다.  
AE의 decoder 부분은 latent space에서 이미지를 생성하는 역할도 하므로 decoder와 generator라는 단어를 같은 의미로 사용한다.  
ㅇ together with the autoencoder network using maxDe minDv lvisual.
**Latent Discriminator:**  
목표 : Latent space의 샘플이 주어진 클래스의 이미지를 잘 나타내는 latent space을 얻는것  
주어진 클래스의 representation이 latent space의 하위 영역에만 국한된다면 이 목표는 달성할 수 없다.  
따라서 클래스 내 sample의 latent representation이 latent space 전체에 균일하게 분포되도록 명시적으로 강제한다.  
이를 latent discrimiantor **Dl**이라고 표현하는 latent space에서 적용하는 D를 사용하여 달성한다.  
D 주어진 클래스의 실제 이미지의 latent representation과 U(-1, 1)d 분포에서 추출한 샘플을 구별하도록 학습된다.  
![image](https://user-images.githubusercontent.com/40943064/145536716-15009fbb-deb1-4218-8017-762d06e2f0ff.png)  
(px는 클래스 내 example의 distribution)  
max(Encoder)min(Dl) l latent를 사용하여 AE와 함께 latent discriminator를 학습한다.  
Latent space는 평형 상태에서 (−1, 1)d 를 support 하는 hyper cube이므로 주어진 클래스의 example의 latent projection은  
U(−1, 1)d 분포를 따라 고르게 분포될 것으로 예상된다.  
  
**Visual Discriminator:**  
네트워크가 클래스를 벗어난 object를 갖지 않도록 latent space에서 철저하게 샘플링하고 해당 이미지가 클래스를 벗어나지 않도록 할 것을 제안한다.  
학습 중에 부정적인 클래스가 없기 때문에 이 조건을 적용하기 어렵다.  
대신, latent sample로 생성된 모든 이미지가 주어진 클래스와 동일한 이미지 공간 분포에 있는지 확인한다.  
이 제약 조건을 적용하기 위해 visual discriminator(Dv)라고 하는 두 번째 D를 사용한다.  
Dv는 디코더 De(s)를 사용하여 임의의 latent 샘플에서 생성된 이미지와 주어진 클래스의 이미지를 구별하도록 훈련된다.  
(s는 임의의 latent sample)  
(뒤 내용에서는 생성 이미지를 가짜 이미지라고 표현한다.)  
Dv 속았을 때, 무작위로 선택된 fake는 일반적으로 주어진 클래스의 예제와 유사하게 보인다.  
Adversarial loss lvisual을 다음과 같이 정의한다.  
![image](https://user-images.githubusercontent.com/40943064/145537593-c136b191-9b88-439d-9738-f01b08c51a3e.png)  
max(De) min(Dv) lvisual를 사용하여 AE와 함께 Dv를 학습한다.  

**Informative-negative Mining:**  
그림 3(a)는 숫자 9를 사용하여 이 세 개의 하위 네트워크를 공동으로 학습하여 얻은 fake이다.  
제안된 네트워크가 대부분의 무작위 latent sample에 대해 주어진 클래스의 그럴듯한 이미지를 생성할 수 있음을 보인다.  
그러나 그림과 같이 생성된 출력이 주어진 클래스와 다르게 보이는 경우가 있다.  
예를 들어, 그림 3(a)에서 강조 표시된 숫자는 9보다 0처럼 보인다. 
![image](https://user-images.githubusercontent.com/40943064/145538124-879a5da4-79b7-428b-a874-45b070a2bf1a.png)

이 결과는 제안된 훈련 절차에도 불구하고 주어진 클래스의 이미지를 생성하지 않는 latent space 영역이 있음을 의미한다.  
이는 특히 latent dimension 차원이 큰 경우 학습중에 latent space의 모든 영역에서 샘플링하는 것이 불가능하기 때문이다. 
이 문제에 대한 순수한 해결책은 latent space의 차원을 줄이는 것이다.  
그러나 차원이 낮을수록 네트워크가 보존하는 세부 정보의 양이 줄어든다는 문제가 있다.  
결과적으로 모든 latent sample이 동급 이미지를 생성하지만 차원이 너무 낮으면 novelty detection 성능이 저하된다.

해법으로 latent space에서 품질이 좋지 않은 이미지를 생성하는 영역을 적극적으로 탐색할 것을 제안한다.  
논문의 나머지 부분에서 우리는 이러한 이미지를 informative-negative sample이라고 한다.  
우리는 informative-negative sample을 사용하여 G를 학습시켜 이러한 latent sample에 대해서도  
우수한 품질의 in-class 이미지를 생성하는 방법을 학습한다.  
그러나 더 약한 샘플을 공급하면 D의 학습을 방해하므로 무작위로 선택된 샘플을 사용하여 두 개의 D를 학습한다.  
Informative-negative sample을 찾기 위해 먼저 임의의 latent space sample로 시작하고 D를 사용하여 샘플에서 생성된 이미지의 품질을 평가한다.  
D 손실은 latent space의 gradient를 back-propagate하 계산하는 데 사용한다.  
그런 다음 D가 생성된 이미지가 클래스를 벗어났다고 확신하는 잠재 공간의 새 지점으로 이동하기 위해 그래디언트 방향으로 작은 단계를 수행한다.  

