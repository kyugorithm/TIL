## Abstract
**attention module**과 **학습 가능한 normalization 기능**을 **end-to-end**로 통합하는 unsupervised i2i translation을 위한 방법을 제안합니다.  
Attention은 보조 분류기가 획득한 attention map을 기반으로 source/target 을 구분하는 중요한 영역에 초점을 맞추도록 모델을 안내합니다.  
Geometric 변화가 불가능한 기존 attention 방식과 달리, 전체변화가 필요하거나 큰 형상의 변화가 필요한 이미지를 모두 변환할 수 있습니다.  
AdaLIN 기능은 attention-guided 모델이 데이터셋에 따라 학습된 매개변수로 모양과 질감의 변화량을 유연하게 제어할 수 있도록 합니다.  
실험 결과는 고정된 네트워크 아키텍처와 하이퍼 매개변수를 가진 기존 SOTA와 비교하여 제안된 방법의 우수성을 보여줍니다.

## 1. Introduction 
