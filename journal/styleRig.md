### 3D morphable model DB
아래 그림과 같이 3D의 얼굴 형상을 Scan하여 남성100명 여성100명 총200명에 대한 형상 정보를 기록한 DB가 존재한다.  
이 데이터를 seed로 하여 각 데이터셋간의 선형 조합으로 모든 사람의 얼굴을 표현하고자 한다.  

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122213191-a9681200-cee3-11eb-85a1-be25b3f3146c.png" alt="factorio thumbnail" width=300 />
  </p>
  <p align="center" style="color:gray">
        <em>200명의 scan DB (남/여 각각 100명)</em>
  </p> 
 
 ### Morphable 3D Face Model
3차원 공간에 n개의 landmark point를 통해 얼굴을 표현하며 shape vector S와 색감을 표현하기 위한 texture vector T가 존재한다.  
각 얼굴에는 약 7만개 point가 존재하며 각 포인트는 XYZ로 표현한다. 그러므로 shape vector는 약 3X70k = 210k개의 차원을 가진 벡터가 되고,  
texture vector 역시 하나의 포인트를 표현하는데 RGB가 필요하도록 되어있어 동일하게 210k개의 차원을 가진 벡터가 된다.  
  
<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122214042-9ace2a80-cee4-11eb-95aa-379532e7c6f9.png" alt="factorio thumbnail" width=450 />
  </p>
  
이때, m명의 사람(m exemplars)를 조합하여 새로운 모델을 표현하는 morphable model을 구성하면 아래와 같이 나타낼 수 있다.   

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122215528-488e0900-cee6-11eb-9b33-8fc49a5b13bb.png" alt="factorio thumbnail" width=350 />
  </p> 
  
여기서 ai는 shape vector에 대한 계수, bi는 texture vector에 대한 계수이다. 그리고 m개의 exemplars에 대한 각 계수의 합은 1이다.  
Si, Ti는 각각 한개의 exemplar에 대한 데이터를 의미한다. 결국, 모델이 표현하는 바는 weighted sum을 통해 얼굴을 표현하는 것이다.  

선형결합을 통해 생성한 얼굴은 이상한 모습을 할 수 있기 때문에 그럴듯함(plausibility)를 정량화 하여 표현해야 한다.  
이는 예제 얼굴 세트의 파라미터 확률분포 추정하고 이 추정된 파라미터의 확률분포에 대해 새롭게 생성된 얼굴의 파라미터 조합이  
추정분포에 가깝게 만들어졌는지를 한다. 즉, exmaplar에 대한 파라미터 최적화를 수행하고 최적화된 파라미터의 분포를 사전  
확률분포 p(a), p(b)라 하면 새 얼굴에서 우리가 얻은 파라미터 a, b의 조합이 prior에 가까운지 평가하여 그럴듯함을 평가할 수 있다는 것이다.  
즉, 추정 분포에서 멀어질 수록 그럴듯한 얼굴이 아니게 되는 것이다.  
(확률분포에 대한 설명은 생략)  

위 모델을 통해 plausibility를 고려하여 새로운 얼굴을 생성할수 있지만, 차원의 문제가 존재한다.  
S와 V가 210k개의 차원을 가진다고 했기 때문에 해당 vector에 대해서 최적의 얼굴 조합을 찾는 일은 계산량이 매우 큰 문제이다.  
이때문에 논문에서는 PCA를 사용한것 같다. m개의 exemplar에 대하여 한번에 PCA를 수행하여 저차원의 PCA component vector  
를 생성하고 이들의 결합으로 새로운 얼굴을 표현하는 새로운 모델을 아래와 같이 표현할 수 있다.  
  
<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122218375-58f3b300-cee9-11eb-904c-06e2a6dc0867.png" alt="factorio thumbnail" width=500 />
  </p>
  여기서 Sbar, Tbar는 모든 exemplar의 평균이 되는 PC component이며 이 값에 shape PC component vector si  
  texture PC component vector ti 각각에 대한 alpha, beta의 조합으로 모델이 구성된다.  
  (참고로 생성된 Smodel, Tmodel은 PCA 계산시 얻어진 kernel을 곱하여 다시 역변환을 수행하며 이때  
  210k -> 3 차원 차이가 dramatic하게 존재하므로 비가역적 정보손실이 발생하여 품질 저하가 있을것으로 예상된다.  
 
 ### Segmented morphable
 바로 위에서 말했던것 처럼 차원의 차이로 인해 PCA의 정보손실이 매우 커지는 문제가 발생하고 이를 해결하기 위해서  
 70k의 landmark point를 여러 segment로 분할하는것으로 추측된다. 눈, 코, 입, 주변 등으로 분할하여 각각에 대해 모델을  
 적용하면 차원이 낮아지기 때문에 PCA로 인한 손실이 매우 낮아질 수 있을 것이다.(추가로 1990년도임을 고려하면 차원이 커질수록  
 PCA계산 시간이 O(n^2)가 되어 매우 challenging하기 때문에 낮추는것일 수도 있을것같다.
   
<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/40943064/122221217-09fb4d00-ceec-11eb-8375-4fe8475c12ae.png" alt="factorio thumbnail" width=500 />
  </p>
   

  
 블로그 참조 :  
 https://wdprogrammer.tistory.com/59
