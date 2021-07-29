# Semi-supervised learning
학습에 **소량의 labeled** 데이터와 **다량의 unlabeled** 데이터를 결합하는 ML approach  
지도학습과 비지도학습의 중간쯤에 놓여있는 방법이며 weak supervision의 특별한 경우이다.  
소량의 labeled 데이터와 함께 사용될때 unlabeled 데이터는 학습 정확도에 있어서 엄청난 향상을 만들어낼 수 있다.  
학습을 위한 labeled 데이터획득은 숙련된 인력(오디오 segment 기록)이나 물리적인 실험(단백질의 3차온 구조결정이나 오일의 특정 위치를 결정짓는)을 필요로한다.  
따라서 라벨링 프로세스와 관련된 비용은 크고 완전히 라벨링된 훈련 세트를 실행 불가능하게 만들 수 있는 반면, 라벨링되지 않은 데이터의 획득은 상대적으로 저렴하다.
이러한 상황에서, 준지도학습은 엄청나게 현실적인 가치를 제공할 수 있다. 준지도학습은 마찬가지로 ML에서 그리고 인간 학습모델로써 이론적인 관심의 대상이 된다.  

![image](https://user-images.githubusercontent.com/40943064/127413456-9cb1b7f7-ed9e-408b-9a7b-57bec2b68eff.png)


준지도 학습은 정보를 결합함으로써 다음의 두가지 경우의 성능을 능가한다.
1) supervised : label이 지정되지 않은 데이터를 버리고 지도 학습
2) unpuservised : label을 버리고 비지도 학습

비지도학습은 transductive 학습 또는 inductive 학습으로 표현할 수도 있다.  
transductive 학습의 목표는 x(k+1), ..., x(l+u)의 unlabeled 데이터가 주어진 경우에 올바른 label을 추론하는 것이다.  
inductive 학습의 목표는 X에서 Y로의 맞는 mapping을 추론하는 것이다.  

직관적으로 학습 문제는 시험으로 볼 수 있으며 교사가 다른 문제 세트를 해결하는 데 도움이 되는 수업을 위해 해결하는 샘플 문제로 label이 지정된 데이터를 사용할 수 있다.  
변환적 설정에서 이러한 미해결 문제는 시험 문제로 작용한다. 귀납적 환경에서는 시험을 구성하는 일종의 연습 문제가 된다.  

전체 입력 공간에 대한 classification rule을 유추하는 방식으로 transductive learning을 수행하는 것은 불필요(Vapnik의 원칙에 따라 부주의)하다.  
그러나 실제로 transduction 또는 induction를 위해 공식적으로 설계된 알고리즘은 서로 바꿔서 사용하는 경우가 많다.  

## Assumptions
unlabeled 데이터를 이용하기 위해서는, 데이터 분포에 내제하는 관계가 존재해야 한다.  
준지도학습알고리즘은 다음의 가정 중 적어도 하나를 이용한다.

### Continuity assumption
*가까운 점은 label을 공유할 가능성이 높다.*  
이는 지도학습에서도 일반적으로 가정되며 기하학적으로 단순한 decision boundary를 선호한다.  
준지도 학습의 경우, smoothness 가정은 low-density 영역에서 decision boundaries를 추가로 선호하기 때문에 서로 가깝지만 class는 다르다.  

### Cluster assumption

*데이터는 이산형 군집을 형성하는 경향이 있으며, 같은 군집의 점은 레이블을 공유할 가능성이 더 높다.  
(단, 라벨을 공유하는 데이터가 여러 군집에 분산될 수 있다).*  
이는 smoothness 가정의 특수한 경우이며 클러스터링 알고리즘으로 feature 학습을 가능하게 한다.  

### Manifold assumption
데이터는 입력 공간보다 훨씬 저차원의 manifold에 근사적으로 놓여 있다.

![image](https://user-images.githubusercontent.com/40943064/127414430-58af3569-1931-4399-8a68-06c22ed5e2ff.png)

이 경우 라벨링된 데이터와 라벨링되지 않은 데이터를 모두 사용하여 manifold를 학습하면 차원의 저주를 피할 수 있다.  
그후 manifold에 정의된 거리와 밀도를 사용하여 학습을 진행할 수 있다.

Manifold assumption은 고차원 데이터가 직접 모델링하기 어려울 수 있지만 자유도가 약간만 있는 일부 프로세스에 의해 생성될 때 실용적이다.  
예를 들어, 사람의 목소리는 몇 개의 성대에 의해 제어되고 다양한 표정의 이미지는 몇 개의 근육에 의해 제어된다.  
이러한 경우 발생하는 문제의 자연적 공간에서의 거리와 부드러움은 각각 가능한 모든 음파 또는 이미지의 공간을 고려하는 것보다 우수하다.

![image](https://user-images.githubusercontent.com/40943064/127415801-071e2415-23e4-41c9-bd19-92d27ecc9215.png)
출처 : https://blog.est.ai/2020/11/ssl/
