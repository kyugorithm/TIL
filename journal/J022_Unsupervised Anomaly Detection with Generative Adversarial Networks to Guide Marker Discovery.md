# Unsupervised Anomaly Detection with Generative Adversarial Networks to Guide Marker Discovery

## Abstract
질병 진행 및 치료 모니터링과 관련된 이미징 마커를 캡처하는 모델을 얻는 것은 어렵습니다.  
모델은 일반적으로 감지 자동화를 목표로 하는 **알려진 마커의 주석이 있는 예제**와 함께 대량의 데이터를 기반으로 합니다.  
**높은 주석 노력과 알려진 마커의 어휘에 대한 제한은 이러한 접근 방식의 활용성을 제한**합니다.  
여기에서 우리는 이미징 데이터의 이상을 마커 후보로 식별하기 위해 **비지도 학습**을 수행합니다.  
우리는 이미지 공간에서 **잠재 공간으로의 매핑을 기반으로 하는 새로운 anomaly score** 체계를 수반하는  
정상적인 **해부학적 다양성의 매니폴드**를 학습하기 위한 심층 컨볼루션 생성 적대 네트워크인 AnoGAN을 제안합니다.  
새 데이터에 적용되는 모델은 이상 항목에 레이블을 지정하고 학습된 분포에 **적합함을 나타내는 이미지 패치에 점수를 매깁니다**.  
망막의 광간섭 단층촬영 이미지에 대한 결과는 접근 방식이 망막액 또는 과반사 초점을 포함하는 이미지와 같은 비정상적인 이미지를  
올바르게 식별한다는 것을 보여줍니다.

## Contribution
Section 2.1에서 설명한 정상적인 모양의 생성 모델(그림 1의 파란색 블록 참조)과  
새로운 데이터(섹션 2.3) 평가를 가능하게 하는 Section 2.2에서 설명한 coupled mapping schema의 적대적 훈련을 제안합니다.  
이상 이미지를 식별하고 이미징 데이터 내에서 이상 영역을 분할합니다(그림 1의 빨간색 블록 참조).  
Spectral-domain OC 스캔에서 추출한 레이블이 지정된 테스트 데이터에 대한 실험은  
이 접근 방식이 알고있는 anomaly를 높은 정확도로 식별하는 동시에 volxel-level 주석을 사용할 수 없는 다른 이상을 감지한다는 것을 보여줍니다.  
우리가 아는 한, 이것은 GAN이 이상 또는 참신 감지에 사용되는 첫 번째 작업입니다.  
또한 사전 이미지 문제를 해결할 수 있는 새로운 매핑 접근 방식을 제안합니다.  
![image](https://user-images.githubusercontent.com/40943064/130891914-e8bbd080-6785-4945-b318-0e7bcd2a626d.png)

## 2. Generative Adversarial Representation Learning to Identify Anomalies
이상을 식별하기 위해 GAN을 기반으로 하는 정상적인 해부학적 변동성을 나타내는 모델을 학습합니다.  
이 방법은 생성 모델과 생성된 데이터와 실제 데이터를 동시에 구별하는 판별자를 훈련합니다(그림 2(a) 참조).  
단일 비용 함수 최적화 대신 비용의 Nash 평형을 목표로 하여 생성 모델의 대표성 및 특이성을 높이는 동시에 생성된 데이터에서  
실제 데이터를 분류하고 해당 기능 매핑을 개선하는 데 더 정확해집니다.  
다음에서는 이 모델을 구축하는 방법(섹션 2.1)과 훈련 데이터에 없는 모양을 식별하는 데 사용하는 방법(Section 2.2 및 2.3)을 설명합니다.  
![image](https://user-images.githubusercontent.com/40943064/130891864-d7e53a0b-5d32-4119-95fd-599ca5ee76af.png)

### 2.1. Unsupervised Manifold Learning of Normal Anatomical Variability

### 2.2. Mapping new Images to the Latent Space 

### 2.3. Detection of Anomalies


## 3. Experiments
