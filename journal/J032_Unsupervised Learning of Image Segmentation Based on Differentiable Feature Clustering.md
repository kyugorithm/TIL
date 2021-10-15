# Unsupervised Learning of Image Segmentation Based on Differentiable Feature Clustering
## Abstract
Unsupervised segmentaion을 위해 label 예측과 네트워크 parameters 학습은 다음 기준을 충족하도록 번갈아 반복된다.  
(a) 유사 형상 픽셀은 동일 label 할당  
(b) 공간적으로 연속 픽셀은 동일 label 할당  
(c) 고유 라벨의 수는 큼  
이러한 기준은 양립할 수 없지만, 제안된 접근방식은 **similarity loss**와 **spatial continuity loss**의 조합을 최소화하여  
앞서 언급한 기준의 균형을 맞추는 라벨 할당의 타당한 솔루션을 찾는다. 이 연구의 기여는 4가지이다.  
1. 정규화와 차별화 가능한 클러스터링을 위한 argmax 함수로 구성된 감독되지 않은 영상 분할의 새로운 종단 간 네트워크를 제안한다.  
2.  이전 작업에서 보유한 고정 세그먼트 경계의 한계를 완화하는 공간 연속성 손실 함수를 소개한다.  
3. 효율성을 유지하면서 기존 방법보다 더 나은 정확도를 보인 스크리블을 사용자 입력으로 분할하기 위해 제안된 방법의 확장을 제시한다.  
4. 네트워크를 재교육하지 않고 몇 개의 참조 이미지로 사전 훈련된 네트워크를 사용하여 보이지 않는 이미지 분할을 소개한다.  
제안된 접근 방식의 효과는 이미지 분할의 여러 벤치마크 데이터 세트에서 검토되었다.  

## Introduction 
Image segmentation은 수십 년 CV에서 주목을 받아왔다. object detection, texture recognition, image compression이 있다.  
Supervised task에서 image pair와 "sky" 또는 "bicycle"와 같은 pixel 수준의 semantic label로 구성된 세트가 학습에 사용된다.  
목표는 pixel에 대해 알려진 범주의 레이블을 분류하는 시스템을 학습하는 것이다.  
대조적으로 unsupervised image segmentation은 "foreground" 및 "background"과 같은 더 일반적인 레이블을 예측하는 데 사용된다.  
후자가 전자보다 더 도전적이다. 또한 이미지를 그럴듯한 영역의 임의의 숫자(≥ 2)로 분할하는 것은 매우 어렵다.  
이 연구는 이미지가 사전 지식 없이 임의의 수의 salient 혹은 semantic 있는 영역으로 분할되는 문제를 고려한다.  
pixel 수준 feature 표현을 얻은 후에는 feature 벡터를 클러스터링하여 영상 세그먼트를 얻을 수 있다.  
그러나 feature 표현 설계는 여전히 난제로 남아 있다. 원하는 feature 표현은 대상 이미지의 내용에 따라 상당히 다르다.  
예를 들어 얼룩말을 foreground로 탐지하는 것이 목적이라면 feature 표현은 흑백 수직 줄무늬에 반응해야 한다.  
따라서 pixel 수준 feature은 각 pixel을 둘러싼 로컬 영역의 색상과 질감을 설명해야 한다.  
최근 자율 주행 및 증강 현실 게임과 같은 supervised learning 시나리오에서 CNN이 semantic image segmentation에 성공적으로 적용되고 있다.  
CNN은 완전한 비지도 시나리오에서는 자주 사용되지 않지만, 비지도 image segmentation에 필요한 이미지 pixel에서 세부 feature를 추출할 가능성이 크다.  
CNN의 높은 feature 설명에 따라, 임의의 이미지 입력에 대해 알 수 없는 클러스터 레이블을 예측하고  
이미지 pixel 클러스터링을 위한 최적의 CNN 매개 변수를 학습하는 공동 학습 접근법이 제시된다.  
그런 다음 각 클러스터의 영상 pixel 그룹이 segment로 추출된다.  
양호한 image segmentation에 필요한 클러스터 레이블의 특성에 대해 자세히 설명한다.  
비지도 image segmentation [1], [2]에 대한 이전 연구와 마찬가지로, 좋은 image segmentation 솔루션은  
인간이 제공할 솔루션과 잘 일치한다고 가정한다.  
Image segmentation 요청을 받으면 segment가 생성될 가능성이 높으며, 각 segment는 단일 객체 인스턴스의 전체 또는 두드러진 부분에 해당한다.  
object instance에는 유사한 색상 또는 텍스처 패턴의 큰 영역이 포함되어 있는 경향이 있다.  
따라서 색상이나 텍스처 패턴이 유사한 공간 연속 pixel을 동일한 클러스터로 그룹화하는 것이 image segmentation을 위한 합리적인 전략이다.  
segment를 서로 다른 object instance에서 분리하려면 서로 다른 패턴의 인접 pixel에 서로 다른 cluster label을 할당하는 것이 좋다.  
cluster 분리를 용이하게 하기 위해 다수의 고유 cluster 레이블을 원하는 전략도 고려된다.  
결론적으로 cluster label의 예측을 위해 다음과 같은 세 가지 기준을 도입한다.  
  
(a) 유사한 feature의 pixel은 동일한 라벨을 할당해야 한다.  
(b) 공간적으로 연속적인 pixel은 동일한 라벨을 할당해야 한다.  
(c) 고유 클러스터 라벨의 수는 커야 한다.  
  
본 논문에서 위 기준을 충족하기 위해 feature 추출 기능과 clustering 기능을 공동으로 최적화하는 CNN 기반 알고리즘을 제안한다.  
CNN의 end-to-end 학습을 가능하게 하기 위해 미분가능한 함수를 사용하여 cluster label을 예측하는 반복적 접근방식이 제안된다.  
코드는 온라인으로 이용할 수 있다.  
본 연구는 ICASSP 2018[3]에 발표된 이전 연구의 확장이다.  
이전 연구에서는 (b) 기준에 대해 단순 선형 반복 클러스터링[4]을 사용한 superpixel 추출을 사용했다.  
그러나 이전 알고리즘은 superpixel 추출 과정에서 세그먼트의 경계가 고정된다는 한계가 있었다.  
본 연구에서는 앞서 언급한 한계를 완화하기 위한 대안으로 **spatial continuity loss**을 제안한다.  
또한 개선된 비지도 image segmentation 방법에 기초한 두 가지 새로운 애플리케이션,  
즉 사용자 입력을 통한 image segmentation과 다른 이미지의 비지도 학습을 사용하여 얻은 네트워크 가중치의 활용이 도입된다.  
제안된 방법은 완전 비지도이므로 사용자의 의도와 항상 관련이 없는 feature 기반으로 이미지를 image segmentation한다.  
제안된 방법의 예로서 낙서를 사용자 입력으로 사용했으며 그 효과를 다른 기존 방법과 비교했다.  
그 후, 제안된 방법은 단일 입력 영상의 image segmentation 결과를 반복적으로 얻기 위해 높은 계산 비용을 발생시켰다.  

따라서 제안된 방법의 또 다른 잠재적 적용으로서, 여러 기준 이미지로 사전 훈련된 네트워크 가중치가 사용되었다.  
제안된 알고리즘을 사용하여 여러 이미지에서 네트워크 가중치를 얻은 후, 보이지 않는 새로운 이미지는 참조 이미지와  
다소 유사할 경우 고정 네트워크에 의해 분할될 수 있다.  
비디오 분할 작업에 이 기술을 활용하는 것도 입증되었다.  
본 논문의 기고문은 다음과 같이 요약된다.  

• Unsupervised image segmentation의 새로운 end-to-end differential 네트워크를 제안했다.  
• 이전 방법의 한계를 완화한 spatial continuity loss를 도입했다[3].  
• 효율성을 유지하면서 기존 방법보다 더 나은 정확도를 보인 낙서를 사용자 입력으로 분할하기 위해 제안된 방법의 확장을 제시했다.  
• 재학습 없이 몇 개의 참조 이미지로 사전 학습된 네트워크를 사용하여 unseen image segmentation을 도입했다.  
  
## 2. Related work  
Image segmentation : 모든 pixel에 걸쳐 특정 특성을 공유하는 pixel에 같은 label을 할당하도록 하는 프로세스  
k-means[5] : 벡터 quantization를 위한 사실상 표준의 고전적인 image segmentation 방법  
Graph based segmentation(GS)[6] : image segmentation에 대한 간단한 greedy 결정을 내리는 또 다른 예  
: 특정 영역 비교 기능에 따라 너무 거칠거나 너무 미세하지 않은 전체적인 특징을 따르는 segmentation 결과를 생성한다.  
  
고전적인 방법과 마찬가지로 제안 방법은 unsupervised image segmentation을 목표로 한다.  
최근 unsupervised image segmentation [7], [8], [9]에 기초한 학습에 대한 몇 가지 방법이 제안되었다.  
MSLRR[7] : unsupervised/supervised 둘 다로 전환할 수 있는 효율적이고 다용도적인 접근법이다.  
(superpixel(전작 [3])을 채용하여 경계가 superpixel의 경계에 고정되는 한계를 초래했다.)  
W-Net[8] : 입력 image에서 segmentation을 추정하고 추정된 segmentation에서 입력 image을 복원하여 수행  
(각 segment의 경계를 추정하지는 않지만 유사한 픽셀이 동일한 label에 할당됨)  
Croitoru[9] : DNN 기법에 기초한 unsupervised segmentation 방법을 제안  
(이진 foreground/background segmentation을 수행)  
위 방법과 달리 우리의 방법은 임의의 수의 segment를 생성한다.  
Image segmentation을 위한 딥 러닝 기법에 대한 종합적인 조사는 [10]에 제시되어 있다.  

이 절의 나머지 부분에서는 사용자 입력을 이용한 image segmentation,  
CNN 기반 WSSS 및 비지도 딥 러닝 방법을 소개한다.  
  
**Image segmentation with user input:**  
**Graph cut**  
이미지 픽셀이 노드에 해당하는 그래프의 비용을 최소화하여 작동하는 일반적인 영상 분할 방법  
낙서 [11] 및 bounding box [12]와 같은 특정 사용자 입력으로 image segmentation에 적용할 수 있다.  
**Image matting**  
일반적으로 사용자 입력 [13], [14]를 사용한 영상 분할에도 사용  
픽셀 레이블을 부드럽게 할당하는 반면, 그래프 컷은 모든 픽셀이 foreground 또는 background에 속하는 hard segmentation을 생성한다.  
**Constrained random walks**[15]  
보다 유연한 사용자 입력으로 대화형 이미지 분할을 달성하기 위해 제안되며,  
이를 통해 낙서가 경계 영역과 전경/배경 시드를 지정할 수 있다.  
최근 우세 집합 클러스터와 관련된 2차 최적화 문제가 낙서, 엉성 등고선 및 경계 상자[16]와 같은 여러 유형의 사용자 입력으로 해결되었다.  
위에서 언급한 방법은 주로 이미지 픽셀을 foreground와 background으로 구분하는 이진 맵을 생성합니다.  
**α-β 스왑 / α-확장 알고리즘**  
다중 라벨 분할 문제에 그래프 컷을 적용하기 위한 방법 [17]  
두 알고리즘 모두 이진 레이블링 문제의 전역 최소값을 찾기 위해 반복적으로 처리한다.  
**α-확장 알고리즘**에서 확장 움직임은 라벨 α에 대해 정의되어 이 라벨이 주어진 픽셀 집합을 증가시킨다.  
이 알고리즘은 라벨 α에 대한 확장 이동이 없는 로컬 최소값을 찾아 더 낮은 에너지로 라벨을 생성한다.  
스왑 이동은 현재 α 라벨이 부착된 픽셀의 일부 부분 집합을 취하여 라벨 β를 할당하고 라벨 α, β 쌍에 대해서도 그 반대이다.  
**α-β 스왑 알고리즘**은 낮은 에너지 라벨링을 생성하는 라벨 α, β 쌍에 대한 스왑 이동이 없는 최소 상태를 찾는다.  

**Weakly-supervised image segmentation based on CNN:**  
CNN에 기초한 의미론적 이미지 분할은 문헌 [18], [19], [20], [21]에서 중요해지고 있다.  
이미지 분할에 대한 픽셀 수준 label을 얻기 어렵기 때문에 object detector [22], [23], [24],  
obejct bounding box [25], [26], 이미지 수준 레이블 [27], [28], [30] 또는 낙서 [31], [32], [33]을 사용하여  
약하게 감독되는 학습 접근법이 널리 사용된다.  
대부분의 약하게 감독되는 분할 알고리즘 [31], [25], [26], [30]은 약한 레이블에서 훈련 목표를 생성하고  
생성된 학습 세트를 사용하여 모델을 업데이트한다. 따라서 이러한 방법은  
(1) 생성된 표적에서 CNN 기반 모델을 훈련하기 위한 경사 하강과  
(2) 약한 라벨에 의한 훈련 표적 생성이라는 두 단계 사이를 번갈아 가는 반복 과정을 따른다.  
예를 들어 ScribbleSup[31]은 이미지에 주석을 완전히 달기 위해 슈퍼픽셀을 사용하여 낙서의 의미적 레이블을 다른 픽셀로 전파하고(1단계)  
주석이 달린 이미지로 의미 분할을 위한 컨볼루션 신경망을 학습한다(2단계).  
e-SVM [25]의 경우, CPMC 세그먼트 [34]를 사용하는 경계 상자 주석 또는 픽셀 수준 주석에서 세그먼트 제안이 생성되고(1단계)  
생성된 세그먼트 제안으로 모델이 훈련된다.(2단계)  
시모다[30]는 영상 수준 label을 이용한 추정 등급 돌출성 맵을 적용하였고(1단계)  
추정 saliency map을 단항 전위로 하여 완전 연결 CRF[35]를 적용하였다(2단계).  
이러한 반복 프로세스는 수렴이 보장되지 않는 위험에 노출된다.  
약한 레이블로 대상 생성을 훈련하는 과정에서 발생한 오류는 전체 알고리즘을 강화하여 원하지 않는 방향으로 모델을 업데이트할 수 있다.  
따라서 라벨이 약한 훈련 목표 생성의 오류를 방지하기 위한 최근 접근법 [33], [32], [36]이 제안된다.  
이 연구에서는 수렴 문제를 다루기 위해 CNN을 기반으로 한 end-to-end 차별화 가능한 방법을 제안한다.  
  
**Unsupervised deep learning:**  
주로 생성 모델 [37], [38], [39]을 사용하여 높은 수준의 feature 표현을 학습하는 데 초점을 맞춘다.  
이러한 연구의 이면에 있는 아이디어는 특정한 의미 개념을 나타내는 뉴런이 존재한다는 신경과학의 추측과 밀접한 관련이 있다.  
대조적으로, 이 연구에서는 image segmentation에 대한 딥 러닝의 적용과 conv. 레이어로 추출한 높은 수준의 형상의 중요성을 조사한다.  
심층 CNN 필터는 텍스처 인식 및 분할 [40], [41]에 효과적인 것으로 알려져 있다.  
특히, 제안된 방법에 사용된 conv. 필터는 ground truth는 없지만 backpropagation 학습이 가능하다.  
따라서 본 연구는 딥 임베디드 클러스터링(DEC)에 대한 최근 연구와 관련이 있다[42].  
DEC 알고리즘은 보조 목표 분포를 사용하여 소프트 할당 데이터 포인트 간의 KL divergence loss를 최소화하여 클러스터를  
반복적으로 조정하는 반면, 제안된 방법은 추정된 클러스터를 기반으로 softmax loss를 최소화한다.  
준지도 학습 프레임워크에 대해 최대 여유 클러스터링 [43] 및 차별적 클러스터링 [44], [45]과 같은 유사한 접근방식이 제안되었지만,  
제안된 방법은 완전히 감독되지 않은 image segmentation에 초점을 맞추고 있다.  
