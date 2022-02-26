## Abstract
Object detection에서 localization과 classification을 결합하는 복잡한 특성은 방법의 성공적인 개발을 가져왔다.  
이전 작품은 다양한 object detection head의 성능을 향상시키기 위해 노력했지만 통합된 관점을 제시하지 못했다.  
본 논문에서, object detection head를 attention과 통합하기 위한 새로운 dynamic head 프레임워크를 제시한다.  
Scale 인식을 위한 feature level 사이, spatial 인식을 위한 공간 위치 사이, task 인식을 위한 출력 채널 내에서  
여러 self-attention 메커니즘을 일관되게 결합함으로써 제안된 접근 방식은 계산 오버헤드 없이 object detection head의 표현 능력을 크게 향상시킨다.  
표준 ResNeXt-101-DCN 백본을 사용하여 널리 사용되는 object detector보다 성능을 크게 개선하고 54.0 AP에서 새로운 SOTA를 달성한다.  

CV분야에서 object detection은 "어디에 어떠 물체가 있는가"에 대한 답변이다. [11, 23, 12, 35, 28, 31, 33]
DL의 시대에서, 거의 모든 object detector는 동일 패러다임을 공유한다. : Bacbone(feature 추출), Head(localization & classification).  
Obejct detection 작업에서 head 성능을 어떻게 향상시킬지 고민하는 것은 매우 중요한 문제가 되었다.
좋은 object detection head를 개발하는데 있어 어려운 도전과제는 세가지로 요약할 수 있다.  
1) Scale-aware : 물체는 이미지 내에 다양하게 구분되는 스케일로 존재
2) Spatial-aware : 물체는 다양한 시점에서 엄청나게 다른 모양, 회전, 위치로 존재
3) Task-aware : 완전 다른 목적과 제약을 가지는 bounding box, center, corner point등 다양한 표현
최근 연구들은 다양한 방식으로 전술한 세가지 문제중 한가지에 대해서마 집중하는것을 알게 되었다.
세가지 문제를 한번에 다루는 통합된 head를 개발하는것은 열린 문제로 남아있다.
본 논문에서, 세가지를 한번에 통합하는 dynamic head라고 하는새로운 detection head를 제안한다.

If we consider the output of a backbone (i.e., the input to a detection head) as a 3-dimensional tensor with dimensions level × space × channel, 
we discover that such a unified head can be re- garded as an attention learning problem. An intuitive solution is 
to build a full self-attention mechanism over this tensor. However, the optimization problem would be too difficult 
to solve and the computational cost is not afford- able.
Instead, we can deploy attention mechanisms separately on each particular dimension of features, 
i.e., level-wise, spatial-wise, and channel-wise. 
The scale-aware attention module is only deployed on the dimension of level. 
It learns the relative importance of various semantic levels to enhance the feature at a proper level for an individual object based on its scale. 
The spatial-aware attention module is de- ployed on the dimension of space (i.e., height × width). 
It learns coherently discriminative representations in spatial locations. 
The task-aware attention module is deployed on channels. 
It directs different feature channels to favor dif- ferent tasks separately 
(e.g., classification, box regression, and center/key-point learning.) based on different convolu- tional kernel responses from objects.
In this way, we explicitly implement a unified attention mechanism for the detection head. 
Although these attention mechanisms are separately applied on different dimensions of a feature tensor, 
their performance can complement each other. Extensive experiments on the MS-COCO benchmark
demonstrate the effectiveness of our approach. 
It offers a great potential for learning a better representation that can be utilized 
to improve all kinds of object detection models with 1.2% ∼ 3.2% AP gains. With the standard ResNeXt- 101-DCN backbone, 
the proposed method achieves a new state of the art 54.0% AP on COCO. 
Besides, compared with EffcientDet [27] and SpineNet [8], dynamic head uses 1/20 training time, yet with a better performance. 
Further- more, with latest transformer backbone and extra data from self-training, 
we can push current best COCO result to a new record at 60.6 AP (see appendix for details).
