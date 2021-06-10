### 목표 
- EDA를 수행하는 접근방법들   
- EDA 기법들 : 통계, 시각적  
- Data 샘플링  
- EDA 시각화 생성  

#### EDA란 무엇인가?
때로는 시각방법을 이용하여 주요 특징을 요약 하기위해 데이터셋을 분석하는 접근 방법이다.  

#### 왜 EDA가 효과적인가?
분석을 시작하기 전에 데이터에 대한 첫 직관을 얻을 수 있도록 한다.  
데이터가 쓸 수 있는지 확인할 수 있거나 cleaning이 필요한지, 데이터가 더 필요한지 알 수 있다.  
데이터의 패턴이나 경향을 분석할 수 있다.(모델링을 통해 찾는것 만큼이나 중요하다.)  

### EDA 기법
통계적 요약 : 평균, 중간값, 최소, 최대, 상관성 등을 이용
시각화      : histogram, scatter, box, etx ,... / matplotlib, seaborn
데이터 Wrangling : pands(데이터논의나 요약통계를 볼때)


입사 지원자의 요약 통계에 대한 EDA의 예 :  
입사 지원자의 특성을 조사 할때 **평균치**, 면접점수평균, 도시/직능별로 나누어서 지원자 점수를 경쟁자 평균과 비교, **최대값**, 지원서의 어떤 단어가 가장 일반적인지 확인할 수 있는 다빈값 등을 뽑아 볼 수 있다.  
기술 평가와 지원자의 수년간의 경험 간의 상이한 **상관관계**를 경험 유형별로 살펴보고 경쟁자들과 비교할 수 있다. 이것은 서로다른 features 사이에 어떤 종류의 초기 관계가 있는지 알 수 있게 해준다.  

### 데이터 샘플링 
``` python
# Sample 5 rows without replacement
sample = data.sample(n=5, replace = False)
print(sample.iloc[:,-3:])
```

데이터가 너무 클 경우 일부샘플을 랜덤하게 뽑는다. 랜덤 샘플을 추출해서 학습을하고 나머지 샘플에 대하여 테스트 할 수 있다.  
또한 결과 변수의 비율이 실제 비율과 같도록 지켜져야 한다. 예를들어 질병관련 데이터 세트를 가지는 경우 실제 질병샘플은 1%미안의 샘플비율을 가질 수 있다. 이 때 동일한 비율을 가지도록 표본을 추출해서 사용해야한다.    
혹여나 더욱더 낮은 비율로 샘플이 얻어진다면 이는 해당 질병의 통계적 분포를 왜곡하는것일 수 있다. 그래서 이것이 stratified sampling이라고 정의하는 것이다.  
위 코드를 보면 매우 쉽게 데이터를 랜덤 샘플링 할 수 있는데 replace 명령어는 복원추출 여부이다.(false는 비복원추출)  

### EDA - Part 2

```python
# Pandas DataFrame approach # plot을 하기위한 library로 matplotlib.pyplot을 사용
import matplotlib.pytplot as plt
plt.plot(data.sepal_length,
data.sepal_width,
ls = '', marker='o')
# plot method에서 x, y 을 순서로 입력하고 ls (line style), marker를 정의
```

```python
# Pandas DataFrame approach # plot을 하기위한 library로 matplotlib.pyplot을 사용
import matplotlib.pytplot as plt
plt.plot(data.sepal_length, data.sepal_width, ls = '', marker='o')
# plot method에서 x, y 을 순서로 입력하고 ls (line style), marker, label을 optional argument로 사용

# Pandas DataFrame approach
plt.hist(data.sepal_length, bins=25)

# matplotlib syntax
fig, ax = plt.subplots()
ax.barh(np.arrange(10),data.sepal_width.iloc[:10])
```

```python
# Set position of ticks and tick labels
ax.set_yticks(np.arange(0.4, 10.4, 1.0))
ax.set_yticklabels(np.arange(1,11))
ax.set(xlabel='xlabel', ylabel='ylabel', title='Title')
# 기존의 plt. 를 이용하는것과는 달리 ax를 만들어 오브젝트를 상속받아 plt와 같은 method를 사용할 수 있게 한다.
# xlabel, ylabel, title 등의 기능은 set으로 이용하고 대부분의 일반적인 style 관련 method는 yticks, yticklabels 등을 가짐
```
```python
# Pandas DataFrame approach 
data.groupby('species').mean().plot(color=['red','blue','black','green'], fontsize=10.0, figsize=(4,4))
# Pandas Frame은 groupby method가 있는데 데이터중 species로 나누어 각 평균값을 얻는것을 의미하는데 또 pandas df는
# plot 메서드를 이용할 수 있다.
```

```python
# Seaborn plot, feature correlations
sns.pairplot(data, hue='species', size=3)
```

```python
# Seaborn hexbin polot
sns.jointplot(x=data['sepal_length'], y=data['sepal_width'],kind='hex')
```


```python
# Seaborn plot, Facet Grid
# First plot statement
plot = sns.FacetGrid(data, col='species', margin_titles=True)
plot.map(plt.hist, 'sepal_width', color='green')
#Second plot statement
plot = sns.FacetGrid(data, col='species', margin_titles=True)
plot.map(plt.hist, 'sepal_length', color='blue')
```
