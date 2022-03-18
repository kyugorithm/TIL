## Abstract
Object detection에서 **localization과 classification을 결합**하는 복잡한 특성은 성공적인 개발을 가져왔다. 이전 작품은 다양한 object detection head의 성능을 향상시키기 위해 노력했지만 통합된 관점을 제시하지 못했다. 본 논문에서, object detection head를 attention과 통합하기 위한 새로운 **dynamic head framework**를 제시한다. Scale-aware를 위한 feature level 간, spatial-aware를 위한 공간 위치 간, task-aware를 위한 출력 채널 내에서 여러 self-attention mechanism을 일관되게 결합함으로써 제안된 접근 방식은 계산 overhead 없이 object detection head의 표현 능력을 크게 향상시킨다. 표준 ResNeXt-101-DCN 백본을 사용하여 널리 사용되는 object detector보다 성능을 크게 개선하고 54.0 AP에서 새로운 SOTA를 달성한다.  

## 1. Introduction
CV분야에서 object detection은 "어디에 어떤 물체가 있는가"에 대한 답변이다. DL의 시대에서, 거의 모든 object detector는 동일 패러다임을 공유한다. (Backbone : feature 추출, Head : localization & classification) Obejct detection에서 head 성능 향상 방안을 고민하는 것은 매우 중요한 문제가 되었다. 좋은 object detection head를 개발하는데 있어 어려운 도전과제는 세가지로 요약할 수 있다.  
1) Scale-aware : 물체는 이미지 내에 다양하게 구분되는 스케일로 존재  
2) Spatial-aware : 물체는 다양한 시점에서 엄청나게 다른 shape, rotation, location로 존재  
3) Task-aware : 완전 다른 목적과 제약을 가지는 bounding box, center, corner point등 다양한 표현  

최근 연구는 전술한 세가지 문제 중 한가지에 대해서만 집중한다.세가지 문제를 한번에 다루는 통합된 head를 개발하는 것은 열린 문제로 남아있다. 본 논문에서, 세가지를 한번에 통합하는 dynamic head라고 하는새로운 detection head를 제안한다. 만약 우리가 backbone 출력을 level x space x channel의 3차원 tensor로 고려한다면, 우리는 통합 head가 attention 학습문제로 여겨질 수 있다는 것을 알아냈다. Naive한 해법은 이 tensor에 걸쳐 완전한 self-attention mechanism을 구축하는 것이다. 그러나 최적화 문제는 풀기 어렵고 계산 비용이 감당하기 어려울 것이다. 대신, 우리는 attention mechanism을 각 3가지 feature 차원에 분리하여 배치할 수 있다.  

#### Scale-aware attention module
다양한 semantic level의 상대적 중요성을 학습하여 개별 물체에 대해 적절한 level에서의 feature를 향상시킨다.  
#### The spatial-aware attention module
공간 차원(i.e., height × width)에 대해 적용되며 공간 위치에서 일관적으로 분별되는 표현을 학습한다.  
#### Task-aware attention module
채널에 대해 적용되며 object의 다양한 conv. 커널 응답을 기반으로 서로 다른 feature 채널이  
여러 작업(예: 분류, 상자 회귀 및 중심/핵심 학습)을 개별적으로 선호하도록 지시한다.  

이러한 방식으로, 우리는 통합된 attention mechanism을 detection head에 대해 명시적으로 구현한다. 이 attention mechanism들이 feature tensor에 대한 서로다른 차원들에 분리되어 적용되었어도, 서로간에 성능 보완이 가능하다. MS-COCO 벤치마크에 대한 광범위한 실험들은 우리 방식의 효과를 증명한다. 이 방법은 모든 종류의 object detection 모델들에 대해 향상되록 활용될 수 있는 훌륭한 잠재성을 제공한다(with 1.2% ∼ 3.2% AP gains). 표준 ResNeXt-101-DCN backbone으로, 제안된 방법은 SOTA를 얻는다. EfficientDet와 SpineNet과 비교하여 dynamic head는 1/20의 학습시간을 필요로 함과 동시에 성능은 더 좋다. 그리고 최신 transformer backbone과 self-training을 통한 추가 데이터를 가지고 COCO에 대해 SOTA 성능을 얻을 수 있다.  

## 2. Related Work
최근 연구에서는 scale-aware, spatial-aware, task-aware등 다양한 관점에서 object detector를 개선하는 데 중점을 둔다.  
  
### Scale-awareness.
자연 이미지에는 서로 다른 scale을 가진 obejct가 공존하는 경우가 많기 때문에 많은 연구에서 object detection에서 scale-aware의 중요성을 공감했다. 초기 연구는 multi-scale 학습을 위한 image pyramid 방법을 이용하는 중요성을 제시해 왔다. (6, 24, 25 : 2016, 2018) Image pyramid 대신 feature pyramid는 downsampled conv. feature pyramid를 연결하여 효율성을 향상시키며 현대 obejct detector의 표준 구성 요소가 되었다. 그러나 여러 level의 feature는 네트워크의 서로 다른 깊이로부터 추출되며 이는 인지가능한 의미적 차이를 야기한다. 이러한 불일치를 해결하기 위해 [18]은 feature pyramid에서 상향식 경로 증대를 통해 하위 레이어의 feature를 향상시킬 것을 제안했다. 나중에 [20]은 balanced sampling과 balanced feature pyramid를 도입하여 이를 개선했다.  
최근 [31]은 수정된 3차원 conv.를 기반으로 scale과 spatial feature를 동시에 추출하는 pyramid conv.를 제안했다. 본 작업에서는 다양한 feature level의 중요성을 입력에 맞게 조정하는 detection head의 scale-aware attention을 제시한다.  
  
**Spatial-awareness.**
과거 작업은 더 나은 의미론적 학습을 위해 object detection에서 spatial-awareness를 향상하기 위해 노력해왔다. Conv. nn은 이미지에 존재하는 공간적 변환을 학습하는데 제한된 것으로 알려져 있다[41]. 일부 작업들은 이문제를 모델용량[13, 32]을 키우거나 추론과 학습에서 극단적으로 높은 계산 비용이 드는 값비싼 data augmentation[14]를 활용해서 완화한다. 이후, 새로운 conv. 연산자들은 공간변환 학습을 향상하기 위해 제안되어 왔다. [34]는 지수적으로 확장되는 receptive field로부터 문맥적 정보를 통합하는 dilated conv.를 사용할 것을 제안했다. [7]은 추가적인 self-learned offset을 가지는 공간위치를 sample하는 deformable conv.를 제안하였다. [37]은 학습된 feature amplitude를 도입하여 오프셋을 재구성하고 그 능력을 더욱 향상시켰다. 이 작업에서 우리는 detection head에서 spatial-aware attention을 제시한다. 이 attetntion은 각 spatial location에 attention을 적용할 뿐 아니라 보다 구별적인 표현을 학습하기 위해 여러 feature level을 함께 적응적으로 집계한다.  

**Task-awareness.** 
Object detection은 먼저 object proposal을 생성한 다음 proposal을 다른 class와 background로 분류하는 2단계 패러다임[39, 6]에서 시작되었다.  
[23] : 두 단계를 단일 conv. 네트워크로 formulation하기 위해 RPN(Region Proposal Networks)을 도입하여 현대적인 2단계 프레임워크를 공식화했다. 이후에 1단계 object detector[22]는 높은 효율로 인해 대중화되었다.  
[16] : 이전 1단계 detector의 속도를 유지하면서 2단계 detector의 정확도를 능가하는 작업별 분기를 도입하여 아키텍처를 더욱 개선했다.  
최근에는 다양한 object representation이 잠재적으로 성능을 향상시킬 수 있다는 것을 발견한 더 많은 작업이 있다.  
[12] : 먼저 bounding box와 object의 segmentation mask를 결합하면 성능을 더욱 향상시킬 수 있음을 보여주었다.  
[28] : 픽셀 단위 예측 방식으로 obejct detection을 해결하기 위해 center representation을 사용하도록 제안했다.  
[35] : 개체의 통계적 특성에 따라 양성 및 음성 샘플을 자동으로 선택하여 중심 기반 방법의 성능을 더욱 향상시켰다.  
[33] : 학습을 용이하게 하기 위해 object detection을 대표적인 key-point로 공식화했다.  
[9] : 잘못된 예측을 줄이기 위해 한 쌍의 key-point가 아닌 각 object를 triplet으로 감지하여 성능을 더욱 향상시켰다.  
[21] : 각 경계의 극단점에서 경계 feature를 추출하여 점특징을 강화하는 방안을 제안하고 최신 성능을 기록하였다.  

이 작업에서 단일, 2단계 detector 또는 box, center, keypoint 기반 detector에 대해 다양한 작업을 적응적으로 선호할 수 있는 채널에 관심을 배치할 수 있도록 detection head에 task-aware attentiond을 제시한다. 더 중요한 것은 위 모든 속성이 head 디자인의 unified attention mechanism에 통합되어 있다는 것이다.  
이는 object detection head의 성공에서 attention이 어떤 역할을 하는지 이해하기 위한 단계를 밟는 최초의 일반 detection head 프레임워크이다.  

## 3. Our Approach 
### 3.1. Motivation
통합된 object detection head에서 scale-aware, spatial-aware 및 task-aware를 동시에 활성화하려면 object detection head의 이전 개선 사항을 일반적으로 이해해야 한다.  
  
Fin = {Fi}(i=1~L)에서 feature의 연결이 주어졌을 때 feature pyramid의 다른 레벨에서 upsampling 또는 downsampling을 사용하여 중간 레벨 feature의 scale로 연속 레벨 feature의 크기를 조정할 수 있다.  
크기 조정된 feature pyramid는 4차원 텐서 F ∈ R^(L×H×W×C)로 표시할 수 있다. (L, H, W, C : pyramid level, 높이, 너비, 채널) S = H × W를 추가로 정의하여 tensor를 3차원 텐서 F ∈ R^(L×S×C)로 재구성한다. 이 표현을 기반으로 각 텐서 차원의 역할을 탐색한다.  


• object scale의 불일치는 다양한 수준의 feature와 관련이 있다. 다양한 F level에서 표현 학습을 개선하면 object detection에 대한 scale-aware에 도움이 될 수 있다.  
• 서로다른 물체 모양으로부터 다양한 기하학적 변환은 다양한 공간 위치의 feature와 관련된다. F의 서로 다른 공간 위치에서 표현 학습을 개선하면 물체 감지의 spatial-aware에 도움이 될 수 있다.  
• Divergent object 표현 및 작업은 다양한 채널의 feature와 관련될 수 있다. F의 다른 채널에서 표현 학습을 개선하면 object detection의 작업 인식에 도움이 될 수 있다. 이 논문에서 위의 모든 방향이 효율적인 attention 학습 문제에서 통합될 수 있음을 발견했다. 우리의 작업은 개선을 극대화하기 위해 통합된 head를 공식화하기 위해 3차원 모두에 대한 다중 attention을 결합하려는 첫 번째 시도이다.

### 3.2. Dynamic Head: Unifying with Attentions
Feature tensor F ∈ R^(L×S×C) 가 주어지면 self-attention을 적용하는 일반적인 공식은 다음과 같다.
W(F) = π(F) · F
(π(·) :attention function).  
이 attention 함수에 가벼운 해는 Fully connected로 구현된다.
그러나 직접적으로 attetention을 전체 차원에 대해 학습하는것은 계산적으로 값비싸고 실제적으로는 차원이 크기 때문에 불가능하다.  
대신, attention feature를 세 개의 순차적 attention으로 변환하며, 각각은 하나의 관점에만 초점을 맞춘다.  
<img src="https://user-images.githubusercontent.com/40943064/155842954-7641680a-2d96-4428-a7af-81e37489eef7.png" width = 200>. 

#### Scale-aware Attention πL
먼저 의미론적 중요성에 따라 다른 scale의 feature를 동적으로 융합하기 위해 scale-aware attention을 도입한다.  
<img src="https://user-images.githubusercontent.com/40943064/155844872-fb305cf4-8d33-4e4a-b37d-246e02469ea5.png" width = 200>  
(f : 1x1 conv.에 의해 근사된 linear 함수, σ(x) = max(0, min(1, x+1 )) : hard-sigmoid function). 

#### Spatial-aware Attention πS
우리는 융합된 feature를 기반으로 하는 또 다른 공간 인식 attention 모듈을 적용하여 spatial location과 feature level 모두에서 일관되게 공존하는 discriminative 영역에 초점을 맞춘다.  
S의 높은 차원을 고려하여 이 모듈을 두 단계로 분해한다. 먼저 demormable conv.를 사용하여 attention 학습을 희소하게 만든 다음 [7] 동일한 공간 위치에서 수준에 걸쳐 feature를 집계한다.  
<img src="https://user-images.githubusercontent.com/40943064/155845090-94ed6534-891f-471a-9150-8b5388ef2110.png" width = 300>  
(K : 희소 샘플링 위치의 수, pk + ∆pk : 판별 영역에 초점을 맞추기 위해 자체 학습된 공간 오프셋 ∆pk만큼 이동된 위치, ∆mk : pk에서 자체 학습된 중요도 스칼라) 둘 다 F의 중앙값 수준에서 입력 feature에서 학습된다.

#### Task-aware Attention πC
공동 학습을 가능하게 하고 object의 다양한 표현을 일반화하기 위해 마지막에 task-aware attention을 배치한다. 다른 작업을 선호하도록 feature 채널을 동적으로 켜고 끈다.  
<img src="https://user-images.githubusercontent.com/40943064/155845493-0c6ac930-53db-4ffc-bfc2-effa6a5023fd.png" width = 300>  
(Fc : c번째 채널의 feature 슬라이스, [α1, α2, β1, β2]T = θ(·) : activation 임계값을 제어하는 방법을 학습하는 hyper function)  
θ(·)는 [3]과 유사하게 구현되며, 먼저 차원을 줄이기 위해 L × S 차원에 대한 전역 평균 풀링을 수행한 다음 두 개의 FC layer와 정규화 계층을 사용하고  
마지막으로 이동된 시그모이드 함수를 적용하여 -1~1로 정규화한다.  

마지막으로 위의 세 가지 attention 메커니즘은 순차적으로 적용하면 방정식 2를 여러 번 중첩하여 여러 πL, πS 및 πC 블록을 효과적으로 스택할 수 있다.  
Dynamic head (즉, 단순화를 위한 Dy-Head) 블록의 자세한 구성은 그림 2(a)에 나와 있다.  
  
요약하면, 제안한 dynamic head를 사용한 object detection의 전체 패러다임이 그림 1에 나와있다.  
모든 종류의 backbone 네트워크를 사용하여 동일한 규모로 크기를 조정하여 3차원 Tensor F ∈ R^(L×S×C)를 형성하는 feature 피라미드를 추출할 수 있다.  
그런 다음 dynamic head에 대한 입력으로 사용된다.  
다음으로 scale-aware, spatial-aware, task-aware attention을 포함한 여러 Dy-Head 블록이 순차적으로 쌓인다.  
동적 헤드의 출력은 classification, center/box regression 등과 같은 object detection의 다양한 작업 및 표현에 사용될 수 있다.  
  
그림 1의 맨 아래에는 각 attention 유형의 출력이 나와 있다. Backbone의 초기 feature map은 ImageNet pretrained의 도메인 차이로 인해 노이즈가 있다.  
Scale-aware Attention 모듈을 통과한 후 feature map은 foreground object 크기 차이에 더 민감해진다.  
Spatial-aware attention 모듈을 더 통과한 후 feature map은 더 희소해지고 foregound object의 구별되는 공간 위치에 초점을 맞춘다.  
마지막으로 작업 인식 attention 모듈을 통과한 후 feature 맵은 다른 다운스트림 작업의 요구 사항에 따라 다른 활성화로 다시 변경된다.  
이러한 시각화는 각 attention 모듈의 효율성을 잘 보여준다.
  
![image](https://user-images.githubusercontent.com/40943064/155846564-d18be8e5-b16c-4524-95a9-be7858b7cb41.png). 
  
### 3.3. Generalizing to Existing Detectors
이 섹션에서는 제안된 dynamic head를 기존 detector에 통합하여 성능을 효과적으로 향상시키는 방법을 보여준다.  

3.3. Generalizing to Existing Detectors

#### One-stage Detector
1단계 검출기는 feature map에서 위치를 조밀하게 샘플링하여 object 위치를 예측하므로 detector 설계가 간소화된다. 일반적인 1단계 검출기(예: RetinaNet[16])는 밀집된 feature을 추출하는 backbone 네트워크와 다른 작업을 개별적으로 처리하기 위한 여러 작업별 하위 네트워크 분기로 구성된다. 이전 작업[3]에서 볼 수 있듯이 object classification 하위 네트워크는 bounding box regression sub-network와 매우 다르게 동작한다. 이 기존 접근 방식에 대해 논란의 여지가 있지만 backbone에 여러 분기 대신 하나의 통합 분기만 연결한다. 다중 attention mechanism의 이점 덕분에 여러 작업을 동시에 처리할 수 있다. 이러한 방식으로 아키텍처를 더욱 단순화할 수 있으며 효율성도 향상된다. 최근에는 FCOS[28], ATSS[35] 및 RepPoint[33]와 같이 1단계 detector의 anchor-free 변형이 인기를 얻었다. RetinaNet과 비교하여 이러한 방법은 classification branch 또는 regression 분기에 centerness 예측 또는 keypoint 예측을 첨부해야 하므로 작업별 분기의 구성이 간단하지 않다. 대조적으로, dynamic head를 배포하는 것은 그림 2(b)와 같이 헤드 끝에 다양한 유형의 예측만 추가하기 때문에 더 유연하다.  

#### Two-stage Detector  
Backbone 네트워크의 feature 피라미드에서 중간 표현을 추출하기 위해 regional proposal 및 ROI 풀링 [23] 레이어를 활용한다. 이 특성을 협력하기 위해 먼저 ROI pooling layer 이전의 feature pyramid에 scale-aware attention 및 spatial-aware attention을 적용한 다음 그림 2(c)와 같이 task-aware attention을 사용하여 원래의 FC layer를 교체한다.  
![image](https://user-images.githubusercontent.com/40943064/155846588-dfb97ce3-cf14-4bcd-aa7d-59ab9aa4a517.png). 
  
  
### 3.4. Relation to Other Attention Mechanism

#### Deformable
Deformable conv.[7, 37]는 희소 샘플링을 도입하여 기존 conv. 레이어의 변환 학습을 크게 개선했다. Feature 표현을 향상시키기 위해 object detection backbone에서 널리 사용되었다. Object detection head에서는 거의 사용되지 않지만 표현에서 S 하위 차원을 모델링하는 것으로 간주할 수 있다. 우리는 backbone에 사용된 deformable 모듈이 제안된 dynamic head를 보완할 수 있음을 발견했다. 사실, ResNext-101-64x4d backbone의 deformable 변형으로 우리의 dynamic head는 새로운 SOTA를 달성한다.  

#### Non-local
Non-Local Networks[30]는 object detection 성능을 향상시키기 위해 attention module듈을 활용하는 선구적인 작업이다. 그러나 내적의 간단한 공식을 사용하여 다른 공간 위치에서 다른 픽셀의 feature를 융합하여 pixel feature를 향상시킨다. 이 동작은 우리의 표현에서 L×S 하위 차원만을 모델링하는 것으로 간주될 수 있다. 
#### Transformer
최근에는 자연어 처리에서 컴퓨터 비전 작업으로 Transformer 모듈[29]을 도입하는 경향이 있다. 이전 연구는 [2, 38, 5]은 object detection 향상에 유망한 결과를 보여주었다. Transformer는 multi-head FC layer를 적용하여 cross-attention 대응을 학습하고 다양한 양식의 feature를 융합하는 간단한 솔루션을 제공한다. 이 동작은 표현에서 S × C 하위 차원만 모델링하는 것으로 볼 수 있다.
  
앞서 언급한 세 가지 유형의 attention는 feature tensor의 하위 차원을 부분적으로만 모델링한다. 통합된 디자인으로서 우리의 dynamic head는 다양한 차원에 대한 관심을 하나의 일관되고 효율적인 구현으로 결합한다. 다음 실험은 이러한 전용 설계가 기존 object detector가 놀라운 이득을 얻는 데 도움이 될 수 있음을 보여준다. 게다가, 우리의 attention mechanism은 기존 솔루션의 암시적 작동 원리와 달리 object detection 문제를 명시적으로 해결한다.  
