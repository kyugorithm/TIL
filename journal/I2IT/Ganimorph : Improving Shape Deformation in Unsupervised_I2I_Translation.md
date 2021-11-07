# Improving Shape Deformation in Unsupervised I2I Translation****
## Abstract
비지도 I2I 변환 기법은 두 도메인간 local texture mapping이 가능케 하지만 형태 변환 문제에는 성공적이지 않다.  
Semantic segmentation에서 영감을 얻어, 이미지 문맥을 학습에 관심을 갖는 dilated conv.를 통해 정보를 사용하는 D를 적용한다.  
이와 함께 object의 기본 형상의 에러를 표현할 수 있는 multi-scale perceptual loss를 적용한다.  
위 방법을 통해 형태변형이 어려운 데이터셋에 대한 성능을 보인다.  
  
**Key concept**
1. Dilated conv.를 D에 적용하여 global context 파악  
2. Multi-scale perceptual loss를 적용하여 obeject shape을 잘 학습  
  
## 1. Introduction
기존 연구(DiscoGAN, CycleGAN)는 unsupervised i2i translation task에서 local texture 변환을 잘 하지만  
고양이->개 변환과 같은 형태 변형이 큰 task에는 어려움이 있다.  
예를들어, 단순히 동물의 질감 정보만 변경해서는 안되고 전체 이미지의 공간 정보를 사용할 수 있는 능력이 필요하다.  
  
**DiscoGAN**과 같이 완전 연결 D의 경우 용량을 크게 설계하면 큰 형태 변형이 가능하지만  
학습이 매우 느리고 디테일한 부분에는 문제가 있다. 
  
**CycleGAN**에서 사용되는 패치 기반 판별기는 고주파 정보를 잘 해석하고 상대적으로 빠르게 학습하지만  
네트워크가 공간적으로 local contents만 고려할 수 있도록 각 패치에 대해 제한된 'receptive field'를 가지고 있다.  
이러한 네트워크는 G에 대한 loss 정보의 양을 줄인다.  
cycle consistency를 유지하는 loss는 고주파 정보를 유지하는데 사용 되기 때문에 모양 변경 작업에는 방해가 된다.  
위와같은 약점을 해결하기 위해 패치 기반 D가 더 많은 이미지 context를 사용할 수 있도록 dilated conv.를 사용한다.  
이를 통해 판별 작업을 semantic segmentation 문제로 취급할 수 있다.  
D는 per-pixel 판별ㅇ르 수행하며 각각은 global context에 의해 정보를 얻는다.  
이러한 방식은 D가 G로의 loss 전달을 더욱 세분화된 정보 전달이 되도록 한다. 
또한 'multi-scale structure similarity perceptual reconstruction loss'를 사용하여 픽셀이 아닌 이미지 영역에 대한 오류를 나타낸다.  

## Our Apporch
모양 변형에서 변환의 성공에 결정적인 요소는 global/local 일관성을 유지하는 능력이다.  
우리의 알고리즘은 순환 이미지 변환 프레임워크를 채택하고 dilated D, residual block 및 skip-connection이 있는 G,  
multi-scale perceptual cyclic loss를 통합하여 필요한 일관성을 달성한다.  

### 3.1 Dilated Discriminator
(DiscoGAN)은 fc 레이어가 있는 global D를 사용하며 이미지의 정확성을 결정하기 위해 이미지를 단일 스칼라 값으로 축소한다.  
(CycleGAN, ContrastingGAN)은 patch 기반 DCGAN D를 사용했으며, 초기에는 스타일 전송 및 텍스처 합성을 위해 개발되었다.  
이러한 유형의 D에서 각 이미지 패치는 가짜 또는 실제 점수를 결정하기 위해 평가된다.  
패치 기반 접근 방식은 각 로컬 패치에서 독립적으로 작동하여 빠른 G 수렴을 돕는다.  
이 접근 방식은 texture transfer, segmentation 및 유사한 작업에 효과적인 것으로 입증되었지만  
전역 공간 정보에 대한 네트워크의 인식을 제한하여 일관된 전역 모양 변경을 수행하는 G의 능력을 제한한다.  
_Reframing Discrimination as Semantic Segmentation_  
이 문제를 해결하기 위해 식별 문제를 real/fake 또는 하위 이미지를 판별하는 것에서  
이미지의 실제 또는 가짜 영역을 찾는 보다 일반적인 문제, 즉 semantic segmentation으로 재구성한다.  
D는 고해상도의 segmentation map을 출력하기 때문에 Generator와 Discriminator 사이의 정보 흐름이 증가한다.  
이것은 DiscoGAN과 같이 FC의 D를 사용하는 것보다 수렴이 빠르다.  
Segmentation을 위한 최신 네트워크는 dilated conv.를 사용하며 유사한 수준의 정확도를 달성하기 위해  
기존의 conv.보다 훨씬 적은 매개변수를 요구하는 것으로 나타났다. Dilated conv.는 global 및 patch 기반 D에 비해 이점을 제공한다.  
동일한 매개변수량에 대해 예측을 통해 더 큰 주변 field의 데이터를 통합할 수 있다.  
이렇게 하면 G와 D 간의 정보 흐름이 증가한다.  
이미지의 영역이 이미지를 비현실적으로 만드는 데 기여한다는 것을 알면 G는 이미지의 해당 영역에 집중할 수 있다.  
dilated conv. 대해 생각하는 또 다른 방법은 D가 context를 암시적으로 학습할 수 있도록 하는 것이다.  

다중 스케일 판별기가 고해상도 이미지 합성 작업의 결과와 안정성을 향상시키는 것으로 나타났지만 [38], 판별자가 영역이 어디에 맞아야 하는지 결정할 수 있으므로 이미지에서 더 멀리 떨어진 정보를 통합하는 것이 번역 작업에 유용하다는 것을 보여줄 것입니다. 주변 데이터를 기반으로 이미지로 변환합니다. 예를 들어, 이렇게 증가된 공간적 맥락은 강아지의 얼굴을 몸에 상대적으로 위치시키는 데 도움이 되며, 이는 이웃과 분리되어 학습된 작은 패치나 패치에서 배우기 어렵습니다. 그림 2(오른쪽)는 판별자 아키텍처를 보여줍니다.
  

Current state-of-the-art networks for segmentation use dilated convolutions, and have been shown to require far fewer parameters than conventional convolutional networks to achieve similar levels of accuracy [42]. Dilated convolutions provide advantages over both global and patch-based discriminator architectures. For the same parameter budget, they allow the prediction to incorporate data from a larger surrounding region. This increases the information flow between the generator and discriminator: by knowing that regions of the image contribute to making the image unrealistic, the generator can focus on that region of the image. An alternative way to think about dilated convolutions is that they allow the discriminator to implicitly learn context. While multi-scale discriminators have been shown to improve results and stability for high resolution image synthesis tasks [38], we will show that incorporating information from farther away in the image is useful in translation tasks as the discriminator can determine where a region should fit into an image based on surrounding data. For example, this increased spatial context helps localize the face of a dog relative to its body, which is difficult to learn from small patches or patches learned in isolation from their neighbors. Figure 2 (right) illustrates our discriminator architecture.
### 3.2 Generator

### 3.3 Objective Function

### 3.4 Training
