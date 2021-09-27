# Improving Shape Deformation in Unsupervised I2I Translation****
## Abstract
비지도 I2I 변환 기법은 두 도메인간 local texture mapping이 가능케 하지만 형태 변환 문제에는 성공적이지 않다.  
Semantic segmentation에서 영감을 얻어, 전체 이미지에 걸쳐 문맥을 학습하는데 관심을 갖는 dilated conv.를 통해 정보를 사용하는 D를 적용한다.  
이와 함께 object의 기본 형상의 에러를 표현할 수 있는 multi-scale perceptual loss를 적용한다.  
위 방법을 통해 형태변형이 어려운 데이터셋에 대한 성능을 보인다.  
  
**Key concept**
1. Dilated conv.를 D에 적용하여 context 파악이 좋음  
2. Multi-scale perceptual loss를 적용하여 obeject 형상 에러를 더 잘 학습함  
  
## Introduction
기존 연구(DiscoGAN, CycleGAN)는 unsupervised i2i translation task에서 local texture 변환을 잘 하지만  
고양이->개 변환과 같은 형태 변형이 큰 task에는 어려움이 있다.  
예를들어, 단순히 동물의 질감정보만 변경해서는 변경이 불가능ㄴ하고 전체 이미지의 공간 정보를 사용할 수 있는 능력이 필요하다.  

**DiscoGAN**과 같이 완전 연결 D를 가진 네트워크의 경우는 용량을 크게 설계하면 더 큰 형태 변형이 가능하지만  
학습속도가 매우 느리고 디테일한 부분에는 문제가 있다. 

**CycleGAN**에서 사용되는 패치 기반 판별기는 고주파 정보를 잘 해석하고 상대적으로 빠르게 학습하지만  
네트워크가 공간적으로 local contents만 고려할 수 있도록 각 패치에 대해 제한된 'receptive field'를 가지고 있다.  
이러한 네트워크는 G에 대한 loss 정보의 양을 줄인다.  
cycle consistency를 유지하는 loss는 고주파 정보를 유지하는데 사용 되기 때문에 모양 변경 작업에는 방해가 된다.  
위와같은 약점을 해결하기 위해 패치 기반 D가 더 많은 이미지 context를 사용할 수 있도록 dilated conv.를 사용한다.  
이를 통해 판별 작업을 semantic segmentation 문제로 취급할 수 있다.  
D는 per-pixel 판별ㅇ르 수행하며 각각은 global context에 의해 정보를 얻는다.  
이러한 방식은 D가 G로의 loss 전달을 더욱 세분화된 정보 전달이 되도록 한다. 
또한 'multi-scale structure similarity perceptual reconstruction loss'를 사용하여 픽셀이 아닌 이미지 영역에 대한 오류를 나타낸다.  
