## 1. Major types of data problems

![image](https://user-images.githubusercontent.com/40943064/145487993-78b8f038-a0d1-4cf9-906c-766f10bddd9c.png)  
  
![image](https://user-images.githubusercontent.com/40943064/145489790-d82685e4-a5b9-4b3a-b943-b47f5d81701d.png)  
  
![image](https://user-images.githubusercontent.com/40943064/145490028-2b238fcc-6a69-485f-ba9b-351cfb9eb14b.png)  

1. Unstructured vs Structured   
: 이미지, 음성과 같이 자연적으로 발생하고 인간이 이해하기 쉬운 형태와 특징이 정돈되어있는 형태를 기준으로 구분한다.  
: Unstructured 데이터는 인간이 labeling 할 수 있으며 최근 여러 기법들이 개발되어 data augmentation도 용이함
2. Small vs Big :  
labeling을 하는데 있어 감당이 가능한 수준인지의 기준으로 정의한다. 개략적으로 10k 샘플을 기준으로 한다.  
Mislabed 데이터의 영향은 small 데이터에서 상대적으로 훨씬 크며 따라서 clean(일관되고 실수없는) 한 labeling이 더욱 중요하다.  
또한 수가 적기 때문에 개별적으로 labeling을 수행할 수 있고 labeling 방식의 통일이 용이하다.  

Big data의 경우 개별 샘플을 모두 볼 수 없기 때문에 데이터를 처리하는 과정에 더 큰 관심이 필요하다.  
(처리과정을 잘 정의해야 모든 labeler가 통일된 방식으로 labeling을 제대로 수행 할 수 있음)  

* 조언은 동일 사분면의 분야에서 종사한 사람에게 듣는것이 더 도움이 된다.  


## 2. Small data and label consistency
데이터가 매우 많다고 해서 꼭 좋은것은 아니다. 데이터가 적더라도 잘 정돈한다면 적은양으로도 훌륭한 결과를 얻어 낼 수 있다.  
따라서 일관성 있는 labeling은 매우 중요하다.  
예제 1)  
![image](https://user-images.githubusercontent.com/40943064/145491674-f4bc4abb-6ec7-44cf-9ddd-7e65a6d7c352.png)  
예제 2)  
![image](https://user-images.githubusercontent.com/40943064/145492126-8c2b228b-c8a7-445d-8e5b-b07c1fd16aff.png)  
 
 
 Big data 문제에서 역시 small data에서 발생하는 문제가 동일하게 발생한다.  
 Rare event가 long tail이므로 이러한 예제에 대해서는 마찬가지로 일관성있는 labeling이 마찬가지로 필요하다.
 (e.x., 자율주행 데이터를 획득할 때, 안전에 중요한 특정 상황의 데이터는 드물게 획득할 수 있음)
 
## 3. Improving label consistency

1. labeler들에게 동일한 샘플을 labeling 하도록 하고 다수의 결정을 따름
2. labeler 방법에 대한 정의를 모두가 동의하도록 약속함
3. x가 잘못됐다고 판단이 되면 x를 다시 제대로 취득(공정내 조명조건을 변경)
4. 앞선 방법들을 반복적으로 수행

동일한 기준으로 정의한 labeling을 통해 consistency를 확보하는 예제  
![image](https://user-images.githubusercontent.com/40943064/145494126-cb4ed4b3-b751-46e7-a2ab-fb98f4449c36.png)    
(항상 가능하지는 않지만 특정 경우에는 class를 단순화하여 정의하면 문제가 간단하게 해결 될 수 있다.  

![image](https://user-images.githubusercontent.com/40943064/145494533-0ac08e17-4402-443a-8458-2d1cf9d361d7.png)  
클래스가 명확하지 않아서 일관된 labeling이 불가능한 경우에는 boderline/uninteligible 같은 새로운 class를 만들어 명확하게 구분할 수 있다.  
  
![image](https://user-images.githubusercontent.com/40943064/145498272-3b8076d7-a0ad-40e1-a1df-507bca6c74b9.png)
(Big data에 대해서는, 일반적으로 두번째 방법을 많이 사용하지만 첫번째 방법을 우선적으로 사용하는것이 바람직함)  

## 4. Human level performance (HLP)
: ML 과제의 답은 근본적으로 모호하기 때문에 명확하게 정의하기 어려우며 baseline으로 활용 될 수 있지만 오용될 수도 있다.  
  
1. 가능한 성능 수준을 정의 : 누군가 과도한 성능을 요구했을때, HLP를 이용해 달성할 수 있는 수준에 대해 정의하고 설득할 수 있다.
2. 학계에서 landmark가 되는 성능 기준이 됨 : 인간의 수준을 뛰어넘은 자체로 의미가 있을때 활용된다.

HLP를 활용하는데 문제도 있을 수 있다.  
레이블링이 일관되기 어려운 불명확한 문제에 대해, HLP는 그러한 근본적 문제로 정확도가 낮아질 수 밖에없다.  
이러한 상황에서 ML은 높은 labeling 규칙을 따라 학습을 하게 되면 수치적으로 높은 성능은 얻을 수 있지만  
이러한 결과가 의미있는 정보를 가지고 있지는 않다.  


## 5. Raising HLP
HLP 기준을 향상함으로써 ML 성능도 높힐 수 있다는 전제하에 HLP를 향상하는 방안을 고민한다.  

외부에 의해 정의된 경우는 HLP는 Bayes error / irreducible error의 기준으로 활용 될 수 있으나  
인간이 labeling 하는 경우 일관성이 확보되지 않아 HLP가 매우 낮을 수 있다.  
이러한 유형의 문제는 일관성을 확보해 labeling을 재수행하므로써 HLP를 향상할 수 있다.  
HLP가 향상하면 ML이 달성해야 하는 목표가 높아지지만 한편으로는 clean 데이터를 획득함으로써 높은 성능을 달성할 수도 있다.  

일부 structured 데이터에도 동일한 기준을 적용할 수 있는 경우가 있다.  
User ID merging, 네트웍 트레픽이 올라갔을때 컴퓨터가 해킹되었는지 여부, 사기판별 여부 등의 문제는 인간의 labeling이 가능한 경우이다.  
따라서 이러한 유형에도 동일한 process를 적용할 수 있다.  


