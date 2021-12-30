# On Face Segmentation, Face Swapping, and Face Perception

## Abstract 

이전까지 정면을 바라보는 특정 이미지 쌍에 대해서만 face swapping이 가능 했지만 본 연구는 그러한 제약 없이 임의 이미지 쌍에 대해 face swapping이 간단한 방식으로 동작할 수 있음을 보인다. 구체적으로 다음과 같은 기여를 한다.  
1)	과거 방식이 segmentation을 위해 시스템을 맞춘 것과 달리 충분한 셋에 학습한 FCN을 활용하여 빠르고 정확한 segmentation을 획득 할 수 있다.  
2)	Segmentation을 활용하여 robust한 face swapping을 새로운 조건에서 수행할 수 있다.  
3)	LFW(Labeled Faces in the Wild) benchmark를 사용하여 동일 인물과 인물간 face swapping을 측정한다.  

## 1. Introduction
  
기술적으로 Segmentation과 face swapping pipeline에 집중한다.  
본논문의 기여는 다음과 같다.  

1) Semi-supervised labeling of face segmentation.  
: Motion cue와 3D data augmentation을 사용하여 얼굴 segmentation 레이블이 있는 풍부한 이미지 세트를 적은 노력으로 생성할 수 있는 방법을 보인다.  
수집한 데이터는 표준 FCN을 학습하여 얼굴을 segment하여 정확도와 속도 모두에서 이전 결과를 능가하는 데 사용된다.  
2) Face swapping pipeline.  
: Face swapping을 위한 파이프라인을 설명하고 개선된 얼굴 segmentation과 강력한 시스템 구성 요소를 사용하면 제약이 없는 까다로운 조건에서도 고품질 결과를 얻을 수 있음을 보인다.  
3) Quantitative tests.  
: 10년이 넘는 작업에도 불구하고 다른 얼굴 처리 작업(예: 인식)과 달리 얼굴 교환 방법은 정량적으로 테스트된 적이 없다.  
본 논문은 LFW 벤치마크[15]를 기반으로 두 가지 테스트 프로토콜을 설계하여 개체 내 및 개체 간 face swapping이 얼굴 recongnition에 미치는 영향을 테스트한다.  

정성적 결과는 우리가 교환한 얼굴이 다른 사람들이 만든 얼굴만큼 매력적이라는 것을 보인다. 정량적 테스트는 또한 intra-subject face swapping이 얼굴 확인 정확도에 거의 영향을 미치지 않는다는 것을 보여준다. 우리의 swapping은 인공물을 도입하거나 피사체 ID에 영향을 주는 방식으로 이러한 이미지를 변경하지 않는다. 무작위로 선택된 쌍에 대한 피험자 간 결과를 보고합니다. 이 테스트에서는 source 얼굴을 새로운 환경과 자연스럽게 혼합하기 위해 얼굴 모양을 변경해야 하는 경우도 있다. 우리는 이것이 그것들을 변화시켜 인식하기 어렵게 만든다는 것을 보인다. 이 perceptual 현상은 20여 년 전에 Sinha와 Poggio[40]가 그들의 잘 알려진 ClintonGore 착시에서 설명했지만 우리는 이것이 machine face recognition에 어떻게 적용되는지에 대한 이전의 정량적 보고서를 알지 못한다.  

## 2. Related work
**Face segmentation.**  
배경이나 occlusion을 제외하고 얼굴만 바꾸기 위해 per-pixel segmentation label이 필요하다. 이전 방법은 눈, 입과 같은 개별 얼굴 영역을 segment하지만 전체 얼굴은 수행하지 않는 방법이었다. Example 기반 방법도 제안되었다. 더 최근에는 deformable part 모델을 사용하여 segmentation과 landmark localization 사이에서 교환함으로써 얼굴을 segment 하였고 COFW 데이터셋에 SOTA 결과를 report 하였다.   
DNN을 이용해 얼굴을 segment하기 위한 두가지 방법이 최근에 제안되었다. [29]에서 네트워크는 전체 얼굴을 포함한 여러 얼굴 영역을 동시에 segment 하도록 학습되었다. 이 방법은 [19]의 face swapping 방법에서 사용되었지만 매우 느릴 수 있다. 더 최근 방식 [39]는 Deconvolutional NN을 사용하여 FaceSwap 데이터와 COFW에서 [11] 보다 나은 실시간 처리 속도 면에서 나은 성능을 보였다. 본 방법은 어려운 학습 examples를 얻을 수 있는 새로운 학습 데이터 컬렉션과 데이터 증강 방법들을 처리하는 segmentation을 위해 FCN을 사용한다.  

**Face swapping.**  
이전 face swapping은 몇가지 공통적인 면이 있다. 첫째, 일부는 전송에 사용되는 대상 사진을 제한한다. 입력 source가 주어지면 큰 얼굴 앨범을 검색하여 얼굴 교체가 쉬운 대상을 선택한다[4, 8, 19]. 이러한 target은 얼굴 톤, 포즈, 표정 등을 포함하여 source와 유사한 모양 속성을 공유하는 대상이다. 우리의 방법을 유사한 설정에 적용할 수 있지만 테스트는 source 및 target 이미지가 임의로 선택되고 실질적으로 다를 수 있는(종종 다를 수 있는) 보다 극한 조건에 초점을 맞춘다.  
둘째, 대부분의 기존 방법은 얼굴의 구조를 추정한다. 일부 방법은 3DMM을 피팅하여 3D 얼굴 모양[1, 4, 27, 28]을 추정한다. 다른 사람들은 대신 밀도가 높은 2D 활성 모양 모델을 추정한다[9, 46]. 이 방법은 개별 얼굴 모양에 걸쳐 텍스처를 올바르게 매핑하기 위해 수행된다.  
마지막으로 이미지 간에 스타일이 전송되는 것처럼 DL을 사용하여 얼굴을 전송했다[22]. 그러나 이 방법은 각 source에 대해 NN을 학습해야 하므로 비실용적일 수 있다.  

## 3. Swapping faces in unconstrained images
### 3.1. Fitting 3D face shapes
### 3.2. Deep face segmentatio
### 3.3. Face swapping and blendin

## 4. Experiments
### 4.1. Face segmentation results
### 4.2. Qualitative face-swapping results
### 4.3. Quantitative tests

## 5. Conclusions
