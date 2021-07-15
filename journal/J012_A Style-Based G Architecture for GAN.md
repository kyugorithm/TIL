## Abstract
GAN에 대해 **style transfer** 영역에서 차용하는 새로운 G 방법론  
High-level (자세, 얼굴), stochastic 변화(주름, 머리카락)에 대한 **비지도적 분리를 자동으로 학습**하고  
직관적인 이미지 합성에 대한 **scale-specific 제어**를 가능하게 한다.  
일반적인 metric에 대해 SOTA 성능을 뛰어넘으며 시연 상에서 나은 **interpolation 특성**을 가지고  
마찬가지로 더 나은 **latent factor 다양성 disentanglement**를 이끌어낸다.  
**interpolation 품질과 disentanglement를 수치화**하기 위해 모든 생성자 구조에 적용가능한 자동화된 2개의 방식을 제안한다.  

## Conclusion
우리와 Chen의 연구결과를 바탕으로 전통적인 GAN의 G 구조가 모든 면에서 style-based 구조에 비해 열등함이 명확해지고 있다.  
제안한 품질 척도 관점에서 명확하며 또한 고차원 특성 분리, stochastic effect, 중간 latent 공간의 linearity는  
GAN 합성에 관한 이해와 제어가능성을 향샹시키는데 유익함을 증명한다.  
Average path length는 regularizer로 linear separability는 metric으로 사용될 수 있음을 확인했다.  
일반적으로 우리는 우리는 중간의 latent space를 학습동안 직접적으로 구성하는 방법이 흥미로운 이점을 제공할것  
으로 예상한다.


## A. The FFHQ dataset
연구팀은 1024 해상도의 얼굴 이미지 70k장을 Flickr에서 수집하였다.  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/125629988-c9162cbc-8c7a-4ded-9aae-05cbc75b6acd.png" width=800 /></p>  
데이터셋은 연령, 인종, 배경등의 관점에서 CELEBA-HQ보다 훨씬 다양하며 안경, 선그라스, 모자등의 악세사리에 대한 다양한 소스가 있다.  
본 이미지들은 Flickr에서 크롤링(해당 웹사이트의 바이어스를 지닐 수 있다.)하였으며 자동적으로 배열되고 크롭되어있다.  
라이선스가 허용된 사진만 수집되었다. 세트를 가지치기 하기 위하여 다양한 자동필터를 사용하였으며 Mechanical Turk는  
일부의 조각상, 그림 또는 사진 사진을 제거할 수 있게 해주었다.  
그림은 다음 주소에서 얻을 수 있다. : https://github.com/NVlabs/ffhq-dataset  

<p align="center"><img src="https://user-images.githubusercontent.com/40943064/125705179-8a0bab76-b66c-43d0-b744-99196576d53d.png" width=600 /></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/125706431-a14691b6-f5f6-4efd-9a6a-b7d9c2520311.png" width=600 /></p>  

## B. Truncation trick in W
학습데이터 분포를 고려하면 저밀도 데이터 영역의 학습 품질은 매우 낮을것이며 G가 학습하기 매우 어려울 것이다.  
이는 모든 생성 모델링 기법에 있어 중요한 문제이다. 그러나 잘리거나 수축한 샘플링 공간으로부터 latent vector를  
그리는 것은 일정부분의 표현은 사라질지라도 평균이미지 품질은 향상시키는것으로 알려져있다.  
이와 유사한 전략을 사용할 수 있다. 먼저, W mass의 중심을 계산한다. (wbar = E_z~p(z)[f(z)])  
FFHQ의 경우 이 지점은 일종의 평균 얼굴을 나타낸다.  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/125635996-7847711d-643e-4126-ab33-62a0a6bfae33.png" width=500 /></p>  
w′= ̄w+ψ(w− ̄w) 수식에서 wbar 평균 얼굴 센터로부터 주어진 w의 편차를 sclae할 수 있다. 

Brock은 직교 정규화를 사용하더라도 네트워크의 일부만 이러한 trunccation 작업을 수행할 수 있으며,  
W 공간의 truncation 작업은 loss 의 변경 없이 안정적으로 작동하는 것을 확인했다.  

## C. Hyperparameters and training details
우리는 PG-GAN의 공식 TensorFlow 구현에 기초하여 대부분의 학습 세부 정보를 상속한다. 원래 설정은 T1-A에 해당한다.  
특히, 동일한 D 아키텍처, resolution 의존하는 mini-batch 크기, Adam [33] hyperparameter 및 G의 EMA를 사용한다.  
CelebA-HQ 및 FFHQ의 경우 mirror augmentation을 사용하도록 설정하지만 LSUN의 경우 미러 확장을 사용하지 않도록 설정한다.  
V100 GPU 8개 학습 시간은 약 일주일이다. T1-B에 대해 전체 결과 품질을 개선하기 위해 몇 가지 수정을 수행한다.  
두 네트워크에서 nearest-neighbor의 up/don sampling을 bilinear 샘플링으로 대체하며, 각 up-sampling layer 이후와  
각 down-sampling layer 앞에 있는 분리 가능한 2nd order binomial 필터로 activation를 구현한다.  
우리는 Karras와 같은 방식으로 progressive growing을 구현한다. 그러나 4x4 대신 8x8 이미지에서 시작한다.  

FFHQ 데이터 세트에 대해, 우리는 WGAN-GP에서 non-saturation R1 정규화 loss(γ = 10)로 전환한다.  
이를통해 FID 점수가 WGAN-GP보다 상당히 오랫동안 계속 감소한다는 것을 알게 되었으며, 따라서 학습 시간이 12M에서 25M으로 늘어났다.  
FFHQ에 대해 Karras와 같은 learning rate 을 사용하지만, CelebA-HQ에 대해서는 0.003대신 0.002를 사용하는것이 512, 1024에 대해  
더 나은 학습 안정성을 가진다는 것을 알게되었다. 

스타일 기반 G에 대해 (T1-F) α = 0.2인 leaky ReLU와 모든 계층에 대해 equalized lr을 사용한다.  
Karras와 동일한 feature map 수를 convolution layer에 사용한다. Mapping network는 FC 8개의 계층으로 구성되며  
z와 w를 포함한 모든 I/O activation의 dimension은 512이다. Mapping network의 depth를 높이면 높은 학습률로 인한  
학습 불안정 경향이 발생한다. 따라서 Mapping network에 대한 학습 속도를 두 자릿수까지 줄인다.(λ' = 0.01λ)  

N (0, 1) 으로 convolution, FC 및 affin 변환 layer의 모든 가중치를 초기화한다. 통합 네트워크에서 상수 입력 하나로 초기화한다.  
bias, noise scaling factor는 0으로 초기화한다. (0으로 초기와 하는 ys에 관련된 bias는 제외)

## D. Training convergence  
그림9는 FID 와 PPL(perceptual path length) metric이 어떻게 B와 F 조합의 FFHQ 학습이 진행되는지를 보여준다.  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/125643721-f4eb942c-b997-47c8-abaf-bb227f443f18.png" width=650 /></p>  


B, F에서 R1 정규화를 이용하면 학습에 따라 FID도 계속 줄어들며 120만장에서 250만장으로 학습을 늘이는데 동기부여하였다.  
심지어는 1024 해상도에 도달했을때 천천히 PPL이 증가하는것은 FID의 개선은 entanglement를 키우는 희생을 하게됨을 암시한다.  
향후 작업을 고려할 때, 이것이 불가피한 것인지, FID의 수렴을 막지 않고 더 짧은 경로 길이를 권장할 수 있었는지에 대한 흥미로운 질문이다.

## E. Other datasets
F10:LSUN, F11:BEDOM, F12:CARS/CATS는 각각의 uncurated 결과 세트를 보여준다. 이 영상에서는 resolution 4 ~ 32에 대해  
 _ψ_ = 0.7의 T1-B의 truncation 트릭을 사용했다. 함께 제공되는 비디오는 스타일 혼합 및 확률적 변동 테스트에 대한 결과를 제공한다.  
BEDOM & CARS / coarse-style : 카메라시점 제어, mid-style : 특정 가구 선택, fine-style : 색상, 작은 재료 디테일  
확률적 변화는 주로 침실의 직물, CARS의 배경 및 전조등, CATS의 털, 배경, 그리고 흥미롭게도 발의 위치 설정에 영향을 미친다.  
다소 놀랍게도 차량의 휠은 확률적 입력에 기초하여 회전하지 않는 것으로 보인다. 이러한 데이터셋은 BEDOM 및 CATS의 경우  
70만 개의 영상 지속 시간 동안 FFHQ와 동일한 설정을 사용하여, CARS의 경우 46M의 영상 지속 시간 동안 훈련되었다.  
많은 이미지에서 처럼 가장 불쾌한 문제들이 저품질의 학습데이터로부터 상속된 심각하게 압축된 artifact이기 때문에  
BEDROOM 셋에 대한 결과는 학습 데이터 한계에 도달하기 시작한다고 의심한다.
CARS는 공간 해상도(2562가 아닌 512 × 384)를 높일 수 있는 훨씬 더 높은 품질의 교육 데이터를 가지고 있으며,  
CATS는 자세, 줌 수준 및 배경의 본질적인 차이로 인해 여전히 어려운 데이터 세트이다.

<p align="center"><img src="https://user-images.githubusercontent.com/40943064/125647502-c19656f0-d50b-4689-b498-6f39e04e0a46.png" width=650 /></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/125647796-8fd087c9-ea0f-4b4f-8efd-376dab6c7a5a.png" width=650 /></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/125648027-0e606fda-2d0d-4527-acf9-2816961490a5.png" width=650 /></p>  
  
