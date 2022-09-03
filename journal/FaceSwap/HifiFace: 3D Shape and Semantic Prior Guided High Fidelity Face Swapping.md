# HifiFace: 3D Shape and Semantic Prior Guided High Fidelity Face Swapping

## Abstract
특징 : 뛰어난 source face shape 표현 + Photo realistic image  
보통 face recognition 모델 만 사용하지만 3DMM 파라미터와 face recon. 모델을 통해 얼굴 shape정보를 적용한다.  
SFF(semantic facial fusion) 모듈을 통해 encoder와 decoder feature를 잘 섞고 모듈의 segmentation을 통해  
사실적인 blending을 가능하게 한다.  

## 1. Introduction
Face Swapping은 source의 ID, target의 속성(포즈, 표현, 조명, 배경 등, 예: 그림 1)을 가진 이미지를 생성하는 작업이며,  
영화와 게임에서 잠재적 사용으로 관심을 끌었다.  
높은 충실도의 fs 결과를 생성하기 위해, 다음과 같은 몇 가지 중요한 문제가 있다. :  
(1) 얼굴 형태를 포함한 결과 얼굴의 ID는 source 얼굴에 가까워야 한다.  
(2) 결과는 target 표정과 자세에 충실하고 target 이미지의 세부 정보(조명, 배경, 폐색)와 일관되는 사실적이어야 한다.  
생성얼굴의 ID 보존을 위해 이전 작업(Nirkin 등, 2018; Nirkin 등, 2019; Jiang 등, 2020)은 3DMM 피팅 또는  
얼굴 랜드마크 유도 재현을 통해 내부 얼굴 영역을 생성하고 그림 2(a)와 같이 target 이미지에 혼합한다.  
이러한 방법은 3DMM이 ID 세부 사항을 모방할 수 없고 target 랜드마크에 target 이미지의 ID가 포함되어 있기 때문에 ID 유사성이 약하다.  
또한 블렌딩 단계는 얼굴의 변화를 제한한다.  
그림 2(b)에 표시된 것처럼(Liu, 2019; Chen, 2020)은 ID 유사성을 개선하기 위해 face recognition NN를 활용한다.  
그러나 이 모델은 texture에 더 초점을 맞추고 geometric structure에 둔감하여 얼굴 형태를 보존이 어렵다.  
사진 사실적 결과 생성에 대해(Nirkin 등, 2018; Nirkin 등, 2019)은 poisson blending 을 사용하여 조명을 고정했지만  
고스팅을 유발하는 경향이 있었고 복잡한 외관 조건을 처리할 수 없었다.  
(Jiang, 2020; Zhu, 2020; Li, 2019)는 조명 또는 폐색 문제를 최적화하기 위해 추가 학습 기반 단계를 설계했지만  
까다롭고 한 모델에서 모든 문제를 해결할 수 없다.  
위의 결함을 극복하기 위해, 우리는 HifiFace라는 새롭고 우아한 end-to-end 학습 프레임워크를 제안하여  
3D shape과 semantic prior를 통해 높은 충실도의 fs을 생성한다.  
특히, 먼저 3D face recon.으로 source와 target face coefficeint를 regression 하고 shape 정보로 재결합한다.  
그런 다음 우리는 그것을 face recognition 모델의 id 벡터와 결합한다.  
3D geometric 구조 정보를 explicit하게 사용하고 source의 id, target의 표정, 자세를 가진 재조합된 3D 얼굴 모델을 auxiliary supervision으로 사용하여  
정확한 얼굴 shape 전송을 수행한다.  
이를 통해, 얼굴 shape에서 더 유사한 id 성능을 달성할 수 있다.  
더 사실적인 결과를 위해  SFF(Semantic Facial Fusion) 모듈을 도입한다.  
조명과 배경과 같은 속성에는 공간 정보가 필요하고 높은 화질 결과에는 상세한 텍스처 정보가 필요하다.  
인코더의 low level feature에는 공간 및 텍스처 정보가 포함되어 있지만 target 이미지의 풍부한 id도 포함되어 있다.  
따라서 id 손상 없이 attribute를 더 잘 보존하기 위해 SFF 모듈은 학습된 적응형 안면 마스크에 의한 low level의 인코더 기능과 디코더 기능을 통합한다.  
마지막으로 occlusion 문제를 극복하고 완벽한 배경을 달성하기 위해 학습된 face mask로 출력물을 target에 혼합한다.  
HifiFace는 직접 블렌딩을 위해 target 이미지의 페이스 마스크를 사용한(Nirkin, 2019)과 달리  
확장 얼굴 의미 분할의 지침에 따라 페이스 마스크를 동시에 학습하므로 모델이 얼굴 영역에 더 집중하고 가장자리 주변에 적응 융합을 할 수 있다.  
HifiFace는 이미지 화질, 폐색, 조명 문제를 하나의 모델에서 처리하여 결과를 보다 사실적으로 만든다. 
광범위한 실험을 통해 우리의 결과가 얼굴 변화가 큰 야생 얼굴 이미지에서 SOTA를 능가한다는 것을 입증했다.  

기여는 다음과 같이 요약될 수 있다.  
  
1. HifiFace라는 새롭고 우아한 end-to-end 학습 프레임워크를 제안한다.  
source shape을 잘 보존하고 높은 충실도의 얼굴 교환 결과를 생성할 수 있다.  

2. 3D shape-aware identity extractor를 제안한다.  
이 추출기는 source face의 얼굴 모양을 보존하는 데 도움이 되는 정확한 형상 정보로 ID 벡터를 생성할 수 있다.  
  
3. 폐색 및 조명 문제를 해결하고 높은 화질로 결과를 생성할 수 있는 semantic face fusion 모듈을 제안한다.  

## 2. Related Work
  
**3D-based Methods**  
  
**GAN-based Methods**  
  
## 3. Approach
### 3.1 3D Shape-Aware Identity Extractor

### 3.2 Semantic Facial Fusion Module
**Feature-Level. **  
**Image-Level.**  

### 3.3 Loss Function
**3D Shape-Aware Identity (SID) Loss.**
**Realism Loss.**
**Overall Loss.**

## 4 Experiments
**Implementation Details.**  
### 4.1 Qualitative Comparisons
### 4.2 Quantitative Comparisons
### 4.3 Analysis of HifiFace
**3D Shape-Aware Identity.**  
**Semantic Facial Fusion.**  
**Face Shape Preservation in Face Swapping.**

## 5 Conclusions
