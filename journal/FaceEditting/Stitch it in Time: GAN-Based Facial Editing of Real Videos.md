## Abstract
Latent space 내에서 풍부한 의미론을 인코딩하는 GAN의 기능은 얼굴 image editing 편집에 널리 채택되었다.  
그러나 비디오에서의 성공은 어려웠다. 고품질 얼굴 비디오 세트가 부족하며, 비디오로 작업하는 것은 극복해야 할 근본적인 장벽인 temporal consistency를 초래한다.  
우리는 이 장벽이 대체로 artificial이라고 제안한다. 소스 비디오는 이미 시간적으로 일관성이 있으며, editing 파이프라인에서 개별 구성 요소를 부주의하게 처리했기 때문에  
부분적으로 이 상태에서의 편차가 발생한다.  
우리는 StyleGAN의 자연스러운 alignment를 활용한다. 
GAN과 신경망의  low frequency functions 학습 경향은 그것들이 강하게 일관된 사전 정보를 제공한다는 것을 보여준다.  
우리는 이러한 통찰력을 바탕으로 비디오에서 얼굴의 의미론적 편집을 위한 프레임워크를 제안하여 현재의 SOTA에 비해 상당한 개선을 보여준다.  
우리 방법은 의미 있는 얼굴 조작을 생성하고, 더 높은 수준의 시간 일관성을 유지하며, 현재 방법이 어려움을 겪고 있는 도전적이고 고품질의 talking head 비디오에 적용할 수 있다.  

## 1. Introduction
GAN을 이용해 사용자는 직관적인 방식으로 사진을 수정할 수 있다. 특히 StyleGAN의 고도로 얽혀있는 latent space는 얼굴 이미지의 사실적인 편집에 널리 적용되었다.  
그러나 이러한 의미론적 편집 도구는 비디오 편집이 시간적 일관성을 유지하는 추가적인 과제를 부과하기 때문에 대부분 이미지로 제한되었다.  
비디오의 모든 조작은 모든 비디오 프레임에 일관되게 전파되어야 한다. 이전 연구는 비디오 합성을 위해 GAN을 훈련시킴으로써 이 과제를 해결할 것을 제안한다[36, 47, 51].  
36 :  Stylegan-v: A continuous video generator with the price, image quality and perks of stylegan2
47 : Video generation using vqvae and transformers
51 : Generating Videos with Dynamics-aware Implicit Generative Adversarial Networks  
그러나 고품질 비디오 데이터 세트가 부족하고 추가 데이터 차원으로 인해 발생하는 복잡성으로 인해 video-GAN은 지금까지 단일 이미지의 품질과 비교할 수 없었다.  

Instead, we propose to meet this challenge by using the latent-editing techniques commonly employed with an off the shelf, non-temporal StyleGAN model. We highlight a fundamental assumption about the video editing process: the initial video is already consistent. In contrast to synthesis works, we do not need to create temporal consistency, but only maintain it. Building on this intuition, we revisit the building blocks of recent StyleGAN-based editing  pipelines, identify the points where temporal inconsistencies may arise, and propose that in many cases these inconsistencies can be mitigated simply through a careful choice of tools.
대신, 우리는 기존의 non-temporal StyleGAN에 일반적으로 사용되는 latent-editing techniques 기술을 사용하여 이 과제를 해결할 것을 제안한다.  
우리는 비디오 편집 프로세스에 대한 근본적인 가정을 강조한다.  
초기 비디오는 이미 일관적이다. 합성 작업과 대조적으로, 우리는 시간적 일관성을 만들 필요가 없고 단지 그것을 유지할 필요가 있다.  
이러한 직관을 바탕으로, 우리는 최근의 StyleGAN 기반 편집 파이프라인의 구성 요소를 다시 살펴보고, 시간적 불일치가 발생할 수 있는 지점을 식별하며, 많은 경우 이러한 불일치는 단순히 도구의 신중한 선택을 통해 완화될 수 있다고 제안한다.  

아래 두 가지 유형의 temporal consistency를 인식함으로써 조사를 시작한다.  
1) Local : 인접 프레임 간 전환이 원활하지 않고 상당한 지터를 표시
2) 정체성 변화와 같은 GAN 편집 프로세스의 부정확성이 시간이 지남에 따라 축적

우리는 최근에 제안된 PTI를 고려한다. (입력 이미지의 근사치를 생성하기 위해 제너레이터를 통해 공급될 수 있는 초기 latent code 'pivot'을 찾는 inversion에 대한 2단계 접근 방식)  
그런 다음, 특정 'pivot' code가 target을 더 잘 재현할 수 있도록 G의 weight가 미세 조정된다.  
PTI는 강력한 글로벌 일관성을 제공하여 ID를 target 비디오와 일치시킨다. 그러나 우리의 조사에 따르면 local benchmark에서 제대로 작동하지 않고 editing 작업에서 일관되지 않게 동작하는 반전이 생성된다.  

이 시점에서 우리는 두 가지 주요 관찰을 한다. G는 low frequency 함수를 학습하는 경향이 있는 것으로 알려진 highly parametric neural function이다.  
따라서 입력(잠재 코드)의 작은 변화는 생성된 이미지의 작은 변화만을 유발할 가능성이 있다.  
더욱이, style-based 모델은 특히 가까운 도메인으로 전환할 때 미세 조정 하에서 놀라운 alignment를 유지하는 것으로 나타났다.  
따라서 G가 매끄럽게 변경되는 latent code 집합에 대해 일관된 editing을 생성하는 경우 미세 조정된 G는 temporal consistency에 대해 유사하게 경향이 있을 것으로 예상합니다.  

이러한 직관을 염두에 두고 우리는 PTI의 local inconsistency가 프로세스의 첫 번째 단계인 'pivot'을 찾는 단계에서 발생한다고 제안한다.  
보다 구체적으로, 사용된 optimization-based inversion은 일관성이 없다. 매우 유사한 프레임은 동일한 초기화 및 랜덤 노이즈 시드를 사용하는 경우에도 잠재 공간의 다른 영역으로 인코딩될 수 있다.  
반면에 encoder 기반 inversion은 highly parametric network를 사용하므로 low frequency 표현으로 편향된다.  
따라서 인코더는 두 개의 인접한 비디오 프레임을 관찰할 때와 같이 입력이 약간만 변경될 때 천천히 변화하는 잠재성을 제공할 가능성이 높다.  

Locally consistent pivot을 발견하기 위한 encoder와 global consistency를 촉진하기 위한 G의 fine-tuning의 두 가지 접근 방식을 병합하고 이미 강력하게 일관된 prior를 제공함을 보여준다.  
그럼에도 불구하고 실제 비디오를 편집하기에는 충분하지 않다. StyleGAN은 전체 프레임에서 작동할 수 없으므로 편집된 crop을 원본 비디오에 다시 연결해야 한다.  
그러나 inversion 및 editing 방법은 일반적으로 배경을 광범위하게 손상시켜 결과를 원본 프레임에 혼합하기 어렵게 만든다.  
이를 위해 공간적으로 일관된 전환을 제공하기 위해 G를 추가로 조정하는 새로운 'stiching tuning' 작업을 설계한다.  
이렇게 하면 editing 효과를 유지하면서 사실적인 blending을 얻을 수 있다.

제안된 editing 파이프라인이 실제 비디오의 얼굴에 latent-based semantic editing을 원활하게 적용할 수 있음을 보여준다.  
Non-temporal 모델만을 사용하지만, 기존 방법으로는 다루지 못하는 큰 움직임과 복잡한 배경을 가진 도전적인 talking head video를 성공적으로 편집할 수 있다.  

## 2. Background and Related Work
### StyleGAN-based Editing
StyleGAN은 의미론적으로 풍부하고 고도로 구조화된 latent space에서 고화질 이미지를 생성하기 위해 style-based 아키텍처를 사용한다.  
놀랍게도 StyleGAN은 간단한 latent code editing을 통해 이미지를 사실적으로 편집할 수 있다.  
이에 동기를 부여받은 많은 방법이 다양한 수준의 supervision을 사용하여 의미 있는 latent 방향을 발견했다.  
Attribute label 이나 facial 3D priors와 같은 완전 감독에서 완전히 unsupervised 제로 샷 접근 방식이 있다.  

### GAN Inversion

그러나 이러한 편집 방법을 실제 이미지에 적용하려면 먼저 주어진 이미지의 해당 latent 표현을 찾아야 하며, 이를 GAN inversion이라고 한다.  
여러 작품에서 StyleGAN의 맥락에서 inversion을 연구했다. 특정 이미지를 재생하기 위해 latent vector를 직접 최적화하거나, 대규모 이미지 컬렉션에 대해 효율적인 encoder를 훈련한다.  
일반적으로 직접 최적화가 더 정확하지만 encoder가 추론에서 더 빠르다.  
더욱이, highly parametric neural function estimator로서의 특성으로 인해 encoder는 더 부드러운 동작을 표시하여 유사한 입력에 대해 보다 일관된 결과를 생성하는 경향이 있다.  
우리는 이러한 이점을 활용한다.  

이전 inversion 방법은 다음 두 공간 중 하나에서 code를 생성했다. 
1) StyleGAN의 기본 latent space(W) 
2) 고유한 latent code가 G의 각 레이어에 할당되는 보다 표현적인 W+  

그 이후로 W가 더 높은 수준의 편집 가능성을 나타내는 것으로 나타났습니다. 이 공간의 latent code는 더 높은 수준의 사실성을 유지하면서 더 쉽게 조작할 수 있다.  
다른 한편 W는 표현력이 낮아 대상 id와 종종 일치하지 않는 inversion이 발생한다.  
Tov는 이것을 distortion-editability trade-off로 정의합니다. 그들은 W에 가까운 W+의 코드를 예측하는 encoder를 설계하여 두 가지 측면의 균형을 맞출 수 있다고 제안한다.  
보다 최근 Roich는 이 절충안을 회피할 수 있음을 보여주었다. 'pivot'이라고 하는 초기 inversion code를 중심으로 G를 미세 조정하여 높은 수준의 편집 가능성으로 최첨단 재구성을 달성한다.  
그러나 비디오에 PTI를 순전히 적용하면 서로 다른 pivot이 반드시 일관성이 있는 것은 아니기 때문에 temporal consistency가 발생할 수 있다.  
Xu는 단일 이미지 대신 일련의 프레임을 사용하여 inversion 품질을 개선하기 위한 다른 접근 방식을 제안했습니다.  

StyleGAN을 사용한 비디오 생성 대부분의 작업에서 이미지 영역에서 StyleGAN의 사용을 탐구했지만 최근 몇 가지 작업은 비디오 생성 및 조작 영역에서 StyleGAN의 많은 이점을 가져오려고 했다.  
생성적 측면에서 Skorokhodov는 짧고(예: 3) 일관된 프레임 시퀀스를 생성할 수 있는 스타일 기반 모델을 제안한다.  
그러나 그들의 방법은 현재 낮은 품질과 불충분한 데이터를 나타내는 임시 데이터 세트를 필요로 한다.  
다른 작업은 사전 학습된 고정 StyleGAN에 대해 시간적으로 일관된 latent code를 생성하기 위해 두 번째 G를 학습한다.  
그들은 공간 및 시간 정보를 분리하는 것을 목표로 한다. Tian은 시간적 LSTM 기반 G를 학습한다.  
Fox는 다른 접근 방식을 사용하여 단일 비디오만 사용한다. 생성된 latent 시퀀스는 나중에 임의의 latent code로 projection되어 무작위 주제에 애니메이션을 적용한다.  
그러나 이러한 방법은 초기의 확실한 결과를 제공하지만 실제 비디오를 충실하게 inversion 하거나 편집하는 데 성공하지 못한다.  

### Video Semantic Editing 
많은 접근 방식이 이미지에서 얼굴 속성의 편집을 제안했다. 그러나 프레임 수준에서 이를 적용하면 일반적으로 시간적 불일치가 발생하여 비현실적인 비디오 조작이 발생한다.  
이 문제를 극복하기 위해 비디오 특정 방법이 제안되었습니다. Duong는 deep reinforcement learning을 사용하여 비디오 시퀀스에서 facial aging을 수행한다.  
우리 작업에 가장 가까운 Yao는 보다 disentangled 편집을 달성하기 위해 전용 latent-code transformer를 훈련하여 StyleGAN을 사용하여 실제 비디오를 편집할 것을 제안한다.  
이러한 편집은 제안된 파이프라인의 일부로 적용되며, 여기에는 먼저 jitter를 줄이기 위한 매끄러운 optical-flow based 자르기 및 정렬 단계가 포함된다.  
그런 다음 그들은 W+ encoder를 사용하여 프레임을 inversion하고 전용 transfomer를 사용하여 편집을 수행하고 segmentation mask를 사용하여 poisson blending을 사용하여 원본 비디오로 다시 연결한다. 우리의 작업에서 우리는 이미 매우 일관된 도구를 구축함으로써 흐름이나 시간 기반 모듈 없이도 더 까다로운 설정과 더 적은 시각적 아티팩트로 향상된 편집을 달성할 수 있음을 보여준다.

## 3. Method
실제 영상과 의미론적 잠재 편집 방향을 고려하여 편집 영상을 제작하는 것을 목표로 합니다. 결과는 원본 프레임의 충실도를 유지하면서 시간적으로 일관된 방식으로 수정하여 의미 있고 사실적인 편집을 달성해야 합니다. 이를 위해 우리는 시간적으로 일관된 정렬, 인코더 기반 반전, 생성기 튜닝, 편집, 스티칭 튜닝 및 최종적으로 결과를 원래 프레임으로 다시 병합하는 6가지 구성 요소의 파이프라인을 설계합니다. 다음 섹션에서는 각 핵심 단계, 구현에 사용된 도구 및 각 선택의 동기에 대해 자세히 설명합니다. 전체 파이프라인의 개요가 그림 2에 나와 있습니다. 또한 편집 파이프라인의 여러 단계에서 비디오 상태의 시각화가 그림 3에 제공됩니다.
