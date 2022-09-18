Efficient Geometry-aware 3D Generative Adversarial Networks

## Abstract
단일 2D 사진 집합만을 사용한 고품질 다시점 이미지 및 3D shape 비지도적 생성은 오랜 도전 과제였다.
현존하는 3D GAN 방식은 아래와 같다.  
계산 집약적 방식 : 품질과 생성 이미지 해상도에 제한이 되도록 함  
근사 방식  : 여러 시점의 일관성이나 shape 품질에 나쁜 영향을 줌  
본 연구는 이러한 근사에 과도하게 의존하지 않은채로 계산적으로 효율적이며 3D GAN의 이미지 품질을 향상시킨다.  
다른 설계 선택과 함께 고해상도 다중 뷰 일관 이미지를 실시간으로 합성할 뿐만 아니라 고품질 3D 지오메트리를 생성하는 표현형 하이브리드 explicit-implicit 네트워크 아키텍처를 소개한다.  
Feature 생성과 neural rendering을 분리함으로써 우리의 프레임워크는 StyleGAN2와 같은 SOTA 2D CNN G를 활용할 수 있다. 그리고 효율성과 표현력을 이어받는다.

## 1. Introduction
SOTA GAN은 2D에서만 작동하며 기본 3D scene을 명시적으로 모델링하지 않는다. 3D aware GAN에 대한 최근 연구는 geometry 또는 multi-view 이미지 컬렉션에 대한 감독 없이 multi-view-consistent image synthesis 그리고 적게는 3D 모양 추출 문제를 해결하기 시작했다. 그러나 기존 3D GAN의 이미지 품질과 해상도는 2D GAN에 비해 크게 뒤처졌다. 게다가, 지금까지 그들의 3D 재구성 품질은 아쉬운 점이 많다. 이러한 격차의 주요 이유 중 하나는 이전에 사용된 3D G와 신경 렌더링 아키텍처의 계산 비효율성이다.  
  
2D GAN과 달리 3D GAN은 G 아키텍처에서 3D-structure-aware inductive bias와 view-consistent result를 제공하는 것을 목표로 하는 neural rendering 엔진의 조합에 의존한다.  
Inductive bias는 명시적 voxel grids 또는  neural implicit representations을 사용하여 모델링될 수 있다.  
Single-scene “overfitting” 시나리오에서는 성공했지만, 이러한 표현은 단순히 메모리가 너무 비효율적이거나 느리기 때문에 고해상도 3D GAN 훈련 적합하지 않다.  
3D GAN을 훈련하려면 수천만 개의 이미지를 렌더링해야 하지만 이러한 표현으로 고해상도에서의 SOTA  neural volume rendering은 계산적으로 불가능하다.  
이를 해결하기 위해 CNN 기반 이미지 업샘플링 네트워크가 제안되었지만, 이러한 접근 방식은 view consistency를 희생하고 학습된 3D 지오메트리 품질을 손상시킨다.  

3D-grounded neural rendering에 충실하면서 렌더링의 계산 효율성을 향상하는 단일 뷰 2D 사진 모음으로부터 감독되지 않은 3D 표현 학습을 위한 새로운 G 아키텍처를 소개한다.  
우리는 두 가지 접근 방식으로 이 목표를 달성한다. 
첫째, 표현력을 손상시키지 않고 완전히 암묵적이거나 명시적인 접근 방식에 비해 상당한 속도와 메모리 이점을 제공하는  **hybrid explicit–implicit 3D 표현**을 통해 3D grounded neural rendering의 계산 효율성을 향상시킨다.  
이러한 장점은 우리의 방법이 이전 접근 방식의 렌더링 해상도와 품질을 제한하고 이미지 공간 컨볼루션 업샘플링에 과도하게 의존하도록 강요하는 계산 제약을 피할 수 있게 한다.  
둘째, 3D 지상 렌더링에서 벗어나는 일부 이미지 공간 근사치를 사용하지만, 우리는 신경 렌더링과 최종 출력 사이의 일관성을 유지하여 바람직하지 않은 뷰 불일치 경향을 정규화하는 이중 식별 전략을 도입한다.  
또한, 우리는 훈련 데이터에 내재된 포즈 상관 속성의 공동 분포를 충실하게 모델링하는 동시에 추론 중에 다중 뷰 일관된 출력에 대한 포즈 상관 속성(예: 얼굴 표정)을 분리하는 포즈 기반 컨디셔닝을 생성기에 도입한다.
  
추가 이점으로, feature 생성을 nerual-rendering에서 분리하여 StyleGAN2 같은 SOTA 2D CNN G 직접 활용할 수 있게 한다.  
3D multi-view-consistent neural volume rendering 이점을 누리면서 3D 장면의 공간을 일반화한다.  
우리의 접근 방식은 viewconsistent 3D-aware image synthesis에 대한 SOTA 질적 및 정량적 결과를 달성할 뿐만 아니라 강력한 3D 구조 인식  inductive bias로 인해 합성된 장면의 고품질 3D 모양을 생성한다(그림 1 참조)   
![image](https://user-images.githubusercontent.com/40943064/190911593-824107f8-d270-4753-b1cf-d1a96c5683f0.png)  

