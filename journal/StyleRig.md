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
훈련 절차는 Face Reconstruction Network와 differentiable renderer의 결합에 의해 활성화되는  
self-supervised 2-way-consistency loss를 기반으로 한다.  
이를 통해 image domain에서 광도 재렌더링 오류를 측정할 수 있으며 고품질 결과를 얻을 수 있다.  
우리는 스타일에 대한 interactive 제어를 포함하여 우리의 방법의 설득력 있는 결과를 보여준다.  
GAN은 잘 정의된 semantic parameter에 따라 조절된 이미지 합성뿐만 아니라 이미지를 생성했다.  

### 3. Overview
<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122589553-5b960a00-d09b-11eb-9a4f-a48d5152ef79.png" alt="factorio thumbnail" width=450 />
</p>
  
**StyleGAN as function from w : latent code to Iw : latent code의 output image**

### 4. Semantic Rig Parameters
<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122594579-27721780-d0a2-11eb-9f12-283c0449ba7d.png" alt="factorio thumbnail" width=450 />
</p>
MoFA에서 소개한 3DMM parameter set, 모델에서는 PCA를 통해 alpha, beta, delta를 저차원으로 다룬다.  
200명의 얼굴을 조합하여 PC 성분을 추출하였으며 원 데이터 셋의 99%의 분산 분포를 cover하도록 PC를 선택했다.  

### 5. Training Corpus

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122593641-e88f9200-d0a0-11eb-9b8d-93be7d11886d.png" alt="factorio thumbnail" width=450 />
</p>
styleGAN을 이용하여 200k개의 (w, Iw) 셋 생성, l = 18 X 512 / 2 X 512 per each resolution level, self-supervised manner  

**self-supervised learning**  
다량의 레이블이 없는 원데이터로부터 데이터 부분들의 관계를 통해 레이블을 자동으로 생성하여 지도학습에 이용

### 6. Network Architecture

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122595937-217d3600-d0a4-11eb-89fb-e05ac843a69d.png" alt="factorio thumbnail" width=450 />
</p>
p : semantic control parameters, what = Rignet(w, p) & I_what = StyleGAN(what) ; p의 제어를 따른다.  
RigNet을 여러 제어모드에 대해 학습할때 분리하여 학습시킨다.  
Differentiable Face Recnstruction 과 2방향 cycle consistency losses를 이용하여 self-supervised 학습을 수행한다.  
  
    
    
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122597411-45417b80-d0a6-11eb-87bb-73b98b261b7d.png" width=450 /></p>    
  DFR:W를 p로 mapping하는 함수(W에 존재하는 이미지 에대한 정보를 p벡터로 표현하도록 mapping)  
  학습을 위해서는 differentiable render layer R 필요(MoFA소개;미분가능 rendering function)  
  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122597450-55595b00-d0a6-11eb-8e9f-b78fbdc97ac1.png" width=750 /></p>  
M은 face mesh 존재하는 값만 살려주는 역할  
Lphoto : 실제 이미지와 Rendering 차이의 2-norm  
Lland : 학습전에 수동으로 설정한 66개의 landmark 포인트에 대하여 집중하여 loss 계산  
MoFA에서는 face관련 파라미터 (alpha, beta, delta)에 대하여 regularization 수행하며 필요시 적용  
(너무 커지면 원래 parameter가 가지는 범위를 벗어남)  
  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122598494-e2e97a80-d0a7-11eb-8c32-fe41b4062e68.png" width=450 /></p>  
encoder : W vector를 512에서 32로 차원축소  
decoder : 입력받은 semantic control parameter와 l를 w와 합하여 W정보에 p정보를 합친 새로운 vector 생성 

### 7. Self-supervised Training
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122599127-cd288500-d0a8-11eb-9e0c-81f6f59881db.png" width=450 /></p>  
원하는 학습-pair가 없으므로 self-supervised 방식으로 cycleGAN과 같은 cycle-consistent editing과 consistency loss를 사용한다.  
  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122599331-2690b400-d0a9-11eb-9687-72d004e54df7.png" width=450 /></p>  
  cycleGAN에서 추가로 적용하는 identity loss와 같은데 갈때와 돌아올때 동일한 input이 되도록 하면 성능 향상에 도움이 된다고 하여 적용
  본 논문의 저자는 latent space에서 anchor 하는 역할이라고 설명하였으며 이 항이 없으면 이미지 성능이 떨어진다고 소개함  
  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122599368-39a38400-d0a9-11eb-84e4-2157c6f9e0b2.png" width=750 /></p>  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122602012-1a0e5a80-d0ad-11eb-9352-621111513011.png" width=450 /></p>  
v 벡터는 control만 적용할 target image로 rigNet에 의해 변환된 what에 semantic control 정보가 전달됐을것이라고 보고 phat=F(what)이 pv와 같도록 학습하면 된다.  
다만 perceptual loss를 적용하면 좋아지는 다른 논문과는 달리 본 문제에서는 약간의 latent vector의 변화가 큰 영향을 주므로 이와같은 loss 설정은 하지 않는다.  
대신, pv에 phat의 control value만 대체하여 Iv와 rendering된 이미지의 차이를 loss로 설정하면(pedit) 유사한 개념으로 학습방향을 설정할 수 있다.
  
  




<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122599434-55a72580-d0a9-11eb-9411-171a810f61d3.png" width=450 /></p>  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122602073-31e5de80-d0ad-11eb-9cca-2433c9a4c56d.png" width=450 /></p>  
위 case처럼 pw에 phat의 control value이외의 값들을 모두 대체하여 Iw와 rendering된 이미지의 차이를 loss로 설정하면(pconsist) 유사한 개념으로 학습방향을 설정할 수 있다.
  
  
