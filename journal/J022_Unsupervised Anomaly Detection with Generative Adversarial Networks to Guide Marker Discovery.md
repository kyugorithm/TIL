# Unsupervised Anomaly Detection with Generative Adversarial Networks to Guide Marker Discovery

## Abstract
질병 진행 및 치료 모니터링과 관련된 label을 캡처하는 모델을 얻는 것은 어렵다.  
모델은 일반적으로 감지 자동화를 목표로 하는 **알려진 레이블이 있는 예제**와 함께 대량의 데이터를 기반으로 한다.  
**높은 anotation 노력과 label 필요성은 이러한 방식의 활용성을 제한**한다.  
여기에서 우리는 이미지 데이터의 anomaly를 마커 후보로 식별하기 위해 **비지도 학습**을 수행한다.  
우리는 이미지 공간에서 **잠재 공간으로의 매핑을 기반으로 하는 새로운 anomaly score** 체계를 수반하는  
정상적인 **해부학적 다양성의 manifold**를 학습하기 위한 심층 컨볼루션 생성 적대 네트워크인 AnoGAN을 제안한다.  
새 데이터에 적용되는 모델은 이상 항목에 레이블을 지정하고 학습된 분포에 **적합함을 나타내는 이미지 패치에 점수를 매긴다**.  
망막의 광간섭 단층촬영 이미지에 대한 결과는 접근 방식이 망막액 또는 과반사 초점을 포함하는 이미지와 같은 비정상적인 이미지를  
올바르게 식별한다는 것을 보여준다.

## Contribution
Section 2.1에서 설명한 정상적인 모양의 생성 모델(그림 1의 파란색 블록 참조)과  
새로운 데이터(섹션 2.3) 평가를 가능하게 하는 Section 2.2에서 설명한 coupled mapping schema의 적대적 훈련을 제안한다.  
이상 이미지를 식별하고 이미징 데이터 내에서 이상 영역을 분할한다(그림 1의 빨간색 블록 참조).  
Spectral-domain OC 스캔에서 추출한 레이블이 지정된 테스트 데이터에 대한 실험은  
anomaly를 높은 정확도로 식별하는 동시에 volxel-level 주석을 사용할 수 없는 다른 이상을 감지한다는 것을 보여준다.  
우리가 아는 한, 이것은 GAN이 anomaly detection에 사용되는 첫 번째 작업이다.  
또한 pre-image 문제를 해결할 수 있는 새로운 매핑 접근 방식을 제안한다.  
![image](https://user-images.githubusercontent.com/40943064/130891914-e8bbd080-6785-4945-b318-0e7bcd2a626d.png)  

## 2. Generative Adversarial Representation Learning to Identify Anomalies
이상을 식별하기 위해 GAN을 기반으로 하는 정상적인 해부학적 변동성을 나타내는 모델을 학습한다.  
이 방법은 생성 모델과 생성된 데이터와 실제 데이터를 동시에 구별하는 D를 훈련한다(그림 2(a) 참조).  
단일 비용 함수 최적화 대신 비용의 Nash 평형을 목표로 하여 생성 모델의 대표성 및 특이성을 높이는 동시에 생성된 데이터에서  
실제 데이터를 분류하고 해당 기능 매핑을 개선하는 데 더 정확해진다.  
다음에서는 이 모델을 구축하는 방법(섹션 2.1)과 훈련 데이터에 없는 모양을 식별하는 데 사용하는 방법(Section 2.2 및 2.3)을 설명한다.  
![image](https://user-images.githubusercontent.com/40943064/130891864-d7e53a0b-5d32-4119-95fd-599ca5ee76af.png)  

### 2.1. Unsupervised Manifold Learning of Normal Anatomical Variability
![image](https://user-images.githubusercontent.com/40943064/131071619-7830ddda-07b3-4daa-91d3-85217568afb0.png)  
GAN을 통해 해부학적 가변성을 인코딩한다. GAN은 G와 D의 적대 모듈로 구성된다.  
G는 z의 매핑 G(z), 잠재 공간 Z에서 샘플링된 균일하게 분포된 입력 노이즈의 1D 벡터를 통해 데이터 x에 대한 분포 pg를 학습한다.  
건강한 예제로 채워진 이미지 공간 **manifold X의 2D 이미지로 변환**한다. 이 설정에서 G의 아키텍처는 stride conv. stack을 활용하는  
conv. decoder와 동일한다.  
D는 2D 이미지를 단일 스칼라 값에 매핑하는 표준 CNN이다. 출력은 D에 대한 주어진 입력이 학습 데이터 X에서 샘플링된 실제 이미지 x이거나  
G에 의해 생성된 G(z)일 확률로 해석될 수 있다. D와 G는 다음을 통해 동시에 최적화된다.  
V(G;D)가 있는 two-player minmax game:  
![image](https://user-images.githubusercontent.com/40943064/131072145-4f82eb6b-ccea-4898-89aa-171e80c08e7a.png)  

### 2.2. Mapping new Images to the Latent Space 
적대적 훈련이 완료되면 G 잠재 공간 표현 z에서 실제(일반) 이미지 x로 매핑 G(z) = z → x를 학습했다.  
그러나 GAN은 inverse mapping µ(x) = x → z를 자동으로 생성하지는 않다.  
잠재 공간은 smooth translation을 가지므로, z에서 가까운 샘플은 시각적으로 유사한다.  
x가 주어지면 유사한 manifold X에 위치한 이미지 G(z)에 해당하는 잠재 공간에서 z를 찾는 것을 목표로 한다.  
x와 G(z)의 유사도는 쿼리 이미지가 G 학습에 사용된 데이터 분포 pg를 어느 정도 따랐는지에 따라 다르다.  
최적의 z를 찾기 위해 latent Z에서 무작위로 z1을 샘플링하고 학습된 G에 입력하여 생성된 이미지 G(z1)를 얻다.  
생성된 이미지 G(z1)를 기반으로 loss 를 정의한다.  
이 loss는 z1 업데이트에 대한 gradient를 제공하여 latent z2에서 업데이트된 위치를 생성한다.  
가장 유사한 이미지 G(zΓ)를 찾기 위해 잠재 공간 Z에서 z의 위치는 γ = 1, 2, . . . , Γ 역전파 단계  
의 방식에 따라 새로운 이미지를 잠재 공간에 매핑하기 위한 손실 함수를 정의한다.  
이 손실 함수는 residual loss와 discrimination 손실의 두 가지 구성 요소로 구성된다.  
residual loss는 G(zγ)와 쿼리 이미지 x 간의 시각적 유사성을 적용한다.  
discrimination loss는 G(zγ)가 학습된 manifold X에 놓이도록 강제한다.  
따라서 훈련된 GAN의 두 구성요소인 D와 G는 역전파를 통해 z의 계수를 조정하는 데 사용된다.  
다음에서는 손실 함수의 두 구성 요소에 대해 자세히 설명한다.  

**Residual Loss**  
이미지 공간에서 생성 이미지와 실제 이미지 간 시각적 불일치성을 나타내는 척도는 다음과 같다.
![image](https://user-images.githubusercontent.com/40943064/131074320-189f83fd-6f79-4183-b8b6-a4d765213828.png)  
완벽한 G와 완벽한 latent 공간 mapping, 이상적인 정상 query case의 가정 하에 이미지와 생성 이미지는 동일한다.  
이 경우에 residual loss는 0이 된다.
**Discrimination Loss**   
이미지 inpainting에  대해 Yeh는 생성 이미지를 입력으로 받는 D 출력을 discrimination loss에 대한 계산을 기반으로 한다.  
![image](https://user-images.githubusercontent.com/40943064/131074778-5b988617-963c-4c58-bf6f-b651ed1f26fd.png)  
**An improved discrimination loss based on feature matching**  
Yeh의 작업과 대조적으로. zγ가 D를 속이도록 업데이트되는 경우 대체 식별 손실 LD(zγ)를 정의한다.  
여기서 zγ는 G(zγ)를 학습된 정규 이미지 분포와 일치시키도록 업데이트된다. 이것은 최근에 제안된 특징 매칭 기법에서 영감을 받았다.  
feature matching은 D 응답에 대한 과도한 훈련으로 인한 GAN의 불안정성을 해결한다.  
feature matching 기법에서 G를 최적화하기 위한 목적 함수는 GAN 훈련을 개선하기 위해 적용된다.  
생성된 샘플에 대한 D의 출력을 최대화하여 G의 매개변수를 최적화하는 대신(식(2)), G는 훈련 데이터와 통계가 유사한 데이터,  
즉 중간 기능 표현이 실제 이미지와 유사한 데이터를 생성해야 한다.  
Salimans는 분류가 대상 작업일 때 feature matching이 특히 유용하다는 것을 발견했다.  
우리는 적대적 훈련 중에 레이블이 지정된 데이터를 사용하지 않기 때문에 클래스별 판별 기능을 학습하는 것이 아니라  
좋은 표현을 학습하는 것을 목표로 한다.  
따라서 우리는 적대적 훈련 동안 G의 훈련 목표를 조정하지 않고 대신 잠재 공간에 대한 매핑을 개선하기 위해 feature matching의 아이디어를 사용한다.  
discrimination loss를 계산하기 위해 D의 스칼라 출력을 사용하는 대신 D의 더 풍부한 중간 기능 표현을 사용하고  
discrimination loss를 다음과 같이 정의할 것을 제안한다.  
![image](https://user-images.githubusercontent.com/40943064/131075314-4d33cc14-15d7-47a8-8d14-d02e7b9aa90a.png)  
여기서 D의 중간 계층 f(·)의 출력은 입력 이미지의 통계를 지정하는 데 사용된다.  
이 새로운 손실 항에 기초하여 z 축의 adaptation은 G(zγ)가 정상 이미지의 학습된 분포에 맞는지 여부에 따라  
학습된 D의 어려운 결정에 의존할 뿐만 아니라 대신 풍부한 적대적 훈련 동안 D가 학습한 특징 표현의 정보를 고려한다.  
이러한 의미에서 우리의 접근 방식은 훈련된 D를 분류자가 아닌 특징 추출기로 활용한다.  
latent space에 대한 mapping에 대하여, 우리는 전체 loss를 두 component의 가중합으로 정의한다.  
![image](https://user-images.githubusercontent.com/40943064/131075533-a06b4158-2fa9-48db-88eb-06528944ff1b.png)    
z에 대한 계수만 backpropagation을 통해 adapt 된다.  
G와 D의 학습된 파라미터들은 고정된다.  

### 2.3. Detection of Anomalies
새로운 데이터에서 Anomaly identification을 위해 우리는 새로운 query 이미지 x를 정상/비정상 이미지로 평가한다.  
잠재 공간에 매핑하는 데 사용되는 손실 함수(Eq. (5))는 모든 업데이트 반복 γ에서 생성된 이미지 G(zγ)와  
adversarial training 동안 본 이미지의 호환성을 평가한다.  
따라서 쿼리 이미지 x의 일반 이미지 모델에 대한 적합도를 나타내는 anomaly score는 매핑 손실 함수(Eq. (5))에서 직접 파생될 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/131075797-eddd020a-facf-4bf2-a48e-f18b2414ac19.png)  
여기서 residual score R(x) 및 discriminator score D(x)는 latent 에 대한 매핑 절차의 마지막(Γ 번째) 업데이트 반복에서  
residual loss LR(zΓ ) 및 discriminator loss LD(zΓ )로 정의된다.  
모델은 비정상 이미지에 대해 큰 비정상 점수 A(x)를 산출하는 반면, 작은 비정상 점수는 훈련 중에 매우 유사한 이미지가 이미 표시되었음을 의미한다.  
이미지 기반 이상 탐지를 위해 이상 점수 A(x)를 사용한다.
추가로 Xr |x - G(zr)|은 이미지 내의 비정상 영역을 정의하기 위해 사용된다.  
비교를 위해 우리는 추가로 reference anomaly score를 사용한다.

## 3. Experiments
