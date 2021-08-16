# Attribute Manipulation Generative Adversarial Networks for Fashion Images

## Abstract
최근 GAN의 발전으로 단일 생성 네트워크를 사용하여 다중 도메인 이미지 대 이미지 번역을 수행할 수 있다.  
Ganimation 및 SaGAN과 같은 최근 방법은 attention을 사용하여 attribute 관련 영역에 대한 번역을 수행할 수 있지만  
attention mask 학습은 주로 분류 손실에 의존하기 때문에 attribute 수가 증가하면 제대로 수행되지 않는다.  
이 문제 및 기타 제한 사항을 해결하기 위해 패션 이미지에 AMGAN을 도입한다.  
AMGAN의 생성기 네트워크는 attention mechanism을 강화하기 위해 CAM을 사용하지만 attribute similiarity를 기반으로 참조(대상)  
이미지를 할당하여 perceptual loss도 이용한다. AMGAN은 비현실적인 번역을 감지하기 위해 attribute 관련 영역에 중점을 둔  
추가 discriminator를 통합한다.  
또한 AMGAN은 소매 또는 몸통 영역과 같은 특정 영역에서 attribute 조작을 수행하도록 제어할 수 있다.  
실험에 따르면 AMGAN은 기존 평가 metric과 이미지 검색을 기반으로 하는 대안을 사용하는 SOTA 보다 성능이 뛰어나다.
