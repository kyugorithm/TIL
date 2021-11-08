# Time-series Generative Adversarial Networks

## Abstract
시계열에 대한 좋은 generative model은 seq.가 시간에 따른 변수 간 원래 관계를 유지한다는 점에서 **temporal dynamics**를 보존해야 한다.  
GAN을 sequential setting으로 가져오는 기존 방법은 시계열 데이터에 고유한 시간적 상관 관계를 적절하게 고려하지 않는다.  
동시에 network dynamics를 보다 세밀하게 제어할 수 있는 seq. 예측을 위한 supervised 모델은 본질적으로 deterministic이다.  
**비지도학습 유연성**과 **지도학습의 제어**를 결합하여 시계열 데이터 생성 프레임워크를 새롭게 제안한다.  
지도 및 적대적 목표 모두와 함께 최적화 학습된 임베딩 공간을 통해 네트워크가 샘플링 중에 학습 데이터의 daynamics를 준수하도록 한다.  
경험적으로 real/fake 시계열 데이터 세트를 사용하여 실제 샘플을 생성하는 방법의 능력을 평가한다.  
질적 및 양적으로, 제안 프레임워크가 **유사성** 및 **예측 능력 측정**과 관련하여 SOTA보다 일관되고 우수함을 발견했다.  
Summary : 지도/비지도 방식의 장점을 각각 적절히 활용하고 데이터의 temporal dynamics를 유지하여 더 나은 샘플을 생성하도록 가이드  

## Itroduction
시계열 데이터에 대한 좋은 generative model은 무엇인가?  
시계열 세팅은 generative modeling에 고유한 문제를 제기한다. 모델은 각 시점 내의 feature 분포를 캡처하는 작업을 수행할 뿐만 아니라  
시간에 따라 해당 변수의 잠재적인 복잡한 dynamics를 캡처해야 한다.  
특히, 다변량 sequential 데이터 x1:T = (x1, ..., xT ) 모델링 시 시간적 transition의 조건부 분포 p(xt|x1:t−1)도 정확하게 캡처하고자 한다.  
Seq. 예측을 위한 Autoregressive 모델의 temporal dynamics를 개선하는 데 많은 작업이 집중되었다.  
주로 multi-step 샘플링 동안 오류를 복잡하게 만드는 문제를 해결하고  
테스트 시간 조건을 보다 정확하게 반영하기 위해 다양한 훈련 시간 수정을 도입한다.  
Autoregressive 모델은 seq. 분포를 조건부 Q t p(xt|x1:t−1)의 곱으로 명시적으로 분해한다.  
그러나 이 접근 방식은 예측의 맥락에서 유용하지만 근본적으로 deterministic하며 외부 조건 없이 새로운 seq.를  
무작위로 샘플링할 수 있다는 점에서 진정으로 생성적이 아니다.  
반면, G와 D의 역할에 대한 recurrent networks를 주로 인스턴스화하여 GAN 프레임워크를 seq. 데이터에 적용하는 데 작업이 집중되었다.  
직관적이지만, 적대적 목적은 autoregressive prior를 활용하지 않고 직접 p(x1:T)를 모델링하려고 한다.  
중요하게도, 벡터 seq.에 대한 standard GAN 손실을 단순히 합산하는 것만으로는 네트워크의 dynamics가 학습 데이터에 존재하는  
단계적 종속성을 효율적으로 캡처하는지 확인하기에 충분하지 않을 수 있다.  
이 논문에서 temporal dynamics를 보존하도록 **명시적**으로 학습된 generative model을 발생시키는  
두 연구 스레드를 함께 묶는 새로운 메커니즘을 제안한다.  
  
다양한 도메인에서 현실적인 시계열 데이터를 생성하기 위한 자연스러운 프레임워크인 TimeGAN를 소개한니다.  
  
첫째, real seq.와 fake seq. 모두에 대한 **비지도** 적대적 손실 외에도 원본 데이터를 감독으로 사용하여 단계적 감독 손실을 도입하여  
모델이 **데이터의 단계적 조건부 분포를 캡처**하도록 명시적으로 권장한다.  
단순히 실제/합성 여부를 분류하는 것 보다 학습 데이터에 더 많은 정보가 있다는 사실을 이용한다.  
이를통해 실제 seq.의 transition dynamics에서 명시적으로 배울 수 있다.  
  
둘째, feature와 latent 표현 간의 가역적 매핑을 제공하기 위해 임베딩 네트워크를 도입하여 적대적 학습 공간의 고차원성을 줄인다.  
이것은 심지어 복잡한 시스템의 시간적 역학이 종종 더 적고 더 낮은 차원의 변동 요인에 의해 구동 된다는 사실을 이용한다.  
중요하게, 감독된 손실은 임베딩 네트워크와 생성기 네트워크를 공동으로 훈련함으로써 최소화되어 latent space가  
parameter 효율성을 촉진하는 역할을 할 뿐만 아니라 시간적 관계를 학습할 때 G를 용이하게 하도록 특별히 조절된다.  
  
마지막으로 static 및 time-series 데이터가 동시에 생성될 수 있는 혼합 데이터 설정을 처리하도록 프레임워크를 일반화한다.  
우리의 접근 방식은 비지도 GAN 프레임워크의 유연성과 autoregressive 모델의 지도 학습이 제공하는 제어를 결합한 첫 번째 방법이다.  
여러 실제 및 합성 데이터 세트에 대한 일련의 실험에서 이점을 보여준다.  
정성적으로 생성된 분포가 원래 분포와 얼마나 유사 한지를 시각화하기 위해 t-SNE [7] 및 PCA [8] 분석을 수행한다.  
정량적으로 우리는 사후 D가 실제 seq.와 생성 seq.를 얼마나 잘 구별할 수 있는지 조사한다.  
또한 "TSTR(Train on Synthetic, Test on Real)" 프레임워크[5, 9]를 seq. 예측 작업에 적용하여  
생성된 데이터가 원본의 예측 특성을 얼마나 잘 보존하는지 평가한다.  
TimeGAN이 현실적인 시계열을 생성하는 데 있어 최첨단 벤치마크보다 일관되고 상당한 개선을 달성한다는 것을 발견했다.

## 2 Related Work
## 3 Problem Formulation
두개의 요소를 구성하는 일반적인 데이터 세팅을 고려해보자.  
Static features : 시간에 독립적인 정보  
Temporal features : 시간적 정보  
_**S**_ 를 정적 feature의 벡터공간으로 두고 _**X**_ 를 시계열 feature로 정의한다. 
s와 x로 명시되는 특정값으로 명시될 수 있는 랜덤 백터로 정의 **S**∈ _S_, **X**∈ _X_ 한다.  
joint distribution 를 가진 (**S**, **X**1:T)의 튜플을 고려한다.  
길이 T 벡터 또한 랜덤변수이다. 학습데이터에서 개별 샘플이 n ∈ {1,...,N} 이 되도록 하여 
학습 데이터를 D = {(sn, xn,1:Tn)}N/n=1 으로 명시한다. (n의 명시는 필요하지만 생략한다.)  

학습 데이터 D를 사용하여 p(S, X1:T)를 가장 잘 근사하는 확률밀도 phat(S, X1:T)을 배우는 것이다.  
이는 다음 3개에 의존하는 high-level 목적함수이다 : length, dimensionality, data distribution  
그리고 표준 GAN framework에서 학습하는 것은 어렵다.  
그러므로 우리는 ![image](https://user-images.githubusercontent.com/40943064/140686016-f0dbfa53-6736-4291-ae1e-8dae13480d07.png)에 대한 autoregressive decomposition를 이용한다.  
