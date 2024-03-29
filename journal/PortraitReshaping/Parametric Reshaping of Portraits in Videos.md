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

### 2.2 Portrait video deformation
얼굴 편집 후 이미지 왜곡을 줄이기 위해 content-aware 이미지 warping은 광범위한 편집 응용 프로그램에서 강력한 도구가 된다.  
그러나, 연속 프레임의 소스에서 대상으로의 매핑이 일반적으로 일관되지 않기 때문에 모든 비디오 프레임에서 연속적이고 안정적인 변형을 생성하는 것은 어렵다. 
Chen은 consistent blending boundary의 중요성을 인식하고 source 비디오와 target 비디오의 gradient를 병합하는 비디오 혼합 접근 방식을 제시했다. 
다른 매개 변수를 변경하지 않고 source로부터 target까지 표정 parameter를 mapping하여 표정을 전송하여 대상 id, rigid head motion 및 scene lighting이 보존될 수 있도록 했다. 
또한 자세, 표정, 장면 조명과 같은 초상화 비디오 속성은 GAN 기반 방법으로 조작할 수 있다.  

## 3. Overview
초상 비디오를 parametric 하게
재구성하여 결과적인 초상화 sequence를 현실적이고 안정적으로 만드는 새로운 방법을 제안한다. 
이를 위해 비디오로부터 초상화의 강력한 추출과 초상화의 모양을 바꾸기 위한 비디오 프레임의 일관된 변형이 필요한데, 이 모든 것이 우리의 방법에 의해 해결된다. 
그림 2는 우리 방법의 파이프라인을 보여준다. 
<img width="840" alt="image" src="https://user-images.githubusercontent.com/40943064/169984432-f4eb2f4a-de2e-42e1-bedb-e471ec353fec.png">  

초상 이미지 시퀀스가 주어지면 우리의 방법은 두 가지 주요 단계로 구성된다. 

1. (S4) Video based face reconstruction을 활용하여 안정적인 포즈/표정으로 고품질 얼굴 ID를 충실하게 재구성  
- 자세 : 각 프레임에서 헤드 포즈를 추정하는데, 이는 프레임 전체에 걸쳐 일관된 ID를 추정하는 데 중요하다.  
- 정체성 : 얼굴 정체성을 가장 잘 나타내는 k 프레임을 찾고 일관된 얼굴 ID를 함께 최적화한다.  
- 표정 : 전체 3D face sequence를 달성하기 위해 각 프레임의 얼굴 표정을 추정한다.  

2. (S5)재구성 결과를 기반으로 3D로 재구성된 얼굴을 생성한 다음 3D로 변형된 얼굴을 활용하여 2D로 재구성된 초상화 비디오 생성을 안내한다.  
- 재구성된 3D 중립 얼굴 모델을 재구성하고 각 비디오 프레임에 대한 얼굴 표정 및 포즈와 결합한다.  
- SDF 기반 방법을 사용하여 reconstruction 전후에 face contour의 2D dense mapping을 구성한다.  
- Contents-aware warping 최적화는 3D의 재구성된 면에 따라 초상화 프레임을 변형하여 최종 재구성된 초상화 비디오를 만드는 데 사용된다.  

## 4 Video based face reconstruction
Parametric face model과 최적화의 기본이 되는 목적함수를 설명한다.  
그리고 강인성과 효율성을 고려하며 pose, id, expression을 최적화하는 방법을 단계적으로 기술한다.  
### 4.1 Parametric Face Model and Objectives
Parametric face model은 id basis vector와 expression basis vector의 선형 결합을 통해 표현될 수 있다.  
<img width="185" alt="image" src="https://user-images.githubusercontent.com/40943064/169990592-7021e67e-f891-4027-9446-b64d9e51b3fa.png">  

### 4.2 Stabilized Face Tracking
#### 4.2.1 Rigid Pose Estimation
#### 4.2.2 Identity Estimation
#### 4.2.3 Expression Estimation

## 5 Reshaping
Reconstructed 3D face를 reshape 하여 reshaped portrait video를 생성하기 위해 가이드로 사용한다.  
Reshaping parameter가 주어지면 linear regression model을 이용하여 각 frame에 대해 reshaped face를 생성한다.(5.1)  
그리고 reshaped face에 대응하는 개별 프레임을 deform하기 위해 image warping을 적용한다.  

### 5.1 3D Face Reshaping
Xiao(Deep Shapely Portraits) : 추정된 조정파라미터 기반의 reshaped portrait image를 생성하기 위한 **reshaping model**을 제안했다.  
본 연구는 단일 이미지 reshaping을 전체 이미지 sequence로 확장한다. Reshaping model은 전체 얼굴을 scalar parameter δ 를 이용하여 deform한다.  
Reshape operator를 f(X;δ)로 표현한다.  
Reconstructed 3D faces Xi(⍺, β(i))(β(i):expression coeff. of i-th frame)에 대해   
Reshaped 3D face model Xi\*는 neutral reshaped face model의 선형결합으로 정의 된다.  
![image](https://user-images.githubusercontent.com/40943064/171128285-174a9984-c83e-4ed1-b1b7-80b44b49c7d6.png)  

### 5.2 Consistent Video Deformation
Reshaped 3D face를 guide로 사용하여, artifact 없이 2D에서의 target shape를 가지는 얼굴을 생성하기 위해 이미지를 warp한다.  
1) warping proxy로써 uniform grid Mu = {ui}를 위치시킨다.  (ui:이미지상의 grid point 2D 좌표)  
2) Face deformation에 의해 유도된 이미지 왜곡을 구동하는 set of control points을 찾는 새로운 방법을 제안한다.  
3) 전체 grid의 왜곡을 최소화함으로써 모든 다른 grid 포인트들을 warp하기 위해 LS 최적화를 적용한다. 

#### Control points selection.
3D face model 위에서 control point를 선택하는것은 직관적이다.  
Jain은 face mesh vertex 들을 선택하고 2D 사영시켜 control point들로 사용했다.

![image](https://user-images.githubusercontent.com/40943064/171131883-0890ee38-3d1b-461f-9118-bd73a3dd8d11.png)  

#### control points selection
#### SDF based selection
#### Warping 

## 6. Evaluation
### 6.1 Results
### 6.2 Comparison
### 6.3 Ablation studies
### 6.4 Implementation Details
## 7. Discussion
## 8. Conclusion
