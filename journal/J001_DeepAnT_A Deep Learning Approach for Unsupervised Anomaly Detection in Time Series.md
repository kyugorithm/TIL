### Abstract

기존의 거리 및 밀도 기반 이상 탐지 기술은 '주기적', '계절적' 관련 포인트 이상 징후를 탐지할 수 없다. non 스트리밍 사례에 동일하게 적용되는 시계열 데이터에 대한 새로운 딥 러닝 기반 이상 탐지 접근법을 제시하며 다음의 세가지에 대하여 강한 성능을 보여준다.

1) point anomalies
2) contextual anomalies
3) discords in time series 

일반적인 방법은 이상징후를 포착하는데 집중하지만 본 방법론은 바람직한 정상패턴을 예측하도록 학습한다.

본 방법론은 아래와같이 구성된다.
1)	Time-series predictor
- CNN구조를 이용하여 과거 시간 window에 대한 정보를 입력받아 미래 시간 윈도우 거동을 예측 한다.
2)	anomaly detector
- 예측값이 만들어지면 실제 측정값과 비교하여 정상/비정상으로 태깅한다.

이상 징후를 제거하지 않고도 학습이 가능하다. 일반적으로 딥 러닝 기반 접근 방식에서는 모델을 훈련시키기 위해 많은 데이터가 필요한 반면에 본 방법론은 CNN의 효과적인 매개 변수 공유로 인해 적은 데이터로 훈련될 수 있다. 또한 unsupervised 특성으로 anomaly의 label이 필요 없다. 따라서, y값 레이블링이 현실적으로 불가능한 데이터에 대해서 적용할 수 있다.


총 433개의 실제 및 합성 시간 시리즈를 포함하는 10개의 이상 탐지 벤치마크에서 15개의 알고리즘에 대한 세부 평가를 수행했으며. 실험에 따르면 DeepAnT는 대부분의 경우 최신 이상 탐지 방법을 능가하는 반면 다른 방법과 동등한 성능을 발휘한다.

#### 나의 생각
본 논문에서말하는 방법론은 time-series predictor를 통하여 미래 패턴을 예측하고 예측된 값과 실제 측정값의 차를 이용하여 차가 큰 부분을 anomaly로 판단하는 방법론을 채택했다. Time-series discord anomaly detection 방법론을 사용한 것이므로 큰 novelty는 없는것으로 보인다. 다만 해당 방법론을 참고해서 나의 연구 사례에도 적용할 가치가 있어보인다.
<img src="https://ieeexplore.ieee.org/mediastore_new/IEEE/content/media/6287639/8600701/8581424/munir1-2886457-large.gif" width="600" height="200">

그림에서 볼수 있듯이 2개의 Convolution(32 filters)-max pooling pair구조를 가진다. 내 생각에는 time-series의 길이에 따라 알맞은 구조나 파라미터가 달라질 것 같은데 이에 대한 설명은 없다는점이 조금 아쉽다.
