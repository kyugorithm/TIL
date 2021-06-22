## Abstract
Image2Image 변환은 정렬된 이미지 짝의 학습세트를 사용하여 입력/출력 이미지 mapping을 배우는 목표인 비전과 그래픽문제이다.  
그러나 많은 task에서 짝을 이룬 학습데이터를 얻는것은 매우 어렵다.   
우리는 짝을 이룬 데이터가 없는 상황에서 source 도메인 X로부터 target 도메인 Y로의 이미지를 변환하기 위한 학습방법을 제시한다.  
우리의 목표는 G(X);생성이미지와 실제 Y의 분포를 구분할수 없이 감쪽같은 mapping G : X → Y을 하는것을 배우는것이다.  

이러한 문제 정의는 매우 under-constrained 이기 때문에 우리는 G와 짝이되는 mapping F : Y → X를 적용하고  
F(G(X)) ≈ X, G(F(Y)) ≈ Y를 강제하는 **cycle consistency loss**를 적용한다.  
Qualitative result : 짝을 이룬 학습 데이터가 없는 여러 task(including collection style transfer, object transfiguration, season transfer, photo enhancement, etc)
Quantitative result : 여러 이전 방법론들과의 비교우위를 제시한다.

## Introduction

클로드 모네는 1873 년 아름다운 봄날 아르 장 퇴유 근처 센 강둑 옆에 자신의 이젤을 놓았을 때 무엇을 보았을까?  
![image](https://user-images.githubusercontent.com/40943064/122921811-eb8acb00-d39d-11eb-86ec-2caf3cc46e72.png)  
컬러 사진이 발명 되었다면 맑고 푸른 하늘과 그것을 반사하는 유리 강을 기록했을지도 모른다.  
모네는 희미한 붓놀림과 밝은 팔레트를 통해 같은 장면에 대한 인상을 전달했다.  
모네가 시원한 여름 저녁에 카시스의 작은 항구에서 일어났다면 어떨까?  
![image](https://user-images.githubusercontent.com/40943064/122921906-09583000-d39e-11eb-9722-6ce104cc3eae.png)  
Monet 그림 갤러리를 잠시 산책하면 그가 장면을 어떻게 렌더링했을지 상상할 수 있다. 아마도 파스텔 색조, 갑작스런 페인트와 다소 평탄한 다이나믹 레인지가 있다.  
그가 그린 장면의 사진 옆에 모네 그림의 나란히있는 예를 본 적이 없음에도 불구하고 우리는이 모든 것을 상상할 수 있다.  
대신 우리는 모네 그림 세트와 풍경 사진 세트에 대한 지식을 가지고 있다. 이 두 세트 간의 **스타일 차이**에 대해 추론 할 수 있으므로  
한 세트에서 다른 세트로 **'번역'** 하면 장면이 어떻게 보일지 상상할 수 있을것이다.  
본 논문에서는 한 이미지 컬렉션의 특수한 특성을 캡처하고 이러한 특성을 다른 이미지 컬렉션으로 변환 할 수있는 방법을 파악하는 등 동일한 작업을 학습 할 수있는 방법을 제시한다.  
이 문제는 이미지를 이미지로 변환하는(주어진 scene에 x 대한 하나의 표현에서 다른 scene y로 이미지를 변환하는) 것으로보다 광범위하게 설명 할 수 있다.  
예를 들어 회색조를 컬러로, 이미지를 레이블로, edge-map을 사진으로 변환하는 예제들이 있다.  

컴퓨터 비전, 이미지 처리, 컴퓨터 사진 및 그래픽에 대한 수년간의 연구를 통해 지도학습에서 강력한 translation 시스템이 만들어졌다.  
여기에서 예제 이미지 쌍 {xi, yi}^N_{i=1}를 사용할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/122922988-28a38d00-d39f-11eb-9bf6-2120e159ed14.png)  
e.x., : [ 11, 19, 22, 23, 28, 33, 45, 56, 58, 62].  

그러나 페어링 된 데이터를 얻는 것은 어렵고 비용이 많이든다. 예를 들어 semantic segmentaion (e.x, : [4])와 같은 작업에 대해  
몇 개의 데이터 세트 만 존재하며 상대적으로 작다. 원하는 출력이 매우 복잡하고 일반적으로 예술적 저작이 필요하기 때문에 예술적 스타일 화와 같은 그래픽 작업에 대한  
입력-출력 쌍을 얻는 것은 훨씬 더 어려울 수 있다. 객체 변형 (예 : zebra↔horse, 그림 1 상단-중간)과 같은 많은 작업의 경우 원하는 출력이 잘 정의되어 있지 않다.  
따라서 우리는 쌍을 이룬 입력-출력 예제없이 도메인 간 번역을 배울 수있는 알고리즘이 필요하다.  
![image](https://user-images.githubusercontent.com/40943064/122923185-60aad000-d39f-11eb-85f8-eff3f282ce78.png)  

예로 동일한 기본 장면의 두 가지 다른 렌더링이라고 가정하고 도메인간 몇가지 기본 관계가 있다고 가정하고 그 관계를 배우려고한다.  
paired 예로 지도학습이 부족하더라도 세트수준에서 지도방식을 이용할 수 있다. 도메인 X에 이미지집합이 있고 도메인 Y에 다른 집합이 주어진다.  
yhat을 분류하도록 훈련 된 Discriminator에 의해 yhat = G (x), x ∈ X, X가 이미지 y ∈ Y와 구별되지 않도록 mapping G : X → Y를 훈련시킬 수 있다.  
이론적으로 이 목표는 경험적 분포 pdata(y)와 일치하는 yhat에 대한 출력 분포를 유도 할 수 있다 (일반적으로 G는 확률 적이어야 함).  

따라서 최적의 G는 도메인 X를 Y와 동일하게 분포 된 도메인 Yhat으로 변환한다.  
그러나 이러한 변환은 개별 입력 x와 출력 y가 의미있는 방식으로 쌍을 이루는 것을 보장하지 않는다.  
yhat에 대해 동일한 분포를 유도하는 mapping G가 무한히 많다. 더욱이, 실제로 우리는 적대적 목표를 분리하여 최적화하는 것이 어렵다는 것을 발견했다.  
표준 절차는 종종 모든 입력 이미지가 동일한 출력 이미지에 mapping되고 최적화가 진행되지 않는 mode collapse 문제로 이어진다.  
이러한 문제는 우리의 objective에 더 많은 구조를 추가 할 것을 요구한다.  
예를들어 영어->프랑스어 번역 후 프랑스어 -> 영어 번역시 원래 문장으로 돌아가야한다는 의미에서 'consistency cycle' 속성을 이용한다.  
수학적으로 우리가 번역가 G : X → Y와 다른 번역가 F : Y → X를 가지고 있다면, G와 F는 서로 역이어야하며 두 mapping 모두 **bijections** 이어야한다. 
mapping G와 F를 동시에 훈련하고 F (G (x)) ≈ x 및 G (F (y)) ≈ y를 장려하는주기 일관성 손실 [64]을 추가하여이 구조적 가정을 적용한다.  
이 loss를 도메인 X 및 Y에 대한 adversarial loss와 결합하면 짝을 이루지 않은 이미지 대 이미지 변환에 대한 전체 목표가 산출된다.  
우리는 컬렉션 style transfer, object transfiguration, season transfer 및 photo-enhancement를 포함한 많은 활용에 우리 방법을 적용한다.  
또한 직접정의 style/content 분해나 shared embedding function에 의존하는 이전 접근과 비교하여 능가한다는 것을 보여준다.  

## Related Work

### Generative Adversarial Networks (GANs)
이미지 생성, 편집, 표현 학습에서 인상적인 결과를 얻었다. 최근에는 text2image, image inpainting, 미래 예측과 같은 조건부 이미지 생성 응용 프로그램뿐 아니라 비디오 및 3D 데이터와 같은 다른 영역에도 동일한 아이디어를 적용한다. GAN의 성공의 열쇠는 생성 된 이미지가 원칙적으로 실제 사진과 구별 할 수 없게 만드는 적대적 손실이라는 아이디어입니다. 이 손실은 이미지 생성 작업에 특히 강력하다. 이는 대부분의 컴퓨터 그래픽이 최적화하려는 목표이기 때문이다. 번역 된 이미지가 대상 도메인의 이미지와 구별되지 않도록 mapping을 학습하기 위해 적대적 손실을 채택한다.  

### Image-to-Image Translation
시작은 적어도 단일 입출력 학습이미지 쌍에 non-parametric 텍스처 모델을 사용하는 Hertzmann의 Image Analogies로 거슬러 올라간다. 최근 접근 방식은 입출력 예제 데이터 세트를 사용하여 CNN을 사용하는 parameter 변환 함수를 학습한다. 우리의 접근 방식은 Isola의 "pix2pix"프레임 워크를 기반으로하며, conditional GAN을 사용하여 입력에서 출력 이미지로의 mapping을 학습한다. 비슷한 아이디어가 스케치 또는 속성 및 의미 레이아웃에서 사진을 생성하는 것과 같은 다양한 작업에 적용되었다. 그러나 위의 이전 작업과 달리 unpaired 데이터로 mapping을 학습한다.

### Unpaired Image-to-Image Translation
다른 몇 가지 방법도 두 개의 데이터 도메인 인 X 및 Y를 연결하는 것이 목표 인 unpaired 설정을 다룬다.  
Rosales는 source 이미지에서 계산 된 패치 기반 Markov 랜덤 필드와 여러 스타일 이미지에서 얻은 likelihood 항을 기반으로 한  
prior를 포함하는 베이지안 프레임 워크를 제안한다. 최근에는 CoGAN 및 크로스 cross-modal scene 네트워크가 weight 공유 전략을 사용하여  
도메인 전체에서 공통된 표현을 학습한다. Liu는 VAE와 GAN을 조합하여 위의 프레임 워크를 확장한다.  
또 다른 동시 작업 라인은 입출력이 'style'이 다를 수 있지만 특정 'content' feature를 공유하도록 한다.  
(class label space, image pixel space, image feature space) 같은 사전 정의 된 metric space의 입력에 근접하도록 출력을 강제하는 추가 term과 함께 Adversarial network를 사용한다.  
우리 방식은 입출력 사이의 작업 별 미리 정의 된 유사성 함수에 의존하지 않으며 동일한 저 차원 임베딩 공간에 있어야한다고 가정하지도 않는다.  
이러한 방식은 우리 방법이 다양한 vision task에 일반적인 해법으로 적용될 수 있게한다. 

### Cycle Consistency

구조화된 데이터를 정규화하는데 transitivity를 사용하는 개념은 오랜 역사를 가진다.  
Visual tracking에서, 간단한 forward-backward consistency를 적용하는것은 몇십년간 표준 트릭이었다.  
언어 도메인에서, “back translation and reconciliation”을 통한 번역을 검증하고 양상시키는 것은 인간 번역가와 기계에 의해 사용된 기법이다.  
최근에는 고차원 cycle consistency가 motion, 3D shape matching, cosegmentation, dense semantic alignment, depth estimation에서 사용되어 왔다.   
물론 Zhou와 Godard는 cycle consistency loass를 CNN 지도학습을 위해 transitivity를 사용하는 방식으로써 사용한 면에서 우리의 연구와 가장 유사하다.  
이 연구에서, 우리는 유사한 loss를 사용하여 G, F가 서로 consistent도록 한다. Yi는 ML변환에서 영감을 받아 image2image 변환을 하는데 유사한 목적함수를 독립적으로 사용하였다.   

### Neural Style Transfer
Image2Image 변환을 수행하는 다른 방법으로, 사전 훈련 된 심층의 Gram-Matrix 통계를 일치시켜 한 이미지의 내용을 다른 이미지의 스타일 (일반적으로 그림)과 결합하여 새로운 이미지를 합성한다.  
반면에 우리의 주요 초점은 더 높은 수준의 외관 구조 간의 일치를 포착하려고 시도하여 두 특정 이미지 사이가 아닌 **이미지 컬렉션 간의 mapping**을 학습하는 것이다.  
따라서 우리의 방법은 단일 샘플 전송 방법이 잘 수행되지 않는 페인팅 → 사진, 물체 변형 등과 같은 다른 작업에 적용될 수 있다.

## Formulation
in one page
![image](https://user-images.githubusercontent.com/40943064/122942682-5a255400-d3b1-11eb-9347-b51d8aff90b3.png)

## Implementation
### Network Architecture

style transfer와 super resolution에서 인상적인 결과를 보여준 Johnson의 논문 [Perceptual Losses for Real-Time Style Transfer and Super-Resolution]  
의 구조를 채택한다. 네트워크 구조는 아래와 같다.  
[3 convolutions, several residual blocks, 2 fractionally-strided convolutions with stride 1 2, 1 convolution that maps features to RGB]  
6 blocks for 128 × 128 images & 9 blocks for 256×256 and 고해상도 학습이미지  
Jonson의 논문과 같이 Instance normalization을 사용한다.  
식별자네트워크에서 70 × 70(overlapping 이미지의 real/fake를 분류하는) PatchGANs을 사용한다. 그러한 patch수준 분류기 구조는  
전체 이미지 판별 자보다 매개 변수가 적으며 완전 컨볼 루션 방식으로 임의 크기의 이미지에 대해 작업 할 수 있다.  

### Training details
학습절차를 안정화하기 위해 최신의 두 가지 기술을 적용한다.  
1. -log대신 least-square loss로 대체하여 사용한다. 이 loss가 학습시에 더 안정적이며 나은 이미지를 만들어낸다.  
 - G : minimize E[(D(G(x))-1)^2]  
 - D : minimize E[(D(y)-1)^2] + E[D(G(x))^2]
2. 학습시 osilation을 줄이기 위해 Shrivastava et al.의 전략을 사용한다.  
 - D 학습시 최신 G 생성 이미지가 아닌 이전에 생성했던 이미지를 사용한다. 과거 buffer로 50개 이미지를 저장한다.  
+@  
cycle-consistency loss lambda=10 
Adam solver를 이용하며 batch size = 1.  
모든 네트워크는 lr = 0.0002을 설정하며 처음부터 학습.  
100 epoch까지 lr 유지 후 다음 100 epoch동안 선형적으로 0으로 decay하도록 한다.  
(상세사항(the datasets, architectures, and training procedures) appendix 참조)
