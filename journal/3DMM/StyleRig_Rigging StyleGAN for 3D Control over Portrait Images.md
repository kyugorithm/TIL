# StyleRig: Rigging StyleGAN for 3D Control over Portrait Images

## Abstract

**StyleGAN**은 눈, 치아, 머리카락, 맥락(목, 어깨, 배경)을 가진 얼굴의 **사실적인 초상화 이미지**를 생성한다.  
그러나 자세, 표정 및 조명등 3D 해석 가능한 **semantic face parameter에 대한 rig-like control이 부족**하다.  
**3DMM**은 semantic parameter에 제어가 가능하지만 rendering 시 **사실성이 부족**하며 **얼굴 내부만 모델링** 할 수 있다.  
우리는 3DMM과 사전 학습되고 고정된 StyleGAN에 대해 rig-like control를 제공하는 첫 번째 방법을 제시한다.  
새로운 rigging network인 RigNet은 3DMM의 semantic parameter와 StyleGAN input 사이에서 self-supervised 방식으로 학습된다.(w(StyleGAN) -> p(3DMM))  
테스트에서 제안방법은 styleGAN으로 photorealistic 초상화 이미지를 생성하고 3D semantic parameter에 대한 explicit control을 제공한다.

## Introduction  
  
**3DMM**  
얼굴의 사실적인 합성은 특수 효과, 가상 현실이나 차세대 통신을 포함한 여러 분야에서 적용될 수 있다.  
컨텐츠 생성 프로세스 동안 id, 표정, 반사율 또는 장면 조명과 같은 face rig의 semantic parameter control이 필요하다.  
CV 커뮤니티는 face rig 모델링에 대한 풍부한 역사를 가지고 있다. 이러한 모델은 3DMM의 다양한 매개 변수를 탐색하면서 사용자 친화적인 제어를 제공한다.  

<p align="center"><img src="https://user-images.githubusercontent.com/40943064/122629496-6fbc2480-d0f8-11eb-8439-e64a364a102a.png" width=450 /></p>  
이러한 방법은 종종 학습데이터 부족, 더 중요하게 렌더링시 현실감이 부족으로 사용되지 못한다.  
3D 스캐닝을 통해 고품질 얼굴 데이터를 얻을 수 있지만 이 데이터에서 파생된 모델은 스캔한 얼굴의 다양성에 의해 구속되며  
풍부한 인간 얼굴의 semantic parameter화에 대한 일반화를 제한할 수 있다.  
Wild 데이터에 대해 학습된 DL 기반 모델은 종종 데이터 기반 prior와 스캔 기반 데이터 세트에서 얻은 다른 형태의 정규화에 의존한다.  
사진 현실성과 관련하여, perceptual loss은 최근 기존 방법에 비해 얼굴 모델링 품질이 향상되는 것을 보여주었다.  
그러나, 그들은 여전히 사실적인 얼굴 렌더링을 일으키지 않는다. 배경은 말할 것도 없고 입 내부, 머리카락 또는 눈도 모델링되기 어렵다.  

**GAN**  
GAN은 최근 얼굴 photorealism을 달성했다.  
ProGAN은 G와 D의 점진적인 성장을 통해 훈련을 더 안정시키고 가속화할 수 있음을 보여준다.  
CelebA-HQ 데이터 세트에 대해 훈련할 때, 이것은 얼굴에 대한 훌륭한 현실성을 보여준다.  

<p align="center"><img src="https://user-images.githubusercontent.com/40943064/122629462-29ff5c00-d0f8-11eb-9f7c-c4eb9f37b487.png" width=450 /></p>  


StyleGAN은 style transfer 아이디어를 사용하고 다양한 얼굴 속성을 분리할 수 있는 아키텍처를 제안한다.  
**Coarse**(머리카락, 기하학), **medium**(표정, 얼굴모발), **fine**(색분포, 주근깨)등의 attribute control에 훌륭한 결과가 나왔다.  
그러나, 이러한 제어 가능한 attribute는 semantic 하게 잘 정의되지 않았으며, 유사하지만 얽힌 몇 가지 의미 속성을 포함하고 있다.  
예를 들어, coarse & middle 특성 모두 얼굴모양 정보를 포함한다. coarse 수준에는 얼굴모양 및 pose와 같은 여러 가지 얽힌 특성이 있다.  

**Proposal**  
얼굴을 위한 semantic parameter 공간을 사용하여 StyleGAN을 조작하는 새로운 솔루션을 제시한다.  
이 방법은 제어 가능한 파라메트릭 특성과 styleGAN의 높은 사진 현실성 두 가지 모두의 장점을 제공한다.  
사전학습된 고정 styleGAN을 사용한다. 학습에 추가 데이터가 필요하지 않다.  
우리의 관심은 semantic parameter에 대한 CV 스타일 rig-like 제어를 제공하는 것이다.  
학습 절차는 face reconstruction network와 differentiable renderer의 결합에 의해 활성화되는  
self-supervised 2-way-consistency loss를 기반으로 한다.  
이를 통해 image domain에서 photometric rerendering error를 측정할 수 있으며 고품질 결과를 얻을 수 있다.  
우리는 스타일에 대한 interactive 제어를 포함하여 우리의 방법의 설득력 있는 결과를 보여준다.  
GAN은 잘 정의된 semantic parameter에 따라 조절된 이미지 합성뿐만 아니라 이미지를 생성했다.  

## 3. Overview
StyleGAN(w)은 latent code w를 이미지 Iw로 mapping해주는 함수로 볼 수 있다. 생성 이미지 품질은 1024의 고품질이 될 수 있지만 생성 이미지는 자세, 표정, 조명등의 semantic한 제어가 존하지 않는다. StyleRig는 의미론적이고 해석 가능한 제어 parameter의 항목으로 StyleGAN 생성 얼굴 이미지에 대해 rig-like 제어를 얻을 수 있도록 해준다.  
  
**순서**  
Semantic control space -> training data -> network architecture -> loss function
  
## 4. Semantic Rig Parameters
<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122594579-27721780-d0a2-11eb-9f12-283c0449ba7d.png" alt="factorio thumbnail" width=450 />
</p>
MoFA에서 소개한 3DMM parameter set, 모델에서는 PCA를 통해 alpha, beta, delta를 저차원으로 다룬다.  
200명의 얼굴을 조합하여 PC 성분을 추출하였으며 원 데이터 셋의 99%의 분산 분포를 cover하도록 PC를 선택했다.  

  ***
  
## 5. Training Corpus

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122593641-e88f9200-d0a0-11eb-9b8d-93be7d11886d.png" alt="factorio thumbnail" width=450 />
</p>
styleGAN을 이용하여 200k개의 (w, Iw) 셋 생성, l = 18 X 512 / 2 X 512 per each resolution level, self-supervised manner  

**self-supervised learning**  
다량의 레이블이 없는 원데이터로부터 데이터 부분들의 관계를 통해 레이블을 자동으로 생성하여 지도학습에 이용
  ***
  
## 6. Network Architecture

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122595937-217d3600-d0a4-11eb-89fb-e05ac843a69d.png" alt="factorio thumbnail" width=450 />
</p>
p : semantic control parameters, what = Rignet(w, p) & I_what = StyleGAN(what) ; p의 제어를 따른다.  
RigNet을 여러 제어모드에 대해 학습할때 분리하여 학습시킨다.  
Differentiable Face Recnstruction 과 2방향 cycle consistency losses를 이용하여 self-supervised 학습을 수행한다.  
  
    
    
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122597411-45417b80-d0a6-11eb-87bb-73b98b261b7d.png" width=450 /></p>    
  DFR:W를 p로 mapping하는 함수(W에 존재하는 이미지 에대한 정보를 p벡터로 표현하도록 mapping)  
  학습을 위해서는 differentiable render layer R 필요(MoFA소개;미분가능 rendering function)  
  

<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122629706-f0c7eb80-d0f9-11eb-9383-79fa550a7608.png" width=750 /></p>  
M은 face mesh 존재하는 값만 살려주는 역할  
Lphoto : 실제 이미지와 Rendering 차이의 2-norm  
Lland : 학습전에 수동으로 설정한 66개의 landmark 포인트에 대하여 집중하여 loss 계산  
MoFA에서는 face관련 파라미터 (alpha, beta, delta)에 대하여 regularization 수행하며 필요시 적용  
(너무 커지면 원래 parameter가 가지는 범위를 벗어남)  
  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122598494-e2e97a80-d0a7-11eb-8c32-fe41b4062e68.png" width=450 /></p>  
encoder : W vector를 512에서 32로 차원축소  
decoder : 입력받은 semantic control parameter와 l를 w와 합하여 W정보에 p정보를 합친 새로운 vector 생성  
  
  ***
  
## 7. Self-supervised Training
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122599127-cd288500-d0a8-11eb-9e0c-81f6f59881db.png" width=450 /></p>  
원하는 학습-pair가 없으므로 self-supervised 방식으로 cycleGAN과 같은 cycle-consistent editing과 consistency loss를 사용한다.  
  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122599331-2690b400-d0a9-11eb-9687-72d004e54df7.png" width=450 /></p>  
  cycleGAN에서 추가로 적용하는 identity loss와 같은데 갈때와 돌아올때 동일한 input이 되도록 하면 성능 향상에 도움이 된다고 하여 적용
  본 논문의 저자는 latent space에서 anchor 하는 역할이라고 설명하였으며 이 항이 없으면 이미지 성능이 떨어진다고 소개함  
  
  ***

<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122629973-962f8f00-d0fb-11eb-8ca3-379c81784a1f.png" width=750 /></p>  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122602012-1a0e5a80-d0ad-11eb-9352-621111513011.png" width=450 /></p>  
v 벡터는 control만 적용할 target image로 rigNet에 의해 변환된 what에 semantic control 정보가 전달됐을것이라고 보고 phat=F(what)이 pv와 같도록 학습하면 된다.  
다만 perceptual loss를 적용하면 좋아지는 다른 논문과는 달리 본 문제에서는 약간의 latent vector의 변화가 큰 영향을 주므로 이와같은 loss 설정은 하지 않는다.  
대신, pv에 phat의 control value만 대체하여 Iv와 rendering된 이미지의 차이를 loss로 설정하면(pedit) 유사한 개념으로 학습방향을 설정할 수 있다.
  
  



  ***
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122599434-55a72580-d0a9-11eb-9411-171a810f61d3.png" width=450 /></p>  
  
<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122602073-31e5de80-d0ad-11eb-9cca-2433c9a4c56d.png" width=450 /></p>  
위 case처럼 pw에 phat의 control value이외의 값들을 모두 대체하여 Iw와 rendering된 이미지의 차이를 loss로 설정하면(pconsist) 유사한 개념으로 학습방향을 설정할 수 있다.

<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122629054-25857400-d0f5-11eb-95ea-aad84e65db95.png" width=1024 /></p>  





  ***
  
## 8. Results
테스트시 StyleRig는 포즈, 표현 및 조명 파라미터를 제어할 수 있다.  
다음 세 가지 응용 프로그램을 통해 접근 방식의 효과를 입증한다.  
**스타일 혼합(8.1), 대화형 리그 제어(8.2) 및 조건부 이미지 생성(8.3)**  
### 8.1. StyleMixing
StyleGAN 벡터는 서로다른 resolution 스타일에 따라 다른 벡터가 대응된다.  
stylemixing을 적용하기 위해 특정 resolution의 latent code를 source에서 target으로 복사함으로써 새 이미지가 생성된다.  
그림 5에서 볼 수 있듯이 각 스타일은 다음의 정보를 포함한다.
1. coarse style : ID & pose
2. middle style : 표정 & 헤어스타일 & 조명
3. fine style   : source의 색상 구조  

<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122627193-ff59d700-d0e8-11eb-99ed-a1f612469e72.png" width=850 /></p>  

styleRig 방법은 유사한 기능을 가지면서 semantic parameter에 대한 훨씬 더 완전한 제어를 보여준다.  
대상 ID로 이미지를 생성하기 위해 face-rig의 source latent를 target latent로 전송(pv->pw)하여 아래 세가지를 제어한다. 
1. 포즈  
2. 표정  
3. 조도  
styleGAN의 경우 여러 벡터를 결합하는경우 semantic dimension끼리 entangle되어 styleRig와 같은 rig-like control이 불가능하다.  

<p align="center" style="color:gray"><img src="https://user-images.githubusercontent.com/40943064/122627212-113b7a00-d0e9-11eb-9665-52e401115a28.png" width=850 /></p>  


그림 4에서, StyleRig에 의해 StyleGAN의 latent code가 전달되는지를 분석한다.  
2500개 이상의 혼합 결과를 계산하여 모든 해상도에서 StyleGAN 잠재 벡터의 평균(l2-norm) 변화와 분산을 보여준다.  
예상대로, coarse latent 코드 벡터는 주로 rotation을 담당한다. 표정은 coarse 레벨과 middle 레벨의 latent code로 제어된다.  
빛의 방향은 대부분 중간 해상도 벡터에 의해 제어된다. 그러나 fine latent code는 이미지의 전역 색상표를 제어하는 데 중요한 역할을 한다.  
StyleRig는 변경할 벡터를 지정해야 하는 대신 semi-supervised 방식으로 이 mapping을 복구한다.  
그림 5와 같이, styleRig는 배경, 헤어 스타일, 액세서리 같은 장면 컨텍스트를 더 잘 보존할 수 있다.  
  ***  
  
### 8.2. Interactive Rig Control  
StyleRig는 3DMM parameter도 독립적으로 제어하므로 StyleGAN에서 생성한 이미지에 대한 명시적인 semantic 제어가 가능하다.  
사용자가 포즈, 표현 및 장면 조명 파라미터를 interactive하게 변경하여 face mesh와 interactive한 UI를 개발한다.  
그리고 업데이트된 parameter를 RigNet에 입력하여 interactive frame rate(~5fps)로 새 이미지를 생성한다.  
  
**Analysis of StyleRig**  
StyleRig 분석 대화형 편집기를 사용하면 훈련된 네트워크를 쉽게 검사할 수 있다. 
네트워크가 대부분의 제어에서 좋은 작업을 수행하지만, 3D 매개 변수 얼굴 모델의 **일부 표현성은 손실**을 관찰한다.  
즉, RigNet은 모든 파라메트릭 제어 모드를 스타일에서 유사한 변경으로 전송할 수 없다.  
예를 들어, in-plane rotation이 무시되며 face mesh의 많은 표정은 생성된 영상으로 잘 변환되지 않는다.  
우리는 이러한 문제 원인을 sytleGAN이 학습되어진 이미지의 bias로 판단한다.  
이러한 모드를 분석하기 위해, 우리는 StyleGAN에서 생성된 훈련 데이터에서 얼굴 모델 매개 변수의 분포를 살펴본다.  
그림을 보면 in-plane(Z 축 주위의 회전) 이 데이터에 거의 존재하지 않으며 대부분의 변동은 Y 축 주위에만.   
이러한 문제는 styleGAN이 Flickr-HQ 데이터 세트에 대해 훈련되었기 때문이다.  
이데이터셋의 대부분의 얼굴의 정적 이미지에는 in-plane rotation이 포함되지 않는다.  
대부분의 생성된 이미지가 무표정, 미소, 웃는 얼굴 등의 표정으로 구성된 편향에도 동일한 추론을 적용할 수 있다.  
face-rig에는 64개의 control vector가 포함되어 있지만, 학습데이터의 분포 bias로 벡터를 잘 제어할 수 없다.  
마찬가지로 조명 조건도 데이터 집합에서 제한된다.   
우리의 접근 방식은 StyleRig뿐만 아니라 StyleGAN에 존재하는 bias도 검사할 수 있는 직관적인 UI를 제공한다.
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/122628031-94ab9a00-d0ee-11eb-927c-bba6ac6c210c.png" width=800 /></p>  

### 8.3. Conditional Image Generation
사전 훈련된 생성 모델에 대한 명시적/암시적 제어를 통해 conditional generative model로 전환할 수 있다.  
제어하는 parameterer에 해당하는 이미지를 생성하기 위해 RigNet에 포즈, 표정 또는 조명 입력을 간단히 수정할 수 있다(그림참조).  
이것은 unconditional generative model를 conditional generative model로 변환하는 직선적인 방법이며, 고해상도의 사실적 결과를 생성할 수 있다.  
StyleRig를 교육하는 데 24시간 미만이 소요되기 때문에 매우 효율적(StyleGAN을 처음부터 학습하는경우 41일 이상의 시간이 걸리는 것에 비하면)(NVIDIA Volta GPU 사용).
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/122628081-01bf2f80-d0ef-11eb-93a7-c606c75267a5.png" width=500 /></p>  


### 8.4. Comparisons to Baseline Approaches (ablation study)
다음에서는 우리의 접근 방식을 몇 가지 기준 접근법과 비교한다.
  
**latent vector "steering"**  
Jahanian(On the ”steerability”of generative adversarial networks.) 연구에 영감을 받아, 우리는 parameter의 변화를 기반으로  
StyleGAN 잠재 벡터를 조향하려고 하는 네트워크 아키텍처를 설계한다. 이 네트워크 아키텍처는 latent w 를 입력으로 사용하지 않으므로 encoder는 필요없다.  
네트워크에 대한 입력은 얼굴 모델의 parameter의 delta이며, 출력은 latent 벡터의 delta이다.  
이런 구조는 네트워크가 얼굴의 형상을 변형할 수 없는 상황에서 바람직한 결과를 이끌어내지 못한다(그림참조).  
따라서 잠재 공간의 semantic 델타도 target paraemter외에 latent 벡터에 conditional 조건이 필요하다.    
  
  
**Different Loss Functions**
Eq. 2(Ltotal = Lrec+Ledit+Lconsist)에서 설명한 바와 같이, 우리의 손실 함수는 세 개의 항으로 구성되어 있다.  
1. Ltotal 제거  
StyleGAN 잠재 코드의 공간에서 이탈하는 출력 잠재 벡터로 이어질 수 있으며, 따라서 non-face 이미지가 생성될 수 있다.  
2. Lconsist 제거
이 loss는 변경되는 매개 변수를 제외한 모든 얼굴 모델 매개 변수의 일관성을 적용한다.  
Lconsist 없이 조명과 같은 차원을 변경하면 헤드 포즈와 같은 다른 차원도 변경된다.  
우리의 최종 모델은 일관된 ID와 장면 정보로 원하는 편집을 보장한다.  
3. Ledit
생성기에 대한 제어가 추가되지 않으므로 좋은 baseline이 아니다.  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/122628303-557e4880-d0f0-11eb-82ba-9698f4c29f9b.png" width=500 /></p>  
  
### 8.5. Simultaneous Parameter Control (추가이해 필요)
parameter를 동시에 제어할 수도 있다. 이를 위해, 우리는 RigNet을 훈련시켜 목표 포즈, 표현 및 조명 파라미터를 입력으로 수신한다.  
모든 (w; v) 훈련 코드 벡터 쌍에 대해, 우리는 세 가지 훈련 샘플을 샘플링한다. 여기에서는 세 개의 파라미터(포즈, 식 또는 조명) 중 한 개가 각 샘플에서 변경된다.  
그런 다음 각 표본에 대해 Eq. 2에 정의된 손실 함수를 사용한다. 따라서, RigNet은 제어 공간의 각 차원을 독립적으로 편집하는 동시에   
동일한 네트워크를 사용하여 편집을 결합할 수 있는 방법을 학습한다. 그림 9는 포즈, 표현 및 조명 매개변수가 소스 이미지에서 대상 이미지로 전송되는 혼합 결과를 보여준다.
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/122628571-bc503180-d0f1-11eb-90c4-bbe2ac78b27a.png" width=500 /></p>  


***
  
## 9. Limitations
StyleGAN에서 생성된 얼굴 이미지에 대한 고품질 의미 제어를 입증했지만, 우리의 접근 방식은 여전히 후속 작업에서 해결할 수 있는 몇 가지 제한에 노출되어 있다.  
분석 섹션에서는 StyleRig가 매개 변수 얼굴 모델의 전체 표현성을 이용할 수 없다는 점에 대해 이미 논의하였다.   
이것은 StlyeGAN의 내부 작업에 대한 멋진 통찰력을 제공하고 그것이 학습한 편견을 성찰할 수 있게 한다.  
미래에는, 이것이 더 나은 생성 모델을 설계하는 방법을 이끌 수 있다. 우리의 접근 방식은 또한 채택된 차별화 가능한 얼굴 재구성 네트워크의 품질에 의해 제한된다.  
현재 이 모델은 미세 스케일 디테일을 재구성할 수 없으므로 명시적으로 제어할 수 없다.  
마지막으로, 매개 변수 얼굴 모델(예: 배경 또는 헤어 스타일)에 의해 설명되지 않는 장면의 일부를 보존하려고 하는 명시적 제약 조건은 없다.  
따라서 이러한 부품은 제어할 수 없으며 매개 변수를 편집할 때 변경될 수 있습다.
  
***
  
## 10. Conclusion
사전 훈련되고 고정된 스타일-GAN 네트워크에 대해 얼굴 리그와 같은 제어를 제공하는 새로운 접근 방식인 스타일 리그를 제안했다.  
우리의 네트워크는 자체 감독 방식으로 훈련되며 추가 이미지 또는 manual annotation이 필요하지 않다.  
테스트 시간에, 우리의 방법은 일련의 의미 제어 매개 변수 세트에 대한 명시적인 제어를 제공하면서 StyleGAN의 광학적 사실성으로 얼굴 이미지를 생성한다.  
우리는 컴퓨터 그래픽 제어와 심층 생성 모델의 결합이 많은 흥미로운 편집 응용 프로그램을 가능하게 하고  
생성 모델의 내부 작동에 대한 통찰력을 제공하며 후속 작업에 영감을 줄 것이라고 믿는다.
