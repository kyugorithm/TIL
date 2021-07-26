## Abstract
실제 이미지와 분간되지 않는 모양과 질감이 전역적이고 지역적으로 일관된 이미지를 합성하기 위한 **capacity**가 GAN의 주요 과제이다.  
이를 위하여 논문은 segmentation분야의 통찰력을 빌려 대안의 **U-Net기반 Discriminator** 구조를 제안한다.  
U-Net 구조는 합성이미지에 대한 전역적 feedback를 제공하여 전역적 일관성을 유지하고 생성기에 상세 **per-pixel feedback**을 전달한다.  
분별기의 픽셀당 응답에 힘입어 CutMix 데이터 augmentation에 기반한 **per-pixel consistency regularization 기법**을 사용하며  
U-Net 판별기가 실제와 가짜가 이미지 사이의 **semantic하고 구조적인 변화에 더욱 집중하도록 장려**하여  
학습 성능을 향상시키며 생성 샘플들의 이미지 품질을 향상시킨다.  
새로운 판별기는 SOTA 방법들에 걸쳐 표준분포와 이미지품질 metrics 항목을 향상시킨다.
이는 생성기가 전역적이고 지역적인 현실성을 유지한채로 변화하는 구조, 외모, 디테일 수준을 가진 이미지를 합성할 수 있도록 한다.  
BigGAN baseline과 비교하여 우리는 평균 2.7FID 향상을 얻었다.  

## 1. Introduction

Large-scale 학습, 구조변경, regularization 적용으로 향상된 학습 안정성 등이 품질 향상에 기여했으나 아래와 같은 한계가 존재한다.  
1) 전체 semantic 일관성  
2) long-range structure  
3) 디테일 정확성  
  
잠재적 문제중 하나는 **D**에 있는데, 데이터 분포를 목표로 합성이미지에 대한 학습 신호를 G에 제공하는 loss function의 역할을 한다.  
D가 강할수록 G의 성능도 향상된다. 현 SOTA GAN 모델에서 D는 단지 실제 이미지와 합성이미지 사이의 가장 분별되는 차이에  
기반하여 효율적으로 G를 penalize하는 표현만을 배운다. 따라서, **D는 때때로 global 혹은 local중 하나에만 집중**한다.  
D가 **non-stationary 환경**에서 학습을 해야함에 따라 이 문제가 증폭된다. :  
학습에 따라 G가 지속적으로 변화하며 합성이미지 샘플 분포는 이동하게 되며 이때문에 과거 task를 까먹게 되기 쉽다.  
(D 학습관점에서 semantic, 구조, 질감등 학습은 다른 task로 여겨질 수있다. : 집중하지 못하는?)  
따라서 이러한 D는 더 global, local 이미지 차이를 학습하는 강력한 D를 유지하는데 incentive를 받지 않게 된다.  
이는 때로 합성 이미지가 일관적이지 않고 부분적으로 얼룩덜룩하게 되도록 하거나 기하적이고 구조적 패턴이 일관적이지 않게 된다.  

전술한 문제를 해결하기 위해 우리는 **global/local 결정을 동시에 출력하는 대안의 D 구조**를 제안한다.  
![image](https://user-images.githubusercontent.com/40943064/125013911-a1952b00-e0a7-11eb-96c5-15f3a8fab7b0.png)  

sementation 분야로부터 아이디어를 얻어, 우리는 D의 역할을 **classifier와 segmenter 두개 부여하도록 재설계**한다.
D를 U-net으로 설정하며 **encoder는 이미지에 대한 분류**, **decoder는 perpixel 분류**역할을 부여한다.  
![image](https://user-images.githubusercontent.com/40943064/125020204-6698f480-e0b3-11eb-8c33-3f2ca4ec50f7.png)  

이러한 아키텍처 변화는 더 강력한 D로 이어지며, 이는 보다 강력한 데이터 표현을 유지하도록 장려되어, D를 속이는 것을 더 어렵게 만들고,  
따라서 생성된 샘플의 품질을 향상시키는 G의 작업을 가능하게 한다.  
우리는 G를 어떤 식으로든 수정하지 않으며, G의 아키텍처 변화, 발산측정, 정규화등에 대한 지속적인 연구와 독립적이다.

제안된 D는  디코더의 2차원 출력 공간에서의 **consistency-regularization을 위해 D에 효과적인 CutMix augmentaion을 채택**한다.  

Segmenter(U-Net 디코더)의 real/fake pathch class와 관련하여 Ground truth label map이 공간적으로 결합되고  
classifier(U-Net Encoder)에 대해 Fake로 설정한다. 이는 CutMix 이미지가 golbally fake로 인식되어야 하기 때문이다.   
![image](https://user-images.githubusercontent.com/40943064/125020507-ecb53b00-e0b3-11eb-981c-adf5e6e7d8e6.png)  

U-Net 식별자의 per-pixel 피드백으로 이러한 CutMix 이미지를 사용하여 consistency-regularization을 수행하고 CutMix 변환 시  
per-pixel inconsistency D 예측에 penalize 한다. 이는 D를 강화하여 real/fake 이미지사이의 semantic 및 structural 변화에  
더 집중하고 도메인을 보존하는 perturbation에 덜 집중할 수 있도록 한다.  
또한 디코더의 localization 능력 향상에 도움이 된다.  
제안된 consistency regularization을 통해 G가 강화되므로 local/global 이미지 사실성에 더욱 주의를 기울인다.  

최첨단 BigGAN 모델을 baseline로 하여 여러 데이터셋에 걸쳐 제안된 U-Net GAN 모델을 평가하고 FID/IS 지표 측면에서 품질을 관찰한다.  
256×256의 FFHQ unconditional 영상 합성에서 U-Net GAN은 BigGAN 모델보다 4개의 FID 포인트를 개선하여 고품질 얼굴을 합성한다.
![image](https://user-images.githubusercontent.com/40943064/125024379-98ae5480-e0bb-11eb-8fa5-1e5dfb290698.png)

128×128 / CelebA : FID : 4.55 -> 2.95
128×128 / COO : FID : 16.37 -> 13.73 (동물 cGAN task)
![image](https://user-images.githubusercontent.com/40943064/125024527-e88d1b80-e0bb-11eb-98c5-2d8663ce1d71.png)  

## 2. Related Work 
### 2.1 GAN
### 2.2 Mix&Cut regularizations

## 3. U-Net GAN Model
'vanila' GAN은 G, D 2개의 네트워크에 대하여 아래 목적함수를 교대로 최소화하도록 구성한다.   
![image](https://user-images.githubusercontent.com/40943064/125053005-880fd580-e0df-11eb-948e-213298f11d94.png)  
G는 tent variable z ~ p(z)를 사전확률분포에서 진짜같아보이는 이미지로 mapping한다.  
D는 실제이미지와 실제 이미지 x와 가짜 이미지 G(z)를 구분하는것을 목표로한다.  
일반적으로 G, D는 decoder encoder CNN 구조로 모델된다.  
GAN은 다양한 목적함수와 구조를 가진 변이 버전이 있다. 본 논문에서는 D를 향상하는데 집중한다.  
기존 classification net에서 기본 encoder 파트 구조는 유지하며 encoder-decoder U-net 구조로 변경한다.  
제안한 D는 global/local 데이터 표현을 유지하도록 하여 G에 더욱 정보가 되는 feedback을 제공한다.  
U-Net decoder의 local per-pixel feedback에 힘입어 실제와 모조 이미지의 CutMix 변환 하에서 per-pixel inconsistent한  
D에 대한 예측에 불이익을 주는 consistency regularization 기술을 제안한다.  
U-Net 판별기의 localization 품질을 높이고 실제/모조 사이 의미/구조 변화에 관심을 갖도록 유도하는 데 도움이 된다.

### 3.1. U-Net Based Discriminator

Encoder-Decoder Network는 조밀한 예측을 위한 강력한 방법을 구성한다.  
여기서 이미지분류 network와 유사하게 encoder는 점진적으로 입력을 downsample하며 global 이미지를 포착한다.  
Decoder는 점진적으로 upsampling을 수행하여 입력에 대한 출력 해상도를 맞추고 그에따라 정확한 localization을 수행한다. 
Skip connection은 두 모듈의 일치해상도 간에 데이터를 보낼수 있도록 하여 네트워크의 세부 정보를 정확하게 segment할 수  
있는 기능을 더욱 향상시킨다.

이와 유사하게, 본 연구에서는, 원래 D분류 네트워크의 빌딩 블록을 Encoder 부품으로 재사용하고 G 빌딩 블록을 decoder로  
사용함으로써, D를 U-Net로 확장할 것을 제안한다.  
다시 말해, D는 원래의 downsampling 네트워크와 새로운 upsampling 네트워크로 구성된다.  
위 두 모듈은 **bottleneck**과 encoder feauture맵을 decoder 모듈과 복사/concatenate 하는 **skip-connection**으로 연결된다.
이 식별자를 DU라고 부른다. 원본 D(x)는 입력 이미지 x를 진짜 or 가짜로 분류하지만, U-Net 판별기 DU(x)는  
per-pixel 분류를 수행하여 Encoder에서 x의 원래 이미지 분류와 함께 이미지 x를 실제 및 가짜 영역으로 segment한다.  
이를 통해 DU는 real/fake 이미지 global/local 차이를 모두 학습할 수 있다.
이후 D의 원래 Encoder 모듈을 DU enc라고 하고 도입된 Decoder 모듈을 DU dec라 한다.  

![image](https://user-images.githubusercontent.com/40943064/125060600-7d593e80-e0e7-11eb-9e0e-77ad8b7580ad.png)  
여기서 기본 GAN loss function과 유사하게 L DU enc는 DU end의 scalar 출력으로부터 계산된다.  
![image](https://user-images.githubusercontent.com/40943064/125064310-7b917a00-e0eb-11eb-8c11-5038912ac140.png)  
Decoder의 per-pixel 출력은 bottleneck으로부터의 upsampling 프로세스를 통해 활성화된 global 정보와 Encoder  
중간 계층으로부터의 skip-connection을 통해 조정되는 low-level feature의 local 정보를 기반으로 한다.  
  
G도 더 강력한 DU를 속이기 위해 이미지를 합성하면서 global 구조와 local 세부 정보에 모두 집중하도록 장려한다.  
![image](https://user-images.githubusercontent.com/40943064/125065042-4e919700-e0ec-11eb-9c38-32622f79bda6.png)  



### 3.2. Consistency Regularization
잘 훈련된 DU의 per-pixel 결정은 이미지의 클래스 도메인 변환에서 동일해야 한다. 그러나 이 속성은 명시적으로 보장하지 않는다.  
이를 가능하게 하기 위해 D는 실제/가짜 샘플 사이의 의미와 구조적인 변화에 집중하고 임의 class-domain 보존 perturbation에  
덜 관심을 기울이도록 정규화되어야 한다.  
따라서, 우리는 DU 판별기의 일관성 정규화를 제안하며, DUdec가 Real/Fake 샘플의 CutMix 변환 하에서 같은 예측값을 출력하도록  
명시적으로 유도한다.  
CutMix는 원래 클래스 도메인을 보존하는 것과 대조적으로 혼합에 사용되는 실제 및 가짜 이미지 패치를 변경하지 않으며  
가능한 다양한 출력을 제공하기 때문에 선택한다.
x와 G(x) in R^(WxHxC)의 혼합으로 DU에 대하여 Mask M을 통해 새로운 샘플 x\~를 생성한다. (M in {0, 1}^(WxH) : binary mask)  
![image](https://user-images.githubusercontent.com/40943064/125068085-06747380-e0f0-11eb-8fee-3c8a101d1091.png)  
DU enc가 생성샘플을 globally하게 학습하여 artifact를 만들 수 있기 때문에 cutmix sample class는 fake(c=0)로 정의한다.  
생성된 x~, c, M은 DU의 모듈 encoder, decoder에 대한 GT이다.  
이때, D의 목적함수에 g the consistency regularization loss를 추가하여 consistent per-pixel 예측이 되도록 학습한다.  
![image](https://user-images.githubusercontent.com/40943064/125068852-e7c2ac80-e0f0-11eb-98fc-67266cf3e0cc.png)  
이는 DU dec(CutMix(x,G(z))) == CutMix(DU(x,G(z)))가 되도록 한다.  
그에 따라 아래와 같이 항을 추가한다.  
![image](https://user-images.githubusercontent.com/40943064/125069548-d3cb7a80-e0f1-11eb-9551-8a1490c434e5.png)  
G loss는 변경되지 않는다. Consistency Regularization 외에도, DU의 encoder/decoder 모듈 모두를 학습하기 위해  
CutMix 샘플을 사용한다. U-Net GAN의 경우 포화 상태가 아닌 GAN objective formula를 사용한다.  

### 3.3. Implementation
- U-Net based discriminat
  
Here  we  discuss  implementation  details  of  the  U-NetGAN model proposed in Section 3.1 and 3.2.U-Net based discriminator.We  build  upon  the  recentstate-of-the-art BigGAN model [5], and extend its discrim-inator with our proposed changes.  We adopt the BigGANgenerator and discriminator architectures for the256×256(and128×128) resolution with a channel multiplierch=64, as described in detail in [5].  The original BigGAN dis-criminator downsamples the input image to a feature mapof dimensions16ch×4×4, on which global sum poolingis applied to derive a16chdimensional feature vector thatis classified into real or fake.  In order to turn the discrimi-nator into a U-Net, we copy the generator architecture andappend it to the4×4output of the discriminator. In effect,the features are successively upsampled via ResNet blocksuntil  the  original  image  resolution  (H×W)  is  reached.To  make  the  U-Net  complete,  the  input  to  every  decoderResNet  block  is  concatenated  with  the  output  features  ofthe encoder blocks that share the same intermediate resolu-tion.  In this way, high-level and low-level information areeffectively integrated on the way to the output feature map.Hereby, the decoder architecture is almost identical to thegenerator, with the exception of that we change the numberof channels of the final output from3toch, append a finalblock of1×1convolutions to produce the1×H×Woutputmap,  and do not use class-conditional BatchNorm [8, 12]in the decoder, nor the encoder.  Similarly to [5], we pro-vide  class  information  toDUwith  projection  [35]  to  thech-dimensional channel features of the U-Net encoder anddecoder output. In contrast to [5] and in alignment with [6],we find it beneficial not to use a hierarchical latent space,but to directly feed the same input vectorzto BatchNormat every layer in the generator.  Lastly, we also remove theself-attention layer in both encoder and decoder, as in ourexperiments they did not contribute to the performance butled to memory overhead.  While the original BigGAN is aclass-conditional model, we additionally devise an uncon-ditional version for our experiments.  For the unconditionalmodel, we replace class-conditional BatchNorm with self-modulation [6], where the BatchNorm parameters are con-ditioned only on the latent vectorz, and do not use the classprojection of [35] in the discriminator.All these modifications leave us with a two-headed dis-criminator.  While the decoder head is already sufficient totrain the network, we find it beneficial to compute the GANloss at both heads with equal weight.  Analogously to Big-GAN, we keep the hinge loss [50] in all basic U-Net models,while the models that also employ the consistency regular-ization in the decoder output space benefit from using thenon-saturating loss [14]. Our implementation builds on topof the original BigGAN PyTorch implementation2  
  
- Consistency regularization  
or each training iteration amini-batch of CutMix images( ̃x,c= 0,M)is created withprobabilitypmix. This probability is increased linearly from0to0.5between the firstnepochs in order to give the gen-erator  time  to  learn  how  to  synthesize  more  real  lookingsamples and not to give the discriminator too much powerfrom the start. CutMix images are created from the existingreal and fake images in the mini-batch using binary masksM.   For  samplingM,  we  use  the  original  CutMix  imple-mentation3: first sampling the combination ratiorbetweenthe real and generated images from the uniform distribution(0,1)and then uniformly sample the bounding box coordi-nates for the cropping regions ofxandG(z)to preserve therratio, i.e.r=|M|W∗H(see Figure 3). Binary masksMalsodenote the target for the decoderDUdec, while we usefake,i.ec= 0, as the target for the encoderDUenc. We setλ= 1.0as it showed empirically to be a good choice. Note that theconsistency regularization does not impose much overheadduring training. Extra computational cost comes only from feeding additional CutMix images through the discrimina-tor while updating its parameters.  

## Appendix
### U-net
![image](https://user-images.githubusercontent.com/40943064/125147460-686fc000-e166-11eb-999a-d0e16bd70797.png)
