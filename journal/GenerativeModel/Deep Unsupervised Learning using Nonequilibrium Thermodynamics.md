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
우리는 아래를 허용하는 확률모델을 정의하기 위한 새로운 방법을 제시한다.  
1) 모델 구조상 극단적인 유연성
2) 정확한 샘플링
3) 다른 분포와의 쉬운 곱(posterior를 계산하기 위해 필요)
4) 모델 log liklihood 그리고 개별상태의 확률이 쉽게 계산되어짐

우리의 방법은 Markov chain을 사용하여 점진적으로 특정 분포에서 다른 분포로 변해가도록 하며 이 아이디어는 Jarzynski의 non-equlibrium physics와 Neal의 sequential Monte Carlo에서 사용되었다.  우리는 diffusion process를 사용하여 단순한 알려진 분포(Gaussian)을 target(data) distribution으로 분포를 옮겨가도록 하는 생성적 Markov chain을 만든다. 
(Markov chain은 한 분포를 점진적으로 다른 분포로 옮겨지도록 하는 방법론으로 활용하며 단순한 Gaussian 분포를 원하는 목표의 데이터 분포로 옮겨가도록 하는데 사용한다는 것)  
  
이 Markov chain을 사용하여 달리 정의된 모델을 대략적으로 평가하기보다는 확률론적 모델을 Markov chain의 끝점으로 명시적으로 정의한다. Diffusion chain의 각 단계는 분석적으로 평가할 수 있는 확률을 가지므로 전체 체인도 분석적으로 평가할 수 있다.  

이 프레임워크에서의 NN모델이 학습하는것은 diffusion 과정에 대한 작은 perturbation 추정하는 것이다. 작은 perturbation을 추정하는 것은 non-analytically-normalizable, potential function
으로 전체 분포를 명시적으로 설명하는 것보다 다루기 쉽다. 또한, 매끄러운 target 분포에 대한 확산 과정이 존재하기 때문에 이 방법은 임의의 형태의 데이터 분포를 포착할 수 있다.  
  
### 1.2. Relationship to other work

Wake-sleep algorithm(Hinton, 1995; Dayan et al., 1995)은 서로에 대한 훈련 추론과 생성 확률 모델의 아이디어를 도입했다. 이 접근법은 일부 예외를 제외하고는 거의 20년 동안 거의 연구되지 않았다. 최근 이 아이디어를 개발하는 작업이 폭발적으로 증가하고 있다. 어떤 연구에서는 잠재 변수에 대한 유연한 생성 모델과 사후 분포를 서로에 대해 직접 훈련할 수 있는 변형 학습 및 추론 알고리듬이 개발되었다.

위 방법들의 variational bound는 우리의 훈련 목표와 (Sminchissu et al., 2006)의 초기 작업에 사용된 것과 유사하다. 그러나 우리의 동기 부여와 모델 형태는 모두 매우 다르며, 현재 연구는 이러한 기술과 관련하여 다음과 같은 차이점과 이점을 유지한다.

1. 우리는 variational Bayesian 방법보다 physics, quasi-static processes, and annealed importance sampling의 아이디어를 사용하여 프레임워크를 개발한다.

2. 학습된 분포와 다른 확률 분포(예: 사후를 계산하기 위한 조건부 분포)를 쉽게 곱하는 방법을 보여준다.

3. 추론 모델과 생성 모델 사이의 목표의 비대칭으로 인해 추론 모델을 훈련하는 것이 variational
inference 방법에서 특히 어려울 수 있다는 어려움을 해결한다. 우리는 inverse(generative) 프로세스가 동일한 functional form을 갖도록 forward(inference) 프로세스를 단순한 functional form으로 제한한다.

4. 우리는 소수의 레이어가 아닌 수천 개의 레이어(또는 시간 단계)로 모델을 교육한다.

5. 각 layer(또는 시간 단계)에서 entropy production에 대한 상한과 하한을 제공한다.

