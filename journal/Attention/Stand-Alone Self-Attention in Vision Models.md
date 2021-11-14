# Stand-Alone Self-Attention in Vision Models

## Abstract
Convolution은 현대 CV 시스템의 기본 구성요소이다. 최근 접근은 **long-range dependency**를 포착하기 위해 conv. 이상의 것을 탐색한다.  
다양한 vision task에서의 장점을 얻기 위해 self-attention, non-local means와 같은 content-based 상호작용을 가지는 conv.를 보강하는데 집중되어 왔다.  
자연스러운 궁금증은 attention이 conv. 의 확장 기능을 하는 것이 아니라 자체의 독립적인 역할을 할 수 있는지 여부이다.  
순수 self-attention 비전 모델을 개발하고 테스트하는 과정에서, 효과적인 독립 실행형 계층이 될 수 있음을 검증한다.  
ResNet 모델에 적용된 self-attention의 형태로 spatial conv.를 간단히 교체하여 12% 적은 FLOPS와 29% 적은 파라미터로  
ImageNet 분류의 기준선을 능가하는 fully self-attentional 모델을 생산한다.  
COCO object detection에서 pure self attention 모델은 기준 RetinaNet의 mAP와 일치하지만 39%의 FLOPS와 34% 적은 파라미터를 가진다.  
Ablation은 self-attention이 특히 뒷단 레이어에서 사용될 때 영향을 미친다는 것을 보여준다.  
이러한 결과는 stand-alone self attention이 전문가의 도구 상자에 중요한 추가 사항임을 입증한다.  

## Introduction
디지털 이미지 처리는 픽셀 이미지에 conv. 방식의 수작업의 선형 필터가 다양한 애플리케이션에 적용할 수 있다는 인식에서 비롯되었다.  
디지털 이미지 처리의 성공과 생물학적 고려사항은 신경망의 초기 연구자들이 이미지의 표현을 학습하기 위한  
매개 변수 효율적 아키텍처를 위해 conv. 표현을 이용하도록 고무했다.  
대규모 데이터 세트와 컴퓨팅 리소스의 출현으로 많은 컴퓨터 비전 애플리케이션의 중추로 CNN가 자리잡았다.  
DL은 recongnition, object detection, segmentation에 대한 성능 향상을 위한 CNN 아키텍처 설계로 크게 전환되었다.  
Conv.의 변환 등변성 특성은 Conv.를 이미지 운영을 위한 빌딩 블록으로 채택한 강력한 동기를 제공했다.  
그러나 대규모 receptive field에 대한 스케일링 속성이 낮아 conv.에 대한 long range interactions을 포착하는 것은 어렵다.  
Long range interactions 문제는 attention 사용을 통해 시퀀스 모델링에서 해결되었다.  
언어 모델링, 음성 인식 및 신경 캡션과 같은 작업에서 주목도가 높은 성공을 거두었다.  
최근, attention 모듈은 전통적인 CNN의 성능을 높이기 위해 차별적인 컴퓨터 비전 모델에 채택되었다.  
주목할 만한 것은 CNN 채널의 규모를 선택적으로 변조하기 위해 Squeeze-Excite라는 채널 기반 attention 메커니즘을 적용할 수 있다는 점이다.  
마찬가지로 spatially-aware attention mechanism은 물체 감지 개선 및 이미지 분류 개선을 위한 상황별 정보를 제공하기 위해  
CNN 아키텍처를 강화하는 데 사용되었다.  
이러한 작업에서는 global attention layer를 기존 컨볼루션 모델에 대한 추가 기능으로 사용해 왔다. 
이 전역 형식은 입력의 모든 공간 위치에 적용되므로 일반적으로 원본 이미지의 상당한 다운샘플링이 필요한 작은 입력으로 사용을 제한한다.
이 연구에서 우리는 content-based interactions이 conv. augmentation으로 작용하는 대신  
비전 모델의 주요 원시적 역할을 할 수 있는지 여부를 확인한다.  
이를 위해, 작은 입력과 큰 입력 모두에 사용할 수 있는 간단한 로컬 self-attention layer를 개발한다.  
우리는 이 독립형 attention 계층을 활용하여 매개 변수 및 계산 효율적이면서도 이미지 분류 및 객체 검출에 대한  
conv. 기준선을 능가하는 완전한 attentional vision 모델을 구축한다.
또한 stand-alone attention를 더 잘 이해하기 위해 여러 가지 ablation을 수행한다.  
결과가 비전 모델을 개선하기 위한 메커니즘으로서 콘텐츠 기반 상호 작용을 탐구하는 데 초점을 맞춘 새로운 연구 방향에 박차를 가하기를 바란다.

