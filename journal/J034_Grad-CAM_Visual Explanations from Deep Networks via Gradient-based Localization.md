# Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization

## Abstract
CNN 기반 모델의 큰 부류에서 결정을 위한 "시각적 설명"을 통해 명쾌하게 하는 기술을 제안한다.  
Gradient-Weighted Class Activation Mapping(Grad-CAM)은 모든 대상 개념의 gradient를 사용하여  
최종 conv.로 흘러들어가 개념을 예측하기 위해 이미지의 중요한 영역을 강조하는 대략적인 localization map을 생성한다.  
Grad-CAM은 구조적 변화나 재학습 없이 아래 CNN 종류에 적용할 수 있다.
(1) Fully-connected layer 존재(e.g. VGG)  
(2) 구조화된 출력 (e.g. captioning)  
(3) 다중 모드 입력 또는 강화 학습이 있는 작업 (e.g. VQA)  


Grad-CAM을 세분화된 시각화와 결합하여 고해상도 CAM을 생성하고 ResNet 기반 아키텍처를 포함한  
이미지 분류, 캡션 및 VQA(시각적 질문 답변) 모델에 적용한다.  


이미지 분류 맥락에서 grad-cam은 아래 기능을 제공한다.

(a) Failure mode에 대한 통찰력을 제공  
(비합리적으로 보이는 예측에 합리적인 원인 판단)  
(b) ILSVRC-15 weakly-supervised localization 작업에서 성능 향상  
(c) 적대적 섭동에 강력  
(d) 기본 모델에 더 충실  
(e) 데이터 세트 편향을 식별하여 모델 일반화를 달성  
  
캡션 및 VQA의 경우 비주의 기반 모델도 입력을 현지화할 수 있음을 보여준다.  
Grad-CAM을 통해 중요한 뉴런을 식별하는 방법을 고안하고 이를 뉴런 이름과 결합하여 모델 결정에 대한 텍스트 설명을 제공한다.  
또한 사용자가 모델의 예측에 대한 적절한 신뢰를 확립하는 데 도움이 되는지 측정하기 위해 인간 연구를 설계수행하고  
Grad-CAM이 훈련되지 않은 사용자가 둘 다 동일한 노드를 만들더라도 '강한' 노드와 '약한' 노드를 성공적으로 구별하는 데 도움이 된다는 것을 보여준다.  
  
## 1. Introudction 
CNN을 기반 심층 신경 모델은 분류, 객체 감지, semantic seg.에서 이미지 캡션, 시각적 질문 답변, 시각적 대화 및  
구체화된 질문 답변에 이르기까지 다양한 컴퓨터 비전 작업에서 전례 없는 혁신을 가능하게 했다.  
이러한 모델은 다만 직관적인 구성 요소로 분해할 수 없기 때문에 해석하기 어렵다.  
결과적으로 오늘날의 지능형 시스템이 실패하면 경고나 설명 없이 실패하는 경우가 많으며 사용자는 일관성 없는  
출력을 보고 동작에 대해 이해하지 못한다. 그래서 해석 가능성이 중요합니다. 지능형 시스템에 대한 신뢰를 구축하고  
일상 생활에 의미 있는 통합을 위해 예측하는 이유를 설명할 수 있는 '명확한' 모델을 구축해야 한다.  
  
대체로 이러한 **명확함과 설명 능력**은 AI 진화의 세 가지 다른 단계에서 유용하다.  
  
1. **인간보다 훨씬 약하고 아직 안정적으로 배포할 수 없는 경우** (예: 시각적 질문 답변)  
- 투명성과 설명의 목표는 failure mode를 식별하여 연구자가 가장 유익한 연구 방향에 노력을 집중할 수 있도록 돕는 것이다.  
2. **인간과 동등하고 안정적으로 배포할 수 있는 경우** (예: 충분한 데이터에 대해 훈련된 이미지 분류)  
- 목표는 사용자에 대한 적절한 신뢰와 신뢰를 구축하는 것이다.  
3. **AI가 인간보다 훨씬 강할 때**(예: 체스 또는 바둑)  
- 설명의 목표는 기계 학습에 있다. 즉, 기계가 인간에게 더 나은 결정을 내리는 방법에 대해 가르치는 것이다.  
  
일반적으로 **정확성**과 **단순성 또는 해석가능성** 사이에는 trade-off가 있다.  
규칙 기반 또는 전문가 시스템은 해석 가능성이 높지만 정확하거나 강력하지 않다.  
수작업으로 설계된 분해 가능한 파이프라인은 개별 요소가 자연스럽고 직관적인 설명을 가정하기 때문에  
더 해석하기 쉬운 것으로 생각된다.  
심층 모델을 사용함으로써 우리는 더 큰 추상화(더 많은 레이어)와 더 긴밀한 통합(종단 간 교육)을 통해  
더 나은 성능을 달성하는 **해석 불가능한 모듈**을 위해 해석 가능한 모듈을 희생한다.  
최근에 도입된 ResNets는 200개 이상의 레이어 깊이를 가지며 여러 도전적인 작업에서 최첨단 성능을 보여주었다.  
이러한 복잡성은 이러한 모델을 해석하기 어렵게 만든다.  
따라서 심층 모델은 해석 가능성과 정확성 사이의 스펙트럼을 탐색하기 시작했다.  
Zhou et al. 최근에 완전히 연결된 레이어를 포함하지 않는 제한된 클래스의 이미지 분류 CNN에서 사용하는  
판별 영역을 식별하기 위한 CAM 이라는 기술을 제안했다.  
본질적으로 이 작업은 모델 작업에 대한 **투명성을 높이기 위해 모델 복잡성과 성능을 절충**한다.  
우리는 아키텍처를 변경하지 않고 기존의 SOTA 모델을 해석 가능하게 하여 **해석 가능성 대 정확성 트레이드 오프를 피한다.**  
이 접근 방식은 CAM의 일반화이며 훨씬 더 광범위한 CNN 모델 제품군에 적용할 수 있다.  

**What makes a good visual explanation?******

이미지 분류를 정당화하기 위해 모델에서 이미지 분류 '좋은' 시각적 설명을 고려하면 다음과 같다.  
(a) class-discriminative(즉, 이미지에서 카테고리를 현지화)  
(b) 고해상도(예: 미세한 세부 묘사 캡처)  

그림 1은 '호랑이 고양이' 클래스(위)와 '복서'(개) 클래스(아래)에 대한 여러 시각화 결과를 보여줍니다.  
Guided Backpropagation 및 Deconvolution과 같은 픽셀 공간 그라디언트 시각화는 고해상도이며 이미지의 세밀한 세부 사항을 강조하지만 클래스를 구분하지는 않습니다  
(그림 1b 및 그림 1h는 매우 유사함).
  
대조적으로, CAM 또는 우리가 제안한 방법인 Grad-CAM과 같은 지역화 접근 방식은 매우 클래스 구분적입니다.  
1c, 그리고 그 반대의 그림 1i).

두 세계의 장점을 결합하기 위해 기존 픽셀 공간 그래디언트 시각화를 Grad-CAM과 융합하여 고해상도와 클래스 구분이 가능한  
Guided Grad-CAM 시각화를 생성할 수 있음을 보여줍니다.  
결과적으로 그림 1d 및 1j에서와 같이 이미지에 가능한 여러 개념에 대한 증거가 포함되어 있더라도 관심 있는 결정에 해당하는  
이미지의 중요한 영역이 고해상도 세부정보로 시각화됩니다.  
'호랑이 고양이'에 대해 시각화할 때 Guided Grad-CAM은 고양이 영역을 강조 표시할 뿐만 아니라  
고양이의 특정 품종을 예측하는 데 중요한 고양이의 줄무늬도 강조 표시합니다.

요약하자면 우리의 기여는 다음과 같다.

(1) 구조변경/재학육 없이 CNN 기반 네트워크에 대한 시각적 설명을 생성하는 Grad-CAM을 소개한다.  
localization(S4.1)와 모델에 대한 faithfulness(S5.3)를 위해 Grad-CAM을 평가한다.  

(2) 기존의 최고 성능 분류, 캡션(S8.1) 및 VQA(S8.2) 모델에 Grad-CAM을 적용한다.  
이미지 분류를 위해 우리의 시각화는 현재 CNN(6.1절)의 실패에 대한 통찰력을 제공하여 겉보기에  
비합리적인 예측에 합리적인 설명이 있음을 보여준다.  
캡션 및 VQA의 경우, 우리의 시각화는 일반적인 CNN + LSTM 모델이 ground 이미지-텍스트 쌍에 대해  
학습을 받지 않았음에도 구별되는 이미지 영역을 지역화하는 데 놀라울 정도로 우수하다는 것을 보여준다.  

(3) 해석 가능한 GradCAM 시각화가 데이터 세트의 편향을 밝혀 오류 모드를 진단하는 데 어떻게 도움이 되는지에 대한 개념 증명을 보여준다.  
이는 일반화뿐만 아니라 사회에서 점점 더 많은 결정이 알고리즘에 의해 이루어짐에 따라 공정하고 편견 없는 결과를 위해서도 중요하다.  
  
(4) 이미지 분류 및 VQA에 적용된 ResNet에 대한 Grad-CAM 시각화를 제시한다(S8.2)  

(5) Grad-CAM의 뉴런 중요도와 모델 결정에 대한 뉴런 이름을 사용하고 텍스트 설명을 얻는다(S7).  

(6) 우리는 Guided Grad-CAM 설명이 계급 차별적이며 인간이 신뢰를 구축하는 데 도움이 될 뿐만 아니라 훈련되지 않은 사용자가  
'강한' 네트워크와 '약한' 네트워크를 성공적으로 분별할 수 있도록 돕는 인간 연구(S5)를 수행한다.  
둘 다 동일한 예측을 하는 경우에도 마찬가지이다.  

**Paper organization**:
  
S3  : GradCAM 및 Guided GradCAM 접근 방식을 제안  
S45 : Localization 능력, classification, trustworthyness, faithfulness를 평가한다.  
S6  : 분류 CNN 진단 및 데이터 세트의 편향 식별과 같은 Grad-CAM의 특정 사용 사례를 보여준다.  
S7  : GradCAM으로 텍스트 설명을 얻는 방법을 제공한다.  
S8  : GradCAM을 시각 및 언어 모델(이미지 캡션 및 VQA)에 적용할 수 있는 방법을 보여준다.  
  
## 2. Related Work
Visualizing CNN
Assessing Model Trust
Aligning Gradient-based Importances
Weakly-supervised localization
## 3. Grad-CAM
3.1 Grad-CAM generalizes CAM  
3.2 Guided Grad-CAM  
3.3 Counterfactual Explanations

## 4 Evaluating Localization Ability of Grad-CAM
4.1 Weakly-supervised Localization
4.2 Weakly-supervised Segmentation
4.3 Pointing Game
  
## 5 Evaluating Visualizations
5.1 Evaluating Class Discrimination
5.2 Evaluating Trust
5.3 Faithfulness vs. Interpretability

## 6 Diagnosing image classification CNNs with Grad-CAM
6.1 Analyzing failure modes for VGG-16
6.2 Effect of adversarial noise on VGG-16
6.3 Identifying bias in dataset

## 7 Textual Explanations with Grad-CAM
## 8 Grad-CAM for Image Captioning and VQA
8.1 Image Captioning
**Comparison to dense captioning.**
8.1.1 Grad-CAM for individual words of caption
**Comparison to Human Attention **
8.2 Visual Question Answering
**Comparison to Human Attention**
**Visualizing ResNet-based VQA model with co-attention**
## 9 Conclusion
