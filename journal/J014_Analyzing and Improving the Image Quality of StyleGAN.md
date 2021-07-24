## Abstract
StyleGAN은 data-driven unconditional 생성이미지 모델링에 있어 SOTA 성능을 만든다.
본 논문은 몇 가지 고유한 아티팩트를 노출 및 분석하고 이를 해결하기 위해 **모델 아키텍처**와 **학습방법** 모두를 변경할 것을 제안한다.  
특히, 생성자 normalization을 재설계하고, PG를 재확인하고, latent->image 매핑에 있어 훌륭한 조건형성을 보장하도록 G를 정규화한다.  
이미지 품질을 향상시키고, PL 정규화는 G의 역이 훨씬 쉽게 되는 추가 이점을 만든다.  
따라서 생성된 이미지를 특정 네트워크에 안정적으로 속성을 지정할 수 있다.
또한 G가 output resolution을 얼마나 잘 활용하는지를 시각화하고 capacity 문제를 파악하여 추가 품질 개선을 위해 더 큰 모델을 교육하도록 동기를 부여한다.  
전반적으로, 개선된 모델은 기존 분포 품질 메트릭과 perceived image quality 측면에서 unconditional image modeling에서 SOTA를 재정의한다.

## 1. Introduction

GAN과같은 생성모델에 의해 생성된 이미지 해상도와 품질은 급격히 향상되고 있고 최근 StyleGAN은 관련분야 SOTA를 찍었다.  
본 논문의 목표는 styleGAN이 가지는 고유 아티팩트를 고치고 품질을 향상하는 것이다.  
StyleGAN의 고유한 특성은 다음과 같다.  
z를 입력하는 대신 z를 mapping network인 f에 통과하여 중간 latent code인 w로 변환하는 것이다.  
그러면 합성네트워크 g에 대하여 AdaIN을 통해 레이어 각각에 대한 제어를 할 수 있는 아핀변환은 **style** 생성한다.  
추가로, 랜덤노이즈를 합성네트워크에 공급함으로써 통계적 다양성을 촉진한다.  
해당 논문의 결과에서 확인할 수 있듯이 W는 Z보다 disentangle한 결과를 만들어냄을 알 수 있었다.  
본 논문에서는 합성 네트워크의 관점에서 관련 잠재 공간인 W에만 모든 분석을 집중한다.  
