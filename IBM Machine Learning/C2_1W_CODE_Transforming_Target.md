**코드내용**
1. helper 사용자 정의 함수에 저장되어 있는 데이터를  boston_dataframe()를 통해 불러온다.
2. scipy.stats.mstats에 수록된 normaltest를 이용하여 target y인 medv의 정규화정도를 파악한다.
3. 정규화하기위해 log 변환 수행후 동일 과정 반복
4. 정규화하기위해 polynomial square 변환 수행후 동일 과정 반복
5. 정규화하기위해 boxcox 변환 수행후 동일 과정 반복
6. 세가지변환을 수행후 scipy.linear_model에 속해있는 LinearRegression 클래스를 lr명의 오브젝트로 생성
7. X, y로 분리하여 변수 생성
8. PolynomialFeature를 degree of 2까지 만든다.
9. Train과 Test를 분할하는 scipy.model_selection의 train_test_split을 이용한다.
10. 각각 X에 대하여 StandardScaler 변환및 y에 대한 boxcox 변환 후에 lr.fi을 이용하여 학습 수행
11. test 샘플에 대해 동일 변환 수행 후 r2 값을 얻어낸다.
12. 미 변환 기본 방법론에 적용하여도 r2값을 얻어낸다.

![image](https://user-images.githubusercontent.com/40943064/121651196-5520f480-cad5-11eb-94cf-b2415a9837f3.png)
