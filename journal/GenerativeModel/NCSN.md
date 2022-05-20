## Abstract
새로운 생성모델 제안 : Score matching으로 추정된 데이터 분포의 gradient를 사용하여 Langevin dynamics를 통해 생성된 샘플을 사용  
Gradient가 ill-defined 일 수 있고 데이터가 저차원의 manifold에 존재하는 경우 추정하기 어려울 수 있기 때문에 우리는 이 문제를 위해 데이터를 다양한 level의 Gaussian noise로 perturb한다.  
그리고 함께 상응하는 score(예를들면 모든 noise level에 대한 perturbed 데이터의 gradient에 대한 vector field)를 추정한다.  
샘플링을 위해, 우리는 (데이터 메니폴드에 더 가까워 지도록 하는 sampling process로써 noise level을 점진적으로 줄여나가는것에 해당하는 gradient를 사용하는) annealed Langevin dynamics를 제안한다.  
우리 프레임워크는 유연한 모델 아키텍쳐를 하게 하고 학습동안의 샘플링이 필요하지 않고 adversarial 방식에 대한 사용도 필요없다.  
또한 (principled model comparisons에 사용될 수 있는) 학습 목적함수를 제공한다.  

## Introduction

## 4. Noise Conditional Score Networks: learning and inference
Random Gaussian noise로 데이터를 perturb 시킴으로써 데이터 분포가 score-based 생성모델링에 더 적합함을 관찰한다.  
1) Gaussian noise 분포의 support는 전체 공간이기 때문에 perturbed 데이터는 저차원 매니폴드에 국한되지 않고, 매니폴드 가설의 어려움을 없애고 score estimation을 잘 정의한다.  
2) 큰 Gaussian noise는 원본 데이터 분포에서의 낮은 densityt 영역을 채우는 효과가 있다. 즉 score matching은 score estimation을 개선하기 위해 더 많은 학습 신호를 얻을 수 있다.  

여러가지 noise level을 사용하여 실제 데이터 분포로 수렴하는 일련의 noise perturbed distribution을 얻을 수 있다.  
Simulated annealing] 및 annealed importance sampling의 정신으로 이러한 중간 분포를 활용하여 multimodal distribution에서 Langevin 역학의 mixing rate를 개선할 수 있다.  

### 4.1 Noise Conditional Score Networks
σ는 σ1부터 σL로 진행되면서 아래와같이 점점 작아지도록 positive geometry sequence가 되도록 설정한다.  
<img src = 'https://user-images.githubusercontent.com/40943064/169560297-86a9c62c-12bc-497c-b2de-21ca9f145142.png' width = 300>  
아래는 perturbed data distribution으로 정의된다.  
<img src = 'https://user-images.githubusercontent.com/40943064/169560092-58de5e76-80ba-4a62-bc64-b8476a8d82d8.png' width = 300>  
Low data density region으로 인해 발생하는 부정확한 score estimation 문제를 해결 하기 위해 σ1을 충분히 크게 설정하고 maximum probability 영역에서는 원 데이터에 대한 영향을 줄이기 위해 σL를 충분히 작게 설정한다.  
이러한 조건을 사용하는 score estimation model인 s는 다음과 같이 입력 x와 sigma condition으로 정의된다.  
<img src = 'https://user-images.githubusercontent.com/40943064/169561205-a378c3ab-0b85-451a-8ce0-6d379d04925a.png' width = 300>
그리고 우리는 모델 sΘ(x, σ)를 Noise Conditional Score Network (NCSN)라고 부르도록 한다.  

Liklihood 기반 모델 그리고 GAN과 유사하게, 고품질의 샘플을 생성하는데 있어 모델 구조 설계는 역할을 한다.  
본 작업은 이미지생성 task에 유용한 architecture에 집중하고 다른 application 영역에 대해서는 future work으로 두기로 한다.  
본 네트워크 sΘ(x, σ)의 입력과 출력은 동일한 dimension을 가지므로 semantic segmentation 분야와 같은 모델 구조로부터 많은 참고를 한다.  
따라서 semantic segmentation에서 매우 효과적임이 증명된 dilated/atrous conv.를 가지는 U-net 구조를 사용한다.  
추가로 일부 generation task에서의 영감을 받아 **instance norm**을 사용한다.  
또한 σi에 대한 conditioning을 부여하기 위해 conditional instance normalization의 수정버전을 사용한다.  

![image](https://user-images.githubusercontent.com/40943064/169564858-e4c90d7a-6d22-4347-a279-cb03065951ad.png)
