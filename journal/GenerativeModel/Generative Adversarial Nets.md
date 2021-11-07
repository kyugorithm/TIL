
 무척 유명한 논문이다. GAN 계열의 파생 논문이 수도없이 쏟아져 나오고 있는것은 그만큼 혁신적인 framework이기 때문인데, 그많은 내용을 다 섭렵하긴 어렵겠지만 필요한것들은 모두 봐야겠다.
사실, StyleMapGAN에 대한 이해를 위한 것인데... 기초부터 다시금 차근차근 정리해 나가려고한다. 모든 이론은 그 뿌리를 제대로 이해해야 된다고 생각한다.
이상!

### Abstract
본 논문은 adversarial 과정을 통하여 generative 모델을 추정하기 위한 새로운 framework을 제시한다.  
이 과정에서 Generator G는 데이터 분포를 최대한 근사하고 Discriminator D는 입력이 G로부터가 아닌 실제 데이터에서 올 확률을 추정한다.  
G의 학습 목표는 D가 틀릴 확률을 **최대**로 높이는 것이다. 이 framework은 따라서 min-max two-player game에 해당한다.  
임의의 G와 D함수 공간에서 G는 학습데이터분포를 만들어내고 D는 1/2이 되도록 하는 유일해는 존재한다.
G와 D가 MLP형태로 정의되어진 경우 전체 시스템은 BP로 학습된다.  
샘플 학습이나 생성에서 Markov chain 혹은 unrolled approximate inference network는 필요가 없다.  
실험을 통해 생성된 샘플들에 대한 양적이고 질적인 평가를 통하여 본 framework에 대한 잠재성을 제시한다.  
(개념 자체로는 이해하기에 그다지 어렵지 않지만 이러한 컨셉을 고안했다는 사실이 정말 대단하다..)

### 1. Introduction

자연 이미지, 음성이 포함 된 오디오 파형 및 자연어 말뭉치의 심벌등과 같은 AI 활용 사례에서 만나게 되는 데이터의 종류에 대해 확률 분포를 표현하는 풍부하고도 구조적인 모델을 확실히 찾아 낼 수 있다.  
지금까지, DL의 대부분의 놀라운 성공은 고차원의 sensor입력을 class 답으로 mapping해주는 Discriminative 모델에 해당한다.[14, 22]  
이러한 놀라운 성공은 주로 특히 잘 작동하는 gradient를 갖는 piecewice linear unit을 사용하여 BP나 dropout알고리즘을 기초로하여 왔다.  
깊은 층의 Generative 계열 모델은 생성적 개념에서 1)MLE와 관련된 전략에서 발생하는 수많은 까다로운 확률 계산을 근사하는 어려움과 2) piecewice linear unit의 이점을 활용하는데에 어려움이 있어 영향력이 크지 않았다.  
제안하는 적대 신경망 framework에서 G는 적대적인것에 대하여 맞선다. : discriminative model(모델분포에서 온 샘플인지 데이터 분포에서 온 샘플인지를 결정하는것을 학습하는)  
G는  가짜 화폐를 생산하고 탐지없이 사용하려고하는 위조자 팀과 유사하다고 생각할 수 있으며, D는 위조 화폐를 탐지하려는 경찰과 유사하다.  
이 게임의 경쟁은 가짜와 진짜가 구별 될 수 없을 때까지 G와 D를 각각 만든다.  
본 framework는 다양한 종류의 모델이나 최적화알고리즘에 대한 특정 학습알고리즘을 만들어낼 수 있다. 본 논문에서 우리는 MLP로 이루어진 G와 D에 대해 G에 임의의 noise를 넘겨 샘플을 생성하는 특별 케이스를 본다. 우리는 이러한 특별한 케이스를 적대적신경망이라고 한다. 이 경우에 우리는 굉장히 성공적인 BP와 dropout만으로 학습할 수 있으며 G의 샘플은 forward propagation만을 사용한다.  
여기서 근사추론이나 Markov chain은 필요가 없다.

### 2. Related Work

latent variable이 있는 방향성 그래픽 모델의 대안은 RBM, DBM 및 다양한 변형과 같은 latent variable이 존재하는 무 방향 그래픽 모델입니다. 이러한 모델 내의 상호 작용은 확률 변수의 모든 상태에 대한 전역 합계 / 통합에 의해 정규화 된 정규화되지 않은 잠재적 함수의 곱으로 표시됩니다. 이 양 (partition function)과 그 기울기는 MCMC를 이용해 추정 할 수 있지만 가장 사소한 경우를 제외하고 모두 다루기 어렵습니다. 믹싱은 MCMC에 의존하는 학습 알고리즘에 중요한 문제를 제기합니다. DBN (딥 신념 네트워크)은 단일 무 방향 레이어와 여러 방향 레이어를 포함하는 하이브리드 모델입니다. 빠르고 근사한 계층 별 학습 기준이 존재하지만 DBN은 무 방향 및 방향성 모델과 관련된 계산상의 어려움을 겪습니다. 점수 일치 및 NCE (noise-contrastive estimation)와 같이 로그 가능도를 근사하거나 제한하지 않는 대체 기준도 제안되었습니다. 이 두 가지 모두 학습 된 확률 밀도를 정규화 상수까지 분석적으로 지정해야합니다. 여러 계층의 잠재 변수 (예 : DBN 및 DBM)가있는 많은 흥미로운 생성 모델에서 다루기 쉬운 비정규 화 확률 밀도를 도출하는 것도 불가능합니다. 노이즈 제거 자동 인코더 및 축약 적 자동 인코더와 같은 일부 모델에는 RBM에 적용된 점수 일치와 매우 유사한 학습 규칙이 있습니다. NCE에서는이 작업에서와 같이 생성 모델에 맞추기 위해 차별적 훈련 기준이 사용됩니다. 그러나 별도의 차별 모델을 맞추는 대신 생성 모델 자체를 사용하여 생성 된 데이터를 고정 된 노이즈 분포 샘플에서 구별합니다. NCE는 고정 된 잡음 분포를 사용하기 때문에 모델이 관찰 된 변수의 작은 하위 집합에 대해 거의 정확한 분포를 학습 한 후에는 학습 속도가 크게 느려집니다. 마지막으로, 일부 기술은 확률 분포를 명시 적으로 정의하는 것이 아니라 원하는 분포에서 샘플을 추출하도록 생성 기계를 훈련시킵니다. 이 접근 방식은 이러한 기계가 역 전파에 의해 훈련되도록 설계 될 수 있다는 장점이 있습니다. 이 분야에서 최근의 저명한 작업에는 일반화 된 잡음 제거 자동 인코더를 확장하는 GSN (generative stochastic network) 프레임 워크가 포함됩니다. 둘 다 매개 변수화 된 Markov 체인을 정의하는 것으로 볼 수 있습니다. 즉, 하나의 단계를 수행하는 기계의 매개 변수를 학습합니다. generative markov chain. GSN에 비해 적대적 네트워크 프레임 워크는 샘플링을 위해 Markov 체인이 필요하지 않습니다. 적대적 네트는 생성 중에 피드백 루프가 필요하지 않기 때문에 조각 별 선형 단위를 더 잘 활용할 수 있으므로 역 전파 성능이 향상되지만 피드백 루프에서 사용할 때 무제한 활성화 문제가 발생합니다. BP를 통해 generative 모델을 훈련시키는 최근의 예에는 auto-encoding variational Bayes 및 stochastic BP 최근 작업이 포함됩니다.

The interactions within such models are represented as the product of unnormalized potential functions, normalized by a global summation/integration over all states of the random variables. This quantity (the partition function) and its gradient are intractable for all but the most trivial instances, although they can be estimated by Markov chain Monte Carlo (MCMC) methods. Mixing poses a significant problem for learning algorithms that rely on MCMC [3, 5].  

DBN은 단일의 무방향의 레이어와 여러개의 방향성의 레이어를 포함하는 하이브리드 모델이다.   

레이어방향으로의 빠른 근사 방법론은 존재하지만, DBN은 방향이 undirected & directed 모델 모두에서 계산상 어려움을 겪는다.

score matching과 NCE와 같은 log우도를 제한하거나 근사하지 않는 대체의 기준도 정의되었다. 이 방법론 둘다 학습된 확률밀도가 normalization 상수까지 분석적으로 명시되는 것을 요구한다. 
DBN이나 DBM같은 여러개의 레이어를 가지는 가지는 많은 흥미로운 생성모델에서 다루기 쉬운 unnormailzed 확률밀도를 유도하는것마저 가능치 않다는것도 유의하자.
denoising AE와 contractive AE와 같은 일부 모델들은 RBM에 적용되는 score match과 유사한 학습 규칙을 가진다.
이번 연구처럼 NCE에서 분류학습 기준은 생성모델을 맞추기 위해 적용된다. 분리된 분류모델을 fitting하는것 대신에 생성모델은 생성된 데이터를 표본으로부터 고정노이즈분포를 구별하는데 사용된다. NCE는 고정잡음분포를 사용하기때문에 관측변수의 작은 부분공간에 대한 올바른 분포를 근사적으로 학습을 한 이후에 학습이 느려진다. 결국 몇몇 기법들은 확률분포를 명시적으로 정의하는것을 포함하지 않는다. 오히려 이상적인 분포로부터 샘플을 이끌어내기 위해 생성모델을 학습한다. 이 접근법은 BP로 학습하도록 설계할수 있다는 장점을 가진다.
이 영역에서 두드러진 최근의 연구는  Generalized denoising autoencoder 를 확장하는 생성 확률 네트워크 프레임워크[5]를 포함한다. 두 가지 모두 매개 변수화된 Markov chain을 정의하는 것으로 볼 수 있다. 즉, 생성 MC의 한 단계를 수행하는 기계의 매개 변수를 학습한다.
GSN과 비교하여 적대적신경망은 샘플링을 위해 Markov chain이 필요 없다. 생성과정 동안에 적대적신경망은 feedback loop를 필요로하지 않기때문에, 이 모델은 (BP의 성능을 향상시키는지만 feedback loop에서 사용될 때 제한없는 activation을 가지는 문제가 존재하는) picewise lienar uint을 더 잘 이용할 수 있다.  
BP를 통해 생성모델을 학습시키는 더 최근의 예로는 AE 변형 베이와 stochastic BP에 대한 최근 연구가 포함된다.


##### 학습이 필요한 이론이나 모델
Directed graphic model  : graph model 은 rbm에서 자주 등장하므로 rbm을 보자
Denoising AE, contractive AE  
NCE(noise-contrastive estimation)  
RBM > DBN  
Generative stochastic network  
Noise distribution  
GSN(generative stochastic network)  
partition function  
MCMC  
