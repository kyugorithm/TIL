
### Beyond a single test set : Cross validation

![image](https://user-images.githubusercontent.com/40943064/122763955-e401ee00-d2d9-11eb-9801-404a40175d62.png)  
단일 학습/테스트에서 얻은 결과는 우연한 확률일 수 있기 때문에 확률적 신뢰를 더 확보하기 위해서는 여러 학습/테스트 셋으로 분할하여 그 결과를 평균하여 얻는 것이다.

![image](https://user-images.githubusercontent.com/40943064/122764503-80c48b80-d2da-11eb-859a-99a6c165d53e.png)
이처럼 겹치지 않는 방식으로 변경하며 세트를 생성하고 검증하는 것이다.

![image](https://user-images.githubusercontent.com/40943064/122764602-989c0f80-d2da-11eb-84d7-2f3d66e74e9f.png)  

### Model complexity vs. Error

![image](https://user-images.githubusercontent.com/40943064/122765051-106a3a00-d2db-11eb-93ed-8db8315e05ca.png)  
Underffitng : Training & cross validation errors are both high  
Overfitting : Traning error is low, cross validation is high  
Just right : Training & cross validation errors are both low  

### Cross validation approaches

![image](https://user-images.githubusercontent.com/40943064/122765260-4ad3d700-d2db-11eb-8783-a7689730637e.png)

### Cross validation : The syntax
![image](https://user-images.githubusercontent.com/40943064/122765536-91293600-d2db-11eb-834e-0449b663169e.png)
