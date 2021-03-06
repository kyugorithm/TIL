### Data Cleaning
#### 데이터 클리닝이 왜 중요할까?
 **결정과 분석**은 점점 **데이터와 모델**에 의해 결정된다.  
 ML 개발과정의 핵심측면들은 cleaned data에 있다.
 - **Obervations** : An data instance (point, row in dataset)
 - 관측치가 clean하지 않다면 우리는 모델, 특징과 목표사이 관계를 잘못 학습할 것이다.
 - **Labels** : An data instance (point, row in dataset)
 - 올바른 label 값을 가지도록 해야한다.
 - ImageNet을 생각해보면 labeling 을 하나라도 잘못 붙이게 된다면 모델이 잘못된 방향으로 학습 될 것이다. 
 - **Algorithms** : 가용 데이터를 기반으로 모델을 추정하는 프로그램
 -  실제 세상을 제대로 알려줌으로써 알고리즘은 학습을 해나간다고 가정할 수 있다.
 - **Features**, **Model**, ...

결론적으로 지저분한 데이터는 "Garbage in, garbage out" 효과로 이어질 수 있으며, 따라서 데이터셋이 제공되면 신뢰할 수 없는 결과를 얻을 수 있다.  
모든것의 첫 번째 단계는 항상 데이터가 깨끗한지 확인하는 것이다.

기업이 직면하는 문제들 
1. 데이터 부족 : 모델이 성공하기 위해서는 데이터가 충분해야한다.
2. 데이터 과잉 : 서로다른 환경과 DB에 너무 많은 데이터를 분산하면 데이터 엔지니어링 문제가 빠르게 발생하며 데이터를 정리하는데 관점을 둬야한다.  
3. 잘못된 데이터 : GIGO / 데이터를 개선해도 품질을 관리하는데는 매우 큰 어려움을 격고 있다.  
결국, 데이터를 실제로 사용할 수 있는 단계인지를 확인해 봐야한다.

#### 지저분한 데이터에서 발생하는 문제들
모델에 추가적인 가중치를 주거나 불필요한 노이즈가 생길 수 있다.  
**복제/불필요한 데이터** : 신용카드 데이터에서 사기 label를 달고 200번을 반복한다면, 관련 모든 feature들은 훨씬 더 큰 비중을 차지하게 될 것이다.(원하지 않게)  
**텍스트와 오타가 일치하지 않는 경우** : 데이터는 종종 올바른 철자에 따라 달라진다. 대문자와 대문자가 아닌 문자 중 추가 공백이 없도록 하여 모두 동일한 피쳐 값, 동일한 피쳐 값이 동일해야 하지만 동일한 피쳐 집합 내에서 다른 값으로 분류된다.  
**Missing Data** : 데이터 누락은 어떻게든 처리해야한다. 혹시라도 feature를 잘못 제거하는 경우 강력한 예측변수를 없애게 될 수도 있다.  
**outlier** : 특이치가 발생하면 형상이 불균형적으로 치우쳐 실제 기본 모델을 찾기 어려울 수 있다.  
**Sourcing issues** : Multi systems, differnt DB types, on promises, in cloud, ...  

#### 복제값 불필요한 값을 확인하는 방법
복제 값을 관심있게 보고 왜 여러 값이 생겨났는지 연구해본다.  
사용하는 feature들을 보고 필요하면 fitler를 건다.  
혹시라도 데이터가 복제되어 있지만 실제세상에서 가능한 경우가 있으니 조심한다.  

#### outlier를 처리하는 규칙
**Remove row** : 쉽게 clean data를 만들 수 있지만 많은 행이 결측치를 가지고 있고 이를 다 제거하면 너무 많은 정보를 잃거나 특정데이터만 제거하여 바이어스가 발생할 수 있다.  
**Impute** : 문제있는 값을 다른 값으로 대체한다. (평균값, 중간값, 다빈값) row, col을 잃지 않는 장점이 있지만 데이터에 **다른 유형의 불확실성**을 추가하게 되는 것이다.   
**Mask** : 결측치만의 category를 만든다. 결측치 자체가 중요한 정보를 줄 수 있다. 전화조사를 할 때 응답하지 않는 사람의 경우 그러한 정보를 추가로 우리에게 제공해주는 것이다. 이때 장점은 마찬가지로 행이나 열을 제거하지 않아도 되는 것이지만 단점은 우리의 missing value 모두가 같은 수준의 값이라는 가정을 함으로써 다른 수준의 불확실성을 추가하는 것이다.    

### Outlier : 다른 대부분의 관측값들과는 거리가 떨어져 있는 관측치

Oulier는 보통 관찰은 수차이며 모델으로 설명하려는 현상의 정확도를 흐린다. 
10~50사이의 가치가 지속되는 가운데 3000의 값이 포함되어있는경우를 생각해보자. 데이터 샘플이 적은경우 값을 평균화하면 200~300까지 원하지 않는 큰 값이 얻어질 수 있다. 이를 피하기 위해 값을 버릴 수 있다. 이경우 데이터를 처리하지 않으면 원하지 않는 모델 결과를 얻게 될 수 있다.  
그러나 일부의 outlier는 데이터에 대한 통찰력을 제공할 수 도 있다. 3000의 값이 발생한 이유를 파악하고 실제 세계에서 발생할 수 있는 경우 유용할 수 있다. 이러한 경우에는 plot, boxplot을 이용하여 발견할 수 있다.

####  Detecting Outliers : Statistics
```python
# Plot a histogram and density plot
sns.displot(data, bins=20);
# plaot a box plot
sns.boxplot(data);

q25, q50, q75 = np.percentile(data,[25,50,75])
iqr = q75-q25 # interquartile range
min = q25-1.5*(iqr) # 최대 oulier 기준값 설정
max = q25-1.5*(iqr) # 최소 oulier 기준값 설정
print(min,q25,q50,q75, max)
```

####  Detecting Outliers : Residuals(실제값과 예측값 간의 차이)는 모델의 실패정도를 나타낸다.

- Standardized : 해당에러/표준에러  
- Deleted      :해당 관측치를 제외한 모든 데이터에 대해 학습된 모델로부터의 잔차
- Studentized  : 해당에러 /residal 표준에러(전체데이터 혹은 현 관측치를 제외한 전체 데이터 기반)

#### Policies for Outliers
Outlier를 탐색한 후에 할 일은?  
Remove : 해당 샘플을 제거한다. : 단, 해당 값에 관련한 전체 데이터를 잃게 된다. 
Assign : 다른 값을 한다. : 이상치가 모델에 미치는 영향을 걱정하지 않아도 되지만 예측할수 없는 다른 결과를 만들어 낼 수 있다. 
Transform : 열을 변환 : log화하면 더이상 이상값이 아니게 될 수 있다.
Predict : 예측모델을 적용 : 유사관측값을 적용하여 해당 outlier가 원래 어떤 값이었을지 예측함(이 경우 더 많은 노력을 필요로 할 수 있음)


이상치로 작업하는 다른 방법보다 훨씬 많은 작업이 필요합니다. 마지막으로 그 가치를 유지할 수 있습니다. 이상치에 강한 모델을 사용하고 싶을 것입니다. 우리는 이후 과정에서 모델링에 들어가면서 그 중 일부를 나중에 논의 할 것입니다.
