## Welcome
ML project의 전체 life cycle에 대한 높은 이해를 갖도록 하는것이 목표

### Deployment example
 
Edge device를 이용해 자동 결함 검사를 수행한다.  
Edge device의 sw는 생산 라인이 시작되면 사진을 찍고 API call을 해서 예측서버에 사진을 전송시킨다.  
예측 서버는 예측을 수행한 후 edge device로 결함 여부를 return 한다.  
그러면 inspection software는 제어결정(라인중단/이상제품제거)을 수행한다.  

머신러닝 관점에서는 이미지 X를 y 결함여부와 mapping하여 학습하여 prediction server에 올리고  
API 세팅을 하고 sw 나머지 부분을 작성함으로써 공정에서 학습 알고리즘을 deploy 한다.  

prediction server는 때로 **cloud**나 **edge device**에 설치될 수 있다.  
대부분 인터넷 접속이 불가하므로 공정에는 edge device에 설치된다.  

위 과정에 대한 코드를 모두 작성하면 어떤 문제가 발생할 수 있을까?  
주어진 데이터셋에 대해 잘 작동하더라도 여러 어려운 문제가 발생할 수 있다.   
  
![image](https://user-images.githubusercontent.com/40943064/143870874-ab7d7567-56b1-49a2-9c02-22ffd43cd368.png)  

### Problem 1. Visual instpection example 
일반 정상/결함 이미지를 통해서는 판단이 어렵지 않다.  
이미지를 얻어서 보면 데이터셋에서 얻은 이미지와는 다른 분포(측정된 시간 차로 인한 조도 차이 등)를 가진 이미지를 얻기 때문이다.  
![image](https://user-images.githubusercontent.com/40943064/143871418-81103d99-affd-47d0-8134-4b1b17414db6.png)  
이런 문제를 **concept drift** / **data drift**라고 한다.

성공적으로 ML을 학습하고 좋은 결과를 얻어도 deploy를 위해서는 많은 시간이 추가로 필요하다.  
누군가는 아니라고 할 수 있지만 데이터가 변하는 문제는 ML engineer가 고려해야할 문제이다.  

### Problem 2. ML in production
ML 모델은 발전을 거듭해왔지만 공정에서 5%-10% 의 수준만 차지하는 정도로 일부의 영역이다.  
![image](https://user-images.githubusercontent.com/40943064/143872614-ff742e2c-d4b0-4bc2-ab23-4c356ce1c6dd.png)
위처럼 생산 공정에서 고려 해야 할 많은 영역들이 있다.  
  
## Steps of an ML Project
ML lifecycle 을 전체적으로 보는것은 수행해야 할 전체 스텝들을 계획하는데 매우 효과적인 방법이다.  

1. Score : 프로젝트 정의, 작업 결정(x,y가 무엇인지? 무엇을 하려고 하는지?)  
2. Data : 데이터 정의, baseline 정의, 데이터 정돈 및 labeling 수행  
3. Modeling : 모델 선택 및 학습 , 에러분석 수행  
- 에러 분석을 통해 이전 단계로 돌아가는 등의 반복적인 작업이 발생  
4. Deployment : 생산에서의 deploy, monitoring & maintain system  
- 초반 deployment시 data drift와 같은 문제로 앞단계로 돌아가는 반복 과정이 발생  
![image](https://user-images.githubusercontent.com/40943064/143873850-ce045b1d-9509-40dc-b643-e6538f1703df.png)  

## Case study: speech recognition
ML lifecycle을 잘 이해할 수 있도록 유명한 예제인 speech recognition 문제에 적용해 보자  
![image](https://user-images.githubusercontent.com/40943064/143876205-f345c829-e40a-4048-8432-934c3f2c3ab0.png)  
![image](https://user-images.githubusercontent.com/40943064/143877353-2b5be542-0283-4f3c-92a6-1df5061997a0.png)  
