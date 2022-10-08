## Abstract
본 논문은 저품질 연속 프레임으로부터 고품질 연속 프레임을 복원한다.  
단일 이미지 복원과는 달리 배열이 맞지 않는 근접프레임들로부터 temporal information 활용이 필요하다.  
현존 딥러닝 방법은 대개 **sliding window strategy** 혹은 **recurrent architecture**를 이용하여 해결한다.  
그러나 위 방법론은 frame 별로 처리를 하거나 긴 범위의 모델링 능력이 부족하다.  
본 연구에서 **병렬 프레임 추정**과 **긴 범위의 temporal dependency modeling** 능력을 가지는 VRT를 제안한다.  

구체적으로 VRT는 아래 두가지 모듈을 여러 해상도로 구성하는 구조이다.  
#### 1) TMSA(temporal mutual self attention) 
- 비디오를 작은 클립으로 나누고 두 종류의 attention을 적용한다.  
- 클립간 상호작용을 가능하게 하기 위해, 비디오 시퀀스는 layer마다 shift 한다.  
- **Mutual attention** : joint motion estimation, feature alignment, feature fusion  
- **Self attention** : feature extraction  

#### 2) Parallel warping
- Parallel feature warping을 통해 인접 프레임 정보를 추가적으로 혼합한다.  

## Introduction
여러 LQ 프레임으로 HQ 프레임을 복원하는 video restoration은 최근 많은 관심을 끌어왔다. reference frame의 복원을 위해서는 단일 이미지 복원과는 달리 매우 연관되지만 배열은 맞지 않는 supporting frame을 최대한 활용하는것이 핵심 과제이다.  
현존하는 video restoration 방법들은 주로 두가지로 분할된다.  
1) Sliding window-based methods (9개)  
- 단일 HQ 프레임 생성을 위해 여러 입력 프레임을 사용하며 sliding window 이용한다.  
- 각 입력 프레임은 추론시에 여러번 처리되며 비효율적 feature 활용과 compuation cost를 야기하게 된다.
2) Recurrent methods (12개)  
- 다음 프레임의 reconstruction을 위해 이전 복원된 HQ 프레임을 주로 사용한다.  
- 재귀적 속성으로 인해 세가지 단점이 존재한다.  
: 효율적인 분산학습을 위한 병렬화 제한된다.
: 정보가 프레임별로 축적됨에도 recurrent model은 temporal dependency modelling에 좋지 못하다. (인접 프레임은 매우 강하게 영향을 주지만 그 영향은 몇개의 스텝이 지나가면 손실된다.)
: 프레임 수가 적은 비디오들에 대해 엄청나게 성능이 떨어진다.  

본 논문에서는 parallel computation, long-range dependency modelling이 가능한 VRT를 제안한다. 
