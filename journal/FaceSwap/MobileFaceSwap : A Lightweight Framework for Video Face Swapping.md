## Abstract
최신 FS 결과는 훌륭하지만 계산량이 많아 모바일 활용 및 실시간 어플리케이션이 어렵다.  
ID에 따라 model parameter를 동적으로 조정하여 인물에 구애받지 않는 FS를 위한 IDN(Identity-aware Dynamic Network)을 제안한다.  
특히 weight prediction 및 modulation를 포함한 두 가지 dynamic neural network 기술을 도입하여 효율적인 IIM(Identity Injection Module)을 설계한다.  
IDN을 업데이트하고 주어진 임의 target에 대하여 fs에 적용한다.  
50만개 파라미터, 프레임당 0.33 GFLOPs만 사용하여 모바일 실시간 비디오 페이스 스왑이 가능하다.  
안정적인 학습을 위해 knowledge distillation 기반 방법을 도입하고, loss reweigting 모듈을 사용하여 더 나은 합성 결과를 얻는다.  
방법은 teacher model 및 SOTA와 유사한 결과를 달성한다.  

## 1. Introduction
기존 FS 방법론은 많은 매개 변수와 높은 계산 비용을 수반한다.  
1) FaceShifter : 두 단계로 구성되어 있으며 첫 단계에만 거의 421M의 매개 변수와 97.4G FLOP가 있다.  
2) FSGAN : 226M 이상의 매개 변수와 총 2440G FLOP를 갖는 보다 복잡하다.  
3) SimSwap : 상대적으로 효율적이지만 107M 매개 변수와 55.7G FLOP를 가지고 있다.  

위 방법은 용량과 계산량으로 인해 모바일이나 실시간 어플리케이션이 활용할 수 없다.  
문제를 해결하기 위한 자연스러운 아이디어는 모델 compression 기술을 사용하여 경량 네트워크를 생성하는 것이다.  
그러나 channel pruning을 적용하고 네트워크를 축소하여 SimSwap 또는 FaceShifter를 크게 압축하면 쾌적한 FS 결과를 얻는 것이 번거롭다는 것을 관찰한다.  
특히, 생성된 이미지 중 일부는 아티팩트가 있거나, 제한된 네트워크 용량으로 ID 정보를 주입하기에 충분하지 않기 때문에 생성된 이미지 ID가 소스 이미지와 비슷하지 않을 수 있다.  
Subject-aware FS 기술(Perov et al. 2020)에서 영감을 받아 소스 이미지를 수정하고 특정 ID에 대한 경량 모델을 학습하면 더 나은 스왑 이미지를 얻을 수 있다는 사실도 발견했다.  
따라서 subject-agnostic 및 실시간 얼굴 교환을 달성하기 위해 직관적인 아이디어는 **ID에 따라 모델 파라미터를 조정**하는 것이다.  
  
Dynamic neural network 기법에 영감을 받아 실시간 FS를 위한 경량 IDN을 제안한다.  
ID 정보를 효율적으로 주입하기 위해 IDN의 매개 변수를 조정하기 위해 weight 예측및 변조를 사용하여 IIM도 설계한다.  
IDN은 ID 정보가 주어지면 업데이트되며, 모든 대상 이미지 또는 비디오에 대한 빠른 FS를 달성한다.  
우리의 방법은 이러한 설계를 사용하여 매개 변수와 계산을 크게 줄이고 다른 최첨단 방법과 유사한 결과를 얻을 수 있다.  
제안된 IDN은 입력 크기가 224일 때 비디오 FS를 위해 프레임당 0.50M 매개 변수와 0.33G FLOPs만 갖는다.(파라미터 및 연산 100배 이상 절약)  
Quantization과 같은 추가 최적화 없이, 미디어와 함께 휴대폰에서 실시간 FS를 할 수 있다.  
Tek Dimensity 1100 칩 기준 26 FPS를 달성한다.  

일반적으로 FS를 위한 학습은 불안정하며, 생성이미지에는 아티팩트가 있을 수 있다.  
Knowledge distillation을 사용하여 FS을 쌍으로 된 학습 작업으로 이전하면 보다 안정적인 학습 프로세스를 달성하고 더 나은 결과를 얻을 수 있다는 것을 알 수 있다.  
따라서, 우리는 teacher로서 잘 학습된 네트워크를 사용하고 학생으로서 경량 네트워크를 학습시킨다.  
그러나 teacher는 생성된 이미지가 소스 이미지와 동일성 유사성이 낮은 것과 같은 일부 실패 사례도 생성할 수 있다.  
Student는 이러한 실패 사례에 의해 misguide될 수 있으며 차선의 결과를 산출할 수 있다.  
본 논문에서는 이 문제를 완화하기 위해 loss reweighting 모듈을 제안한다.  
특히, 우리는 teacher 품질을 평가하고 동시에 distillation loss의 weight를 adaptive하게 조정한다.  
이러한 방식으로 student는 더 나은 teacher 출력으로부터 배울 수 있으므로 더 적은 아티팩트와 더 높은 identity 유사성으로 더 나은 생성된 결과를 얻을 수 있다.  


**논문의 기여**  

1. 비디오 FS를 위한 실시간 프레임워크 제안 : 파라미터(0.50M) 계산량(0.33G FLOPs), 모바일 속도(26FPS)  

2. IDN를 구축하기 위해 weight prediction 및 modulation을 활용하여 효율적인 ID 정보 주입을 하는 IIM을 제시  

3. 학습 프로세스를 안정화시키기 위해 knowledge distillation 프레임워크를 사용하여 제안된 네트워크를 학습하고 생성된 결과를 질적, 양적으로 개선하기 위해 loss reweigting 모듈을 제안  

## 2. Related Work
**Face swapping.**
DeepFace-Lab은 subject-aware FS를 위해 Encoder-Decoder를 학습시키고 매력적인 결과를 달성했지만 특정 ID에 대한 FS만 가능하다.  
최근에는 보다 편리하게 사용할 수 있는 Subject-agnostic 방법이 추가로 제안되고 있다.  
크게 source oriented 및 target oriented 두 가지로 나눌 수 있다.  
1) source oriented. 
src의 포즈와 표현을 target 이미지로 전송한 다음 blending을 통해 스왑된 얼굴 이미지를 얻는다.  
Nirkin은 소스 이미지를 대상 이미지와 정렬하기 위해 3DMM을 사용한다.  
FSGAN은 얼굴 재현 및 혼합 프로세스를 구현하기 위해 두 가지 모델을 훈련시킨다.  
그러나 이러한 방법은 불안정하며 부자연스러운 색상과 같은 아티팩트를 생성하기 쉽다.  

2) target oriented
src와 trg의 feature를 혼합하여 FS을 얻는다.  
FaceShifter는 2단계 프레임워크를 활용한다. 첫 번째 단계는 FS를두 번째 단계는 occlusion 처리를 위한 것이다.  
SimSwap은 AdaIN을 활용하여 대상 피쳐 맵에 ID 정보를 주입한다.  
Face-Controller는 3DMM 계수를 기반으로 한 얼굴 표현과 스타일 및 아이덴티티 임베딩을 제안하여 FS보다 더 많은 속성 편집을 달성할 수 있다.  
HifiFace는 3DMM 계수를 사용하여 FS를 위해 src의 얼굴 모양을 보존한다.  
그러나 위의 방법은 모두 계산량과 용량이 매우 크다.  

**Dynamic neural networks.**
추론 중에 구조나 parameter를 입력에 적응시켜 계산 효율을 높이는 네트워크이다.  
De Brandere에 의해 처음 제안되었다.  
Style transfer, SR, i2i translation과 같은 다른 응용 프로그램에 적용되었다.  

**Knowledge distillation.**
Teacher 네트워크에서 더 작은 student 네트워크로 지식을 전달하기 위해 제안되었으며, 모델 압축에 널리 사용된다.  
최근방법은 지식 증류를 사용하여 이미지 간 변환을 위해 GAN을 압축한다.  
이러한 방법은 또한 지식 증류를 활용하여 짝을 이루지 않은 훈련 과제를 쌍으로 학습하여 훈련 안정성을 향상시킬 수 있음을 확인했다.  
따라서 얼굴 교환에 지식 증류를 도입한다.  

## 3. Method
먼저 ID 주입 모듈(IIM), IDN(ID-aware Dynamic Network), weakly semantic fusion module에 대한 세부 정보를 포함하여 MobileFaceSwap의 네트워크 아키텍처를 설명한다.  
그런 다음, 학습 안정성 문제와 합성을 더 잘 교환된 결과를 해결하기 위해 knowledge distillation 및 loss reweigting 모듈을 도입한다. (전체적인 프레임워크 : Fig2)  

![image](https://user-images.githubusercontent.com/40943064/179921550-bfc62cd6-ebf6-4f5b-bf7a-3eac454c9cac.png)  

**Network Architecture**
아키텍처는 두 개의 신경망을 포함한다.  
1) IIN(ID Injection Network) : 필요한 매개 변수를 얻기 위해 여러 개의 IIM이 있는 구조  
2) IDN(ID-aware Dynamic Network) : 추론을 위한 경량 네트워크   

ArcFace에 의한 src의 ID 표현을 고려할 때, IIM에는 IDN에 id 정보를 주입하는 두 가지 dynamic network 기술이 포함되어 있다.  
주입을 마치면 IDN을 사용하여 임의의 대상 이미지 또는 비디오와 얼굴을 교환할 수 있다.  

IDN은 U-Net에서 표준 convolution을 depthwise/pointwise convolution으로 대체함으로써 단순화된다.  
주어진 src에 따라 IDN의 parameter를 수정하기 위해, depthwise/pointwise convolution에 대한 weight prediction 및 modulation을 도입한다.  
Cin(입력채널), Cout(출력채널), K(커널크기)  
아래와 같이 ID 임베딩 zid를 입력으로 하여 depthwise convolution 레이어의 weight를 예측한다.  
<img src = "https://user-images.githubusercontent.com/40943064/179923816-51d03a72-d29f-4a93-aeca-dd3ca0f8a276.png" width = 120>  
1) Wd ∈ R^(Cin x 1 x K x K) : depthwise convolution layer. 
2) Fp : IIM의 conv. layer를 몇개 포함하는 prediction module  

Cout은 일반적으로 K x K 보다 정보량이 크기 때문에 pointwise convolution weight Wp(R^(Cin x Cout x 1 x 1))를 예측하는것은 더 많은 파라미터가 필요하다. 
마찬가지로, 우리는 그것이 weight modulation을 사용하여 pointwise convolution 레이어의 weight에 ID 정보를 주입함으로써 더 나은 결과를 얻을 수 있다는 것을 관찰한다.  
posintwise convolution의 (Wp:origin, Wp hat:modulation, Wp tilde:demodulation) weight이며 i, j, k는 input/output feature map과 convolution의 공간적 footprint를 명시한다.  
<img src = "https://user-images.githubusercontent.com/40943064/179928879-2476524e-4dc5-4862-a35f-5f680b82584d.png" width = 350>  
Fm : 몇개의 FC를 포함하는 IIM의 변조모듈  
IIM을 적용함으로써, IDN은 subject-agnostic FS를 달성할 수 있고 0.413M 파라미터를 포함하고 0.328G FLOPs만 계산한다.  

**Weakly-semantic fusion module**  
생성이미지 배경과 머리카락을 대상 이미지와 동일하게 유지하는 것은 어렵다. 이 문제는 비디오 FS에 대한 jitter를 유발하기도 한다.  
보통 이 문제는 face segmentation과 같은 계산 집약적인 후처리를 추가하면 해결할 수 있다.  
본 논문에서는 target 이미지 배경을 병합하기 위한 weakly-semantic fusion module을 제안한다.  
IDN의 feature map을 재사용하여 weak fusion mask를 예측한다.  
Semantic fusion module은 0.083M 매개 변수와 0.005G FLOP만 포함한다.  
이 모듈은 매우 가벼운 반면 예측된 융합 마스크는 그림 2에서 입증한 바와 같이 꽤 훌륭하다.  
비디오 FS를 위한 전체 네트워크를 구축했는데, 이는 0.495M 매개 변수를 가지고 있으며 입력 크기가 224일 때 총 0.333G FLOPs가 필요하다.

**Training Objectives**  
FS를 학습하려면 생성된 결과가 FS의 정의를 충족하도록 보장하기 위해 여러가지 loss가 필요하다. 이러한 서로 다른 손실의 경쟁은 제약 조건에 대해 쌍으로 구성된 GT가 없기 때문에 학습을 불안정하게 하고 아티팩트를 생성하기가 더 쉬워진다.  
본 논문에서는 knowledge distillation 프레임워크를 도입하여 FS를 쌍으로 된 학습으로 전환한다.  
Teacher로서 잘 훈련된 FS 네트워크와 student로서 제안된 네트워크를 고려할 때, 우리는 다음과 같이 학생 출력 Ig와 교사 출력 I0g 사이의 **L1** loss와 perceptual loss를 활용한다.  
![image](https://user-images.githubusercontent.com/40943064/179930376-6583164c-aea5-4bc5-8552-e155b582dc7c.png)  
본 학습은 knowledge distillation에 의해 더 안정적인 학습과 더 나은 합성 결과를 얻을 수 있다.  

하지만, teacher 모델은 완벽하지 않고 몇몇 나쁜 사례들이 teacher 출력에서 발견될 수 있다. 구체적으로, 우리는 이러한 failure case를 크게 두 가지 범주의 페이스 스왑으로 나눈다.  
1) 일부 출력은 src ID를 잘 표현하지 못한다.  
2) 일부 출력은 noise및 지저분한 이마와 같은 부자연스러운 결과나 아티팩트를 가질 수 있다.  

만약 우리가 eq. 3의 각 teacher 출력에 동일한 가중치를 할당한다면, student 네트워크는 또한 이러한 나쁜 사례를 생성하는 방법을 배울 것이다.  
본 논문에서는 이 문제를 완화하기 위해 loss reweighting module을 제안한다.  
각 teacher 출력에 대한 id similarity와 이미지 품질을 고려한다.  
구체적으로, 우리는 id 유사성을 측정하기 위해 teacher 출력의 id 표현과 src 사이의 cosine distance의 제곱을 사용한다.  
그러나 이미지의 품질을 평가하는 것은 중요하지 않다. 학습 과정 중 변환 결과가 점차 좋아지는 것을 관찰하기 때문에, 교사 출력의 이미지 품질을 적절하게 평가하기 위해 teacher 학습 과정에서의 완료된 반복 비율에 따라 각 교사 출력을 0에서 1 사이의 점수로 할당한다.  
그 후, ResNet-18을 사용하여 L2 손실로 감독함으로써 이러한 점수를 회귀시킨다.  
마지막으로, teacher 출력의 이미지 품질을 평가하기 위해 이 모델 Q를 사용한다.  
최종 distillation loss reweigting coefficeint ⍺ 는 다음과 같이 계산된다.  

<img src = "https://user-images.githubusercontent.com/40943064/179931495-a6a53a22-c0e6-46f5-b1f5-dce796dd97c8.png" width = 500>  

z'id : teacher output의 id vector.  
Loss reweighting module을 도입함으로써 생성이미지와 src 간의 ID 유사성을 향상시킬 수 있을 뿐만 아니라 결과품질을 향상시킬 수 있다.  
Distillation loss를 사용하여 teacher knowledge를 student에 전달하지만, id 대한 감독은 불충분하다. id 유사성에 대한 정량적 결과는 교사에 비해 크게 떨어진다.  
따라서 FaceShifter에 이어 더 나은 id supervision을 위해 추가 id loss를 추가한다. 추출기 Fid로 ArcFace를 사용하고 src Is와 생성이미지 Ig의 id vector 사이의 cosine 유사성을 계산한다.  
![image](https://user-images.githubusercontent.com/40943064/179946588-8f33ab3f-60a7-484d-b174-d995f2d481f6.png)  
Fusion 마스크 예측을 위해 weak supervision을 사용한다. 구체적으로, 우리는 생성이미지가 trg와 동일하게 유지되도록 이미지의 배경만 제한한다.  
Full supervision에 비해 weak mask loss는 local texture와 같은 대상 이미지의 속성을 더 잘 유지할 수 있다.  
마스크 손실은 다음과 같이 정의된다.  

![image](https://user-images.githubusercontent.com/40943064/179946878-f9a66c97-d30f-4969-afc1-8230663b4295.png)  

(Mt:trg mask, Mg : swapped mask, M[bg] : mask의 bg.)  
Bisenet을 사용하여 배경에 해당하는 semantic 레이블을 조합하여 Mt를 얻는다.  
전체 loss는 아래와 같이 정의된다.  

![image](https://user-images.githubusercontent.com/40943064/179947343-79284a84-14c2-4026-babd-71b3a3bf9f1e.png)
                                                                  







