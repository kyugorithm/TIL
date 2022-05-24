# Abstract
인물 비디오의 프레임을 직접적으로 수정하는것은 부드럽고 안정적인 비디오 시퀀스를 생성하지 못하게 한다.  
이를 해결하기 위해 강인하고 사용하기 쉬운 parametric 방식을 제안한다.  
아래 두단계의 스텝으로 처리를 수행한다.  

**1) Stabilized Face Reconstruction :**  
- 비디오 프레임 전반에 걸쳐 강인한 얼굴포즈 변환 추정
- 여러장 프레임을 이용한 정확한 얼굴 ID 복원 최적화   

**2) Continuous Video Reshaping :** 
- 얼굴 weight 변화를 반영하는 parametric reshaping model을 이용해서 복원된 3D 얼굴을 변형
- 변형된 3D 얼굴을 활용한 비디오 프레임의 warping 가이드  

Mapping 방법론  : 왜곡을 최소화하는 reshaping 전후의 얼굴 윤곽 warping을 위한 새로운 **SDF(signed distance function)** 기반의 mapping 방법론을 개발  
Dense mapping : temporal consistency를 달성하기 위해 얼굴의 3D 구조를 사용하여 dense mapping을 수정  
배경 왜곡 최소화  : Content-aware warping mesh를 최적화하여 배경 왜곡을 최소화하여 최종 결과를 생성  

## 1. Introduction
연구는 얼굴의 색상, 질감, 스타일 혹은 얼굴형에 대한 수정에 집중되어 왔으며 사진과 비교했을때 동영상 수정은 관심이 상대적으로 적었다.  
개별 프레임 수정을 통해 비디오를 처리할 수 있으나 editing consistency와 temporal coherence을 고려하지 못함으로 인해 주변 프레임간에 걸친 다양한 형태의 artifact가 쉽게 발생할 수 있다.  
목표는 비디오로 인물에 대한 전체적 얼굴 수정을 어색하지 않게 고품질로 만드는것이다. 이러한 기술은 맵시있는 얼굴 생성과 같은 영역에서 사용할 수 있다.  
기존 초상화 수정 방법론들과 비교할 때, 우리 방법론은 3D에서의 신뢰할 수 있는 얼굴 변형을 통한 2D 초상화 수정을 가이드하기 위해 3D 복원 기반의 접근방법을 사용한다.  
그러나 그럴듯한 비디오 수정을 위해서 발생하는 핵심적인 차이는 전체 비디오에 걸친 변형된 초상화의 consistency와 coherency를 요구한다는 것이다.  
이 새로운 요구 사항은 실제로 두 가지 과제, 즉 재구성된 3D 얼굴뿐만 아니라 재구성된 비디오 프레임에서도 consistency와 coherency를 달성하는 방법을 제시한다.  
본 논문에서 고품질의 재구성된 초상화 비디오를 생성할 수 있는 parametric reshaping 방법을 제시한다.  

입력 비디오가 주어지면, 위의 두 가지 과제를 해결하기 위한 두 가지 주요 단계를 포함한다.  
1) 주로 consistent and coherent face reshaping에 초점을 맞춘다. SOTA face parametric model을 기반으로 pose transformation, face identity parameter 및 face expression parameters를 각각 강인하게 추정하는 다단계 최적화를 사용한다.  
우리의 방법은 특히 reshaping후 artifact를 피하기 위한 얼굴 추적에서 얼굴 contour의 안정성과 관련이 있다. 모든 프레임에서 일관된 얼굴 정체성을 추정하기 위해 모든 프레임이 아닌 대표 프레임을 공동으로 최적화하여 계산 비용을 절감한다.  
최적화의 energy term은 spatial-temporal 계산 효율성을 모두 고려하여 광범위한 ablation 연구를 통해 신중하게 선택된다.  

2) 시각적 아티팩트가 없는 재구성된 비디오 프레임을 생성하려고 시도한다.  
3D로 재구성된 얼굴의 안내를 받아 content-aware image warping을 사용하여 각 프레임을 변형한다. 재구성 후 얼굴 occlusion으로 인한 왜곡 아티팩트를 방지하기 위해 SDF를 사용하여 재구성 전후에 얼굴 윤곽의 조밀한 2D 매핑을 구성한다. 또한, 얼굴의 3D 구조를 사용하여 dense mapping을 수정한다. 그런 다음 dense 2D 매핑은 비디오 프레임을 워프하기 위해 희박한 그리드 포인트 세트로 전송된다.

• 고품질의 재구성된 초상화 비디오 생성을 위한 최초의 강력한 parametric reshaping을 제시한다.  
• 정제된 dense flow energy를 가진 multi-phase optimization을 사용하여 효율적이고 안정적인 3D face reconstruction을 제안한다.  
• 아티팩트가 없는 초상화 영상을 변형하기 위해 SDF와 3D 정보를 기반으로 하는 효과적인 대응 추정 방법을 제안한다.  

## 2. Related work
본 절에서 관련 과거 접근법을 논의한다. 비디오에서의 초상화 parametric reshaping 방법의 선행 연구가 없기 때문에 비디오 기반 reconstruction과 비디오 deformation 관련 방법 두가지에 대해 리뷰하는것으로 구성한다.

### 2.1 Video based face reconstruction
#### Morphable Model
단안 이미지 기반 3D 얼굴 재건은 얼굴의 id와 표정에 대한 prior를 요구하는 ill-posed 최적화 문제이다. 
1) 3DMM(Blanz) : Face reconstruction을 위한 ID prior로 사용 될 수 있는 3D 스캔에 대한 PCA를 사용하는 3DMM을 제안  
2) Blend-shapes Model : 동일한 topology의 다른 표정을 가진 얼굴 이미지들을 이용해 표정 Prior를 제공  

지난 몇년간 수많은 작업들은 선형 모델과 그 확장 모델을 face reconstruction을 위해 사용해왔다.  

Surrey Face Model(Huber) : Multi-resolution 3DMM 모델로 다양한 해상도의 mesh를 포함한다.  
Booth : 최적화에서 조명 파라미터를 줄이기 위해 얼굴모양에 대한 통계모델과 in the wild 텍스처 모델을 결합함으로써 3DMM을 확장  

제약조건이 없는 상황 하에서도 reconstruction 속도, 정확성, 편리성을 향상하기 위해 급격한 진보가 이루어져왔지만 학습 데이터의 타입과 양이 선형 3DMM의 성능을 제한했다.  

Tran1 : 광범위한 DB를 생성하기 위해 3D face scan 보다 얼굴 이미지로부터 비선형 3DMM을 학습하는것을 제안  
Tran2 : 더 나아가 loss와 network structure 관점에서 고품질의 reconstruction 결과를 획득하기 위해 비선형 3DMM을 향상  
Li : 4,000장의 high-resolution face scan set 기반으로 deep-learning morphable face model을 제안  

#### Video based reconstruction
초상화 비디오는 프레임이 풍부하지만 얼굴 자세, 표정, ID등에 대한 joint 최적화는 여전히 어렵다.  
단순히 제약조건을 최적화에 추가하는것 만으로는 만족스러운 결과를 얻기 힘들다.  

Thies : model-based non-rigid bundle adjustment를 서로다른 머리의 자세들에 대한 keyframe에 걸쳐 사용  

Cao : 사실적인 데이터셋으로부터 학습한 dynamic rigidity prior를 사용하여 face tracking을 위한 on-the-fly 방법 제안  
랜드마크가 안정적이고 대부분 보여지는 경우에는 그럴듯한 결과를 획득할 수 있었지만 현재시간의 프레임에 대한 reconstruction은 과거 frame의 결과에 의존한다.  
만약 frame 사에에서 landmark가 정확하지 않고 매우 다르다면 정확하고 연속적인 결과를 얻는것은 여전히 어려운 문제이다.  

## 2.2 Portrait video deformation
