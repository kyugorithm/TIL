## Abstract
StyleGAN은 data-driven unconditional 생성이미지 모델링에 있어 SOTA 성능을 만든다.
본 논문은 몇 가지 고유한 아티팩트를 노출 및 분석하고 이를 해결하기 위해 **모델 아키텍처**와 **학습방법** 모두를 변경할 것을 제안한다.  
특히, 생성자 normalization을 재설계하고, PG를 재확인하고, latent->image 매핑에 있어 훌륭한 조건형성을 보장하도록 G를 정규화한다.  
이미지 품질을 향상시키고, PL 정규화는 G의 역이 훨씬 쉽게 되는 추가 이점을 만든다.  
따라서 생성된 이미지를 특정 네트워크에 안정적으로 속성을 지정할 수 있다.
또한 G가 output resolution을 얼마나 잘 활용하는지를 시각화하고 capacity 문제를 파악하여 추가 품질 개선을 위해 더 큰 모델을 교육하도록 동기를 부여한다.  
전반적으로, 개선된 모델은 기존 분포 품질 메트릭과 perceived image quality 측면에서 unconditional image modeling에서 SOTA를 재정의한다.
