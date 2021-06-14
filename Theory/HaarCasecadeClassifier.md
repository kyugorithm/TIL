**Haar Cascade Classifier**  
OpenCV에서 제공하며 1) 이미지의 밝기 차에 따라 Haar-like feature를 추출한 후 2) Adaboost를 이용하여 중요 feature를 걸러내고  
3) casecade를 이용하여 중요도에 따라 순서를 정하여 가속화함으로써 특징에 따라 대상을 분류하는 알고리즘이다.  

**Haar-like Feature**  

아래의 사각형은 'kernel' 이라고 정의한다. 이미지의 x와 y좌표(window sliding)를 이동해가며 **흰색 영역 픽셀 합 - 검정색 영역 픽셀 합** 과 같이 차를 통해  
임계점이상 차이가 존재하면 특징점으로 추출하는 방식을 사용한다. 
![image](https://user-images.githubusercontent.com/40943064/121895151-dfc65580-cd5a-11eb-8439-86e71e0597c1.png)  


**Integral Images**  
위와같은 feature 계산방식은 계산량이 무지하게 많다. 다양한 kernel 형태에 대해서 박스의 크기를 바꿔가며 모든 픽셀에 대해 sliding을 하며 계산을 하기 때문에  
O(n^2)의 복잡도로 계산이 수행된다. 이러한 문제를 줄이기 위해 이미지의 픽셀에 따른 적분값을 사전에 계산해 둠으로써 계산량을 줄이는 기법을 사용한다.  


**Adaboost**  
엄청 중요한 알고리즘인데 Adaptive 하게 boosting 기법을 사용하여 학습 성능에 따라 샘플에 대한 중요도 차등을두어 여러개의 학습을 순서대로 학습하는 방식을 적용한다.  
이 방법을 이용하면 각 kernel * 크기 * 위치에 따라 만들어진 수많은 feature의 얼굴 탐색 성공여부에 따라 진짜 의미있는 feature를 찾을 수 있게 된다.  
Adaboost의 방법론은 강필성 교수님의 youtube 강의를 참조하였다.  
<https://www.youtube.com/watch?v=Y2rsmO6Nr4I>
![image](https://user-images.githubusercontent.com/40943064/121895925-b8bc5380-cd5b-11eb-8f16-e00c299c1d3d.png)
**추가 이해 및 정리 필요**


**Cascade Classifier**  
이미지에서 얼굴에 해당하는 Haar Feature를 활용하여, 얼굴을 찾는다.
(정확하게는 윈도우 내에 Haar Feature가 있어, 윈도우가 더 큰 개념인 것 같다. 약간 '초점을 맞춘다' 해야하나)
이미지 대부분 공간은 얼굴이 없는 영역이기 때문에, 지금 현재 윈도우 영역에 얼굴이 있는지 빠르게 판별하기 위해서 단계별로 진행한다.
낮은 단계에서 얼굴이 존재하지 않는다고 판단되면, 다음 단계는 확인도 하지 않고 넘어가는 식이다.
**추가 이해 및 정리 필요**

![image](https://user-images.githubusercontent.com/40943064/121896638-7cd5be00-cd5c-11eb-82e6-19f68990bcb9.png)  
최소 box 크기, threshold등의 세팅값을 변화시킴에 따라 검출결과가 많이 달라진다.
