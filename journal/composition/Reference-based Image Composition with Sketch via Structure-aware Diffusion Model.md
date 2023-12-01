# Reference-based Image Composition with Sketch via Structure-aware Diffusion Model

## Abstract
최근 큰 발전을 이룬 대규모 텍스트-이미지 생성 모델은 고화질 이미지 생성에서 매력적인 결과를 보여준다. 편집성을 향상시키고 세밀한 생성을 가능하게 하기 위해, 참조 이미지와 sketch를 새로운 모달로 결합한 "multi-input-conditioned image composition model"을 소개한다. sketch를 통한 에지 수준의 제어 덕분에, 우리 방식은 사용자가 원하는 구조(즉, sketch)와 내용(즉, 참조 이미지)을 가진 이미지의 하위 부분을 편집하거나 완성할 수 있다. 우리 프레임워크는 참조 이미지를 사용해 누락된 영역을 채우면서 sketch 가이드를 유지하는 사전 훈련된 diffusion model을 미세 조정한다.

## Introduction
### 1. Diffusion 모델을 활용한 텍스트-이미지 생성의 발전
최근 대규모 텍스트-이미지 연구(DALL-E 2, Stable Diffusion, Imagen)에서 diffusion model의 발전은 주목할 만하다. 이들은 텍스트 입력으로 복잡한 이미지를 생성하는 뛰어난 능력을 보여준다. 이런 기본 생성 모델을 기반으로, 다양한 접근 방식이 개발되어 편집 가능성을 높이고 있다. 특히, 'Paint-by-Example'은 시각적 힌트를 통해 텍스트 설명의 모호성을 줄이고, 사용자가 참조 이미지를 이용해 객체의 의미를 조작할 수 있게 한다.

### 2. 편집 가능성 향상을 위한 새로운 접근법
본 연구의 목표는 sketch를 새로운 modal로 사용해 generative diffusion model을 발전시키는 것이다. sketch는 직관적이고 효율적인 도구로, 예술가와 대중에게 오랫동안 사랑받아 왔다. sketch의 주요 장점은 텍스트나 이미지와 다르게 edge 수준에서의 제어를 통해 이미지 합성 중 기하학적 구조를 안내한다는 것이다. 이런 기능은 텍스트 설명이나 단독 시각적 힌트보다 더 세밀한 이미지 생성 및 편집을 가능하게 한다. 실제로, 만화 콘텐츠 생성에서 sketch의 유용성은 매우 높으며, 이 연구는 특히 만화 장면의 편집에 중점을 두고 있다.

### 3. sketch 기반의 multi-input-conditioned image composition model
이 연구에서는 sketch와 참조 이미지를 결합해 결과물을 생성하는 multi-input-conditioned image composition model을 제안한다. 생성 과정에서 sketch는 대상 영역의 형태를 결정하는 structure prior로 작용한다. 이를 위해, diffusion model을 훈련시켜 sketch 가이드를 유지하면서 참조 이미지로 누락된 영역을 완성하도록 한다. 추론 단계에서는 'sketch 플러그 앤 드롭' 전략을 제안해 모델에 유연성을 부여한다. 이 방법은 기존 프레임워크와 비교해 이미지 조작을 위한 독특한 사용 사례를 제공한다. 제공된 예시들은 이 방법이 임의의 장면에서 사용자 주도의 수정을 가능하게 하는 효과를 잘 보여준다.
![image](https://github.com/kyugorithm/TIL/assets/40943064/bed7298f-0656-4b37-8608-1899568b54d2)

## 2. Methods
### 2.1. Preliminaries
Latent Diffusion Model
모델 구조: 인코더(E)가 입력 이미지(x(∈R3))를 잠재 표현(z = E(x))으로 변환하고, 디코더(D)가 이 잠재 표현으로부터 이미지를 재구성합니다. 입력 이미지(x)는 높이(H)와 너비(W)를 가집니다. / 모델은 time-conditioned U-net구조를 가진다.
훈련과 손실 함수: 조건부 확산 모델은 텍스트 조건(y)과 함께 훈련됩니다. 여기서 y는 CLIP 텍스트 인코더에 입력됩니다. t={1, ..., T}는 일정 범위 내에서 균등하게 샘플링되며, zt는 잠재 표현 z의 잡음이 가미된 버전입니다.
효율적인 훈련: 빠른 수렴을 위해 Stable Diffusion을 강력한 사전 지식으로 사용합니다.

![image](https://github.com/kyugorithm/TIL/assets/40943064/5c360b5d-daa3-4998-89dc-7005fefe7fe8)

### 2.2. Proposed Approach
#### 2.2.1 Training Phase
##### Problem Setup
초기 이미지(xp∈R^3xHxW), 이진 마스크(m∈{0,1}^HxW), 스케치 이미지(s∈{0,1}^HxW), 참조 이미지(xr∈R^3xHxW)를 입력으로 받습니다. 마스크는 편집할 영역을 나타내고, 스케치는 마스크된 영역의 구조 정보를 전달합니다. 모델은 훈련 중에 마스크된 영역을 스케치 가이드에 따라 참조 이미지의 내용으로 채웁니다.
##### Initialization
모델이 스케치 가이드를 따르도록 최적화되기 전에, 이전 연구의 훈련된 가중치를 초기화로 사용합니다. 이 초기화는 모델이 참조 이미지를 마스크된 영역에 효과적으로 배치하는 데 도움을 줍니다.
##### Model Forward
모델 훈련: 자기 지도 학습(self-supervised training)을 사용하여 모델을 훈련합니다. 훈련 배치는 초기 이미지, 마스크, 스케치, 참조 이미지로 구성됩니다. RoI(관심 영역)를 임의로 생성하고, 이 영역에 대한 참조 이미지를 CLIP 이미지 인코더에 입력하여 확산 모델의 조건을 만듭니다.
##### Inference Phase(스케치 Plug-and-Drop 전략)
사용자에게 유용한 스케치 조건임에도 불구하고, 모델이 때때로 윤곽 구조를 엄격하게 유지하는 데 어려움을 겪습니다. 특히 경계가 모호한 풍경 배경을 생성할 때 눈에 띕니다. 이러한 경우를 위해 스케치 조건의 융합 단계를 유연하게 조정하는 간단하면서도 효과적인 방법을 추가합니다.
##### Self-reference Generation
스케치 가이드 생성은 객체의 형태를 조작하거나 포즈를 변경하는 등 다양한 경우에 사용될 수 있습니다. 특정 객체의 부분을 생성할 때 적합한 참조 이미지를 얻기 어려우므로, 초기 이미지의 특정 부분을 대안으로 사용하는 것이 합리적인 방법으로 나타났습니다.
이 연구는 이미지 생성 및 편집 과정에서 텍스트, 스케치, 참조 이미지를 결합하는 새로운 접근 방식을 제안하고 있으며, 이는 특히 사용자가 원하는 영역을 더 세밀하게 편집할 수 있게 합니다.

##### Initialization. 
훈련 중에 모델은 sketch 가이드를 따라 masked regiosn을 생성하고 참조 이미지를 적절히 배치하는 책임이 있다. 이는 모델에게 추가적인 작업일 수 있으나, 우리는 이전 작업 Paint by example 에서 훈련된 가중치를 초기화로 사용하기로 결정했습니다. 이렇게 함으로써 모델은 masked region에 참조 이미지를 가져오는 강력한 사전 지식을 가지게 됩니다. 초기화는 모델이 sketch 가이드를 따라 최적화된 가중치를 조정함으로써, 보다 쉽게 목표를 달성하게 합니다. 우리는 강력한 사전 지식 없이는 모델이 수렴하는 데 더 오랜 시간이 걸린다는 것을 발견했습니다. 

##### diffusion model. 
iteration마다, 훈련 배치는 초기 이미지(xp), 마스크(m), 스케치(s), 참조 이미지(xr)로 구성됩니다. 모델의 목표는 마스크된 부분 m과 초기 이미지 xp를 적절히 생성하는 것입니다. 우리는 RoI를 bounding box로 무작위로 생성합니다. 이 영역에서는 이전 작업 Paint by example의 mask shape augmentation을 적용하여 그려진 것처럼 보이는 마스크를 시뮬레이션한다. 다른 분기에서는 RoI 영역을 자르고 증강하여 참조 이미지 xr을 생성하고, 이를 연속적으로 CLIP에 입력하여 Diffusion model의 조건 c를 만듭니다. 공식적으로 이는 c = MLP(CLIP(xr))로 표현할 수 있으며, 여기서 MLP는 간단한 피드포워드 네트워크로, 출력 분포를 diffusion 모델의 조건에 적절히 조정하도록 변환합니다. 각 diffusion 단계에서 마스크된 초기 이미지, 스케치, 그리고 이전 단계의 결과 yt가 연결되어 diffusion model에 입력됩니다.

#### 2.2.2 Inference Phase
스케치 Plug-and-Drop 전략: 자유롭게 그린 스케치는 사용자에게 편리한 조건이지만, 모델이 때때로 윤곽 구조를 엄격하게 유지하는 데 어려움을 겪을 수 있습니다. 이는 특히 구름이나 눈 덮인 나무와 같은 경치 배경을 생성할 때 눈에 띄며, 이러한 경우 경계가 모호합니다. 이런 상황에서는 간단한 직선만으로는 부족할 수 있지만 사용자의 부담은 최소화될 수 있습니다. 이를 위해, 우리는 간단하면서도 효과적인 방법인 'Sketch Plug-and-Drop'을 추가한다. 이 방법에서는 스케치 조건의 융합 단계가 유연하게 조정됩니다.

##### Self-reference Generation. 
Sketch-guided generation은 객체의 형태를 조작하거나 포즈를 변경하는 등 다양한 경우에 사용될 수 있습니다. 특정 객체의 부분을 생성할 때 적합한 참조 이미지를 얻는 것은 쉬운 일이 아닙니다. 왜냐하면 마스크된 부분을 포함한 조화로운 이미지를 수집하는 것이 어렵기 때문입니다. 실제로, 우리는 초기 이미지의 특정 부분을 대안으로 사용하는 것이 참조 이미지를 얻는 합리적인 방법임을 발견했습니다.

## 3. Experiments
훈련 및 테스트 데이터셋: Danbooru(원본 데이터셋의 방대한 양으로 인해 부분집합 사용 결정, 다양한 예술 스타일을 가진 애니메이션 캐릭터 포함)  
에지 추출 방법: 최근 발표된 에지 감지 방법(Pidinet) 사용, 추출된 에지 이진화  
데이터셋 구성: 1) 훈련 데이터셋: 55,104개의 이미지-스케치 쌍 / 2) 테스트 데이터셋: 13,775개의 이미지-스케치 쌍  
질적 평가를 위한 실제 만화 장면 수집: Naver Webtoon 및 Ghibli 스튜디오의 영화  
### 3.1. Comparisons with Baselines
#### Baseline
아직까지 diffusion model 접근 방식을 사용하는 multi-input-conditioned image composition model에 대한 연구는 제안되지 않았습니다. 따라서, 우리는 모델을 질적 및 양적으로 분석하기 위해 두 가지 기준 모델을 구현합니다. (1) Paint-by-T+S (2)Paint-by-E(xample)를 구현합니다. 우리의 관심사 중 하나는 다른 안내 방법과 비교했을 때 Paint-by-E+S의 우수성을 보여주는 것입니다. 다음 실험에서, 우리는 뛰어난 양적 결과를 보여주는 것뿐만 아니라 우리 모델의 다양한 사용 사례를 제공함으로써 이러한 가이드의 잠재력을 밝히는 데 집중합니다. 모든 기준 모델과 우리 모델은 동일한 구성으로 훈련됩니다.
#### Comparison Results
그림 2는 각 입력 설정에서 분명한 차이를 보여줍니다. 단일 참조 이미지만을 사용하는 것은 누락된 부분에 대한 좋은 추측을 만들기에 충분하지 않아, 미적으로 매력적이지 않은 완성 결과를 만들어냅니다(그림 2의 두 번째 열 참조). 반면에, 단순히 스케치 입력을 제공하는 것은 구조를 안내함으로써 시각적 품질을 크게 향상시킵니다. 특히, 일반적으로 전체 이미지에 대한 정보를 포함하는 텍스트 조건과 달리, 예시 이미지는 로컬 맥락을 채우는데 효율적인 조건이 될 수 있습니다. 표 1은 기준 모델과의 정량적 비교를 보여줍니다. 볼 수 있듯이, Paint-by-E는 마스크된 영역 내의 구조에 대한 명시적인 안내가 없기 때문에 다른 모델들보다 상대적으로 성능이 떨어집니다. 이에 비해, Paint-by-T+S와 Paint-by-E+S는 스케치 조건 덕분에 우수한 성능을 보여줍니다. 특히, Paint-by-E+S 접근법은 스케치와 예시 이미지를 함께 사용함으로써 가장 뛰어난 성능을 보여줍니다.  
<img src = "https://github.com/kyugorithm/TIL/assets/40943064/0ae0104e-8b74-4381-92ef-41df28424538" width=400>