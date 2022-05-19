## Abstract
새로운 생성모델 제안 : Score matching으로 추정된 데이터 분포의 gradient를 사용하여 Langevin dynamics를 통해 생성된 샘플을 사용  
Gradient가 ill-defined 일 수 있고 데이터가 저차원의 manifold에 존재하는 경우 추정하기 어려울 수 있기 때문에 우리는 이 문제를 위해 데이터를 다양한 level의 Gaussian noise로 perturb한다.  
그리고 함께 상응하는 score(예를들면 모든 noise level에 대한 perturbed 데이터의 gradient에 대한 vector field)를 추정한다.  
샘플링을 위해, 우리는 (데이터 메니폴드에 더 가까워 지도록 하는 sampling process로써 noise level을 점진적으로 줄여나가는것에 해당하는 gradient를 사용하는) annealed Langevin dynamics를 제안한다.  
우리 프레임워크는 유연한 모델 아키텍쳐를 하게 하고 학습동안의 샘플링이 필요하지 않고 adversarial 방식에 대한 사용도 필요없다.  
또한 (principled model comparisons에 사용될 수 있는) 학습 목적함수를 제공한다.  

## Introduction
