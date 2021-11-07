# StarGAN v2: Diverse Image Synthesis for Multiple Domains
## Abstract
좋은 I2I translation 모델은 1) **다양성** 2) **도메인 확장성**을 충족하면서 도메인간 매핑을 학습해야 한다.  
기존 방법은 모든 도메인에 대해 제한된 다양성 또는 다중 모델을 갖는 문제 중 하나만 해결한다.  
본 연구는 두 가지를 모두 처리하고 기준선에 비해 크게 개선된 결과를 보여주는 단일 프레임워크인 StarGAN v2를 제안한다.  
CelebAHQ 및 AFHQ에 대한 실험은 시각적 품질, diversity 및 scalability 측면에서 우수성을 검증한다.  
I2I translation 모델을 더 잘 평가하기 위해 도메인 간 및 도메인 내 차이가 큰 고품질 동물 얼굴인 AFHQ 공개한다.  

## 1. Introduction
I2I 변환은 도메인간 매핑 학습을 목표로 한다. 도메인은 시각적으로 구별되는 범주로 그룹화할 수 있는 이미지들을 의미하며  
각 이미지는 고유한 모양을 가지며 이를 스타일이라고 한다.  
예를 들어, 성별로 도메인을 설정할 수 있다. 스타일에는 메이크업, 수염, 헤어스타일이 포함된다(그림 1의 위쪽 절반).  
이상적인 I2I 변환은 각 영역의 다양한 스타일을 고려하여 이미지를 합성할 수 있어야 한다.  
그러나 많은 수의 스타일과 도메인이 있을 수 있으므로 이러한 모델을 설계하고 학습하는 것이 복잡해진다.  
  
스타일 다양성을 위해 많은 작업이 연구되었다. 이 방법은 표준 가우스 분포에서 무작위 샘플 저차원 latent를 D에 입력한다.  
도메인별 디코더는 이미지를 생성할 때 latent를 다양한 스타일의 레시피로 해석한다.  
그러나 이러한 방법은 도메인 간의 매핑만 고려했기 때문에 증가하는 도메인 수에 맞게 확장할 수 없다.  
예를 들어, K 도메인이 있는 경우 K(K-1) G를 훈련시켜 각 도메인 간의 변환을 해야 하므로 사용이 제한된다.  
  
확장성을 위해 여러방법이 제안됐다. StarGAN은 단일 G를 사용하여 모든 도메인 간의 매핑을 학습하는 초기 모델 중 하나이다.  
G는 도메인 레이블을 추가 입력으로 사용하고 이미지를 해당 도메인으로 변환하는 방법을 학습한다.  
그러나 StarGAN은 여전히 데이터 분포의 multi-modal을 포착하지 못하는 각 도메인별로 결정적 매핑을 학습한다.  
이러한 제한은 각 도메인이 미리 결정된 레이블로 표시된다는 사실에서 비롯된다.  
G는 입력으로 고정 레이블(예: one-hot 벡터)을 사용하므로 소스 이미지가 주어지면 필연적으로 각 도메인마다 동일한 출력을 생성한다.  
  
두 장점을 최대한 활용하기 위해 여러 도메인에 걸쳐 다양한 이미지를 생성할 수 있는 확장 가능한 접근 방식인 StarGAN v2를 제안한다.  
특히 StarGAN에서 시작하여 도메인 레이블을 특정 도메인의 다양한 스타일을 나타낼 수 있는 제안된 도메인별 스타일 코드로 교체한다.  
이를 위해 매핑 네트워크와 스타일 인코더의 두 가지 모듈을 소개한다.  
**매핑 네트워크**는 가우시안 노이즈를 스타일로 변환하는 방법을 학습하고 **인코더**는 이미지에서 스타일을 추출하는 방법을 학습한다.  
여러 도메인을 고려할 때 두 모듈에는 각각 특정 도메인에 대한 스타일 코드를 제공하는 **여러 출력 분기**가 있다.  
마지막으로 이러한 스타일 코드를 활용하여 G는 여러 도메인에서 다양한 이미지를 성공적으로 합성하는 방법을 학습한다(그림 1).  

StarGAN v2의 개별 구성 요소의 효과를 조사하고 실제로 스타일 코드를 사용함으로써 이점을 얻는다는 것을 보여줍니다(섹션 3.1).  
제안방법이 여러 도메인으로 확장 가능하고 주요 방법에 비해 품질 및 다양성 측면에서 훨씬 나은 결과를 제공함을 입증한다.  
마지막으로, 큰 도메인 간/내 차이에 대한 I2I 변환모델 성능을 잘 평가하기 위해 고품질의 다양한 변형이 있는  AFHQ를 제시한다.  
우리는 연구 커뮤니티에서 공개적으로 사용할 수 있는 이 데이터 세트를 공개한다.
## 2. StarGAN v2
본 순서에서 제안 프레임워크와 학습 목적함수를 설명한다. 
### 2.1. Proposed framework
X, Y는 이미지 셋이고 가능한 도메인이다.  
x ∈ X, y ∈ Y 가 주어지면 목표는 주어진 이미지 x로 도메인 y의 **다양한** 이미지를 만들 수 있는 **단일** G를 학습하는것이다.  
각 도메인에 대한 학습된 스타일 공간에서 도메인 특정 스타일 벡터를 생성하고 G가 스타일 벡터를 반영할 수 있도록 학습한다.  
그림2는 아래 설명의 4개 모듈을 가지는 프레임워크를 설명한다.  
<img src ="https://user-images.githubusercontent.com/40943064/134599225-1ee34f8f-6115-4129-8543-269f13b495bd.png" width=600>  
  
#### Generator
G는 입력 x에 대해 F나 E에 의해 제공받은 특정 스타일 s를 반영하는 G(x,s)로 변환한다. s를 G에 주입하기 위해 AdaIN을 사용한다.  
s는 특정 도메인 y의 스타일을 표현하기 위해 설계되어 y를 G에 입력할 필요성을 제거해주며 모든 도메인에 대해 합성할 수 있도록 한다.  
  
#### Mapping network
latent z와 도메인 y가 주어지면 s = Fy(z)를 생성한다.  
모든 가능한 도메인에 대한 스타일 생성을 위해 MLP로 구성되어 여러 출력 분기로 형성된다.  
latent z와 도메인 y를 무작위로 샘플링하여 다양한 스타일을 생성한다.  
멀티 태스크 구조로 인해 효율적으로 모든 도메인에 대한 스타일을 학습한다.  
  
#### Style encoder
latent z와 도메인 y가 주어지면 s = Ey(x)를 생성한다. F와 유사하게 멀티태스크 학습 세팅으로부터 이득을 얻다.  
E는 여러 x를 이용해 다양한 스타일 s을 생성한다. 즉, x의 스타일 s를 반영한 출력 이미지를 합성할 수 있도록 한다.  
  
#### Discriminator
D는 멀티태스크 분류기로 여러개의 출력 분기를 구성한다. 각 분기 Dy는 각 도메인이 진짜/가짜임을 분류한다.  

### 2.2. Training objectives
x와 원 도메인 y에 대해 아래의 목적함수를 이용해 본 프레임워크를 학습한다.
#### Adversarial objective.
**z**, **y\~** 를 샘플링하고 타겟 style **s~=Fy~(z)** 생성한다. G는 아래를 통해 **x**, **s\~** 를 입력받아 **G(x,s~)** 를 생성한다.  
  
<img src = "https://user-images.githubusercontent.com/40943064/134600814-0caa2038-bd7c-4a73-8400-960f63e00b51.png" width = 450>  
  
#### Style reconstruction. 
**G**가 **s\~** 를 활용할 수 있도록 하기 위해 style reconstruction loss를 추가한다.  
  
<img src = "https://user-images.githubusercontent.com/40943064/134601646-a420d009-c8f0-4aad-b160-4f4434dc1ba9.png" width = 300>  
  
본 목적함수는 image → latent 매핑을 하는 접근법과 유사하나 특별한 차이는 multi-modal/multi-domain을 위한 단일 E를 학습한다는 점이다.  
테스트 시에 학습된 E는 G가 이미지를 원 이미지의 스타일을 반영하도록 한다.  
#### Style diversification. 
G가 다양한 이미지를 만들기 위해, 명시적으로 diversity sensitive loss를 이용하여 G를 정규화한다.

<img src = "https://user-images.githubusercontent.com/40943064/134618979-ddec0d67-b03b-4be9-8d3c-8d60d11a6efe.png" width = 400>  
  
여기서 목표 스타일 **s\~1** 과 **s\~2** 는 latent z1과 z2에 의해 F를통해 각각 생성이 된다.  
정규화 항을 최대화 함으로써 G가 다양한 이미지를 생성하기 위해 이미지 공간을 탐색하고 의미있는 스타일 feature를 찾아내도록 한다.  
원 loss에서 분모에서 ||z1-z2||1의 작은 차이는 loss를 엄청나게 키우고 이로인해 학습의 gradient가 커지며 불안정해짐을 알아야한다.  
따라서 분모항을 없애고 새로운 식을 고안하여 안정하면서 동일한 직관을 같도록 한다.  
#### Preserving source characteristics
생성 이미지 G(x, s\~)가 적절하게 x의 도메인 불변 특성(pose)를 보존하도록 하기 위해 cycle consistency loss를 적용한다.  
  
<img src = "https://user-images.githubusercontent.com/40943064/134619549-6a7cd648-89a5-4836-9adb-54c74ebb2e77.png" width = 400>  
    
여기서shat = Ey(x)는 입력 이미지에 대한 추정된 스타일이며 y는 x의 원 도메인을 의미한다.  
G가 shat 스타일의 x를 복원할 수 있도록 함으로써 G는 x를 스타일은 신뢰있게 변화시키는 반면 원 특성은 보존하도록 배운다.  
#### Full objective.

<img src = "https://user-images.githubusercontent.com/40943064/134622557-b8398aea-4f96-48a1-8360-9913d67faa81.png" width = 450>  


## 3. Experiments
### 3.1. Analysis of individual components
### 3.2. Comparison on diverse image synthesis
#### Latent-guided synthesis.
#### Reference-guided synthesis.
#### Human evaluation.

## 4. Discussion
## 5. Related work
## 6. Conclusion