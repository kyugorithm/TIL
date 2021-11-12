# AttentionGAN: Unpaired Image-to-Image Translation using Attention-Guided Generative Adversarial Networks

## 핵심요소  
• Attention-Guided GAN 제안  
몇 가지 loss 및 optimization 방법으로 attention 및 contents 마스크를 공동으로 근사  
(GAN의 학습을 안정화시켜 생성 이미지 품질 향상)  
  
• 차별적인 foreground 부분을 잘 인식하고 생성하며 초점이 맞지 않는 물체와 배경을 잘 보존하기 위해  
두 가지 새로운 attention guided generation scheme을 설계  
G/D는 다중 도메인 I2I 변환 작업을 개선하기 위해 다른 GAN에 유연하게 적용 가능  

## Method

### A. Attention-Guided Generation GAN**

**Attention-Guided Generation Scheme I.**  

Built-in attention mechanism이 있는 G를 통해 mapping을 학습   (G:x→[Ay, Cy]→G(x), y→[Ax, Cx]→F(y))
Ax, Ay : Attention Mask : Cx, Cy의 유효 영역에 대한 픽셀단위 강도를 정의
Cx, Cy : Contents Mask  
G(x), F(y) :생성된 이미지  
배경(static element)을 rendering 할 필요가 없으며 content 생성만 집중하므로 더 선명하고 사실적인 이미지를 합성 할 수 있다.  

그런 다음 입력 이미지 x, 생성된 주의 마스크 Ay 및 콘텐츠 마스크 Cy를 융합하여 대상 이미지 G(x)를 얻는다.  
이런 식으로 가장 구별되는 의미론적 객체와 이미지의 원하지 않는 부분을 disentangle할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/141480608-3d013429-36e0-47a3-aabf-80c4cfcbb0f2.png)
Attention guided G는 눈/입과같은 새롭게 생성해야하는 이미지 영역에만 focus를 해서 
그림 2를 예로 들면 주의 유도 생성기는 눈과 입과 같은 새로운 표현을 생성하는 역할을 하는 이미지 영역에만 초점을 맞추고 
머리카락, 안경, 옷 등은 그대로 둔다. A의 강도가 높을수록 표현을 변경하는 데 더 큰 기여를 한다.  
G 입력 : 3채널 이미지(x∈R H×W×3) / G 출력 : A(∈{0, ..., 1} H×W) & C(∈R H×W×3)
G(x) = Cy * Ay + x * (1 − Ay)

A는 변경된 일부 특정 영역에 더 집중하도록 하고 이를 C에 곱하면 선명한 컨텐츠와 불분명한 배경이 있는 이미지를 생성한다.  
배경은 real/fake 모두 유사하도록 수식을 구성한다.

1번 방식은 expression-to-expression 도메인이 크게 겹치는 작업에서 잘 수행된다.  
그러나 아래와 같이 horse2zebra 번역과 같은 복잡한 작업에서 사실적인 이미지를 생성할 수 없음을 관찰했다.  
![image](https://user-images.githubusercontent.com/40943064/141481883-ab4d714b-e0f1-4550-aa68-dc640d95d613.png)

단점은 세 가지가 있다.  
(i) A와 C는 하나의 네트워크에서 생성되므로 이미지의 품질이 저하될 수 있다.  
(ii) 전경을 변경하고 입력 이미지의 배경을 동시에 보존하기 위해 하나의 A만 생성한다.  
(iii) 전경 콘텐츠를 생성하는 데 유용한 콘텐츠를 선택하기 위해 하나의 C 마스크만 생성한다.   
위 단점을 해결하기 위해 그림 3과 같이 보다 발전된 Attention-guided generation 방식 II를 추가로 제안한다.  
![image](https://user-images.githubusercontent.com/40943064/141482036-ae6bcd24-643a-4e9e-82ee-a358a027b476.png)

### E. Implementation Details

**Attention-Guided Generation Scheme II.**  
제안하는 G는 위 그림과 같이 A와 C를 생성하기 위한 두 개의 sub-net으로 구성된다.  
1) 매개변수 공유 인코더(GE) : low-level 및 high-level deep feature 추출  
2) A 생성기(GA)
3) C 생성기(GC)
GA, GC 모두 고유 네트워크를 구성하여 방해하지 않도록 구성된다.  
1번 방식의 2번 단점(하나의 A만 생성하는)을 수정하기 위해 A생성기 GA는 n-1개의 전경 A와 1개의 배경 A를 생성하는것을 목표로 한다.  
이를 통해 제안 네트워크는 새로운 전경을 동시에 학습하고 입력 이미지의 배경을 보존할 수 있다.  
방식 II의 핵심 성공은 전경 및 배경 A를 생성하여 모델이 전경을 수정하고 동시에 입력 이미지의 배경을 보존할 수 있도록 하는 것이다.  
3번의 단점(하나의 C만 생성하는)을 수정하기 위해서 n-1개의 C와 x를 통해 n개의 C를 만든다.

**Network Architecture.**
공정한 비교를 위해 CycleGAN의 G를 사용하며 약간만 수정한다.  
Scheme I : RGB(3ch) 입력으로 A(1ch) 와 C(3ch) 출력  
Scheme II : RGB(3ch) 입력으로 n개 * A, n-1개 * C 출력
(u128, u64,c7s1-10)
uk : k 필터와 stride 1/2 / 3x3 fractional-strided-Convolution-InstanceNormReLU 레이어 
c7s1-k : k 필터와 stride 1 / 7x7 Convolution-InstanceNorm-ReLU 레이어  
(n = 10) 
제안하는 D에서는 A와 이미지를 입력으로 사용

**Training Strategy.**  
본 방법의 novelty는 학습 전략보다는 제안된 모델의 구조에 있다.  
따라서 공정한 비교를 위해 GAN/CycleGAN 의 표준 최적화 방법을 따른다.  
G에 비해 D의 속도를 늦추기 위해 우리는 CycleGAN을 따르고 D를 최적화하면서 objective를 2로 나눈다.  
학습중 모델을 안정화하기 위해 MSE를 사용한다.  
CycleGAN과 유사하게 생성 이미지 pool을 이용하여 D를 업데이트한다.
