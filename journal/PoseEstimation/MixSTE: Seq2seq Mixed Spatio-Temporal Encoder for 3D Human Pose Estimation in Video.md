MixSTE: Seq2seq Mixed Spatio-Temporal Encoder for 3D Human Pose Estimation in Video

## Abstract
시공간 상관 관계를 학습하기 위해 전체 프레임의 신체 관절을 고려하여 2D 키포인트 시퀀스에서 3D 자세를 추정하는 tranformer 기반 방법론이 최근 도입되었다. 관절에 따라 움직임이 크게 달라지는 것을 알 수 있다. 그러나 이전 방법으로는 각 관절의 견고한 프레임 간 대응관계를 효율적으로 모델링할 수 없으므로 시공간적 상관관계에 대한 학습이 불충분하다. 각 관절의 시간적 움직임을 별도로 모델링하는 시간적 transformer 블록과 관절 간 공간적 상관관계를 학습하는 공간적 transformer 블록이 있는 MixSTE(Mix Spacio-Temporal Encoder)를 제안한다. 이들 2개의 블록을 번갈아 사용하여 시공간 feature encoding을 개선한다. 또, 네트워크 출력을 중앙 프레임으로부터 입력 비디오의 전체 프레임까지 연장해, 입력 시퀀스와 출력 시퀀스의 일관성을 향상시킨다. 제안된 방법을 평가하기 위해 세 가지 벤치마크(Human3.6M, MPI-INF-3DHP, HumanEva)에 대해 광범위한 실험을 수행했다. 결과는 우리 모델이 Human3.6M 데이터 세트에서 10.9% P-MPJPE 및 7.6% MPJPE만큼 최첨단 접근 방식을 능가한다는 것을 보여줍니다.
