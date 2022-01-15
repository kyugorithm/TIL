# FSGAN: Subject Agnostic Face Swapping and Reenacment

Created: 2022년 1월 2일 오후 8:05
Property: 2022년 1월 3일
Property 1: 이규철
Tags: 3Dface, Synthesis, face reenactment, face swap

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled.png)

[https://www.youtube.com/watch?v=BsITEVX6hkE&feature=emb_title](https://www.youtube.com/watch?v=BsITEVX6hkE&feature=emb_title)

## Abstract

---

**Functional Novelty**

1. **Reenactment →** **Swapping** 순서로 pipeline을 구성하여 두 가지 task 모두 가능
2. 특정 얼굴에 대해 학습 없이 임의 얼굴에 대해 **Swapping** 가능

### **Methodological Novelty**

1. **Video Sequences 사용 시 interpolation**(**reenactment, Delaunay triangulation, 무게중심**)을 통해  ****더 나은 결과 획득
2. RNN 활용 **단일 이미지 혹은 단일 비디오 sequence**에 대한 Reenactment(**자세, 표정)**
(landmark 필요)
3. face completion network(in-paint network)를 통해 Occluded 영역  처리
4. 얼굴 색상이나 조명 조건을 보존하기 위해 Perceptual loss에 Poisson blending loss(Poisson optimization)를  추가한 blending network 활용

**Keyword : RNN using reenactment, interpolation, in-painting NN, Poisson blending**

## 1. Introduction

---

### 1) 3D 모델을 활용한 방법

단점 **: Occluded region 처리 시 특별한 처리가 필요함**

- (CVPR2016) Face2Face: real-time face capture and reenactment of rgb videos

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%201.png)

- (TOG2017) Synthesizing obama: learning lip sync from audio
- (FG 2018) On face segmentation, face swapping, and face perception
: 2D facial landmark detection → 3D fitting(pose+expression) →segmentation → blending

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%202.png)

### 2) GAN을 활용한 방법

: cGAN(pix2pix) 아이디어 활용

- (ECCV2018) Ganimation: Anatomically-aware facial animation from a single image
- Triple consistency loss for pairing distributions in gan-based face synthesis

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%203.png)

- (ECCV2018) Reenactgan: Learning to reenact faces via boundary transfer

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%204.png)

<aside>
💡 분야 확장에 큰 기여를 한 DeepFake 도 cGAN과 3D 모델을 활용한 방법임

</aside>

### 3) Latent feature 분리 방법

**단점 : ID 정보 분리시 중요 정보가 손실되어 합성 이미지 품질이 저하**

- (ACCV2018) Fsnet: An identity-aware generative model for image-based face swapping

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%205.png)

- Rsgan: face swapping and editing using face and hair representation in latent spaces

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%206.png)

- Cr-gan: learning complete representations for multi-view generation
: Z space를 전체 학습하도록 하여 complete representations을 만들면 보지못한 입력에도 이미지 생성 가능

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%207.png)

<aside>
💡 앞서 소개되었던 Synthesizing obama, DeepFake, Deep video portraits, Reenactgan 방법 모두 Subject specific 방법론

</aside>

### 기존 방법론의 단점

1) Subject specific

2) 3D 모델 활용시 occluded 처리 방법 필요

2) Latent 분리로 인한 이미지 품질저하

## 3. Face swapping GAN

---

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%208.png)

### 1) 문제 정의

**주어진 이미지 세트에 대해**

Fs(Source faces) ∈ Is(Source images)

Ft(Target faces)∈ It(Target images)

**Target image 를 기반으로 자세와 표정을 유지하면서  Ft가  Fs에 의해 대체되도록 함**

### 2) **FSGAN pipeline의 3가지 구성 요소**

**1-1. Reenactment Gr**

: Ft의 (자세와 표정)과 일치하도록 하며  : Fr이 Fs를 모사하도록 reenact 된 이미지 Ir을 생성 : Fr의 Segmentation  Sr 생성

**1-2. Segmentation Gs**

1-1. 결과에 target image 가이드라인을 주기 위해 Ft에 대한 얼굴과 헤어 segmentation 생성  

**2.  Inpainting Gc** Ir는 source ID의 occlusion에 영향 받을 수 있기 때문에 이를 처리하기 위해 in-painting network 사용

입력으로 Ir~와 St를 사용

**3. Blending Gb**

완성된 얼굴이미지 Fc를 It에  입힘

### 3) 네트워크 구조

**Gs** : U-net + biliear interpolation upsampling

**Gr**, **Gc** , **Gb** : Pix2PixHD(coarse-to-fine G and multi-scale D) + U-net + concat(not sum)
+ biliear interpolation upsampling(segmentation 과 동일한 upsampling 방식 적용)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%209.png)

(pix2pixHD의 Generator network 구조)

### 4) Etc.

- **Subject agnostic** 방식이므로 pose 차이가 큰 경우 변환이 실패하기 쉬움. 이를 위한 해결책으로 두가지 방법을 사용
1) 큰 pose의 차이를 여러 변환 단계로 분할
2) target pose에 가장 가까운 source를 찾아 interpolation

### 3.1. Training losses

- **Domain specific perceptual loss.**

:  VGG의 layer별 feature 값으로(layer 1~n) **high-frequency detail**을 비교하기 위해 활용
: 다양한 분야에서 활용되며 얼굴합성에서도 빈번하게 사용
: 얼굴 이미지의 고유정보를 포착하는데 문제가 있어 사전학습된 ImageNet을 사용하지 않고 적용하는 도메인 데이터를 이용하여 얼굴 인식 및 속성 분류문제에 학습하여 활용

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2010.png)

- **Reconstruction loss.**

: perceptual loss만 사용하면 low-frequency content의 reconstruction에 해당하는 부정확한 색상의 이미지를 생성하기에 L1 loss 사용

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2011.png)

따라서 모든 **G 학습**에 사용되는 통합 reconstruction loss는 아래와 같다.

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2012.png)

- **Adversarial loss.**

: 이미지의 사실성 향상(실제 분포 근사)을 위해 adversarial loss도 함께 활용
: Multi-scale D를 활용 반영
x : Is, y:It

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2013.png)

<aside>
💡 **Multi-scale D**
고해상도 이미지를 처리하기 위해서는 (깊은 layer, 큰 kernel을 통해 receptive)를 넓혀야 한다. 이 경우 표현 capacity는 증가하지만 해상도에 비해 작은 데이터 셋의 한계로 over-fitting이 발생할 수 있다. 이를 해결하기 위해 multi-scale D를 사용하고 입력으로 pyramid image(해상도를 2, 4씩 낮춘)를 사용한다. 동일 구조의 D에 대해 다른 해상도를 입력하여 학습하는 것이다.
(**ref. :** Generative Multi-Adversarial Networks, pix2pixHD)

</aside>

multi-scale D가 없으면 생성된 이미지에 반복되는 패턴이 많이 나타나는 것을 관찰할 수 있다.

### 3.2. Face reenactment and segmentation

사용되는 변수와 그 크기는 아래와 같음

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2014.png)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2015.png)

먼저, source와 target의 pose 차이가 큰 경우 해결책으로 제시했던 **분할 방식**을 설명한다.

오일러각 es와 et, vs와 vt의 무게중심 사이를 보간하여 중간 2D 랜드마크 위치 pj를 생성하고 vs를 Is로 다시 투영하는 중간 지점을 사용한다. 

Is → Ir1 → Ir2 → ... (I rn = Ir)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2016.png)

기존에 사용되었던 방법인 0/1 mask와 달리 얼굴과 머리카락 영역을 추가로 고려함으로써 얼굴 segmentation 정확도를 향상시킬 수 있다.

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2017.png)

**Traning.**

기존 정의한 Lrec에 대한 loss 계산 입력으로 rn 버전과 r 버전 모두 사용하며 분할을 통한 loss 계산 term은 stepwise consistency loss라고 정의한다.

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2018.png)

Gs 에 대해서는 아래와같이 정의 된다.
Srt(Gr(It;H(pt)))는 source와 target 동일 id로 주어진 경우를 특별히 정의하는 상황이며

동일 해당 이미지에 대한 Segmentation label이 있기 때문에 학습 가능하다.

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2019.png)

학습은 Gr과 Gs를 1 epoch씩 번갈아가며 수행하며 이 경우 성능이 가장 잘 나온다.

### 3.3. Face view interpolation

연속적인 view를 만들기 위한 새로운 방법을 제시한다. 

특정 비디오 프레임에서 학습하지 않고도 전체 소스 비디오 시퀀스를 사용할 수 있어 agnostic하다.

특정 video sequence에 대해 다음의 데이터를 정의한다.

이미지 세트 {Is1, Is2, ..., Isn}, 오일러 각도 세트 {es1, es2, ..., esn}, 얼굴 세트 {Fs1, Fs2, ..., Fsn} 

이때 아래 그림과 같이 source video에 대해 appearance map을 구성한다. 

(roll angle은 drop : head pose를 추정하는데 크게 중요하지 않은듯)

이때, 가까운 point는 제거하며 (roll angle이 0이 되는 포인트를 남김) blurry 한 이미지 제거

남은 포인트에 대해 -75 ~ 75 영역에서 들로네 삼각형을 이용해 mesh를 구성

Query가 되는 et 입력 → 가까운 삼각형을 탐색 → vertex를 구성하는 3개의 x에 대한 Is 추출 → 3개의 무게중심으로 weight 계산 → 아래 수식을 통하여 연산 후 결과 추출 
(포인트 x가 boundary line에 존재하는 경우 하나의 포인트를 제거하고 lamda를 다시 normalize하여 2개로 계산)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2020.png)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2021.png)

### 3.4. Face inpainting

Source에 존재하는 occlusion 영역을 처리해야 제대로 target이미지를 변환할 수 있다.

저자의 과거 방식에서는 Is와 It에서 occlusion이 없는 영역만을 segmentation으로 탐색해서 swapping 했기 때문에 문제가 있었다.

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%202.png)

학습목표 : Fs의 결과인 ~Ir가 Ft의 St 얼굴 영역을 cover 하도록하여  Fs의 occlusion을 Ft의 얼굴에 맞추어 채워줌

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2022.png)

(저자의 ECCV oral 설명 발췌)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2023.png)

 

### 3.5. Face blending

Fs와 Ft는 skin tone과 lighting이 다르기 때문에 해당 차이를 맞추는 작업 필요

논문 ‘**Semantic Image Inpainting with Deep Generative Models**’ 으로부터 아이디어를 얻어 

**poisson blending optimization**를 적용

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2024.png)

## 4. Datasets and training

### 4.1. Datasets and processing

**Gr 학습 :** 

IJB-C 데이터셋을 사용, 11k 개중 HD 해상도 5.5k 개 video를 사용

3.3의 pruning 기법을 이용해 frame 제거

**Gs 학습** : 

사진이 이미지에서 차지하는 비율이 15% 이하인 경우 제거

dlib 라이브러리를 활용하여 전체 이미지에서 subject 별 100개의 이미지로 grouping 수행(2D landmark 변화가 최대가 되도록 선택)

**Perceptual loss :**

VGG-19 학습시

1) VGGFace2(**3.3M** images depicting **9,131  ID**)로 FR학습 

2) CelebA(**202k** images with **40** binary attributes)로 face attribute classification 학습

## 5. **Experiment Results**

---

### **1) Qualitative face reenactment results**

- 제안한 기본 방법론을 이용해 얻은 결과
- 일반적인 정성적 결과  : 4번째 열의 극단적 차이(Pose와 Expression이 매우 큼)에도 대응가능
- Yaw 크기에 따른 결과  : 큰 angle 변화에 대해 iterative 방식으로 접근하면 ID와 texture가 더 잘 보존 (의견 : 큰 차이는 없어 보임)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2025.png)

### 2) **Qualitative face swapping results**

실험데이터 : FaceForensics++

다양한 표정, 얼굴, occlusion 케이스 사용 [35]와 대등한 비교를 위해 target과 가장 유사한 자세의 source 선택( KC 이해안됨)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2026.png)

### **3) Comparison to Face2Face**

Face2Face와 동일하게 입만 전송하는 문제로 정의 Face2Face는 전반적으로 artifact가 나타나며 target 입 모양을 잘 표현하지 못함

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2027.png)

### **4) Quantitative results**

source의 ID 보존 & target의 자세/표정 반영 1, 2) 품질  비교    : ID, SSIM(dlib 얼굴인식/탐지등 관련 라이브러리) (ID : Face Recognition 모델을 통과한 값의 차이로 계산할 듯) (SSIM : 우리눈은 artifact를 잘 발견하지만 SSIM은 제대로 반영하지 못해서 수치의 차이가 발견되지 않음)

3) 자세 정확도 : Euler angle의 유클리드 거리 ; 단위 degree(Fb vs It) 4) 표정 정확도 : 2D landmark 유클리드 거리; 단위 pixel (Fb vs It) (FaceForensics++에서 500개의 비디오의 첫 100개 프레임 관측값에 대한 평균과 분산 추출)  ID와 SSIM읜 유사하지만 자세와 표정이 잘 반영

(규철 : SSIM이 알맞은 performance measure인가?)

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2028.png)

### **5) Ablation Study**

아래 4가지 케이스 비교 
(Gs는 고정 사용)

모든 경우 ID 동일 

자세와 표정에서 가장 성능이 좋음

SSIM 성능 하락 : 추가 네트워크와 처리단계가 추가가 원인

![Untitled](FSGAN%20Subject%20Agnostic%20Face%20Swapping%20and%20Reenacmen%2018852680da9144e19a34a7a6c7f1cae3/Untitled%2029.png)

## 6. Conclusion

---

### **Limitations.**

1) iteration을 많이 분할 하면 texture blur가 심해짐

2) 아래 그림에서 보는 것과 같이 포즈의 차이가 커질 수록 ID와 texture 품질이 저하됨

3) Face2Face 처럼 이미지로부터 texture를 warp하는 3DMM 기반 방법과 달리 본 방식은 학습데이터 해상도의 한계에 품질이 제한됨

4) Landmark를 사용하기 때문에 landmark 가 sparse한 경우 복잡한 표정을 잘 따라가지 못할 수 있음