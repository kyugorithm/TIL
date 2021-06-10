다룰 내용  
- Feature engineering and variable transformation
- Feature encoding
- Feature scaling

#### Transforming Data : Background  
ML workflow에 사용되는 모델은 때때로 데이터에 대해서 가정을 한다.  
1. linear regression : 관측값과 target 변수간의 선형적 관계를 가정한다.  
yb(x) = b0 + b1x1 + b2x2 (b represent the model's parameters), (box office 예제 /  x1 : cast budget, x2: marketing budget)
그러나 feature는 항상 target 변수와 선형적인 관계를 가지는 것은 아니기 때문에 선형관계를 만들어주기 위해 변환을 수행한다.  

#### 1) log 변환 
```python
import math 
log_data = [math.log(d) for d in data['Unemployment']]
sns.distplot(log_data, bins=20); # 기존의 graph
```

#### 2)  polynomial 변환 
```python
# Import the class containing the transformation method
from sklearn.preprocessing import PolynomialFeatures

# Create the polynomial features and then transform the data
polyFeat = polyFeat.fit(X_data)
X_poly = polyFeat.transform(X_data)
```

#### Variable Selection : Background  
Variable selection : 모델에 포함하기 위한 feature 집합을 선택하는것을 포함한다.  
변수들은 모델에 적용되기 전에 변환되어야 한다.  
#### Encoding : 수치가 아닌 특성을 수치로 변환  
categorical 특성에 적용  

#### 유형  
1) Nominal(명목형): 순서가 없는 category 데이터  
2) Ordinal(순서형): 순서가 있는 category 데이터  

#### Encoding 방법
1) Binary encoding: True, False(Male/Female)같은 값을 0, 1로 변환한다.  
2) One-hot encoding : 각 요소가 열성분이 되도록 여러개의 변수를 추가한다.  
3) Ordinal encoding : 순서형 categorical 데이터를 순서대로 할당한다.  

#### Feature Scaling  
: 특성을 다른 특성과 order로 변환  

다른 feature와 변수를 비교할 수 있도록 변수 scale을 조정하는 작업이 포함된다.  
e.x., 제품 가격: 0~10, 제품판매상점 : 10,000 ~ 50,000일때 두 변수를 모두 사용하여 예측하는경우 두 변수를 유사한 scale로 변환하여 사용한다.  
![image](https://user-images.githubusercontent.com/40943064/119228827-cfea9580-bb4f-11eb-8897-3ac7338fdc20.png)

위험에 처한 환자에 대한 분석을 하는 모델을 개발한다고 할때 위에서 볼 수 있는 그림은 의사수 vs 환자의 나이다.  
여기에서 환자의 나이를 year 단위가 아닌 second 단위로 한다면 1년 차이인 31.5m이 되고 scale이 매우 커지기 때문에 의사수의 차이는 의미가 없고 나이차이를 기준으로 분류가 될 것이다. 따라서 우리는 우측의 그림과 같이 유사한 scale로 표현해야 한다.

#### Feature Scaling 방법들
1) Standard scaling : (value-mean)/std (Z score와 유사) : 표준화된 단위로 퍼짐정도를 측정하기 위한 척도이며 outlier를 고려해야 한다.  
2) Min-Max scaling : (value-min)/(max-min) : Outlier에 큰 영향을 받을 수 있다.  
3) Robust scaling : min과 max를 1, 4 사분위수로 솔정하는것이다 : 이는 이상치로부터의 왜곡에서 강력하지만 0~1사이에 머물 수 있음을 보장하지는 않는다. 

![image](https://user-images.githubusercontent.com/40943064/119229259-0a553200-bb52-11eb-9381-33f65541d255.png)

```python
# Useful functions for sclaing variables
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RoubstScaler
# Useful functions for encoding categorical variables
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, OneHotEncoder
from pandas import get_dummies
# Useful functions for encoding ordinal variables
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import OrdinalEncoder



```


연속적인 숫자 값의 경우 표준 스케일링, 최소-최대 스케일링 및 강력한 스케일링과 같이 방금 논의한 변환을 사용하려고합니다. 그런 다음 Python에서이 작업을 수행하기 위해 sklearn.pre-processing에서 가져올 수 있습니다. 표준 스케일링의 경우 표준 스칼라, Min-Max 스케일링의 경우 MinMaxScaler, 각 범주의 RobustScaler에서 가져올 수 있습니다. 다음으로, 참 또는 거짓과 같이 정렬되지 않은 명목 또는 범주 데이터가 있습니다. 빨간색, 파란색 또는 녹색 일 수도 있습니다. 이를 위해 기능이 두 개 뿐인 경우 바이너리를 사용하고 해당 기능 내에 여러 다른 값이있는 경우 원-핫 인코딩을 사용하려고합니다. 따라서 알아야 할 일부 기능인 labelEncoder, labelBinarizer 및 OneHotEncoder는 모두 SKLearn에서 유사하게 작동 할뿐만 아니라 Pandas에서 더미를 가져 와서 0과 1의 원-핫 인코딩을 만들어 여러 개를 생성 할 수 있습니다. 단일 열의 열.
