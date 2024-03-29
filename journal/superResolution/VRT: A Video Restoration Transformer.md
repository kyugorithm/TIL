## Abstract
본 논문은 저품질 연속 프레임으로부터 고품질 연속 프레임을 복원한다.  
단일 이미지 복원과는 달리 배열이 맞지 않는 근접프레임들로부터 temporal information 활용이 필요하다.  
현존 딥러닝 방법은 대개 **sliding window strategy** 혹은 **recurrent architecture**를 이용하여 해결한다.  
그러나 위 방법론은 frame 별로 처리를 하거나 긴 범위의 모델링 능력이 부족하다.  
본 연구에서 **병렬 프레임 추정**과 **긴 범위의 temporal dependency modeling** 능력을 가지는 VRT를 제안한다.  

구체적으로 VRT는 아래 두가지 모듈을 여러 해상도로 구성하는 구조이다.  
#### 1) TMSA(temporal mutual self attention) 
- 비디오를 작은 클립으로 나누고 두 종류의 attention을 적용한다.  
- 클립간 상호작용을 가능하게 하기 위해, 비디오 시퀀스는 layer마다 shift 한다.  
- **Mutual attention** : joint motion estimation, feature alignment, feature fusion  
- **Self attention** : feature extraction  

#### 2) Parallel warping
- Parallel feature warping을 통해 인접 프레임 정보를 추가적으로 혼합한다.  

## Introduction
여러 LQ 프레임으로 HQ 프레임을 복원하는 video restoration은 최근 많은 관심을 끌어왔다. reference frame의 복원을 위해서는 단일 이미지 복원과는 달리 매우 연관되지만 배열은 맞지 않는 supporting frame을 최대한 활용하는것이 핵심 과제이다.  
현존하는 video restoration 방법들은 주로 두가지로 분할된다.  
1) Sliding window-based methods (9개)  
- 단일 HQ 프레임 생성을 위해 여러 입력 프레임을 사용하며 sliding window 이용한다.  
- 각 입력 프레임은 추론시에 여러번 처리되며 비효율적 feature 활용과 compuation cost를 야기하게 된다.
2) Recurrent methods (12개)  
- 다음 프레임의 reconstruction을 위해 이전 복원된 HQ 프레임을 주로 사용한다.  
- 재귀적 속성으로 인해 세가지 단점이 존재한다.  
: 효율적인 분산학습을 위한 병렬화 제한된다.
: 정보가 프레임별로 축적됨에도 recurrent model은 temporal dependency modelling에 좋지 못하다. (인접 프레임은 매우 강하게 영향을 주지만 그 영향은 몇개의 스텝이 지나가면 손실된다.)
: 프레임 수가 적은 비디오들에 대해 엄청나게 성능이 떨어진다.  

본 논문에서는 parallel computation, long-range dependency modelling이 가능한 VRT를 제안한다. 
VRT는 다중 스케일 프레임워크를 기반으로 비디오 시퀀스를 겹치지 않는 클립으로 나누고 클립 간 상호 작용을 활성화하기 위해 번갈아 이동한다. 특히 VRT의 각 스케일에는 여러 개의 TMSA 모듈과 병렬 warping 모듈이 있다. TMSA에서 mutual attention은 인접 두 프레임 클립 간의 상호 정렬에 초점을 맞추고 self attention은 feature 추출에 사용된다. 각 해상도의 끝에서 parallel warping을 사용하여 인접 프레임 정보를 현재 프레임에 fusion한다. Multi-scale feature extraction, alignment 및 fusion 후 HQ 프레임은 해당 프레임 feature에서 개별적으로 재구성된다.  

VRT는 기존 비디오 방식 대비 몇 가지 이점을 제공합니다.  
1) 긴 비디오 시퀀스에 대해 병렬로 학습되고 테스트된다. 반면 sliding window 기반 방법과 recurrent 방법 모두 프레임별로 테스트되는 경우가 많다.  
2) 각 프레임을 재구성하는 동안 여러 인접 프레임의 정보를 활용하여 장거리 시간 의존성을 모델링할 수 있다. 반면, sliding window 기반 방법은 긴 시퀀스 모델링으로 쉽게 확장할 수 없는 반면, recurrent 방법은 여러 타임스탬프 후에 먼 정보를 잊어버릴 수 있다.  
3) joint feature alignment 및 fusion을 위해 mutual attention을 사용할 것을 제안한다. support 프레임의 feature를 적응적으로 활용하여 reference 프레임에 융합하는데, 이는 암묵적인 움직임 추정 및 feature 왜곡으로 간주할 수 있다.  

우리의 기여는 다음과 같이 요약할 수 있다.
  
1) 병렬 계산과 장거리 종속 모델링을 특징으로 하는 비디오 복원 트랜스포머(VRT)라는 새로운 프레임워크를 제안한다. 프레임 feature를 여러 scale로 공동으로 extract/align/fusion한다.  
2) 프레임 간 상호 alignment에 대한 mutual attention를 제안한다. (implicit motion 추정 후 이미지 warping의 일반화된 "soft" 버전)

## 3. Video Restoration Transformer
### 3.1. Overall Framework

I_LQ ∈ R(T x H x W x Cin) - Low-quality frames  
I_HQ ∈ R(T x H x W x Cout) - High-quality frames  
T(frame number),H(height),W(width),Cin/out(in/out ch no.)  
s : upscaling facter(>=1)  

아래 그림과 같이 두가지 부분으로 나뉠 수 있다. (Feature extraction / Reconstruction)  
![image](https://user-images.githubusercontent.com/40943064/194894967-f6a7a0b5-9398-46ee-ba2a-0079c67faa92.png)  
#### Feature extraction.
먼저 단일 2D conv.를 이용해 LQ로부터 SF를 만든다. (I_SF ∈ R(T x H x W x C) - shallow features)  
다음 단계로 여러 이미지 해상도에서 frame들을 align하는 multi-scale network를 제안한다.  
특히, 총 scale 수가 S일 때, downsample을 S-1회 수행한다. : linear layer를 통해 channel 차원과 채널 개수를 2 x 2 neighborhood squeezing(**이해 필요**)  
그리고 원 사이즈로 feature를 unsqueezing하여 점진적으로 feature를 upsample한다.  
이러한 방식으로 feature를 extract하고 TMSA와 parallel 두 가지 종류의 모듈에 의해 서로 다른 scale의 object 또는 카메라 motion을 처리할 수 있다.  
각 scale에 대해 skip connection을 더한다. 마지막으로 multi-scale feature **extraction/alignment/fusion** 후에 추가적인 feature refinement를 위해 몇개의 TMSA를 추가하고 I_DF ∈ R(T x H x W x C)를 얻는다.

#### Reconstruction.
다음 단계로 ISF + IDF로부터 HQ를 복원한다. 각 프레임은 각자 상응하는 feature들을 기반으로 독립적으로 복원된다. 게다가, feature learning의 burden을 줄이기 위해, global residual learning을 적용하고, biliearly upsampled LQ와 HQ 사이의 잔차를 추정하도록 한다. 실질적으로 목적에 따라 서로 다른 구조를 가진다. (SR:sub-pixel conv., , deblur : single conv.)  이와는 별개로 구조적 설계는 모든 테스크에 대해 동일하게 유지된다.  

#### Loss function.  
기존 방법과의 공정한 비교를 위해 I^RHQ와 I^HQ(GT) 사이에 일반적으로 사용되는 Charbonnier loss를 다음과 같이 사용한다.  
![image](https://user-images.githubusercontent.com/40943064/194900606-bcdd7bbb-b3bb-4dc3-91a4-b6976275a086.png)



### 3.2. Temporal Mutual Self Attention
#### Mutual attention.
#### Temporal mutual self attention (TMSA).
#### Discussion.

### 3.3. ParallelWarping
