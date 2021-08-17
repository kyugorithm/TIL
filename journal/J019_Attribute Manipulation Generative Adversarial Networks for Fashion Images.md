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

## 1. Introduction
Attribute manipulation은 이미지를 목표 attribete 기반하에 변환/조정하는 것이다.  
패션상품에서 관심있는 attribute는 소매길이, 색상, 패턴과 같은 시각적 품질과 관련되고 속성값은 긴소매, 빨간색 및 일반 패턴과 같은 특정 레이블에 해당한다.  
이미지의 속성을 조작할 수 있다는 것은 사용자가 일부 속성에 만족하지 못하는 등 다양한 상황에서 특히 유용하다.  
최근 이 작업은 속성 조작을 수행한 후 데이터 세트에서 대상 이미지를 검색하는 것과 관련된 이미지 검색 관점에서 연구되었다.  
그러나 이미지 검색 접근 방식은 데이터 세트 크기와 증가하는 속성 수로 인해 제한된다.  
GAN이 도입된 이후로 이미지 생성 작업은 많은 관심을 받았다. 많은 컴퓨터 비전 작업과 함께 GAN은 이미지 대 이미지 번역 문제에 적용될 수 있습니다.  
StarGAN은 단일 생성 네트워크로 다중 도메인 이미지-이미지 변환을 수행할 수 있다. Ganimation, SaGAN은 생성 네트워크에 attention mechanism을 통합하는 여러 접근 방식이 제안됐다.  
Attention mechanism을 갖는 것은 속성 관련 영역에서 속성 조작을 수행해야 하는 반면 다른 영역은 동일하게 유지해야 할 때 특히 유용하다.  
그러나 속성의 수가 증가함에 따라 이러한 attention based 방법은 주로 분류 손실을 통해 학습된 attention 영역이 불안정해진다.  
또한, D는 attention 메커니즘의 이점을 얻을 수 있으며 G가 보다 현실적인 속성 조작을 수행하도록 한다.  
본 논문에서는 사용자가 속성 조작을 수행할 수 있도록 하는 패션 이미지에 대한 다중 도메인 I2I translation에 초점을 맞춘 속성 조작 GAN(AMGAN)를 제안한다.  
현재 I2I 변환 네트워크는 대부분 얼굴 이미지 용이지만 AMGAN은 패션 이미지와 같이 덜 딱딱한 개체에 대해 이를 달성한다.  
그림 1은 Deepfashion, Shopping100k 데이터 세트에 대한 속성 조작의 몇 가지 예를 보여준다.  
제안 방법은 AMGAN은 다른 속성을 유지하면서 대상 속성의 변경 사항을 기반으로 입력 이미지를 새 이미지로 변환하는 기능이 있다.  
제안 방법은 속성 위치에 대한 정보를 활용하지 않고 속성 조작을 위한 attention mechanism을 통합한다.  
**속성 조작에서 목표는 관심 속성이 있는 영역을 찾아 새로운 영역으로 변환할 수 있도록 하는 것이다**.  
따라서 G가 조작할 속성을 기반으로 영역을 올바르게 지역화하는 것이 중요하다. CAM을 사용하여 속성의 식별 영역을 올바르게 지역화할 수 있다.  
CAM을 attention loss로 사용함으로써 AMGAN의 G는 attention 마스크를 올바르게 생성할 수 있으므로 결과적으로 속성 조작 능력이 향상된다.  
다른 연구가 전체 이미지에 대해 단일 판별자를 사용하는 반면, AMGAN은 속성 관련 영역에 초점을 맞춘 추가 판별자 네트워크를 사용하여  
이미지 번역 성능을 개선하기 위해 비현실적인 속성 조작을 감지한다. unpaired i2i translation의 경우 입력 이미지 및 속성 조작에 따른  
참조(대상) 이미지가 없으므로 지각 손실을 사용할 수 없다. 속성 유사성을 기반으로 참조 이미지를 할당하여 이 문제를 해결한다.  
결과적으로 AMGAN은 CAM을 추출하는 동일한 CNN의 기능을 기반으로 하는 perceptual loss 함수의 이점을 얻는다.  
perceptual loss로 AMGAN은 속성 조작을 일치시키는 능력이 향상되는 동안 보다 사실적인 이미지를 생성할 수 있다.  
기존의 i2i translation 외에도 AMGAN은 attention mask를 사용하여 특정 영역에 대한 속성 조작을 수행하도록 조정할 수 있다.  
예를 들어, AMGAN은 주의 마스크를 "소매 없는" 속성 조작용 마스크로 교체하여 소매 영역에서 "빨간색" 속성 조작을 수행하도록 조정할 수 있다.  
이 기능은 지역별 속성 조작을 자동화하는 데 유용하다.  
AMGAN의 주요 기여는 아래와 같다.  

• CAM으로 G의 attention mechanism을 강화하여 attribute similarity를 기반으로 하는 perceptual loss 가능  
• 속성 관련 영역에 중점을 둔 추가 D를 통합  
• 특정 영역 속성 조작 활성화  
• 두 가지 패션 데이터 세트에 대한 자세한 실험을 통해 AMGAN이 SOTA임을 증명(특성 조작의 성공 여부를 테스트하기 위해 이미지 검색을 기반으로 하는 새로운 방법 소개)

## 2. Related Work
GAN, cGAN : 생략
I2I translation : pix2pix : paried -> cycleGAN : unpaired 1-domain -> StarGAN : Multi-domain -> Attention based architecture  
(Attention based 방법 단점 :  classification loss 의존)

## 3. AMGAN
multi-domain i2i 변환(속성 조작)을 수행할 수 있는 AMGAN에 대해 설명한다. 다음으로 AMGAN을 조정하여 지역별 속성 조작을 수행하는 방법을 이해한다.  
  
**Problem Definition.**  
AMGAN 아키텍처는 그림 2와 같이 G(Enc.-Dec. 구조:속성 조작 m을 적용하여 입력 이미지 xI를 출력 이미지로 변환 : ![image](https://user-images.githubusercontent.com/40943064/129750323-8f8fd92d-8d99-4fb9-97f6-8df4a89f2ad7.png)))와 DI, DC로 구성하며 가능한 모든 속성 조작 작업은 m = {m1, ...mN , r}로 인코딩될 수 있다.   
N은 속성 값의 수(예: 긴 소매, 빨간색 등)이고 r은 조작 중인 속성(소매, 색상 등)을 나타낸다. G 각 학습 반복에 대한 특정 속성에 초점을 맞추도록 한다.  
r과 m은 모두 원-핫 인코딩으로 표현된다.

3.1. Network Construction
3.2. Discriminators
3.3. Generator
