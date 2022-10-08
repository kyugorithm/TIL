## Abstract
본 논문은 저품질 연속 프레임으로부터 고품질 연속 프레임을 복원하는것을 목표로 한다.  
단일 이미지 복원과는 달리 배열이 맞지 않는 근접한 여러 프레임으로부터 temporal information 활용이 필요하다.  
현존하는 딥러닝 방법은 보통 sliding window strategy나 recurrent architecture를 이용하여 해결한다.  
그러나 접근법은 frame 별로 처리를 하거나 긴 범위의 모델링 능력이 부족하다.  
본 연구에서 **병렬 프레임 추정**과 **긴 범위의 temporal dependency modeling** 능력을 가지는 VRT를 제안한다.  
구체적으로 VRT는 아래 두가지 모듈를 여러 해상도로 구성하는 구조이다.  
#### 1) TMSA(temporal mutual self attention). 
- TMSA는 비디오를 작은 클립으로 나누고 두 종류의 attention을 적용한다.  
- **Mutual attention** : joint motion estimation, feature alignment, feature fusion  
- **Self attention** : feature extraction  
(클립간 상호작용을 가능하게 하기 위해, 비디오 시퀀스는 layer마다 shift 시킨다.)  

#### 2) Parallel warping
- Parallel feature warping을 통해 인접 프레임 정보를 추가적으로 혼합한다.  
