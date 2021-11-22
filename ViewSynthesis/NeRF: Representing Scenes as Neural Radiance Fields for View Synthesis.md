# NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis

## Abstract
(희소 이미지 view 셋)으로 (underlying continous volumetric scence function을 최적화)하여 (complex scene에 대한 view synthesis)  
  
1. Structure : FC DNN(non-conv.) 
2. Input____ : 5D 공간좌표(x,y,z) 및 시야 방향 (θ, φ)  
3. Output___ : 해당 위치의 Volume density & view dependent emitted radiance  
  
카메라 ray를 따라 5D 좌표를 쿼리하여 view synthesis + 고전적 volume rendering 기술을 사용하여 출력 색상과 밀도를 이미지에 projection한다.  
Volume rendering은 본래 구분할 수 있기 때문에 표현을 최적화하는데 필요한 입력은 알려진 카메라 포즈가 있는 이미지 세트뿐이다. 
Neural radiance field를 효과적으로 최적화하여 복잡한 기하학과 외관을 가진 장면의 사실적인 새로운 뷰를 렌더링하는 방법을 설명한다.

## Introduction
Continous 5D scene representation의 parameters를 직접 최적화하여 capture image set의 rendering 오류를 최소화함으로써  
오래 연구된 view synthesis 문제를 새롭게 해결한다.  
(x, y, z)에서 각 방향(θ, φ)에서 방출되는 광도를 출력하는 연속 5D 함수와 (x, y, z) 통과하는 광선에 의해 누적되는 광도를  제어하는  
차동 불투명도처럼 작용하는 각 지점의 밀도로 정적 장면을 나타낸다.  
우리의 방법은 단일 5D 좌표(x, y, z, θ, φ)에서 단일 볼륨 밀도 및 뷰 의존 RGB 색상으로 회귀하여  
이 기능을 나타내도록 conv. 없이 FNN를 최적화한다.  
  
특정 관점에서 이 신경 방사장(NeRF)을 rendering 하려면  
  
1) 카메라 ray를 scene으로 이동하여 샘플링된 3D 포인트 세트를 생성  
2) 이러한 점과 그에 상응하는 2D 보기 방향을 신경망에 대한 입력으로 사용하여 색상과 밀도의 출력 세트를 생성  
3) 기존의 volume rendering 기술을 사용하여 색상과 밀도를 2D 이미지로 축적  
  
이 프로세스는 자연적으로 미분 가능하기 때문에, 각 관찰된 이미지와 우리의 표현에서 제공된 해당 뷰 사이의 오류를 최소화함으로써  
이 모델을 최적화하기 위해 경사 하강법을 사용할 수 있다.  
여러 view에서 이 오류를 최소화하면 네트워크가 실제 기본 장면 콘텐츠를 포함하는 위치에 높은 볼륨 밀도와  
정확한 색상을 할당하여 장면의 일관성 있는 모델을 예측할 수 있다.  
그림 2는 이러한 전체적인 파이프라인을 보여준다.  
![image](https://user-images.githubusercontent.com/40943064/142862694-8fa77181-3d86-4769-b69e-8b59dc2d6c27.png)

복잡한 장면에 대해 신경 방사장 표현을 최적화하는 기본 구현은 충분히 높은 해상도 표현으로 수렴되지 않으며  
카메라 광선당 필요한 샘플 수가 비효율적이라는 것을 발견했다.  
우리는 입력 5D 좌표를 MLP가 더 높은 주파수 기능을 나타낼 수 있는 위치 인코딩으로 변환하여 이러한 문제를 해결하고,  
이러한 high-frequency scene representation을 적절하게 샘플링하는 데 필요한 쿼리 수를 줄이는 계층적 샘플링 절차를 제안한다.  
우리의 접근 방식은 체적 표현의 장점을 계승한다.  
둘 다 복잡한 실제 geometry와 외관을 나타낼 수 있으며 투영된 이미지를 사용한 그라데이션 기반 최적화에 매우 적합하다.  
결정적으로, 우리의 방법은 고해상도로 복잡한 장면을 모델링할 때 이산화된 복셀 그리드의 엄청난 저장 비용을 극복한다.  
   
요약하자면, 기여는 다음과 같다.  
  
– Complex geometry 및 materials를 가진 continuous scene을 5D Nerf로 표현하기 위한 접근 방식으로, MLP로 구성  
  
– RGB 이미지에서 이러한 표현을 최적화하기 위해 사용하는 기존의 volume rendering 기술을 기반으로 한 미분가능 rendering 이다.  
Visible scene content가 있는 공간에 MLP의 capacity를 할당하는 hierarchical sampling 전략이 포함된다.  
  
– 각 입력 5D 좌표를 더 높은 차원의 공간으로 매핑하는 위치 encoding으로, high-frequency scene content를  
나타내도록 nerf를 성공적으로 최적화할 수 있다.  

결과 nerf 방법이 neural 3D representation을 scene에 맞추는 작업과 샘플화된 volumetric 표현을 예측하기 위해  
deep CNN을 학습시키는 작업을 포함하여 SOTA view synthesis 방법을 양적 및 질적으로 능가한다는 것을 입증한다.  
우리가 아는 한, 이 논문은 자연 환경에서 캡처한 RGB 이미지에서 실제 물체와 장면의 고해상도 사실적 참신한 뷰를 렌더링할 수 있는  
최초의 연속적인 neural scence representation을 제시한다.  
