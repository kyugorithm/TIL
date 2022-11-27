# Abstract
FOV(field-of-view)가 넓은 사진은 왜곡이 강하게 발생한다.  
이를 전문가의 수동 수정이 아닌 알고리즘 접근을 통해 해결한다.  
알고리즘은 다른 부분은 왜곡하지 않고 되돌려야하는 얼굴만 수정한다.  
#### 핵심
아래 두개조건을 만족하도록 **content-aware warping mesh**를 생성하는 최적화문제를 구성한다.
1) 얼굴 : Locally adapt to the stereographic projection
2) 배경 : Seamlessly evolve to the perspective projection  

## 1. INTRODUCTION
### 1. 배경
최신 카메라는 많은 object를 담을 수 있음
### 2. 문제점
왜곡 발생
### 3. 해결방법
입력 이미지가 주어지면 입력 이미지 위 coarse 메시에 vertex별 가중치를 할당하기 위해 대상 마스크를 계산한다.  
구와 평면 사이의 conformal mapping인 stereographic projection을 locally emulate 하도록 facial vertex를 encourage하는 energy term을 구성한다.  
방법론의 출력은 stereographic & perspective projections를 단일 이미지에 대해 결합한다.  
제안하는 energy function은 얼굴 경계에서 충돌하는 두개의 projection들 사이에서 **부드러운 transition을 장려**한다.  
### 4. 성능검증
다양한 이미지에 대해 검증 + 빠른 속도  
### 5. 기여
왜곡을 자동으로 해결하는 알고리즘을 제안하며, stereographic & perspective projection을 얼굴과 배경에 대해 통합한다.  

## 2. RELATED WORK
### 3D Projection.
3D projection은 필연적으로 렌더링된 2D 이미지에 왜곡을 초래한다. Perspective projection은 카메라 중심에서 멀리 떨어진 물체에 대해 인식된 형상을 왜곡하는데, 특히 카메라 FOV가 우리의 시각 시스템의 편안한 영역보다 넓을 때 그렇다. 르네상스 초기까지 거슬러 올라가는 예술가들은 이미 원근 왜곡을 발견하고 그것을 "**anamorphosis**"라고 부른다. 그들은 FOV가 60°를 넘으면 건축 장면과 같은 더 넓은 그림을 조심스럽게 다룬다.  

휴대용 카메라로 단체 사진을 찍으려면 60°보다 넓은 FOV가 필요한 경우가 많다. GoPro 카메라 및 파노라마와 같은 광각 이미지의 경우 투시 왜곡을 완화하기 위해 stereo, Mercator 및 Pannini projection이 널리 사용된다. 이러한 global projection에는 인간이 만든 구조에서 흔히 볼 수 있는 길고 돌출된 직선 가장자리가 구부러지는 부작용이 있어, 결과적으로 photorealism의 손실을 초래한다(그림 2). 우리의 방법은 line-bending artifacts를 피하기 위해 locally adaptive mesh를 사용한다.  

### Lens Distortion.
렌즈 왜곡은 렌더링된 이미지에서 아티팩트를 유발하는 또 다른 요인이다. 렌즈 왜곡은 렌즈 설계 과정에서 기인하며 광각 렌즈의 경우 피하기 어렵다. 일반적으로 이미지 모서리의 직선을 왜곡한다. 왜곡 프로파일은 보정할 수 있으며 다양한 방법으로 이 문제를 해결할 수 있다.  

그러나 렌즈 왜곡 보정 이미지는 여전히 perspective distortion을 보인다. 초상화 사진작가들은 망원 렌즈를 사용하거나 피사체를 카메라 센터로 조심스럽게 안내해야 한다. 우리의 방법은 카메라 뷰의 모든 곳에서 얼굴을 수정하고, 초상화 사진작가를 이러한 구성 제한으로부터 자유롭게 한다.

### Perspective Distortion Manipulation
Projection center는 왜곡이 없기 때문에 새로운 가상 카메라 뷰나 planar projection geometry를 가진 새로운 영상 평면을 신중하게 선택하여 후처리의 왜곡을 줄일 수 있다. 기존 방법은 Photoshop의 Perspective Warp 기능과 같이 수동으로 결정된 글로벌 homography warping을 적용하거나 자동으로 적용한다. 대신, 우리의 작업은 원본 샷의 시야각과 FOV를 보존하기 위해 로컬 보정을 수행한다.  
  
몇 가지 mesh 기반 방법은 사용자가 straight line 또는 vanishing point와 같은 scene constraint를 제공하고 conformality cost과 같은 왜곡 메트릭을 최소화하여 결과를 생성해야 한다. 대조적으로, 우리의 알고리듬은 완전 자동이며 즉각적인 공유를 위해 모바일에서 실시간으로 실행된다.  

### Content-Aware Warping
우리의 방법은 다양한 image manipulation, 즉 panorama stiching 및 reshaping, 광각 이미지 및 비디오 수정, 이미지 및 비디오 대상 변경, texture deformation, stereoscopic 편집 및 비디오 stabilization에 적용되어 온 content-aware warping에 속한다. 일반 객체의 기하학적 구조를 복원하는 기존 방법과 달리, 우리의 작업은 특히 인물사진을 다룬다. 인간의 눈은 얼굴의 artifact에 매우 민감하기 때문에, face-specific 문제는 여러 얼굴이 함께 있을 때 특히 어렵다.  

### Face Undistortion
Fried는(Perspective-aware Manipulation of Portrait Photos) 3D 얼굴 모델을 사용하여 카메라 초점 거리를 조정하여 초상화의 왜곡을 줄인다. 우리 작업은 피사체 수가 임의인 단체 사진, 얼굴 포즈, occlusion 등 야생에서 촬영된 초상화를 강화한다. 이러한 경우 정확하고 강력한 얼굴 모델을 얻는 것은 어렵다. Foreshortening은 얼굴이 카메라에 매우 가까이 있을 때 발생하며, 우리의 작업과는 다른 얼굴 왜곡 문제이다.  

아름다움에 대한 통계적 합의에 의존하는 얼굴 미화와는 달리, 우리의 목표는 사진 옆면의 얼굴을 최소한의 왜곡으로 카메라 중심에서 찍은 것처럼 보이게 하는 것이다. 이를 달성하기 위해, 우리는 미적 선호도에 의존하지 않고 단일 이미지에서 두 가지 다른 projection geometry의 조합 사용한다.  

## 3 PRELIMINARIES AND OVERVIEW
<img width="1525" alt="image" src="https://user-images.githubusercontent.com/40943064/204079915-d49d3c23-bd97-4b84-98e1-021c15619d1e.png">

이미지 입력은 perspective projection된 것으로 가정한다.  
1) 인물 segmentation mask를 계산함으로써 먼저 얼굴 영역을 확인  
2) Camera focal length를 이용해 stereographic projection 추정
3) Energy minimization을 이용해 얼굴 영역에 대한 국소 stereographic warp를 수행하는 target mesh를 계산
(이 단계는 배경의 전체적인 모습을 바꾸지 않고 얼굴을 교정하는 최적화된 메시를 출력)
4) 얼굴의 왜곡을 되돌리기 위해 최적화된 매시를 이용해 입력을 warp

