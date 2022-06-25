# Abstract
ML의 중심 문제는 학습, 샘플링, 추론 및 평가를 위해 복잡한 데이터를 모델링 하는데 (해석적으로나 계산적으로 다루기 쉬운 확률분포의 family)만 사용할 수 있다는것이다.
Flexibility와 tractability를 동시에 달성하는 접근법을 개발한다.  
(Non-equilibrium statistical physics에서 영감을 받은 본질적인 아이디어)  
1) 반복적 forward diffusion process를 통해 데이터 분포의 구조를 체계적이고 천천히 파괴  
2) 데이터 구조를 복원하는 reverse diffusion process를 학습하여 데이터의 flexible하고 tractable한 생성 모델을 산출  
이 접근 방식을 통해 수천 개의 레이어 또는 시간 단계를 가진 deep generative model에서 확률을 빠르게 학습, 샘플링 및 평가하고 학습된 모델에서 조건부 및 사후 확률을 계산할 수 있다.  

# 1. Introduction
역사적으로 확률론적 모델은 두 가지 상충되는 목표, 즉 tractability와 flexibility 사이의 tradeoff로 어려움을 겪는다.  
1) Tractable model : 분석적으로 평가할 수 있고 데이터(예: 가우스 또는 라플라스)에 쉽게 적합할 수 있지만 rich dataset의 구조를 적절하게 설명할 수 없다.  
2) Flexible model  : 임의 데이터의 구조에 맞게 성형할 수 있다. 예를 들어, 우리는 유연한 분포 p(x) = ϕ(x) / Z(normalizing constant)를 산출하는 임의의 (non-negative) 함수의 관점에서 모델을 정의할 수 있다.  
그러나 normalizing constant Z를 계산하는 것은 일반적으로 어렵다. 이러한 유연한 모델에서 샘플을 평가, 훈련 또는 그리려면 일반적으로 계산량이 매우 큰 monte-carlo process가 필요하다.  

이러한 tradeoff를 개선하지만 제거하지는 않는 다양한 해석적 근사가 존재한다.
1)  Mean field theory and its expansions (T, 1982; Tanaka, 1998)
2)  Variational Bayes (Jordan et al., 1999)
3)  Contrastive divergence (Welling & Hinton, 2002; Hinton, 2002)
4)  Minimum probability flow (Sohl-Dickstein et al., 2011b;a)
5)  Minimum KL contraction (Lyu, 2011)
6)  Proper scoring rules (Gneiting & Raftery, 2007; Parry et al., 2012)
7)  Score matching (Hyvarinen ¨ , 2005)
8)  Pseudolikelihood (Besag, 1975)
9)  Loopy belief propagation (Murphy et al., 1999)
10) Non-parametric method

### 1.1. Diffusion probabilistic models

