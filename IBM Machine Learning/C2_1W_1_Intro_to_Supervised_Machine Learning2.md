## Introduction to Supervised Machine Learning: Types of Machine Learning

#### 머신러닝의 종류
![image](https://user-images.githubusercontent.com/40943064/121360061-0a856800-c96f-11eb-9491-4c67981c371e.png)  


 
**Supervised ML Framework**  
![image](https://user-images.githubusercontent.com/40943064/121373580-28a49580-c97a-11eb-8534-2fea5177b15b.png)   
![image](https://user-images.githubusercontent.com/40943064/121377853-a74f0200-c97d-11eb-846b-e69629e882b0.png)  
  
1) Ω : parameters  
- 학습과정과 함께 변경되는 값  
- 차후 과정에서 Hyperparameter를 배울텐데 학습하는 값이 아니고 직접 결정하는 값이다.(절편을 넣을지 말지 선택등)  
- 여러 기법들을 적용해서 파라미터 선택하는 방법도 연구할 것이다.  

2) x : input(Observations : 행 또는 한개의 샘플의 단위, Features : 열으로 각 특성에서 측정하는 여러 특성)  
yp 와 y는 분리해서 사용
x는 하나 이상의 행과 열 , y는 하나 이상의 행과 한개의 열을 가짐 (x, y의 행은 같음)  

3) loss : 
- 대부분의 모델은 얼마나 예측을 잘했는지에 대한 척도를 수치형 점수로 나타낸다.
- 전형적으로 실제값과 얼마나 가까운지를 측정한다.  
4) Update rule : 
- 특성 x와 y를 이용하여 J를 최소화하는 Ω를 선택한다.
6) Regression : 수치형 변수를 예측하는 경우(주가, 박스오피스수익, x, y 위치등)
7) Classification : 범주형 변수를 예측하는 경우 (얼굴인식, 이탈예측, 다음에 올 단어예측 등)
고객이탈사례를 예를들면 x는 고객이 유지한 기간, 월별 구독료등 이탈여부를 예측하는데 도움을 주는 것들이다.  
그러면 예측하는 값은 이탈 여부의 True/False 값이다.  
한개의 샘플은 한명의 고객이다. 대하여 그들이 지불하는 월별 구독료는 하나의 column이 된다.  

각 샘플 x는 일부 결과 변수 y와 관련되며 데이터 과학자는 주어진 샘플들에 기반하여 최고의 Ω를 찾는 모델을 학습한다.
샘플이 많을 수록 ML 모델은 x와 y 간 관계를 정의하는 Ω를 더 잘 학습할 수 있다.  

![image](https://user-images.githubusercontent.com/40943064/121376994-f6e0fe00-c97c-11eb-86d5-45e22351ca03.png)  
그런데 학습하는데 있어 모든 샘플을 학습에 이용하지는 않는다. 매우 복잡한 모델이 원하는 경향이 아닌  
특정 패턴을 학습해버릴 수 있기 때문이다.  
따라서 우리가 원하는것은 새로운 샘플에 대해서도 적용될 수 있도록 일반화된 모델을 학습하는 것이다.  
그래서 일부 데이터에 학습하고 학습되지 않은 hold out 샘플에 대해 테스트하여  
실제 새로운 샘플이 들어왔을 때를 대비한다.  

다음 단계에서는 여러가지 종류의 supervised ML를 다룰것이다.
