다룰 내용  
- Feature engineering and variable transformation
- Feature encoding
- Feature scaling

Transforming Data : Background  
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
