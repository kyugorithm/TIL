# Improving Shape Deformation in Unsupervised I2I Translation
## Abstract
비지도 I2I 변환 기법은 두 도메인간 local texture mapping이 가능케 하지만 형태 변환 문제에는 성공적이지 않다.  
Semantic segmentation에서 영감을 얻어, 이미지 문맥을 학습에 관심을 갖는 dilated conv.를 통해 정보를 사용하는 D를 적용한다.  
Object의 기본 형상의 에러를 표현하는 multi-scale perceptual loss를 적용한다.  
위 방법을 통해 형태변형이 어려운 데이터셋에 대한 성능을 보인다.  
  
**Key concept**
1. D(Dilated conv.)의 global context 파악  
2. Multi-scale perceptual loss를 적용하여 obeject shape을 잘 학습함  
  
## 1. Introduction
기존 연구(DiscoGAN, CycleGAN)는 unsupervised i2i translation task에서 local texture 변환을 잘 하지만  
형태 변형이 큰 task(고양이->개)에는 어려움이 있다. 단순히 동물의 질감 정보만 변경해서는 안되고  
전체 이미지의 공간 정보를 사용할 수 있는 능력이 필요하다.  
  
**DiscoGAN** : FC D의 경우 용량을 크게 설계하면 큰 형태 변형이 가능하지만 학습이 느리고 디테일한 부분에는 문제가 있다. 
  
**CycleGAN** : patch D는 고주파 정보를 잘 해석하고 상대적으로 빠르게 학습하지만  
네트워크가 공간적으로 local contents만 고려할 수 있도록 각 패치에 대해 제한된 'receptive field'를 가진다.  
이러한 네트워크는 G에 대한 loss 정보량을 줄인다.  
Cycle consistency를 유지하는 loss는 고주파 정보를 유지하는데 사용 되기 때문에 모양 변경 작업에는 방해가 된다.  
위와같은 약점을 해결하기 위해 패치 기반 D가 더 많은 이미지 context를 사용할 수 있도록 dilated conv.를 사용한다.  
이를 통해 판별 작업을 semantic segmentation 문제로 취급할 수 있다.  
D는 per-pixel 판별을 수행하며 각각 global context에 의해 정보를 얻는다.  
이러한 방식은 D가 G로의 loss 전달을 더욱 세분화된 정보 전달이 되도록 한다. 
또한 'multi-scale structure similarity perceptual reconstruction loss'를 사용하여 픽셀이 아닌 이미지 영역에 대한 오류를 나타낸다.  

## Our Apporch
모양 변형에서 변환의 성공에 결정적인 요소는 global/local 일관성을 유지하는 능력이다.  
우리의 알고리즘은 cyclic image translation framework를 채택하고 dilated D, residual block 및 skip-connection이 있는 G,  
multi-scale perceptual cyclic loss를 통합하여 필요한 일관성을 달성한다.  

### 3.1 Dilated Discriminator
(DiscoGAN)은 fc 레이어가 있는 global D를 사용하며 이미지의 정확성을 결정하기 위해 이미지를 단일 스칼라 값으로 축소한다.  
(CycleGAN, ContrastingGAN)은 patch 기반 DCGAN D를 사용하며 초기 스타일 전송 및 텍스처 합성을 위해 개발되었다.  
이러한 D에서 각 이미지 패치는 real/fake를 결정하기 위해 평가된다.  
patch 기반 접근 방식은 로컬 패치에서 독립적으로 작동하여 빠른 G 수렴을 돕는다.  
이 접근 방식은 texture transfer, segmentation 및 유사한 작업에 효과적이지만  
전역 공간 정보에 대한 네트워크의 인식을 제한하여 일관된 전역 모양 변경을 수행하는 G의 능력을 제한한다.  
_Reframing Discrimination as Semantic Segmentation_  
이 문제를 해결하기 위해 식별 문제를 real/fake 또는 하위 이미지를 판별하는 것에서  
이미지의 실제 또는 가짜 영역을 찾는 보다 일반적인 문제, 즉 semantic segmentation으로 재구성한다.  
D는 고해상도의 segmentation map을 출력하기 때문에 Generator와 Discriminator 사이의 정보 흐름이 증가한다.  
이것은 DiscoGAN과 같이 FC의 D를 사용하는 것보다 수렴이 빠르다.  
Segmentation을 위한 최신 네트워크는 dilated conv.를 사용하며 유사한 수준의 정확도를 달성하기 위해  
기존의 conv.보다 훨씬 적은 매개변수가 필요하다. Dilated conv.는 global 및 patch 기반 D에 비해 이점을 제공한다.  
동일한 매개변수량에 대해 예측을 통해 더 큰 주변 field의 데이터를 통합할 수 있다.  
이렇게 하면 G와 D 간의 정보 흐름이 증가한다.  
이미지 영역이 이미지를 비현실적으로 만드는 데 기여한다는 것을 알면 G는 이미지의 해당 영역에 집중할 수 있다.  
dilated conv. 대해 생각하는 또 다른 방법은 D가 context를 암시적으로 학습할 수 있도록 하는 것이다.  

다중 스케일 D가 고해상도 이미지 합성 작업의 결과와 안정성을 향상시키지만, D가 영역이 어디에 맞아야 하는지 결정할 수 있으므로  
이미지에서 더 멀리 떨어진 정보를 통합하는 것이 번역 작업에 유용하다는 것을 보여줄 것이다.  
주변 데이터를 기반으로 이미지로 변환합니다.  
예를 들어, 이렇게 증가된 공간적 맥락은 강아지의 얼굴을 몸에 상대적으로 위치시키는 데 도움이 되며,  
이러한 방식은 이웃과 분리되어 학습된 작은 패치나 패치에서 배우기 어렵다. 그림 2(오른쪽)는 판별자 아키텍처를 보여준다.
  ![image](https://user-images.githubusercontent.com/40943064/140634771-d16e0b0b-0fa6-48e9-85fd-664a52c81c92.png)
Fig. 2. (L) Unsupervised 방법론들의 G 구조. ResBlock과 Skip connection이 더하기가 아닌 concat.에 의해 결합되어있다.  
(R) 우리의 D는 fully-convolutional segmentation network이다. (skip connection으로 local context에 대한 네트웍의 view를 보존할 수 있다.)

### 3.2 Generator
우리의 G 구조는 DiscoGAN과 CycleGAN을 기본 구조로 한다. DiscoGAN은 표준 encoder-decoder 구조(fig.2 좌측상단)를 가진다.  
그러나, bottleneck이 좁기 때문에 입력 이미지의 중요한 visual detail을 보존하지 못한다.  
또한, 네트워크의 용량이 낮아 제한된 해상도(64x64)만 표현할 수 있다.  
CycleGAN은 이미지 translation 을 배우기 위해 residual block을 이용해 용량을 높힌다.  
Residual block은 극단적으로 깊은 네트웍에서 효과가 있는것으로 알려져있으며 저차원 정보를 표현할 수 있다.  
그러나 단일 scale에서 residual block을 사용하면 bottleneck으로 넘겨주는 정보와 네트워크가 학습할 수 있는 기능을 제한한다.  
우리의 G 구조는 여러 해상도의 decoder-encoder에 residual block을 사용하여  
네트워크가 여러 해상도 변환을 배우게하며 다양한 해상도의 feature를 학습할 수 있도록 한다. (fig.2 좌측하단)  

### 3.3 Objective Function
_Perceptual Cyclic Loss_  
이전의 비지도 I2IT 작업에에 따라 cyclic loss를 사용하여 도메인 간의 bijective mapping을 학습한다.  
그러나 모든 이미지 번역 기능이 완벽하게 bijective 될 수는 없다.  
예를 들어 얼굴 사진과 애니메이션 그림과 같이 한 도메인의 모양 변화가 더 작은 경우이다.  
번역에서 입력 이미지의 모든 정보를 보존할 수 없는 경우 순환 손실 항은 가장 중요한 정보를 보존하는 것을 목표로 해야 한다.  
네트워크는 보는 사람에게 중요한 이미지 속성에 초점을 맞춰야 하므로 생성된 이미지와 대상 이미지 간의 모양과  
모양 유사성을 강조하는 지각 손실을 선택해야 한다. 명시적 shape loss를 정의하는 것은 어렵다.  
명시적 용어에는 도메인 간의 알려진 이미지 대응이 필요하기 때문이다. 이것은 우리의 예와 비지도 환경에 존재하지 않는다.  
또한 loss 계산에 보다 복잡한 perceptual 신경망을 포함하면 상당한 계산 및 메모리 오버헤드가 발생한다.  
사전 학습된 이미지 분류 네트워크를 perceptual 손실로 사용하면 스타일 전송 속도를 높일 수 있지만 사전 학습된 네트워크는  
낮은 수준의 텍스처 정보만 캡처하는 경향이 있으므로 모양 변경에는 작동하지 않으므로 MS-SSIM(다중 구조 유사성 손실)을 사용한다.  
이 loss은 noisy한 고주파 정보 대신 사람이 볼 수 있는 feature를 더 잘 보존한다.  
또한 MS-SSIM은 area statistics를 통해 geometric 차이를 인식할 수 있으므로 형상 변화에 더 잘 대처할 수 있다.  
그러나 MS-SSIM만으로는 작은 세부 사항을 무시할 수 있으며 색상 유사도를 잘 포착하지 못한다.  
최근 연구에 따르면 MS-SSIM과 L1 또는 L2 손실을 혼합하는 것이 초해상도 및 분할 작업에 효과적이다.  
따라서 생성된 이미지의 선명도를 높이는 데 도움이 되는 가벼운 가중치 L1 손실 항도 추가한다.  
  
_Feature Matching Loss_
모델안정성을 향상하기 위해 우리의 목적함수는 feature matching loss를 사용한다.  
![image](https://user-images.githubusercontent.com/40943064/140635231-5acf121a-63c1-4e7c-8a1d-15c9f4b70bd8.png)  
여기서 fi ∈ D(x)는 D의 i 번째 계층의 raw activation potential을 나타내고 n은 D의 layer의 수이다.  
이 항은 가짜 및 실제 샘플이 D에서 유사한 활성화를 생성하도록 장려하므로 G가 대상 도메인과 더 유사하게 보이는 이미지를 생성하도록 한다.  
GAN이 종종 취약한 G의 mode collapse를 방지하기 위해 이 손실 항을 사용한다.  
  
_Scheduled Loss Normalization (SLN)_
multi-part loss에서 linear weight는 종종 서로에 대해 항을 정규화하는 데 사용되며 이전 작업에서는 단일 가중치 집합을 최적화하는 경우가 많다.  
그러나 적절하게 균형 잡힌 weight를 찾는 것은 ground truth 없이는 어려울 수 있다.  
또한, loss의 크기가 훈련 과정에서 변하기 때문에 종종 단일 가중치 세트가 부적절하다.  
대신에 각 loss를 주기적으로 재정규화하여 상대적 값을 제어하는 절차를 만든다.  
이를 통해 사용자는 가중치의 합이 1이 되는 가중치를 직관적으로 제공하여 훈련에 따라 크기가 어떻게 변할지 알지 않고도  
모델의 loss term의 균형을 맞출 수 있다.  
L을 손실 함수라고 하고 Xn = {xt} bn t=1이라고 하면 L(xt)가 반복 t에서의 훈련 손실이 되도록 각 b개의 이미지가 큰 n개의 훈련 입력 배치의 시퀀스이다.  
손실의 지수 가중 이동 평균을 계산한다.  

![image](https://user-images.githubusercontent.com/40943064/140635346-79d5b8a7-f125-4ab3-9cb4-8480c739a4fe.png)  
여기서 β는 감쇠율이다. 이 moving average로 나눔으로써 loss 함수를 renormalize 할 수 있다.  
그러나 이것을 매 학습 iteration에 대해 하는 경우 loss는 normalized average에 머무를 것이고 학습 진행이 되지 않는다.  
대신 loss 정규화를 다음과 같이 스케줄링한다.  
![image](https://user-images.githubusercontent.com/40943064/140635392-c9ae1590-a519-4ba1-8b9b-5f1578726772.png)  
여기서 s는 매 s 훈련 반복마다 정규화를 적용하는 스케줄링 매개변수이다.  
모든 실험에 대해 β = 0.99, eps = 10−10 및 s = 200을 사용한다.  
CycleGAN/DiscoGAN과 우리의 접근 방식 간의 또 다른 정규화 차이점 중 하나는 각각 인스턴스 정규화와 배치 정규화를 사용하는 것이다.  
배치 정규화로 인해 훈련 데이터에 과도하게 과적합되는 것을 발견하여 instance norm을 사용했다.  


_Final Objective_  
최종 목적함수는는 (standard GAN loss, feature matching loss, two cyclic reconstruction losses)로 구성된다.  
도메인 X 및 Y가 주어지면 G : X → Y가 X에서 Y로 매핑되고 F : Y → X가 Y에서 X로 매핑된다.  
DX 및 DY는 각각 G 및 F에 대한 D를 나타낸다. GAN loss의 경우 Goodfellow의 일반 GAN 손실 조건을 결합한다.  
![image](https://user-images.githubusercontent.com/40943064/140635463-f5d88b1c-ac44-4079-a71b-af310938f872.png)  
각 도메인에 대해 1번 항의 feature matching loss를 아래와 같이 적용한다.  
![image](https://user-images.githubusercontent.com/40943064/140635479-b96aad9f-17ba-47a7-b56e-eaf283767d76.png)

두 개의 cyclic reconstruction loss에 대해 구조적 유사성과 L1 loss를 고려한다.  
X0 = F(G(X)) 및 Y 0 = G(F(Y))를 순환적으로 재구성된 입력 이미지라고 하자. 그러면 :  
![image](https://user-images.githubusercontent.com/40943064/140635517-1a64077d-2d7e-4370-afbb-360e1735fa33.png)
여기서 우리는 discorrelation 없이 MS-SSIM을 계산한다.  
SLN을 포함한 최종 목적함수는 다음과 같다.  
![image](https://user-images.githubusercontent.com/40943064/140635534-3eecc6b7-34ee-4bc7-add2-9ac8553cbd52.png)
(λGAN=0.49 + λFM=0.21 + λCYC=0.3) = 1, (λSS=0.7 + λL1=0.3) = 1 & (all coefficients ≥ 0).  
경험적으로, 이러한것들은 mode collapse를 줄이며 모든 데이터셋에 동작한다.  

### 3.4 Training

네트워크 아키텍처는 128×128 이미지를 소비하고 출력한다. 모든 모델은 배치 크기가 16인 단일 NVIDIA Titan X GPU에서 3.2일 이내에 학습했다.  
단계당 G 업데이트 수는 데이터 세트 난이도에 따라 각 데이터 세트에 대해 1에서 2까지 다양했다.  
G의 각 업데이트는 D의 업데이트에서와 별도의 데이터를 사용했다.  
도메인에 따라 Epoch당 1,000개의 배치로 50–400 Epoch에 대해 학습한다.  
전반적으로 이것은 어려운 데이터 세트(예: 고양이에서 개)에 대한 교육 과정에서 400,000개의 G 업데이트와  
더 쉬운 데이터 세트(예: 인간에서 인형)에 대한 200,000개의 G 업데이트로 이어졌다.  
도메인에서 이미지를 생성하기 어려운 경우 데이터 세트를 하드 또는 쉬움으로 경험적으로 정의한다.  

_Data Augmentation_  
데이터 세트 과적합을 완화하는 데 도움이 되도록 각 데이터 세트에 다음의 augmentation을 적용했다.  
1.1x 입력 비율로 재조정, 이미지의 임의 수평 뒤집기, 어느 방향으로든 최대 30도의 임의 회전, 임의 크기 조정 및 임의의 이미지 자르기  

## 4 Experiments

### 4.1 Toy Problem: Learning 2D Dot and Polygon Deformations

모양과 질감이 일관된 변형을 학습하는 능력을 평가하기 위해 어려운 toy example을 실험한다.  
정다각형 영역 X와 변형된 등가 Y의 두 영역을 정의한다(그림 3).  
각 예제 Xs,h,d ∈ X에는 면과 겹쳐진 점의 변형된 행렬과 함께 다음 요소를 포함한다.  
1) s : s ∈ {3 ... 7} 면의 중심 정다각형  
2) h : random normal 2x2 행렬 : Dot matrix의 단위 점 grid 행렬에 대한 변환 조건  
3) d : R2의 gaussian 법선 벡터인 변위 벡터
Y에서 대응하는 도메인은 Ys,h,d이며, 대신에 h로 변환된 다각형과 도트 행렬은 규칙적으로 유지된다.  
이 구성은 X에서 Y로의 bijective를 형성하므로 번역 문제가 잘 제기된다.  

X에서 Y로의 매핑을 학습하려면 고정된 이미지 위치가 있는 로컬 패치가 추가된 변위 d를 극복할 수 없기 때문에  
네트워크가 도트 매트릭스에 있는 대규모 신호를 사용하여 다각형을 성공적으로 변형해야 한다.  
표 2는 DiscoGAN이 도메인간 매핑이 불가하며  데이터의 평균(회색)에 가까운 출력을 생성하는것을 보여준다.  
CycleGAN은 일반 공간에서 변형 공간으로 매핑할 때 다각형의 파란색 쪽으로 색조 이동을 생성하고 대부분의 경우 변형에서  
일반 공간으로 매핑할 때 변형되지 않은 도트 매트릭스를 생성하는 local 변형만 학습한다.  
그러나 우리의 접근 방식은 dilated D가 이미지 전체에서 정보를 통합하여 변형을 학습하는 데 훨씬 더 성공적이다.  

_Quantitative Comparison_  
출력은 고도로 변형된 이미지이므로 샘플링을 통해 학습된 변환 매개변수를 추정한다.  
우리는 GT polygon과 변환 후 생성된 polygon 이미지에서 500개 포인트 샘플 사이의 Hausdorff 거리를 계산한다.  
finite point X와 Y 세트의 경우 d(X, Y) = max(y∈Y)min(x∈X) ||kx−yk|| 이다.  
네트워크에 대해 생성된 220개의 polygon 경계에 손으로 주석을 달고 경계를 따라 무작위로 균일하게 샘플링한다.  
샘플은 왼쪽 하단 모서리가 (0, 0)인 단위 정사각형에 존재한다.

첫째, DiscoGAN은 원본 이미지를 재구성할 수 있지만 다각형을 전혀 생성하지 못한다.  
둘째, 'regular to deformed'의 경우 CycleGAN은 다각형을 생성하지 못하는 반면  
우리의 접근 방식은 0.20 ± 0.01의 평균 하우스도르프 거리를 생성한다.  
셋째, 'deformed to regular'의 경우 CycleGAN은 거리가 0.21 ± 0.04인 다각형을 생성하는 반면  
우리의 접근 방식은 거리가 0.10 ± 0.03이다.  
실제 데이터 세트에서 일반 다각형은 중앙에 있지만 CycleGAN은 원래 왜곡된 다각형 위치에서만 다각형을 구성한다.  
우리의 네트워크는 원하는 대로 이미지 중앙에 정다각형을 구성한다.  

![image](https://user-images.githubusercontent.com/40943064/140635883-03f8bbf4-eae1-4558-bb6b-5bd6433e1d81.png)
