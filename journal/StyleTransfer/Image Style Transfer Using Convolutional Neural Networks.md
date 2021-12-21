#Abstract
Content에 다른 이미지의 style을 입히는 작업은 어려운 작업이며 이전까지 style과 content를 분리하는것에는 한계가 있었다.  
이 문제를 해결하기 위해, CNN의 high-level 이미지 정보를 명시적으로 표현하는 방식을 활용해서  
content와 style을 분해하고 결합할 수 있도록 하는 방법론을 제시한다.  
결과는 CNN을 활용한 깊은 이미지 표현에 대한 통찰력과 high-level 이미지 합성/조절에 대한 잠재력을 제시한다. 

# 1. Introduction
한 이미지에서 다른 이미지로 style을 전송하는 것은 texture transfer 문제로 간주될 수 있다.  
Texture transfer의 목표는 target image의 의미론적 내용을 보존하기 위해 texture 합성을 제한하면서  
source image의 texture를 합성하는 것이다.  
Texture 합성을 위해 주어진 source texture의 픽셀을 다시 샘플링하여 사실적인 natural texture를 합성할 수 있는  
강력한 non-parametric 알고리즘이 광범위하게 존재한다.  
이전 texture 전송 알고리즘은 texture 합성을 위해 이러한 non-parametric 방법에 의존하는 동시에  
target image의 구조를 보존하기 위해 다양한 방법을 사용했다.  

Efros : texture 합성 절차를 제한하기 위해 이미지 intensity와 같은 target image의 feature를 포함하는  
correspondence map을 도입했다.  
Hertzman : image analogies를 사용하여 이미 style화된 이미지에서 target image로 texture를 전송한다.  
Ashikhmin : target image의 coarse 스케일을 유지하면서 고주파 texture 정보를 전송하는 데 중점을 둔다.  
Lee : edge 방향 정보로 texture 전송을 추가로 알려 이 알고리즘을 개선한다.  

이러한 알고리즘은 놀라운 결과를 달성하지만 모두 동일한 근본적인 한계를 가진다.  
Target image의 low-level 이미지 feature만 사용하여 texture 전송을 알린다.  
그러나 style transfer 알고리즘은 target 이미지에서 semantic content를 추출한 다음  
source style로 target의 semantic content를 렌더링하도록 texture transfer 절차를 알릴 수 있어야 한다.  

따라서 근본적인 전제 조건은 semantic content와 표현되는 style의 변형을 독립적으로 모델링하는 이미지 표현을 찾는 것이다.  
이러한 분해된 표현은 이전에 다른 조명 조건의 얼굴과 다른 글꼴 style의 문자 또는 손으로 쓴 숫자 및 집 번호와 같은  
자연 이미지의 제어된 하위 집합에 대해서만 달성되었다.  
자연 이미지에서 일반적으로 content를 style과 분리하는 것은 여전히 매우 어려운 문제이다.  
그러나 최근 Deep CNN의 발전으로 자연 이미지에서 high-level semantic 정보를 추출하는 방법을 배우는  
강력한 CV 시스템이 만들어졌다.  
객체 인식과 같은 특정 작업에 대해 충분한 레이블이 지정된 데이터로 훈련된 Convolutional Neural Networks는  
데이터 세트 전체와 텍스처 인식 및 예술적 스타일 분류를 포함한 다른 시각 정보 처리 작업까지 일반화하는  
일반 feature 표현에서 high-level content를 추출하는 방법을 학습하는 것으로 나타났다.  

이 작업에서는 고성능 CNN에서 학습한 일반 feature 표현을 사용하여 자연 이미지의  
content와 style을 독립적으로 처리하고 조작하는 방법을 보인다.  
개념적으로는 SOTA CNN의 feature 표현으로 texture 합성 방법을 제한하는 texture transfer 알고리즘이다.  
Texture 모델도 deep image representation을 기반으로 하기 때문에 style transfer 방법은  
단일 신경망 내에서 최적화 문제로 우아하게 축소된다.  
새 이미지는 예시 이미지의 feature 표현과 일치하도록 사전 이미지 검색을 수행하여 생성된다.  
이 일반적인 접근 방식은 이전에 texture 합성의 맥락에서 그리고 deep image 표현에 대한 이해를 향상시키기 위해 사용되었다.  
Style transfer 알고리즘은 CNN을 기반으로 하는 매개변수 texture 모델과 이미지 표현을 반전시키는 방법을 결합한다.  

## 2. Deep image representations
아래 제시된 결과는 사전학습(object recognition / localization)된 VGG를 기반으로 생성되었으며  
원본 작업에 광범위하게 설명되어 있다.  
19 layer의 VGG의 16개 Conv. layer와 5개 pooling의 정규화된 버전에서 제공하는 feature space를 사용했다.  
이미지와 위치에 대한 각 Conv. 필터의 평균 activation이 1과 같도록 weight를 조정하여 네트워크를 정규화했다.  
VGG는 출력을 변경하지 않고 선형 활성화 함수를 수정하고 feature map에 대한 정규화 또는 풀링을 포함하지 않기 때문에  
이러한 재조정은 VGG에 대해 수행할 수 있다. (max-pooling 대신 average-pooling 사용)
