## Abstract
전형적인 GAN의 합성 과정이 **계층적 Conv. 연산**을 수행하지만 불건전한 방식으로 **절대적인 픽셀 위치에 의존**한다.  
(앞 레이어 latent에 conditional한 것이 아니라 해당 픽셀 위치에 존재 확율이 높은 것으로 여겨지는 문제)  
이는 예를 들어 묘사된 객체의 표면 대신 이미지 좌표에 붙어있는 디테일로 나타난다.  
G에서 aliasing을 유발하는 부주의한 신호 처리가 근본 원인으로 보인다.  
네트워크 신호를 연속신호로 해석함으로써 원치 않는 정보가 계층적 합성 프로세스로 유출되지 않도록 보장하는 일반적으로 적용 가능한 작은 아키텍처 변경을 도출한다.  
StyleGAN2의 FID와 일치하지만 내부 표현 방식이 크게 다르고 subpixel 스케일에서 마저 translation과 roation에 등변성을 가진다.  
결과는 비디오와 애니메이션에 더 적합한 생성 모델을 위한 기반을 제공한다.

## 1. Introduction
GAN 이미지의 해상도와 품질은 최근 빠른 개선을 보였다. 이미지 편집, 도메인 변환, 비디오 생성을 포함한 다양한 응용 프로그램에 사용되었다.  
생성 과정을 제어하는 몇 가지 방법이 발견되었지만, **합성 과정의 기초**는 부분적으로만 이해되었다.  
실제 세계에서는 서로 다른 scale의 detail이 계층적으로 변환되는 경향이 있다. 예를 들어, 머리를 움직이면 코가 움직이고 코에 있는 피부 모공이 움직인다.  
일반적인 GAN G의 구조는 유사하다. Coarse한 저해상도 feature는 업샘플링하여 계층적으로 정제되고, conv.에 의해 locally 혼합되며,  
비선형성을 통해 새로운 detail이 도입된다.  
이러한 피상적인 유사성에도 불구하고 현재의 GAN 아키텍처가 자연스러운 계층적 방식으로 이미지를 합성하지 않는다는 것을 관찰했다.  
Coarse feature는 주로 미세한 특징의 존재를 제어하지만 정확한 위치는 제어하지 않는다.  
그대신 미세한 세부 사항의 대부분이 픽셀 좌표에 고정된 것처럼 보인다. 이 불안한 "texture sticking"은 latent interpolation 
(그림 1 및 프로젝트 페이지 https://nvlabs.github.io/stylegan3의 첨부 비디오 참조)에서 명확하게 볼 수 있어  
견고하고 일관된 object가 공간에서 움직일것으로 예상되는 환상을 깨뜨린다.  
목표는 각 feature의 정확한 subpixel 위치가 기본 coarse feature에서 독점적으로 **상속**되는 보다 자연스러운 변환 및 계층 구조를 나타내는 아키텍쳐이다.  

현재 네트워크는 이미지 border[28, 35, 66], per-pixel noise input[33] 및 positional encoding, aliasing을 통해  
중간 레이어에서 사용할 수 있는 의도치 않은 위치 참조를 사용하여 이상적인 계층 구조를 **부분적으로 우회할 수 있다**[5, 69].  
(근본적으로 해결되는것이 아니라 우회해서 주먹구구식으로 해결함). 
Aliasing은 미묘하고 중요한 문제[44]에도 불구하고 GAN 문헌에서 거의 주목받지 못했다.  
우리는 이에 대한 두 가지 원인을 확인한다.  
  
1) Nearest, bilinear, strided convolution과 같은 비이상적인 업샘플링 필터로 인한 픽셀 그리드의 희미한 잔상
2) ReLU 또는 swish와 같은 비선형성의 포인트별 적용[47].  
   
네트워크가 아주 작은 양의 aliasing이라도 증폭할 수 있는 수단과 동기를 가지고 있다는 것을 발견했으며  
이를 여러 스케일에 걸쳐 결합하면 화면 좌표에 고정된 텍스처 모티브의 기반을 구축할 수 있다.  
이는 딥 러닝[69, 59]에서 일반적으로 사용되는 모든 필터와 이미지 처리에 사용되는 고품질 필터에도 적용된다.  
그렇다면 어떻게 원치 않는 부가 정보를 제거하여 네트워크가 이를 사용하지 못하도록 막을 수 있을까?  
약간 더 큰 이미지에서 단순히 작업하여 테두리를 해결할 수 있지만 alising은 훨씬 어렵다.  
우리는 aliasing이 고전적인 Shannon-Nyquist 신호 처리 프레임워크에서 가장 자연스럽게 처리된다는 점에 주목하는 것으로 시작하고,  
단순히 개별 샘플 그리드로 표시되는 연속 도메인의 bandlimitted function으로 초점을 전환한다.  
이제 위치 참조의 모든 소스를 성공적으로 제거하면 픽셀 좌표에 관계없이 세부 사항이 동등하게 잘 생성될 수 있으며,  
이는 차례로 모든 레이어에서 하위 픽셀 변환(및 선택적으로 회전)에 대한 연속 등가성을 적용하는 것과 같다.  
이를 달성하기 위해 StyleGAN2 G의 모든 신호 처리 측면에 대한 포괄적인 정밀 검사를 설명한다.  
우리의 기여에는 현재의 업샘플링 필터가 단순히 앨리어싱을 억제하는 데 충분히 공격적이지 않으며  
100dB 이상의 감쇠를 갖는 매우 고품질의 필터가 필요하다는 놀라운 발견이 포함된다.  
또한, continuous 영역에서의 효과를 고려하고 결과를 적절하게 저역 통과 필터링함으로써  
pointwise 비선형성[5]으로 인한 aliasing에 대한 원칙적 솔루션을 제시한다.  
우리는 또한 정밀 검사 후에 1x1 conv.를 기반으로 하는 모델이 강력한 회전 등변 G를 생성한다는 것을 보여준다.  
  
모델이 보다 자연스러운 계층적 개선을 구현하도록 alasing이 적절히 억제되면 작동 모드가 크게 변경된다.  
이제 새로운 내부 표현에는 세부 사항을 기본 표면에 올바르게 부착할 수 있는 좌표계가 포함된다.  
이것은 비디오 및 애니메이션을 생성하는 모델에 대한 상당한 개선을 약속한다.  
새로운 StyleGAN3 생성기는 FID [26] 측면에서 StyleGAN2와 일치하지만 계산적으로 약간 더 무거워진다.  
몇몇 최근 연구는 주로 분류의 맥락에서 CNN에서 번역 등변의 부족을 연구했다.  
우리는 이 문헌에서 anti-aliasing 조치를 크게 확장하고 그렇게 하면 근본적으로 변경된 이미지 생성 동작을 유도한다는 것을 보여준다.  
그룹 등가 CNN은 변환 가중치 공유의 효율성 이점을 회전 및 스케일로 일반화하는 것을 목표로 한다.  
우리의 1x1 컨볼루션은 예를 들어 채널별 ReLU 비선형성 및 변조와 호환되는 연속 E(2)-equivariant 모델 [62]의 인스턴스를 볼 수 있다.  
GAN에 90º 회전 및 뒤집기 등변 CNN[16]을 적용하여 향상된 데이터 효율성을 보여준다.  
우리의 작업은 상호 보완적이며 효율성에 의해 동기가 부여되지 않는다.  
최근의 implicit 네트워크 기반 GAN은 유사한 1x1 conv.을 통해 각 픽셀을 독립적으로 생성한다.  
등변이지만 이러한 모델은 업샘플링 계층을 사용하지 않거나 얕은 antialiasing 되지 않은 계층을 구현하지 않기 때문에 텍스처 고정에 도움이 되지 않는다.  

## 2. Equivariance via continuous signal interpretation
CNNs에서 등변성에 대한 분석을 시작하기 위해 네트워크를 통해 흐르는 신호가 무엇인지에 대한 우리의 관점을 재고해보자. 
pixel grid에 데이터가 저장될 수 있지만, 신호를 직접적으로 나타내기 위해 이런 값을 순진하게 유지할 수는 없다.  
그렇게 하면 feature map의 내용을 0.5픽셀로 변환하는 것과 같은 사소한 작업을 고려하지 않게 된다.  
  
Nyquist-Shannon 샘플링 정리[51]에 따르면 규칙적으로 샘플링된 신호는 샘플링 속도의 0~반 사이의 주파수를 포함하는 연속 신호를 나타낼 수 있다.  
다양한 크기의 Dirac 임펄스의 규칙적인 격자로 구성된 2차원의 이산적으로 샘플링된 피쳐 맵 Z[x]를 고려해 보자. s는 샘플링 속도인 1/s 단위 간격으로 떨어져 있습니다. 이것은 무한한 2차원 값 그리드와 유사하다.  
  
Z[x] 및 s가 주어지면 Whittaker-Shannon 보간 공식[51]에 따르면 해당 연속 표현 z(x)는 이산적으로 샘플링된 Dirac 그리드 Z[x]를  
이상적인 interpolation filter φs로 convolution하여 얻을 수 있다. 즉, z(x) = (φs * Z)(x).  
∗는 연속 컨볼루션을 나타내고 φs(x) = sinc(sx0) · sinc(sx1)을 정의하는 신호 처리 규칙을 사용하여 sinc(x) = sin(πx)/ (πx).  
φs는 수평 및 수직 차원을 따라 s/2의 bandlimit을 가지므로 결과적인 연속 신호가 샘플링 속도 s로 나타낼 수 있는 모든 주파수를 캡처하도록 한다.  
연속 영역에서 이산 영역으로의 변환은 Z[x]의 샘플링 지점에서 연속 신호 z(x)를 샘플링하는 것에 해당하며,  
이는 "픽셀 중심"에 놓이도록 샘플 간격의 절반만큼 오프셋되도록 정의한다(그림 2 왼쪽 참조).  
이것은 2차원 Dirac comb IIIs 으로 곱셈으로 표현할 수 있다.  
<img src='https://user-images.githubusercontent.com/40943064/156923152-e23128ea-3365-4e94-b7c8-25ff7be31b46.png' width=400>
  
![image](https://user-images.githubusercontent.com/40943064/156923244-669442a0-5112-4b7d-9f0a-fdb3ab1e8142.png)




### 2.1 Equivariant network layers
연산 **f**는 아래 조건을 만족하는 경우 2D 평면의 공간 변환 **t**에 대해 등변이다.  
연속 도메인에서 상호교환가능(commute)하다(t o f = f o t). 
우리는 입력이 s/2에 bandlimitted될 때, 등변 연산이 출력 bandlimit s'/2의 주파수성분을 넘도록 생성하지 못함을 주목한다. 그렇지 않으면 충실한 이산 출력 표현이 존재하지 않는다.  
  
본 논문에서는 두가지 타입의 등변성에 대해 집중한다. (변환 / 회전). 
회전의 경우 stepctral 제약이 다소 엄격하다.  
: 이미지를 회전하는것은 spectrum을 회전하는 것에 상응하며 수평/수직 방향에서의 대역 제한을 보장하기 위해서  
: spectrum은 s/2 지름을 가지는 disc에 제한되어야 한다. 
downsampling을 위해 사용되는 bandlimiting과 마찬가지로 초기 네트워크 입력에도 적용된다.  
  
우리는 이제 전형적인 G 네트워크에서 원시적 연산들을 고려한다. (conv., upsampling, downsampling, nonlinearity.). 
일반성을 잃지 않고 우리는 단일 feature map에 작용하는 연산을 논의한다.(feature의 점별 선영 결합은 분석에 영향이 없다.). 
  
#### Convolution
Discrete kernel K를 가지는 표준 conv.를 고려해보자. 우리는 K를 sampling rate s를 가지고 입력 feature map와 동일한 grid에 존재한다고 해석할 수 있다.  
1) conv.의 commutativity.  
2) 동일 sampling rate s에 대한 이산화 -> 연속화(conv. with low-pass filter)는 identity operation이라는 사실  
의 이유로 Discrete-domain 연산은 **F**conv(Z) = K * Z이며 우리는 그에 상응하는 continuous 연산을 Eq.1로부터 얻을 수 있다.  
(identity operation : 항등작용소)  
![image](https://user-images.githubusercontent.com/40943064/157000736-aca79053-3b68-4afa-97c4-ad8f44ca4eda.png)  
다시말해, conv.는 연속적으로 이산화된 kernel을 연속적인 feature map 표현에 sliding함으로써 동작한다.  
이러한 conv.는 어떠한 새로운 주파수도 도입하지 않으므로, 변환과 회전 등변성에 대한 bandlimit 요구사항은 trivial하게 충족된다.  
Conv.는 마찬가지로 연속 도메인에서 변환과 commute 하고 이때문에 연산이 변환에 등변이다.  
회전 등변성에 대해서, 이산 kernel K는 방사적으로 대칭이다.  
(3.2절에서 symmetric 1 x 1 conv. kernel은 단순성에도 불구하고 등변 생성 네트워크를 위해 실행가능한 선택임을 보인다.)  

#### Upsampling and downsampling
이상적인 upsampling은 연속표현을 수정하지 않는다. 유일한 목적은 출력 sampling rate (s' > s)를 증가시켜 후속 레이어가 추가 contents를 도입할 수 있는 스펙트럼에서 헤드룸을 추가하는 것이다.  
번역과 회전 등변성은 업샘플링이 연속 도메인에서 등가 연산이 되는 것에서 직접 나타난다.  
fup(z) = z 과 함께, eq1.에 따른 discrete 연산은 <img src='https://user-images.githubusercontent.com/40943064/157023950-660792f6-b716-46d9-af68-71c31af36e50.png' width = 200> 이다. s, = ns를 정수 n으로 선택하는 경우, 이 연산은 Z를 0으로인 interleave하여 샘플링 rate를 높인 다음 이산화된 필터(<img src= 'https://user-images.githubusercontent.com/40943064/157030643-dadc1e08-36d1-400c-aae5-f8faed46ffd8.png' width = 150 >)로 컨볼루션하여 구현할 수 있다.
  
다운샘플링에서는 신호가 더 coarse한 이산화에 충실하게 표현될 수 있도록 z를 low-pass filter하여 출력 대역 한계 이상의 주파수를 제거해야 한다.  
연속 도메인에서의 연산은 fdown(z) 이며 여기서 이상적인 low-pass filter psi=s2phi는 
~ 수식 ~

#### Nonlinearity

## 3 Practical application to generator network
### 3.1 Fourier features and baseline simplifications (configs B–D)
### 3.2 Step-by-step redesign motivated by continuous interpretation
#### Boundaries and upsampling (config E)
#### Filtered nonlinearities (config F)
#### Non-critical sampling (config G)
Filter cutoff가 정확히 bandlimit에 설정된 critial sampling 방식은 antialiasing과 고주파 detail 유지 사이에 균형을 맞추기 때문에 많은 영상 처리 애플리케이션에 이상적이다[58]. 그러나 aliasing은 G의 등변성에 매우 해롭기 때문에 우리의 목표는 현저하게 다르다. 고주파 디테일이 출력 이미지와 따라서 고해상도 계층에서 중요하지만, 정확한 해상도가 처음에는 다소 임의적이라는 점을 고려할 때 초기 계층에서는 덜 중요하다.  
  
Aliasing을 억제하기 위해 cutoff 주파수를 fc = s/2 - fh로 낮추면 s/2 이상의 모든 alias 주파수가 stopband에 있도록 할 수 있다. 예를 들어 그림 4a에서 파란색 필터의 컷오프를 낮추면 주파수 응답이 왼쪽으로 이동하여 aliasing 주파수의 worst-case 감쇠가 6dB에서 40dB로 개선된다. 현재 동일한 수의 샘플을 사용하여 이전보다 느린 가변 신호를 표현하기 때문에 이 오버샘플링은 더 나은 antialiasing의 계산 비용으로 볼 수 있다. 실제로, G는 결국 교육 데이터와 일치하도록 선명한 이미지를 생성할 수 있어야 하기 때문에 우리는 고해상도 레이어를 제외한 모든 레이어에서 fc를 낮추기로 선택한다. 이제 신호에 공간 정보가 덜 포함되므로, 우리는 feature map의 수를 샘플링 속도 s 대신 fc에 반비례하도록 결정하는 데 사용되는 휴리스틱을 수정한다. 이러한 변경 사항(구성 G)은 변환 등변성을 더욱 개선하고 FID를 원래 StyleGAN2 아래로 밀어넣는다.  
![image](https://user-images.githubusercontent.com/40943064/157044287-b4d796a0-54e5-4bdf-b6a2-dbd95508acb5.png)

#### Transformed Fourier features (config H)
등변 G 레이어는 중간 feature에 도입된 기하학적 변환이 최종 이미지 zN으로 직접 전달되기 때문에 비정렬 및 임의 지향 데이터 세트에 매우 적합하다. 그러나 입력 피처는 계층 자체의 전역 변환을 도입하는 제한된 능력으로 인해res z0는 zN의 전역 방향을 정의하는데 중요한 역할을 한다. 이미지별로 방향이 달라지도록 하기 위해, G는 w를 기반으로 z0을 변환할 수 있는 능력을 가져야 한다. 이것은 입력 푸리에 기능에 대한 전역 변환 및 회전 매개 변수를 출력하는 학습된 아핀 레이어를 도입하도록 동기를 부여한다(그림 4b 및 부록 F). 계층은 정체성 변환을 수행하기 위해 초기화되지만 시간이 지남에 따라 유익할 때 메커니즘을 사용하는 방법을 학습한다. 구성 H에서 이것은 FID를 약간 개선한다.
![image](https://user-images.githubusercontent.com/40943064/157048029-cd3bcb92-f6ac-4b3e-958f-7170543908f3.png)

#### Flexible layer specifications (config T) 
#### Rotation equivariance (config R)

## 4 Results
#### Ablations and comparisons
#### Internal representations

## 5 Limitations, discussion, and future work
