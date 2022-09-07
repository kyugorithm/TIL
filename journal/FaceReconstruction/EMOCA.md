## Abstract
단안 이미지에서 parametric 3D face model을 회귀시키는 최신 방법은 미묘/극단적 감정의 얼굴 표정 스펙트럼을 캡처할 수 없다.  
표준 reconstruction metric(landmark reprojection error, photometric error, and face recognition loss)이 고화질 표현을 캡처하기에 충분하지 않다.  
본 연구는 **Deep perceptual emotion consistency loss**를 도입하여 입력 이미지에 묘사된 표정과 일치하는지 확인하는 데 도움을 주는 방법을 제안한다.  
SOTA와 동등한 3D reconstruction error를 달성하고 표정의 품질과 지각된 감정 콘텐츠 측면에서 훨씬 능가한다.  
또한 valence와 arousal의 수준을 직접 회귀하고 추정된 3D 얼굴 매개변수에서 기본 표정을 분류한다.  
Wild 이미지 감정 인식 작업에서 우리의 순수한 기하학적 접근 방식은 SOTA 이미지 기반 방법과 동등하며 인간 행동 분석에서 3D 기하학의 가치를 강조한다.

## Introduction
얼굴과 감정 표현은 사람의 내부 감정 상태에 대한 중요한 정보를 제공한다. 
감정의 자동화된 분석을 지원하기 위해 단일 RGB 이미지가 주어지면 3D 모양, 포즈 및 표정을 포함한 사람의 얼굴을 캡처한다. 
이를 위해 기존 작업을 넘어 풍부한 감성 콘텐츠를 담은 3D 지오메트리를 추출한다. 
우리는 3D 아바타 생성, 이미지 합성, 비디오 편집 및 얼굴 인식에 광범위하게 적용할 수 있는 매개변수 방법(예: 애니메이션 가능 및 모델 기반)에 중점을 둔다.  
  
3D face reconstruction 분야는 지난 20년 동안 빠르게 발전했다.  
기존의 방법은 표정을 자세하게 캡처하는 데 어려움을 겪고 입력 이미지의 감정적 내용을 전달하지 않는다.   
원인은 아래와 같다.  
  
1) 일부 3D 얼굴 모델은 미묘하거나 극단적인 표정을 포착하기에 충분한 표현력이 부족하다.  
2) landmark reprojection loss, photometric loss, face recognition loss, multi-image consistency losses 같은 재구성 메트릭은 얼굴 표정과 관련이 없거나 이미지 정렬이 필요하다.  
  
그러나 기하학의 미묘한 변화는 지각된 감정에 큰 차이를 초래할 수 있다. 3D 표정을 정확하게 복구하려면 이미지 간의 표정 차이를 측정하는 새로운 reconstruction metric이 필요하다.  
  
이를 위해 3D supervision 없이 wild 이미지 애니메이션 가능한 얼굴 모델을 학습하는 EMOCA에 대해 설명한다. Wild 이미지에서 affect(또는 emotion)을 추정하는 데 엄청난 발전을 이룬 얼굴 감정 인식 분야의 발전에서 영감을 받았다. SOTA emotion recognition 모델을 학습하고 EMOCA 학습중에 이를 supervision으로 활용한다. 입력과 렌더링된 재구성 사이의 감정적 내용의 유사성을 장려하는 새로운 perceptual emotion consistency loss를 도입한다.  
  
새로운 손실은 감정을 더 잘 재구성하지만 이것만으로는 충분하지 않다. 이전 3D Recon. 방법에서 사용된 대용량 이미지 데이터 세트는 다양한 인종의 많은 대상을 포함하지만 감정 표현이 부족하다. 반면에 표정, valence, arousal이 있는 대규모 데이터 세트는 감정이 풍부하지만 다양한 조건 및 더 작은 데이터 세트에서 인물당 여러 이미지를 제공하지 않는다. 통제된 설정에서는 딥 러닝에 적합하지 않다. 그러나 현재의 최신 3D face Recon.을 학습하려면 동일한 사람의 여러 이미지가 필요하다.  
이를 극복하기 위해 공개적으로 사용 가능한 3D 얼굴 재구성 프레임워크인 DECA 위에 구축되어 SOTA id shape Recon. 정확도를 달성한다. 특히, 다른 부분은 고정된 상태로 유지하면서 표정에 대해 학습 가능한 추가 예측 분기로 DECA의 아키텍처를 보강한다. 이를 통해 감정이 풍부한 이미지 데이터에 대해 EMOCA의 표정 부분만 학습할 수 있으므로 DECA의 id 얼굴 모양 품질을 유지하면서 감정 재구성 성능이 향상된다.  

학습을 마치면 EMOCA는 단일 이미지에서 3D 얼굴을 재구성하고, 표정 품질이 SOTA를 훨씬 능가하며, SOTA id 모양을 유지한다.  
재구성 정확도 및 재구성된 얼굴을 쉽게 애니메이션할 수 있다. 또한 EMOCA에 의해 회귀된 expression parameter는 최고의 이미지 기반 방법과 동등한 성능으로 wild 감정 인식을 위한 충분한 정보를 전달한다.  
  
주요 기여는 아래와 같다.  
1) 정확한 감정의 얼굴 표정을 복구하고 wild 이미지에서 애니메이션 가능한 3D face model Recon  
2) 재구성된 감정의 정확성을 보상하는 새로운 perceptual emotion-consistency loss  
3) 야생 감정 인식을 위한 최초의 3D geometry 기반 프레임워크로, SOTA 이미지 기반 방법과 유사한 성능
4) 코드 및 모델은 연구 목적으로 공개적으로 사용 가능

## 2. Related Work
### Monocular face reconstruction:
Model-free 방식은 이미지에서 3D mesh/voxel을 직접 회귀하거나 얼굴 이미지에 맞게 SDF를 최적화한다.  
이런 방법은 대부분 명시적인 3D supervision이 필요하다. 출력에는 모델이 없지만 일반적으로 학습 데이터를 수집하는 데 3DMM이 사용된다.  
따라서 표현 얼굴을 재구성하는 능력은 3DMM 기반 합성 학습 데이터와 실제 이미지 간의 도메인 갭 쌍을 이루는 훈련 데이터를 생성하는 데 사용되는 3DMM 기반 재구성 또는 고정 3DMM 피팅 결과에 대한 정규화에 의해 제한될 수 있다.  
반면 EMOCA는 self-supervised로 교육되므로 덜 제한된 표현을 캡처할 수 있다.  
다른 self-supervised 방법은 얼굴 영역 특정 지식을 활용하지 않으므로 일반 개체에 적용할 수 있지만 재구성 품질이 제한된다.  
EMOCA와 달리 이러한 모델 프리 방법 중 어느 것도 얼굴 표정에서 얼굴 식별을 분리하지 않으므로 표정 retargetting 또는 animation과 같은 응용 프로그램에 적합하지 않다.  
  
여러 작업에서 BFM/FaceWarehouse/FLAME과 같은 고정 통계 모델의 매개변수를 재구성하거나 모델을 공동으로 학습하고 이미지에서 얼굴을 재구성한다.  
기존의 방법은 **최적화 기반**과 **학습 기반**으로 분류할 수 있다. 
후자는 예측된 2D keypoints, 2D 얼굴 윤곽, photometric constraints, face recognition features, multi-view constraints으로 완전히 감독되거나 자체 감독된다.  
각 감독 신호는 고유한 방식으로 재구성된 3D 얼굴에 영향을 준다. 명시적 3D 메시 또는 모델 매개변수 감독은 pseudo-GT 생성에 사용되는 방법에 대한 bias를 유도한다.  
학습 중 face recognition feature를 사용하거나 동일한 인물의 여러 이미지를 활용하는 것은 주로 인물 모양과 외모에 영향을 준다.  
keypoint loss는 얼굴 모양 이미지 align(전역 변형, 아이덴티티 및 표정 모양 매개변수)에 영향을 미치지만 예측된 키포인트는 희박하고(일반적으로 51-68포인트) 종종 부정확하다(특히 극단적인 표정과 머리 포즈의 경우).  
photometric loss는 모든 모델 매개변수(전역 변형, 정체성 및 표현 모양, 모양, 조명)에 영향을 미치지만 키포인트 손실과 마찬가지로 예측된 3D 얼굴과 이미지 사이의 오정렬에 의해 크게 영향을 받는다.  
Multi-view 데이터를 사용하면 보다 정확한 3D 얼굴을 재구성할 수 있는 잠재력이 있지만 많은 수의 ID와 표현, 민족, 연령, 조명 조건 등이 매우 다양한 대규모 데이터 세트가 없다.  
결과적으로, 단안의 wild 얼굴 캡처는 엄청난 발전을 이루었지만, 3D 모양에서 인식할 수 있는 감정을 제한하는 재구성된 표현의 정확성에 여전히 한계가 있다.  
반면 EMOCA는 재구성된 표현에 주로 전파되는 감정 특징을 다양한 표정의 대규모 데이터 세트를 활용할 수 있는 고유한 자체 감독 프레임워크와 결합하여 표현적인 얼굴을 재구성하는 방법을 배운다.  

### Emotion analysis from images:
감정 상태는 일반적으로 이산적 기본(예: 행복, 놀라움, ...) 또는 복합 표정 카테고리(예: happily surprised), 지속적인 valence(긍정적) 및 arousal(relaxed-intensive) 또는 FACS activation(각 동작 단위(AU)는 특정 감정 관련 안면 근육 움직임에 해당).  
  
표정 인식에 대한 초기 작업은 얼굴 구성 요소의 모양과 위치, appearance feature 또는 이들의 조합을 정의하는 geometric feature을 추출한다.  
지난 10년 동안 단일 이미지 표현 분석 및 audio-visual video를 위한 대규모 데이터 세트의 가용성은 수동으로 설계된 기능에서 end-to-end 학습 모델로 초점을 옮겼다.  
Wen과 Huang과 같은 초기 작업은 3D 비강체 표면 추적을 사용하여 표현 재구성을 위한 특징을 추출하지만 대부분의 3D 기반 방법은 3D 스캔에서 표현을 인식하는 데 중점을 둔다.  
EMOCA와 가장 관련성이 높은 것은 [65] 3DMM feature를 사용하여 3가지 표현(3DMM을 스캔에 맞춰 얻음)을 분류하기 때문이다.  
대부분의 다른 방법은 texture가 있는 3D 스캔에서 추출한 다양한 2D 및 3D 기능을 사용한다.  

이미지에서 표정을 인식하는 3DMM 기반 방법은 거의 없다.  
Bejaoui : 3DMM을 이미지에 맞춤  
Chang : 3DMM을 이미지와 비디오에 fiting하여 얻은 parameter에 의해 fully supervised 3DMM parameter regressor를 학습하고 3DMM 표현식 매개변수에서 다양한 표현식을 분류하는 방법을 배운다.  
Shi   : EMOCA와 가장 관련이 있는데 학습중에 표정 인식 손실을 사용하지만 더 discriminative latent representation을 얻는 것을 목표로 한다. 이러한 방법은 3D 재구성을 개선하는 것이 아니라 표현을 인식하는 데 중점을 둔다.  
반면 EMOCA는 감정 인식의 최근 발전을 활용하여 보다 표현력 있는 3D 얼굴을 재구성한다.  
