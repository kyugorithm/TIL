**학습목표**  
- 학습/테스트 샘플 분리  
- 교차검증방법들  
- 모델복잡성 vs 에러 trade-off  
  
**학습/테스트 샘플 분리 **  
![image](https://user-images.githubusercontent.com/40943064/121656448-71736000-cada-11eb-8a78-8023e9faec9a.png)  
  
모든 데이터를 외워서 학습하면 학습한 샘플에 대해서는 100% 정확도를 가질 수 있다. 그러나 보지 못한 샘플에 대한 성능은 보장되지 않는다.  
따라서 우리는 학습과 테스트 샘플을 분리해서 학습/테스트를 단계적으로 수행해야 한다.  
  
**학습/테스트 샘플 사용단계 **  
![image](https://user-images.githubusercontent.com/40943064/121656742-c31bea80-cada-11eb-8de6-69f9f75babf9.png)  
학습 샘플로 학습 -> 테스트 샘플로 성능 평가  
![image](https://user-images.githubusercontent.com/40943064/121656792-cfa04300-cada-11eb-8703-1f459c7fd2a5.png)  
  
**문법**  
![image](https://user-images.githubusercontent.com/40943064/121656840-dc249b80-cada-11eb-92f1-e38e5509b2d5.png)  
