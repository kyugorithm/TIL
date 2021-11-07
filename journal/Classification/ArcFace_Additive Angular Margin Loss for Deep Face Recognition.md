## Abstract
대규모 얼굴인식을 위한 DCNN을 이용한 feature 학습의 주요과제 : 분류성능 향상을 위한 **`적절한 loss funciton 설계`**  
Center loss는 deep feature와 클래스 내 compact성을 얻기위한 class center와의 uclidian distancce를 penalise.
![image](https://user-images.githubusercontent.com/40943064/124759144-4b6e9d80-df6a-11eb-9150-400a7d3c5a51.png)  
SphereFace 마지막 FC의 선형변환 행렬이 각도공간에서 클래스 센터로 사용되고 deep feature와 그에 해당하는  
weight 사이 각도에 곱셈방식으로 margin을 penalise한다.  
![image](https://user-images.githubusercontent.com/40943064/124759809-0b5bea80-df6b-11eb-9274-b35472108b9a.png)

최근, 유명한 연구분야는 얼굴 class 분별력 최대화를 위해 loss function에 **`margin을 결합`** 하는것이다.  
본 논문에서 우리는 얼굴인식을 위해 매우 분별력있는 특성을 얻기 위해 **`additive angular margin loss`** 를 제안한다.  
Hypersphere 측지거리에 해당하는 정확한 일치 때문에 제안한 ArcFace는 명백한 기하적 해석을 가진다.  
![image](https://user-images.githubusercontent.com/40943064/124760815-13685a00-df6c-11eb-9558-79adf5070830.png)

우리는 10개 이상의 얼굴 인식 벤치마크에서 모든 최신 얼굴 인식 방법에 대한 가장 광범위한 실험 평가를 제시한다.  
ArcFace가 SOFA를 뛰어넘으며 무시할만한 계산적인 over-head를 가지고 쉽게 구현됨을 보인다.  
우리는 논문재생산에 도움이 되는 모든 자료를 공개한다.

## Introduction
관분야 소개  

### ArcFace의 장점

**Engaging**
1. normalized hypersphere에서는 각도와 호가 동일하므로 측지선 margin을 직접적으로 최적화 할 수 있다.  
2. 직관적으로 직관적으로 512차원에서 발생하는 상황을 feature와 weight간 각도의 통계로써 묘사한다.  
  
**Effective**
10개 DB에 대하여 SOTA 성능을 가짐 
  
**Easy**
알고리즘을 구현하기 위해 단지 몇개의 라인만 추가하면 되며 구현 난이도가 매우 쉽다. 
 
**Efficient**  
학습동안 계산복잡도가 무시할만큼 낮다. 
