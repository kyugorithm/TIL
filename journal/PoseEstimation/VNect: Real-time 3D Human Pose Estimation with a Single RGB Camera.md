# VNect: Real-time 3D Human Pose Estimation with a Single RGB Camera

## Abstract
단일 RGB 카메라를 이용해 시간적으로 안정된 방식으로 글로벌 3D 골격 자세를 포착하는 첫 실시간 방법을 제시한다.  
본 방법은 **CNN 기반 pose regressor**와 **kinematic skeletal fitting**을 결합한다.  
새로운 fully conv. 포즈 formulation은 실시간으로 2D 및 3D joint 위치를 함께 회귀하며 맞게 자른 프레임이 필요없다.  
실시간 kinematic skeletal fitting은 CNN 출력을 사용하여 일관된 kinematic skeleton을 기반으로  
시간에 안정적인 3D 글로벌 pose reconstruction을 얻는다.  
3D 캐릭터 제어와 같은 실시간 애플리케이션에서 사용할 수 있는 최초의 단일 카메라 RGB 방식으로 만들었다.  
(지금까지는 RGB-D 카메라를 사용한 방식이 유일하다.)  
본 방법의 정확도는 최고의 오프라인 3D 단안 RGB 포즈 추정 방법과 수치적으로 동등하다.  
본 결과는 질적으로 Kinect와 같은 단안 RGB-D 접근 방식의 결과와 비교할 수 있으며 때로는 더 낫다.  
그러나 우리는 우리의 접근 방식이 RGB-D 솔루션보다 더 광범위하게 적용 가능하다는 것을 보여준다.  
즉, 실외 환경, 커뮤니티 비디오 및 저품질 상품 RGB 카메라에 작동한다.

**Summary :**
1) 단일 카메라를 통한 실시간 전체 3D skeltal pose capture 방법 제시  
2) CNN기반 pose regressor와 kinematic skeletal fitting 방법론 결합  
3) 실시간 방식은 2D, 3D를 함께 regression하며 cropped input frame이 필요 없음
4) RGB-D가 아닌 일반 RGB 카메라를 사용하면서 광범위한 적용이 가능하고 때로 성능이 더 높음  

## Introduction
**Optical skeletal motion capture**는 영화, 게임, 스포츠, 생체역학, 의학용 캐릭터 애니메이션등 응용 프로그램에서 널리 사용된다.  
**Marker suit**를 필요로 하는 상용 시스템의 한계를 극복하기 위해, 연구자들은 멀티뷰를 사용하여 보다 일반적인 상황에서  
모션을 추정하는 **marker-less motion capture** 방법을 개발했다.  
실시간 motion base 3D 게임 캐릭터 제어, 3D 가상 및 증강 현실에서의 자기 몰입, 인간과 컴퓨터 상호 작용과 같은 응용 프로그램의 인기가 높아지면서  
Microsoft Kinect와 같이 설치가 용이한 단일 depth 카메라만을 사용한 새로운 실시간 전신 모션 추정 기술이 탄생했다.  
RGB-D 카메라는 단안 포즈 재구성을 크게 단순화하는 가치가 높은 깊이 데이터를 제공한다.  
그러나 RGB-D 카메라는 햇빛 간섭으로 야외에서 종종 실패하고, 더 크고, 더 높은 전력 소비를 가지며,  
더 낮은 해상도와 제한된 범위를 가지며, 일반 카메라만큼 광범위하고 저렴하게 사용할 수 없다.  
단일 RGB 카메라의 skeletal pose estimation은 훨씬 더 어렵고 제약이 심한 문제이다.  
2D 단안 RGB 자세 추정은 널리 연구되었지만 2D 한계가 있다.  
학습 기반 판별 방법, 특히 DL 방법, 2D 포즈 추정의 최신 기술을 나타내며 이러한 방법 중 일부는 실시간 성능을 보여준다.  
3D 골격 자세의 단안 RGB 추정은 상대적으로 연구결과가 적은 훨씬 어려운 과제이다.  
불행히도 이러한 방법은 일반적으로 오프라인이며 이미지별로 3D joint position을 개별적으로 재구성하는 경우가 많다.  
이는 시간적으로 불안정하고 일정한 뼈 길이를 적용하지 않는다.  
대부분의 방식은 전체 전역 3D 포즈가 아니라 bounding box에 상대적인 local 3D 포즈도 캡처한다.  
이로 인해 실시간 3D 캐릭터 제어와 같은 애플리케이션에는 적합하지 않다.  
  
본 연구에서는 일반 환경의 단일 RGB에서 실시간(30Hz)으로 안정적인 단일 kinematic skeletal의 joint 각도 측면에서  
시간적으로 일관된 전역 3D 인간 자세 캡처 방법을 처음 제시한다.  

접근 방식은 CNN을 사용하여 최고 성능의 단일 RGB 3D 포즈 추정 방법을 기반으로 한다.  
높은 정확도는 부분적으로 bounding box 추출과 같은 추가 사전 처리 단계로 인해  
실시간으로 실행이 어려운 비교적 깊은 네트워크를 훈련해야 한다.  
Mehtaet은 100-layer 구조를 사용하여 2D 및 3D joint 위치를 동시에 예측하지만 실시간 실행에는 적합하지 않다.  
Runtime 개선을 위해 더 얕은 50-layer 네트워크를 사용한다. 그러나 실시간 프레임 속도에서 최상의 품질을 위해  
더 얕은 변형을 사용하는 것이 아니라 새로운 완전 컨볼루션 공식으로 확장한다.  
이를 통해 특히 end effector(손, 발)의 보다 정확한 2D 및 3D 포즈 회귀가 실시간으로 가능하다.  
기존 솔루션과 달리 자르지 않은 이미지에 대한 작업을 수행하며 런타임이 문제인 경우 간단한 bounding box tracker를 부트스트랩하는 데 사용할 수 있다.  
또한 CNN 기반 joint position 회귀를 효율적인 최적화 단계와 결합하여 3D 골격을 이러한 재구성에 시간적으로 안정적인 방식으로 맞추면 골격의 전체 포즈와 joint 각도를 산출한다.  
요약하면 단일 RGB 비디오에서 전역 3D kinematic 골격 자세를 캡처하는 최초의 실시간 방법을 제안하여 기여한다.  
계산 복잡성과 정확성 사이에서 좋은 절충안을 찾기 위해 우리의 방법은 다음을 결합한다.  

• CNN을 사용하여 2D/3D joint 위치를 동시에 산출하고 무거운 bounding box 필요성을 없애는 새로운 실시간 fully convolution 3D body pose formulation.  
  
• 2D/3D에 대한 모델 기반 kinematic skeletal fitting은 실시간으로 메트릭 글로벌 3D 골격의 시간적으로 안정적인 joint 각도를 생성하기 위한 예측을 제시한다.  
  
본 실시간 방법은 특히 end effector(S5.2)에 대해 표준 3D human body pose benchmark에서 최고의 오프라인 RGB 포즈 추정 방법에 필적하는 정확도를 달성한다.  
결과는 최신 단일 RGB-D 방법, 심지어 상용 방법과 질적으로 비교할 수 있고 때로는 더 좋다.  
이것이 게임 캐릭터 제어 또는 몰입형 1인칭 가상 현실(VR)과 같은 유사한 실시간 3D 응용 프로그램(지금까지는 RGB-D 입력으로만 가능)에  
사용할 수 있는 최초의 단일 RGB 방법을 실험적으로 보여준다.  
야외환경, 공개 비디오 및 스마트폰 카메라의 저품질 비디오 스트림과 같이 기존 RGB-D 방법이 성공하지 못하는 설정에서의 성공을 보여준다.  

## 2 RELATED WORK
**Multi view:**  
Multi-view를 통해 marker-less motion capture 방법은 더 높은 정확도를 달성한다.  
생성 이미지 형성 모델을 통해 frame-to-frame으로 수동으로 초기화된 actor 모델을 추적하는 것이 일반적이다.  
대부분의 방법은 오프라인 연산을 통해 높은 품질을 목표로 한다. 실시간 성능은 모델 대 이미지 피팅을 허용하는 공식 외에  
가우시안 및 기타 근사치로 행위자를 대표함으로써 달성할 수 있다.  
그러나 이러한 추적 기반 접근방식은 최적화하는 비볼록 피팅 함수의 국소 최소값에서 궤적을 잃는 경우가 많으며, 별도의 초기화가 필요하다.  
단일 입력 관점과 자기 중심 관점에서도 생성적 추정과 차별적 추정의 조합으로 강건성을 높일 수 있다.  
생성 추적 구성 요소를 활용하여 시간적 안정성을 보장하지만 추정 속도를 높이기 위해 전체 이미지 형성 모델을 통한 모델 투영을 피한다.  
대신, 제한되지 않은 환경에서 성공하기 위해 차별적 자세 추정과 kinematic 피팅을 결합한다.

## 3 OVERVIEW 
단일 RGB 카메라에서 시간적으로 일관된 완전한 인간의 3D 골격 포즈를 얻을 수 있다.  
3D 포즈를 추정하는 것은 고유한 모호성으로 인해 어렵고 제약이 적은 문제이다.  
그림 2는 이 어려운 문제를 해결하는 방법에 대한 개요를 제공한다.  
![image](https://user-images.githubusercontent.com/40943064/139999064-1bb7c124-7259-49b6-a90c-f05483f08b6d.png)  
두 가지 기본 구성 요소가 있다. 
첫 번째는 ill-posed 단안 캡처 조건에서 2D/3D joint 위치를 회귀하는 CNN이다.  
이는 주석이 달린 3D 인간 포즈 데이터 세트에서 학습되며, 주석이 달린 2D 인간 포즈 데이터 세트를 활용하여 개선된 실제 성능을 제공한다.  
두 번째는 회귀된 joint 위치를 kinematic skeletal fitting과 결합하여 시간적으로 안정적인 카메라 기준 전체 3D 골격 포즈를 생성한다.  

**CNN Pose Regression:**:  
핵심은 실시간으로 2D 및 루트(골반) 상대 3D joint 위치를 모두 예측하는 CNN이다.  
새로 제안된 fully conv. 자세 formulation은 3D joint 위치 정확도에서 SOTA 오프라인 방법과 성능이 동등하다. 
완전 conv.이기 때문에 object만 자른 이미지가 필요없다.   
CNN은 상황에 관계없이 다양한 활동 클래스에 대한 joint 위치를 예측할 수 있으며  
시간적으로 일관된 전체 3D 포즈 매개변수를 생성하기 위한 추가 자세 개선을 위한 강력한 기반을 제공한다.  
  
**Kinematic Skeleton Fitting:**  
CNN의 2D/3D 예측 , 시퀀스의 시간 기록과 함께 카메라 공간에 국한된 골격 루트(골반)와 함께  
시간적으로 일관된 전체 3D 골격 포즈를 얻는 데 활용할 수 있다. 우리의 접근 방식은 최적화 기능을 사용한다.  
(1) 예측된 2D 및 3D joint 위치를 결합하여 운동학적 골격을 least-square 개념에 맞춘다.  
(2) 시간 흐름에 따라 부드러운 추적을 보장한다. 다양한 단계에서 필터링 단계를 적용하여 추정 자세 안정성을 더욱 향상시킨다.  
  
**Skeleton Initialization (Optional):**  
시스템은 대부분의 인간에게 기본적으로 잘 작동하는 기본 스켈레톤으로 설정된다.  
정확한 추정을 위해 초기 몇 프레임에 대한 CNN 예측을 평균화하여 기본 골격의 상대적 신체 비율을 대상의 신체 비율에 맞출 수 있다.  
스케일 참조 없이 단안 재구성이 모호하기 때문에 CNN은 높이 정규화된 3D joint 위치를 예측한다.  
사용자는 실제 미터법 공간에서 3D 포즈를 추적할 수 있도록 높이(머리에서 발끝까지의 거리)를 한 번만 제공하면 된다.  
  
## 4 REAL-TIME MONOCULAR 3D POSE ESTIMATION
단안 RGB 입력 시퀀스에서 시간적으로 일관된 3D 골격 움직임을 추정하는 방법의 다양한 구성 요소에 대해 자세히 설명한다.  
입력으로 단안 RGB 이미지 {..., It−1, It }의 연속 스트림을 가정한다.  
입력 스트림의 프레임 t에 대해 우리 접근 방식의 최종 출력은 추적되는 사람의 전체 전역 3D 골격 포즈인 P_t^G 이다.  
이 출력은 이미 시간적으로 일관되고 전역 3D 공간이므로 3D 캐릭터 제어와 같은 프로그램에서 쉽게 사용할 수 있다.  
제안 방법의 중간 구성 요소에서 출력에 대해 다음 표기법을 사용한다.  
CNN 포즈 regressor는 2D joint 위치 **Kt**와 root-relative 3D joint position **P_t^G** 를 공동으로 추정한다.  
3D skeletal fitting 구성 요소는 2D/3D joint 위치 예측을 결합하여 카메라 공간의 전역 위치 d와 운동학적 골격 S의 joint 각도 θ에 의해  
매개변수화된 부드럽고 시간적으로 일관된 포즈 P_t^G(θ, d)를 추정한다.  
**J**는 joint 수를 나타낸다.
  
### 4.1 CNN Pose Regression
CNN pose regression의 목표는 2D 및 3D 모두에서 joint 위치를 얻는 것이다.  
신경망을 사용한 2D 포즈 추정의 경우 x,y 신체 joint 좌표의 직접 회귀에서  
Heatmap 기반 신체 joint 감지 공식으로 공식의 변경이 최근 2D 포즈 추정 개발의 핵심 동인이었다.  
Heatmap 기반 공식은 각 joint j ∈ {1..J }에 대한 이미지 plane에 대한 confidence heatmap **Hj,t**를 예측하여  
이미지 증거를 포즈 추정에 자연스럽게 연결한다.  
3D 포즈 추정에 대한 기존 접근 방식에는 이러한 이미지-예측 연관이 부족하여 종종 root relative joint 위치를 직접 회귀하여  
joint의 정도가 이미지에 있는 사람의 joint 범위를 반영하지 않는 예측된 포즈로 이어진다. (그림 9 참조)  
![image](https://user-images.githubusercontent.com/40943064/140046027-015ca3ed-2699-4c7b-a08c-644849bae7ed.png)  
그림9. 직접적인 fully conv. 구조의 3D 예측 vs Mehta 방법의 비교 : image evidence와 강력하게 연결되어 있어 특히 끝 부분의 자세 품질이 좋음  


포즈를 joint 위치의 벡터로 처리하면 fully connected formulation이 있는 네트워크에 대한 자연스러운 중력이 발생하여  
입력이 고정된 해상도에서 좁은 crop으로 제한되어 극복해야 하는 한계가 있다.  
이러한 방법은 tight한 bounding boxes를 사용할 수 있다고 가정하므로 실제 사용을 위해 별도의 bounding boxes 추정기로 보완해야 하므로  
이러한 방법의 실행 시간이 추가된다.  
Pavlakos의 fully-convolutional formulation은 이러한 문제 중 일부를 완화하려고 하지만 여전히 잘린 입력에 의존하고  
더 큰 이미지 크기로 잘 확장되지 않는 계산량이 큰 joint별 volumetric formulation에 의해 제한된다.  

Joint j당 3개의 추가 location-map Xj, Yj, Zj를 사용하여 2D heatmap 공식을 3D로 확장하고 root 상대 위치 xj, yj 및 zj를 각각 캡처하여  
새로운 formulation을 통해 이러한 제한을 극복했다.  
3D 포즈 예측이 이미지의 2D 모양에 더 강력하게 연결되도록 하기 위해 xj , yj 및 zj 값은 해당 joint의 2D heatmap Hj 최대값의 위치에 있는  
각각의 location-map에서 판독되어 PL = {x, y, z} 위치에 저장된다.  
여기서 x ∈ R 1×J는 각 joint 최대값의 좌표 x 위치를 저장하는 벡터이다.  
포즈 formulation은 그림 3에 시각화되어 있다.  
![image](https://user-images.githubusercontent.com/40943064/140048317-07421fe1-aebb-438a-9f0e-c6508292c6d0.png)

이 fully convolution formulation을 사용하는 네트워크는 입력 이미지 크기에 제약을 받지 않으며 타이트한 자르기 없이 작동할 수 있다.  
또한 네트워크는 추가 오버헤드 없이 2D 및 3D 공동 위치 추정을 제공하며, 이를 실시간 추정을 위한 후속 단계에서 활용한다.  
S5.2는 이 formulation이 제공하는 개선 사항을 보여준다.  

**Loss term**:  
Joint j의 2D 위치에 있는 각각의 맵에서 xj , yj 및 zj에만 관심이 있다는 사실을 적용하기 위해  
joint location-map loss는 joint의 2D 위치 주변에서 더 강하게 가중치가 부여된다.  
L2를 사용한다. xj의 경우 loss 공식은 다음과 같다.  
![image](https://user-images.githubusercontent.com/40943064/140038207-2a1bcc54-3889-448b-ac58-4865c43c9618.png)  
여기서 GT는 실측 정보를 나타내고 ⊙는 하다마드 product이다.  
Location map은 각 GT 2D heatmap H GT j로 가중치를 부여하며,  
이는 다시 joint j의 2D 위치에 국소화된 작은 지지대를 가진 가우스와 동일한 신뢰도를 갖는다.  
Location map에 어떤 구조도 부과되지 않는다는 점에 유의해야한다.  
예측된 location map에 나타나는 구조는 영상 평면에서 joint j의 root relative joint position과 xj 및 yj의 상관 관계를 나타낸다. (그림 3 참조)  
  
**Network Details**:  
제안된 공식을 사용하여 He의 ResNet50 네트워크 아키텍처를 적용한다.  
res5a부터 ResNet50의 그림 5에 표시된 구조 교체하여 joint j ∈ {1..J }에 대한 heatmap과 location-map을 생성한다.  
학습 후 Batch Normalization은 이전 컨볼루션 레이어의 가중치와 병합되어 순방향 패스의 속도를 향상시킨다.  
![image](https://user-images.githubusercontent.com/40943064/140038975-92a943d2-1c70-4d1f-93b1-b1a6992599e8.png)  
  
**Intermediate Supervision**:  
res4d 및 res5a의 feature에서 2D heatmap 및 3D location-map을 예측하여 반복 횟수가 증가함에 따라 중간 손실의 가중치를 줄인다.  
또한 root-relative location-maps Xj , Yj 및 Zj 와 유사하게 res5b 의 feature에서  
kinematic 부모 상대 location-map ∆Xj , ∆Yj 및 ∆Zj 를 예측하고 다음과 같이 뼈 길이 맵을 계산한다.  
![image](https://user-images.githubusercontent.com/40943064/140039379-fc4ed675-fd76-48cf-bfa9-d6fa0fe79d48.png)  
이러한 중간 예측은 이후에 중간 feature와 연결되어 네트워크에 예측을 안내하는 뼈 길이의 명시적 개념을 제공한다. (그림 5를 참조)  
실험에 따르면 ResNet의 더 깊은 변종은 계산 시간의 상당한 증가(1.5배)에 대해 약간의 이득만 제공하므로  
제안된 공식으로 실시간이지만 매우 정확한 joint 위치 추정을 가능하게 하기 위해 ResNet50을 선택해야 한다.  
  
**Training**:  
네트워크는 Mehta가 제안한 대로 우수한 wild 성능을 허용하기 위해 2D 포즈 추정을 사전학습한다.  
2D : MPII, LSP
3D : MPI-INF3DHP, Human3.6m(S9, S11 제외)  
프레임을 샘플링한다.  
카메라 시점에 대한 어느 정도의 불변성을 학습하기 위해 5대의 가슴 높이 카메라, 2대의 머리 높이 카메라(아래로 기울어짐)  
및 1대의 무릎 높이 카메라(위쪽)에서 시퀀스를 선택한다. 샘플링된 프레임 사이에 > 200mm만큼 이동한 joint이 하나 이상 있다.  
우리는 선택된 프레임의 70%에 배경, 오클루더(의자), 상체 및 하체 확대의 다양한 조합을 사용한다.  
사람 중심 crop으로 학습하고 2개의 스케일(0.7×, 1.0×)에서 이미지 스케일 증대를 사용하여 Human3.6m에 대해  
75k 훈련 샘플 및 MPI-INF-3DHP에 대해 100k 훈련 샘플을 생성한다. 그림 4는 훈련 데이터의 몇 가지 대표적인 프레임을 보여준다.  
![image](https://user-images.githubusercontent.com/40943064/140058111-d878b994-1184-457f-b0e4-6a5529ae3393.png)  

일반적으로 고려되는 17개의 joint 외에도 발 끝 위치를 사용한다.  
실제 joint 위치는 높이 정규화 골격(무릎-목 높이 92cm)을 기준으로 한다.  
학습을 위해 Caffe 프레임워크를 사용하고 반복이 증가함에 따라 학습률이 감소하는 Adadelta를 사용한다.  

**Bounding Box Tracker**:  
기존 offline 솔루션은 별도의 개인 현지화 및 BB 자르기 단계에서 각 프레임을 처리하거나 경계 상자를 사용할 수 있다고 가정한다.  
우리의 fully convolution formulation은 CNN이 자르기 없이 작동하도록 허용하지만 CNN의 실행 시간은 입력 이미지 크기에 크게 의존한다.  
또한 250–340픽셀 범위의 피사체 크기에 대해 학습되므로 각 시간 단계에서 전체 프레임을 처리하는 경우  
프레임당 여러 이미지 스케일(스케일 공간 검색)에서 예측의 평균을 요구한다.  
실시간 속도를 보장하려면 네트워크에 대한 입력의 크기를 제한하고 각 프레임에서 스케일 공간을 검색하지 않도록  
이미지의 사람 스케일을 추적해야 한다. 우리는 통합된 방식으로 이를 수행한다.  
각 프레임에서 CNN의 2D 포즈 예측은 예측 주변의 약간 더 큰 상자를 통해 다음 프레임의 BB를 결정하는 데 사용한다.  
키포인트 K를 포함하는 가장 작은 직사각형이 계산되고 버퍼 영역이 수직으로 1.2x 수평 1.4x 로 증가한다.  
추정치를 안정화하기 위해 BB는 2D 예측의 중심으로 수평으로 이동하고 모서리는 0.75의 모멘텀을 사용하여 이전 프레임의 BB와 가중 평균으로 필터링된다.  
크기를 정규화하기 위해 BB 자르기의 크기가 368x368픽셀로 조정된다.  
BB tracker는 처음 몇 프레임에 대한 전체 이미지에 대한 (느린) 다중 스케일 예측으로 시작하여 fully-conv. 네트워크의  
BB 불가지론적 예측을 사용하여 이미지의 사람을 연마한다.  
제안된 네트워크는 2D와 3D 포즈를 함께 출력하고 임의의 입력 크기에서 작동하기 때문에 BB 추적은 구현하기 쉽고 런타임 오버헤드가 없다.  

### 4.2 Kinematic Skeleton Fitting
비디오에 프레임별 포즈 추정 기술을 적용하면 모션의 시간적 일관성을 이용하거나 보장할 수 없으며  
작은 포즈 부정확성은 대부분의 그래픽 애플리케이션에서 허용할 수 없는 아티팩트인 시간적 지터로 이어진다.  
정확하고 시간적으로 안정적이며 강력한 결과를 얻기 위해 시간 필터링 및 스무딩과 함께  
joint 최적화 프레임워크에서 2D 및 3D joint 위치를 결합한다.  
첫째, 2D 예측 Kt는 시간적으로 필터링되고 location map 예측에서 각 joint의 3D 좌표를 얻는 데 사용되어 PtL을 제공한다.  
골격 안정성을 보장하기 위해 PtL의 뼈 방향을 유지하는 간단한 리타게팅 단계에서 PtL 고유의 뼈 길이가 기본 골격의 뼈 길이로 대체된다.  
다음의 목적 에너지를 최소화하여 골격 joint 각도 θ와 카메라 공간 d에서 루트 joint의 위치에 대한 결과 2D 및 3D 예측을 결합한다.  
![image](https://user-images.githubusercontent.com/40943064/140042258-de333751-ae58-4f62-b96a-e5a07bd4b537.png)  
3D 역기구학 항 EIK는 3D CNN 출력 PtL과의 유사성에 따라 전체 포즈를 결정한다.  
Projection 항 Eproj는 전역 위치 d를 결정하고 감지된 2D 키포인트 Kt에 재투영하여 3D 포즈를 수정한다.  
두 항 모두 아래의 L2 norm으로 수행한다.  
![image](https://user-images.githubusercontent.com/40943064/140042503-940ecf43-4cf7-4d1e-b99b-4f15d85dd1d7.png)  
여기서 Π는 3D에서 이미지 평면으로의 프로젝션 함수이며 PGt= PGt(θ, d) 이다.  

우리는 pinhole 프로젝션 모델을 가정한다. 만약 카메라 캘리브레이션을 알지 못하는 경우 수직 view는 54도를 가정한다.  
시간적 안정성은 smoothness prior Esmooth = ∥PcG t ∥2로 부과되며 PcGt를 가속하는것에 패널티를 부과한다.  
단안 재구성에서 강한 깊이 불확실성에 대응하기 위해 Edepth = ∥[PfG t ]z ∥2로 깊이의 큰 변화에 추가로 페널티를 부여한다.  
여기서 [PfG t ]z 는 PfGt의 3D 속도 z성분이다. 마침내, 3D 자세는 1 euro filter로 filtering 된다.
