**학습목표**
1. 선형회귀 소개및 모델링 방법
2. 최고의 연습 사례
3. 에러 측정

**Introduction to Linear Regression**  
  
![image](https://user-images.githubusercontent.com/40943064/121533205-06268100-ca3b-11eb-9ae4-77adc1b8453e.png)  
![image](https://user-images.githubusercontent.com/40943064/121533563-5ef61980-ca3b-11eb-84e1-92776425d847.png)  
  
주어진 데이터에서 beta와 x로 구성된 선형 수식을 설정하여 최적의 선을 맞춘다.  
여기서 costfunction을 최소화하여 beta(paramter)를 얻어낸다. 
  
**Calculating the Residuals**  
![image](https://user-images.githubusercontent.com/40943064/121533724-864ce680-ca3b-11eb-89a5-06bbc9089229.png)  

**Minimizing the Error Function**  

![image](https://user-images.githubusercontent.com/40943064/121534187-f5c2d600-ca3b-11eb-9b8a-e35ad0d16f25.png)
  
**Modeling Best Practice**  
모델링에있어 모범 사례는 우리가 최소화하고자 하는 cost function을 먼저 세우는것이다.  
이것이 모델간 성능을 비교하는 방법을 제공해 주는 것이다.  
그 후 최고 성능을 내는 모델을 찾기 위해 여러 hyperparameter로 여러 모델들을 테스트 한다.  
그리고 마지막으로 우리의 cost function에 최고로 잘 맞는 결과를 비교선택한다.  

**Other Measures of Error**  
MSE와 별개로 또다른 중요한 척도는R square이다. 그리고 이것의 구성요소를 분해한다.  
![image](https://user-images.githubusercontent.com/40943064/121535174-e001e080-ca3c-11eb-87b1-7c747334ba31.png)   
![image](https://user-images.githubusercontent.com/40943064/121535445-25bea900-ca3d-11eb-9877-3ef05e13e0dc.png)   
SSE(Sum of squared errors) : 회귀 추정 y의 편차제곱의 합  
TSS(Total sum of squares) : 총변동 : 개별 y의 편차 제곱의 합  
R^2 : 1 - SSE / TSS : R-squared (R제곱;결정계수) : 총 변동 중에 설명된 변동의 비율  
  
즉, y-ybar의 총 변량(TSS)에서 yhat-ybar는 설명가능한 변량(SSR) y-yhat은 설명 불가한 변량(SSE)이므로  
SSR/TSS은 설명가능한 변량이 총변량에서 차지하는 비율을 의미하기 되며 1에 가까우면 설명하는 변량이 y와 동일함을  
의미 하며 모두 설명할 수 있음을 의미한다.

**Linear Regression: The Syntax**  
![image](https://user-images.githubusercontent.com/40943064/121545203-42f77580-ca45-11eb-816f-e03b60b99f94.png)
