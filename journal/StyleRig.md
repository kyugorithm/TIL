### Abstract

**StyleGAN**은 눈, 치아, 머리카락, 맥락(목, 어깨, 배경)을 가진 얼굴의 **사실적인 초상화 이미지**를 생성한다.  
그러나 얼굴 포즈, 표현 및 장면 조명과 같은 3D로 해석 가능한 **의미론적 얼굴 매개변수에 대한 리그와 같은 제어가 부족**하다.  
반면에 **3DMM**은 의미 매개변수에 대한 제어를 제공한다.  
그러나 rendering 시 **사실성이 부족**하며 **얼굴 내부만 모델링** 할 수 있다.  
우리는 3DMM과 사전 훈련되고 고정된 StyleGAN에 대해 rig 제어를 제공하는 첫 번째 방법을 제시한다.  
새로운 연결 네트워크인 RigNet은 3DMM의 semantic parameter와 StyleGAN input 사이에서 훈련된다.  
네트워크는 지도학습 없이 selp-superviced 감독 방식으로 훈련된다.  
테스트 시, 우리의 방법은 스타일의 광학적 사실성으로 초상화 이미지를 생성한다.GAN 및 얼굴의 3D 의미 매개변수에 대한 명시적 제어를 제공한다.  

### Introduction  
  
**3DMM**  
얼굴의 사실적인 합성은 특수 효과, 가상 현실이나 차세대 통신을 포함한 여러 분야에서 적용될 수 있다.  
컨텐츠 생성 프로세스 동안 얼굴모양 정체성, 표현, 반사율 또는 장면 조명과 같은 페이스 리그의 의미론적 매개 변수 제어가 필요하다.  
컴퓨터 비전 커뮤니티는 얼굴을 장비로 모델링한 풍부한 역사를 가지고 있다. 이러한 모델은 3DMM의 다양한 매개 변수를 탐색하면서 사용자 친화적인 제어를 제공한다.  
이러한 방법은 종종 학습데이터 부족, 더 중요한 것은 렌더링시 현실감이 부족으로 사용되지 못한다.  
3D 스캐닝을 통해 고품질 얼굴 데이터를 얻을 수 있지만 이 데이터에서 파생된 모델은 스캔한 얼굴의 다양성에 의해 구속되며  
풍부한 인간 얼굴의 semantic parameter화에 대한 일반화를 제한할 수 있다.  
현장 데이터에 대해 훈련된 딥 러닝 기반 모델은 종종 데이터 기반 prior와 스캔 기반 데이터 세트에서 얻은 다른 형태의 정규화에 의존한다.  
사진 현실성과 관련하여, perceptual 손실은 최근 기존 방법에 비해 얼굴 모델링 품질이 향상되는 것을 보여주었다.  
그러나, 그들은 여전히 사실적인 얼굴 렌더링을 일으키지 않는다. 배경은 말할 것도 없고 입 내부, 머리카락 또는 눈도 모델링되기 어렵다.  

**GAN**  
GAN은 최근 얼굴의 사진 현실주의를 달성했다.  
ProGAN은 G와 D의 점진적인 성장을 통해 훈련을 더 안정시키고 가속화할 수 있음을 보여준다.  
CelebA-HQ 데이터 세트에 대해 훈련할 때, 이것은 얼굴에 대한 현저한 수준의 현실성을 보여준다.  
StyleGAN은 style transfer 문헌의 아이디어를 사용하고 다양한 얼굴 속성을 분리할 수 있는 아키텍처를 제안한다.  
**거친**(머리카락, 기하학), **중간**(표정, 얼굴모발), **미세**(색분포, 주근깨)등의 속성 제어에 훌륭한 결과가 나왔다.  
그러나, 이러한 제어 가능한 속성은 semantic 하게 잘 정의되지 않았으며, 유사하지만 얽힌 몇 가지 의미 속성을 포함하고 있다.  
예를 들어, coarse & middle 특성 모두 얼굴모양 정보를 포함한다. coarse 수준에는 얼굴모양 및 pose와 같은 여러 가지 얽힌 특성이 있다.  

**Proposal**  
얼굴을 위한 의미론적 매개 변수 공간을 사용하여 StyleGAN을 조작하는 새로운 솔루션을 제시한다.  
이 방법은 제어 가능한 파라메트릭 특성과 styleGAN의 높은 사진 현실성 두 가지 모두의 장점을 제공한다.  
사전학습된고정 styleGAN을 사용한다. 학습에 추가 데이터가 필요하지 않다.  
우리의 관심은 의미론적 매개 변수에 대한 컴퓨터 그래픽 스타일 rig-like 제어를 제공하는 것이다.  
훈련 절차는 Face Reconstruction Network와 differentiable renderer의 결합에 의해 활성화되는 self-supervised 2-way-consistency loss를 기반으로 한다.  
이를 통해 image domain에서 광도 재렌더링 오류를 측정할 수 있으며 고품질 결과를 얻을 수 있다.  
우리는 스타일에 대한 interactive 제어를 포함하여 우리의 방법의 설득력 있는 결과를 보여준다.  
GAN은 잘 정의된 semantic parameter에 따라 조절된 이미지 합성뿐만 아니라 이미지를 생성했다.  

### 3. Overview

![image](https://user-images.githubusercontent.com/40943064/122589553-5b960a00-d09b-11eb-9a4f-a48d5152ef79.png)  
**StyleGAN as function from w : latent code to Iw : latent code의 output image**

### 4. Semantic Rig Parameters
![image](https://user-images.githubusercontent.com/40943064/122592002-b5e49a00-d09e-11eb-90c6-07b05f1fa6c2.png)
MoFA에서 소개한 3DMM parameter set, 모델에서는 PCA를 통해 alpha, beta, delta를 저차원으로 다룬다.  
200명의 얼굴을 조합하여 PC 성분을 추출하였으며 원 데이터 셋의 99%의 분산 분포를 cover하도록 PC를 선택했다.  

### 5. Training Corpus

![image](https://user-images.githubusercontent.com/40943064/122593641-e88f9200-d0a0-11eb-9b8d-93be7d11886d.png)
styleGAN을 이용하여 200k개의 (w, Iw) 셋 생성, l = 18 X 512 / 2 X 512 per each resolution level, self-supervised manner  





