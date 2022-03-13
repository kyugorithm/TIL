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
이제 위치 참조의 모든 근원을 성공적으로 제거하면 픽셀 좌표에 관계없이 세부 사항이 동등하게 잘 생성될 수 있으며,  
이는 차례로 모든 레이어에서 하위 픽셀 변환(및 선택적으로 회전)에 대한 연속 등가성을 적용하는 것과 같다.  
이를 달성하기 위해 StyleGAN2 G의 모든 신호 처리 측면에 대한 포괄적인 정밀 검사를 설명한다.  
우리의 기여에는 현재의 업샘플링 필터가 단순히 앨리어싱을 억제하는 데 충분히 공격적이지 않으며  
100dB 이상의 감쇠를 갖는 매우 고품질의 필터가 필요하다는 놀라운 발견이 포함된다.  
또한, continuous 영역에서의 효과를 고려하고 결과를 적절하게 저역 통과 필터링함으로써  
pointwise 비선형성[5]으로 인한 aliasing에 대한 원칙적 솔루션을 제시한다.  
우리는 또한 정밀 검사 후에 1x1 conv.를 기반으로 하는 모델이 강력한 회전 등변 G를 생성한다는 것을 보여준다.  
  
모델이 보다 자연스러운 계층적 개선을 구현하도록 alasing이 적절히 억제되면 작동 모드가 크게 변경된다.  
이제 새로운 내부 표현에는 세부 사항을 기본 표면에 올바르게 부착할 수 있는 좌표계가 포함된다.  
**이것은 비디오 및 애니메이션을 생성하는 모델에 대한 상당한 개선을 약속한다.**  
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
pixel grid에 데이터가 저장될 수 있지만, 신호를 직접적으로 나타내기 위해 이런 값을 순수하게 유지할 수는 없다.  
그렇게 하면 feature map의 내용을 반으로 변환하는 것과 같은 사소한 작업을 고려하지 않게 된다.  
  
Nyquist-Shannon 샘플링 정리[51]에 따르면 규칙적으로 샘플링된 신호는 샘플링 속도fs에 대해 0~fs/2 사이를 포함하는 연속 신호를 나타낼 수 있다.  
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

#### Discrete and continuous representation of network layers
실제적 NN은 이산 샘플링된 feature map에서 동작한다. 이산 feature map에 대해 동작하는 연산 **F**(conv., nonlinearity, etc.) : Z' = **F**(Z)를 고려해보자  
Feature map은 상응하는 연속 도메인에서의 counterpart를 가지므로 우리는 상응하는 mapping도 가진다. z' = **f**(z). 
그러면, 한 도메인에서 명시되는 연산은 다른 도메인에서 상응하는 연산을 수행하는것으로 볼 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/158046818-eb8dfa7e-65b3-4520-ad78-23749b3941a6.png)
(s, s' : 입력/출력 sampling rate)




### 2.1 Equivariant network layers
연산 **f**는 아래 조건을 만족하는 경우 2D 평면의 공간 변환 **t**에 대해 등변이다.  
연속 도메인에서 상호교환가능(commute)하다(t o f = f o t). 
우리는 입력이 s/2에 bandlimitted될 때, 등변 연산이 출력 bandlimit s'/2의 주파수성분을 넘도록 생성하지 못함을 주목한다. 그렇지 않으면 충실한 이산 출력 표현이 존재하지 않는다.  
  
본 논문에서는 두가지 타입의 등변성에 대해 집중한다. (변환 / 회전). 
회전의 경우 spectral 제약이 다소 엄격하다.  
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
앞 섹션으로부터 얻은 이론적 아이디어를 실제로 잘 구성된 StyleGAN2 G에 대해 translation과 rotation에 완전히 등변성이 존재하도록 변환하여 적용한다.  
우리는 필요한 변화를 단계별로 도입하여 Figure3에 각각의 영향을 평가한다. D는 우리의 실험에서 고정한다.  
  
StyleGAN2 G는 두개 파트로 구성되어있다. 먼저, mapping network는 초기 normally distributed latent를 중간 latent code w ~ _W_ 로 변환한다.  
그리고 synthesis network G는 학습된 4 X 4 X 512 상수 Z0로부터 시작하여 N개 연속적인 레이어를 적용하여 ZN = G(Z0, w)를 생성한다.  
레이어는 각 해상도에서 두 레이어를 실행하고 각 업샘플링 후 feature map의 수를 절반으로 줄이는 엄격한 2배 upsampling 스케줄을 따른다.  
추가로 ,StyleGAN2는 skip connection, mr, path length regularization을 적용한다.  
  
목표는 연속 신호에 대해 G의 모든 레이어가 등변성이 되도록 해서 모든 상세한 detail이 local 주변에 대한 더 coarse한 feature와 함께 변환이 되도록 한다.  
이것이 성공하면, 전체 네트워크는 비슷하게 등변하게 된다.  
즉, 연속 입력 z0에 적용되는 변환 t(변환 및 회전)과 관련하여 합성 네트워크의 연속 작동 g를 등변으로 만드는 것을 목표로 한다. : **g**(**t**[z0];**w**) = **t**[**g**(z0;**w**)]. 
다양한 구조적 변화들과 실질적 근사의 영향을 평가하기 위해 등변성을 얼마나 잘 구현했는지를 측정하는 방법이 필요하다.  
Translation 등변성의 경우, 합성 네트워크의 입력과 출력을 임의의 양으로 변환하여 얻은 두 이미지 세트 사이의 PSNR을 Zhang의 정의와 유사하게 사용한다.  
![image](https://user-images.githubusercontent.com/40943064/158053255-07067c2c-bb1e-4bd9-98cf-78a256f2dbed.png)  
w의 다른 무작위 선택에 해당하는 각 이미지 쌍은 상호 유효한 영역 V 내의 정수 픽셀 위치 p에서 샘플링된다.  
색상 채널 c는 독립적으로 처리되며 생성된 이미지의 동적 범위 -1 ~ +1은 Imax = 2를 제공한다.  
연산자 tx는 정수 오프셋의 분포 X 2에서 도출된 2D 오프셋 x로 공간 변환을 구현한다.  
우리는 U(0˚ , 360˚ )에서 그린 회전각으로 회전에 대한 유사한 메트릭 EQ-R을 정의한다.  
Appendix E는 구현 세부 사항을 제공하며, 함께 제공되는 비디오는 다양한 dB 값의 실질적인 관련성을 강조한다.  

### 3.1 Fourier features and baseline simplifications (configs B–D)
입력 z0의 정확한 연속 translation과 rotation을 용이하게 하기 위해, 우리는 StyleGAN2의 trained input constant를 fourier feature로 대체한다.  
Fourier feature는 공간적으로 무한한 map을 자연스럽게 정의할 수 있는 장점이 있다.  
우리는 원래의 4×4 입력 해상도와 일치하는 원형 주파수 대역 fc = 2 내에서 균일하게 주파수를 샘플링하고 학습 과정 동안 고정 상태를 유지한다.  
이 변경(왼쪽 그림 3의 A와 B 구성)은 FID를 약간 개선하며 결정적으로 연산자 t를 근사화할 필요 없이 등분산 메트릭을 계산할 수 있다.  
이 기준 아키텍처는 등변성과 거리가 멀다.  
함께 제공되는 비디오는 입력 feature가 원래 위치에서 변환되거나 회전할 때 출력 이미지가 급격히 악화된다는 것을 보여준다.  
  
다음으로, 픽셀당 노이즈 입력은 자연스러운 변환 계층이라는 우리의 목표와 강하게 상충되기 때문에 제거한다. 즉, 각 형상의 정확한 하위 픽셀 위치는 기본 거친 형상에서 독점적으로 상속된다. 이 변경(구성 C)은 대략 FID 중립이지만, 고립되어 고려될 때 등변성 메트릭을 개선하지 못한다.

설정을 더욱 단순화하기 위해 Karas가 권장하는 대로 mapping network 깊이를 줄이고 mixing regularization과 path length regularization을 비활성화한다. 마지막으로 ouput skip connection도 제거한다. 이것들의 이점이 대부분 학습 중 gradient 크기 dynamics와 관련이 있다고 가정하고 각 conv. 전에 간단한 정규화를 사용하여 근본문제를 보다 직접적으로 해결한다. 우리는 학습 중 모든 픽셀 및 feature map에 대한 지수 이동 평균을 추적하고 feature map을 sqrt(sigma^2) 로 나눈다. 실제로, 우리는 효율을 향상시키기 위해 분할을 컨볼루션 weight를 굽는다(?). 이러한 변경 사항(구성 D)은 FID를 StyleGAN2 수준으로 되돌린 반면 translation의 등변성을 약간 개선시킨다.  

### 3.2 Step-by-step redesign motivated by continuous interpretation
#### Boundaries and upsampling (config E)
우리의 이론은 대상 캔버스 주위에 고정 크기 여백을 유지하고 각 레이어 다음에 확장된 캔버스로 자르는 방식으로 근사한 feature map에 대한 무한한 공간 범위를 가정한다. 이 명시적 확장은 border padding이 절대 이미지 좌표를 내부 표현으로 유출하는 것으로 알려져 있기 때문에 필요하다. 실제로는 10픽셀 여백이면 충분하다. 추가 증가는 결과에 눈에 띄는 영향을 미치지 않습니다.

이론적 모델에 동기를 부여하여 bilinear 2x upsampling 필터를 이상적인 low-pass filter에 대한 더 나은 근사값으로 대체한다. 크기가 n = 6인 비교적 큰 kaiser window를 가진 windowed sing filter를 사용한다. 즉, 각 출력 픽셀은 upsampling에서 6개 입력 픽셀의 영향을 받고 각 입력 픽셀은 다운샘플링에서 6개 출력 픽셀에 영향을 준다. Kaiser window는 **translation band**와 **attenuation**을 명시적으로 제어할 수 있기 때문에 우리의 목적에 특히 좋은 선택이다(그림 4a). 이 섹션의 나머지 부분에서는 translation band를 명시적으로 지정하고 Kaiser의 원래 공식(부록 C)을 사용하여 나머지 매개변수를 계산한다. 지금은 critical sampling을 선택하고 필터 컷오프 = s/2, 즉 정확히 대역 제한 및 전이 대역 √c 반폭 fh = ( 2 − 1)(s/2)로 설정한다. 섹션 2의 정의에 따라 샘플링 속도 s는 픽셀 단위의 캔버스 너비와 같다는 것을 기억한다.  
Boundary와 upsampling(구성 E)의 개선된 처리는 더 나은 translation equivariance를 이끈다. 그러나 FID는 16% 낮아진다. Feature map에 포함될 수 있는 항목을 제한하기 시작했기 때문일 수 있다. 추가 ablation(그림 3, 오른쪽)에서 작은 resampling filter(n = 4)는 translation equivariance를 손상시키는 반면 큰 필터(n = 8)는 주로 학습 시간을 증가시킨다.
  
#### Filtered nonlinearities (config F)
비선형성에 대한 우리의 이론적 처리는 일부 배율 m에 대해 m x upsampling과 m x downsampling 사이에서 누출되는 각 ReLU(또는 일반적으로 사용되는 다른 비선형성)를 wrapping 해야 한다. 또한 신호가 대역 제한되어 upsampling 및 convolution 순서를 전환할 수 있으므로 일반 2 x upsampling과 linearity와 관련된 후속 m x upsampling을 단일 2m x upsampling으로 융합할 수 있다. 실제로 m = 2이면 충분하므로(그림 3, 오른쪽) EQ-T(구성 F)가 다시 향상된다. upsample-LReLU-downsample 시퀀스를 구현하는 것은 현재 DL 프레임워크에서 사용할 수 있는 기본 요소를 사용하여 효율적이지 않으므로 이러한 작업을 결합하는 사용자 지정 CUDA 커널을 구현하여 10배 빠른 훈련과 상당한 메모리 절약으로 이어진다.

#### Non-critical sampling (config G)
Filter cutoff가 정확히 bandlimit에 설정된 critial sampling 방식은 antialiasing과 고주파 detail 유지 사이에 균형을 맞추기 때문에 많은 영상 처리 애플리케이션에 이상적이다[58]. 그러나 aliasing은 G의 등변성에 매우 해롭기 때문에 우리의 목표는 현저하게 다르다. 고주파 디테일이 출력 이미지와 따라서 고해상도 계층에서 중요하지만, 정확한 해상도가 처음에는 다소 임의적이라는 점을 고려할 때 초기 계층에서는 덜 중요하다.  
  
Aliasing을 억제하기 위해 cutoff 주파수를 fc = s/2 - fh로 낮추면 s/2 이상의 모든 alias 주파수가 stopband에 있도록 할 수 있다. 예를 들어 그림 4a에서 파란색 필터의 컷오프를 낮추면 주파수 응답이 왼쪽으로 이동하여 aliasing 주파수의 worst-case 감쇠가 6dB에서 40dB로 개선된다. 현재 동일한 수의 샘플을 사용하여 이전보다 느린 가변 신호를 표현하기 때문에 이 오버샘플링은 더 나은 antialiasing의 계산 비용으로 볼 수 있다. 실제로, G는 결국 교육 데이터와 일치하도록 선명한 이미지를 생성할 수 있어야 하기 때문에 우리는 고해상도 레이어를 제외한 모든 레이어에서 fc를 낮추기로 선택한다. 이제 신호에 공간 정보가 덜 포함되므로, 우리는 feature map의 수를 샘플링 속도 s 대신 fc에 반비례하도록 결정하는 데 사용되는 휴리스틱을 수정한다. 이러한 변경 사항(구성 G)은 변환 등변성을 더욱 개선하고 FID를 원래 StyleGAN2 아래로 밀어넣는다.  
![image](https://user-images.githubusercontent.com/40943064/157044287-b4d796a0-54e5-4bdf-b6a2-dbd95508acb5.png)

#### Transformed Fourier features (config H)
등변 G 레이어는 중간 feature에 도입된 기하학적 변환이 최종 이미지 zN으로 직접 전달되기 때문에 비정렬 및 임의 지향 데이터 세트에 매우 적합하다. 그러나 입력 피처는 계층 자체의 전역 변환을 도입하는 제한된 능력으로 인해res z0는 zN의 전역 방향을 정의하는데 중요한 역할을 한다. 이미지별로 방향이 달라지도록 하기 위해, G는 w를 기반으로 z0을 변환할 수 있는 능력을 가져야 한다. 이것은 입력 푸리에 기능에 대한 전역 변환 및 회전 매개 변수를 출력하는 학습된 아핀 레이어를 도입하도록 동기를 부여한다(그림 4b 및 부록 F). 계층은 정체성 변환을 수행하기 위해 초기화되지만 시간이 지남에 따라 유익할 때 메커니즘을 사용하는 방법을 학습한다. 구성 H에서 이것은 FID를 약간 개선한다.
![image](https://user-images.githubusercontent.com/40943064/157048029-cd3bcb92-f6ac-4b3e-958f-7170543908f3.png)

#### Flexible layer specifications (config T) 
변경 사항으로 등분산 품질이 상당히 개선되었지만 첨부된 비디오에서 보여주듯이 일부 눈에 보이는 아티팩트가 여전히 남아 있다. 자세히 살펴보면 필터의 attenuation(구성 G에 대해 정의됨)이 여전히 최저 해상도 레이어에 충분하지 않은 것으로 나타났다. 이러한 레이어는 bandlimit 근처에서 풍부한 주파수 콘텐츠를 갖는 경향이 있어 aliasing을 완전히 제거하기 위해 매우 강력한 attenuation이 필요하다.

지금까지 filter cutoff fc 및 half width fh에 대한 단순한 선택과 함께 StyleGAN2의 엄격한 sampling rate progression을 사용했지만 반드시 그럴 필요는 없다. 레이어별로 이러한 매개변수를 자유롭게 specification할 수 있다. 특히, 정지 대역의 감쇠를 최대화하기 위해 fh가 가장 낮은 해상도 계층에서는 높지만, 학습 데이터의 고주파 세부 정보를 일치시킬 수 있도록 가장 높은 해상도 계층에서는 낮았으면 한다. 

그림 4c는 끝에 두 개의 임계적으로 샘플링된 전체 해상도 레이어가 있는 14레이어 G에서 필터 매개변수의 진행 예를 보여준다. Cutoff frequency는 첫 번째 계층의 fc = 2에서 첫 번째 critical sampling layer의 fc = sN=2까지 기하학적으로 증가한다. ft,0 = 2^2.1에서 시작하도록 허용 가능한 최소 저지대역 주파수를 선택하고 기하학적으로 증가하지만 차단 주파수보다 느리다. 테스트에서 마지막 레이어의 저지대역 목표는 ft = fc x 2^0.3이지만 첫 번째 critical 샘플링 레이어에서 진행이 멈춘니다. 다음으로, 출력 해상도를 초과하지 않고 다음 2승으로 반올림하여 최대 ft의 주파수를 수용하도록 각 레이어에 대한 샘플링 속도 s를 설정한다. 마지막으로, aliasing 주파수의 attenuation을 최대화하기 위해 translation halfband를 fh = max(s/2, ft) - fc로 설정한다. 그 결과 향상은 ft와 s=2 사이에 얼마나 많은 여유 공간이 남아 있느냐에 따라 달라진다. 극단적 예로, 이 방식을 사용하면 첫 번째 계층 stopband attenutaion이 42dB에서 480dB로 개선된다.

새 계층 specification은 translation 등변성(구성 T)을 다시 개선하여 나머지 아티팩트를 제거한다. 추가 ablation(그림 3, 오른쪽)은 ft,0이 등분산 품질을 위해 학습 속도를 교환하는 효과적인 방법을 제공함을 보여준다. 레이어 수는 이제 출력 해상도에 직접적으로 의존하지 않는 자유 매개변수이다. 사실, 우리는 N의 고정된 선택이 여러 출력 해상도에서 일관되게 작동하고 학습률과 같은 다른 하이퍼파라미터가 더 예측 가능하게 동작한다는 것을 발견했다. 이 문서의 나머지 부분에서는 N = 14를 사용한다.

#### Rotation equivariance (config R)
두 가지 변경 사항이 있는 네트워크의 rotation equivariant 버전을 얻는다. 먼저, 3x3 conv.를 모든 레이어에서 1x1로 교체하고 feature map의 수를 두 배로 늘려 줄어든 용량을 보상한다. Upsampling 및 downsampling 작업만 이 구성의 픽셀 간에 정보를 퍼뜨린다. 둘째, sinc 기반 downsampling 필터를 동일한 kaiser scheme(appendix C)을 사용하여 구성하는 radially symmetric jinc 기반 필터로 교체한다. 우리는 학습 데이터의 잠재적으로 비방사성 스펙트럼을 일치시키는 것이 중요한 두 개의 critically 샘플링된 layer를 제외한 모든 layer에 대해 이를 수행한다. 이러한 변경 사항(config R)은 각 계층에 훈련 가능한 매개 변수가 56% 적더라도 FID를 손상시키지 않고 EQ-R을 개선한다.

우리는 또한 이 구성에서 추가적인 안정화 트릭을 사용한다. 학습 초기에는 gauss filter를 사용하여 D가 보는 모든 이미지를 흐리게 한다. σ = 10 픽셀로 시작하여 처음 20만 개의 이미지에서 0으로 이동한다. 이는 가 초기에 고주파수에 지나치게 집중하는 것을 방지한다. 이 트릭이 없으면 구성 R은 G가 때때로 작은 지연으로 높은 주파수를 생성하는 방법을 학습하여 D의 작업을 단순화하기 때문에 조기에 collape되기 쉽다.

## 4 Results
Our alias-free generator architecture contains implicit assumptions about the nature of the training data, and violating these may cause training difficulties. Let us consider an example. Suppose we have black-and-white cartoons as training data that we (incorrectly) pre-process using point sampling [44], leading to training images where almost all pixels are either black or white and the edges are jagged. This kind of badly aliased training data is difficult for GANs in general, but it is especially at odds with equivariance: on the one hand, we are asking the generator to be able to translate the output smoothly by subpixel amounts, but on the other hand, edges must still remain jagged and pixels only black/white, to remain faithful to the training data. The same issue  can also arise with letterboxing of training images, low-quality JPEGs, or retro pixel graphics, where the jagged stair-step edges are a defining feature of the aesthetic. In such cases it may be beneficial for the generator to be aware of the pixel grid. In future, it might be interesting to re-introduce noise inputs (stochastic variation) in a way that is consistent with hierarchical synthesis. A better path length regularization would encourage neighboring features to move together, not discourage them from moving at all. It might be beneficial to try to extend our approach to equivariance w.r.t. scaling, anisotropic scaling, or even arbitrary homeomorphisms. Finally, it is well known that antialiasing should be done before tone mapping. So far, all GANs—including ours—have operated in the sRGB color space (after tone mapping). Attention layers in the middle of a generator [68] could likely be dealt with similarly to non-linearities by temporarily switching to higher resolution – although the time complexity of attention layers may make this somewhat challenging in practice. Recent attention-based GANs that start with a
tokenizing transformer (e.g., VQGAN [18]) may be at odds with equivariance. Whether it is possible to make them equivariant is an important open question.
#### Ablations and comparisons
#### Internal representations

## 5 Limitations, discussion, and future work
