## Abstract
Content에 다른 이미지의 style을 입히는 작업은 어려운 작업이며 이전까지 style과 content를 분리하는것에는 한계가 있었다.  
이 문제를 해결하기 위해, CNN의 high-level 이미지 정보를 명시적으로 표현하는 방식을 활용해서  
content와 style을 분해하고 결합할 수 있도록 하는 방법론을 제시한다.  
결과는 CNN을 활용한 깊은 이미지 표현에 대한 통찰력과 high-level 이미지 합성/조절에 대한 잠재력을 제시한다. 

## 1. Introduction
한 이미지에서 다른 이미지로 style을 전송하는 것은 texture transfer 문제로 간주될 수 있다.  
Texture transfer의 목표는 target image의 의미론적 내용을 보존하기 위해 texture 합성을 제한하면서  
source image의 texture를 합성하는 것이다.  
Texture 합성을 위해 주어진 source texture의 픽셀을 다시 샘플링하여 사실적인 natural texture를 합성할 수 있는  
강력한 non-parametric 알고리즘이 광범위하게 존재한다.  
이전 texture transfer 알고리즘은 texture 합성을 위해 이러한 non-parametric 방법에 의존하는 동시에  
target image의 구조를 보존하기 위해 다양한 방법을 사용했다.  

Efros : texture 합성 절차를 제한하기 위해 이미지 intensity와 같은 target image의 feature를 포함하는  
correspondence map을 도입했다.  
Hertzman : image analogies를 사용하여 이미 style화된 이미지에서 target image로 texture를 전송한다.  
Ashikhmin : target image의 coarse 스케일을 유지하면서 고주파 texture 정보를 전송하는 데 중점을 둔다.  
Lee : edge 방향 정보로 texture transfer을 추가로 알려 이 알고리즘을 개선한다.  

이러한 알고리즘은 놀라운 결과를 달성하지만 모두 동일한 근본적인 한계를 가진다.  
Target image의 low-level 이미지 feature만 사용하여 texture transfer을 알린다.  
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
아래 제시된 결과는 사전학습(object recognition / localization)된 VGG-19를 기반으로 생성되었다.  
모델의 표준 구조를 이용해 feature space를 사용했다.  
이미지와 위치에 대한 각 Conv. 필터의 평균 activation이 1과 같도록 weight를 조정하여 네트워크를 정규화했다.  
VGG는 출력을 변경하지 않고 선형 활성화 함수를 수정하고 feature map에 대한 정규화 또는 풀링을 포함하지 않기 때문에  
이러한 재조정은 VGG에 대해 수행할 수 있다. (max-pooling 대신 average-pooling 사용)

### 2.1. Content representation
네트워크의 각 계층은 네트워크에서 계층의 위치에 따라 복잡성이 증가하는 비선형 필터 뱅크를 정의한다.  
따라서 주어진 입력 이미지 ~x는 해당 이미지에 대한 필터 응답에 의해 CNN의 각 레이어에서 인코딩된다.  
  
Nl = layer l의 filter 수 (feature map 수)  
Ml = layer l의 h x w  
그러므로 layer l의 응답은 activation 행렬 Fl ∈ RNl×Ml에 저장 될 수 있다.  

계층 구조의 다른 레이어에서 인코딩된 이미지 정보를 시각화하기 위해 백색 잡음 이미지에 대해 경사 하강법을 수행하여  
원본 이미지의 특징 응답과 일치하는 다른 이미지를 찾을 수 있습니다(그림 1, 콘텐츠 재구성)[24].  
  
![image](https://user-images.githubusercontent.com/40943064/147050763-d7124a65-156b-4b10-b6c2-3329e071d097.png)  
  
~p : 원본이미지  
~x : 생성이미지  
Pl : 원본의 feature map  
Fl : 원본의 feature map  
이미지간 Content Loss :  
![image](https://user-images.githubusercontent.com/40943064/147104865-25f9e0f1-659f-4b4b-8445-5d8b8e23e049.png)  
레이어 l의 activation에 대한 이 손실의 미분은 아래와 같다.  
![image](https://user-images.githubusercontent.com/40943064/147104974-50774777-4af2-4619-9427-b7f285dd03c6.png)
여기서 이미지 ~x에 대한 기울기는 표준 오차 역전파를 사용하여 계산할 수 있다(그림 2, 오른쪽).  
![image](https://user-images.githubusercontent.com/40943064/147105087-9f339077-186d-4a1a-9cb6-d12f37df1670.png)  
따라서 CNN의 특정 레이어에서 원본 이미지 ~p와 동일한 응답을 생성할 때까지 초기 랜덤 이미지 ~x를 변경할 수 있다.  
CNN이 객체 인식에 대해 학습되면 처리 계층 구조를 따라 객체 정보를 점점 더 명확하게 만드는 이미지 표현을 개발한다.  
따라서 네트워크의 처리 계층 구조를 따라 입력 이미지 이미지의 실제 내용에 점점 더 민감해지는 표현으로 변환되지만  
정확한 모양에는 상대적으로 변하지 않는다.  
따라서 네트워크의 상위 계층은 개체 및 입력 이미지의 배열 측면에서 상위 수준 콘텐츠를 캡처하지만  
재구성의 정확한 픽셀 값을 크게 제한하지 않는다(그림 1, 콘텐츠 재구성 d, e).  
대조적으로, 하위 레이어로부터의 재구성은 단순히 원본 이미지의 정확한 픽셀 값을 재현한다(그림 1, 콘텐츠 재구성 a-c).  
따라서 네트워크의 상위 계층에서 feature 응답을 content 표현이라고 한다.  


### 2.2. Style representatio
입력 이미지의 스타일 표현을 얻기 위해 텍스처 정보를 캡처하도록 설계된 feature 공간을 사용한다.  
이 feature 공간은 네트워크의 모든 layer에서 filter 응답 위에 구축할 수 있다.  
이는 다양한 필터 응답 간의 상관 관계로 구성되며, 여기서 feature map의 공간적 범위에 대한 expectation이 적용된다.  
이러한 feature 상관 관계는 gram matrix Gl ∈ RNl×Nl로 제공되며,  
여기서 Glij는 레이어의 벡터화된 특징 맵 i와 j 사이의 내적이다.  

![image](https://user-images.githubusercontent.com/40943064/147111293-b610cac9-a551-47e8-837c-51aec0d36ef4.png)  

여러 레이어의 feature correlation을 포함하여 입력 이미지의 고정된 다중 스케일 표현을 얻는다.  
이 표현은 텍스처 정보는 캡처하지만 global arrangement는 캡처하지 않는다.  
다시 말하지만, 주어진 입력 이미지의 스타일 표현과 일치하는 이미지를 구성함으로써  
네트워크의 다른 레이어에 구축된 이러한 스타일 특징 공간에 의해 캡처된 정보를 시각화할 수 있다(그림 1, 스타일 재구성).  
이것은 원본 이미지의 gram matrix 항목과 생성할 이미지의 gram matrix 항목 사이의 평균 제곱 거리를 최소화하기 위해  
백색 잡음 이미지에서 경사 하강법을 사용하여 수행된다.  
~a : 원본 이미지 (Al : 원본 이미지 style 표현)  
~x : 생성 이미지 (Gl : 생성 이미지 style 표현)
총 손실에 대한 레이어 l의 기여는 다음과 같다.  

![image](https://user-images.githubusercontent.com/40943064/147111693-4f12efb2-c7ba-42d4-847b-bb30f1c99fdf.png)  
  
여기서 wl은 총 손실에 대한 각 레이어의 기여도에 대한 가중치 요소이다(결과에서 wl의 특정 값은 아래 참조).  
layer l의 activation에 대한 El의 도함수는 다음과 같이 분석적으로 계산할 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/147111828-80567c4d-3e9c-4de7-9f0c-926c60095451.png)  
픽셀 값 ~x에 대한 El의 기울기는 표준 오차 역전파를 사용하여 쉽게 계산할 수 있다(그림 2, 왼쪽).  

## 2.3. Style transfer
작품 ~a의 스타일을 사진 ~p로 전송하기 위해 ~p의 콘텐츠 표현과 ~a의 스타일 표현과 동시에 일치하는 새로운 이미지를 합성한다(그림 2).  
따라서 우리는 한 layer에 있는 사진의 content 표현과 CNN의 여러 레이어에 정의된 그림의 style 표현에서  
white noise 이미지의 feature 표현의 거리를 공동으로 최소화한다.  
최소화하는 손실 함수는 다음과 같다.  
![image](https://user-images.githubusercontent.com/40943064/147112111-7cd9ad96-e34e-4427-859a-e4ee005c32a9.png)  
  
(α, β  : content, style reconstruction에 대한 가중치)  
픽셀 값 ∂Ltotal/∂~x에 대한 기울기는 일부 수치 최적화 전략의 입력으로 사용할 수 있다.  
여기서 이미지 합성에 가장 잘 작동하는 L-BFGS를 사용한다.  
비슷한 규모의 이미지 정보를 추출하기 위해 feature 표현을 계산하기 전에 항상 style 이미지의 크기를 콘텐츠 이미지와 동일한 크기로 조정했다.  
마지막으로 [24]와 달리 합성 결과를 이미지 prior로 정규화하지 않는다.  
그러나 네트워크의 하위 레이어의 텍스처 기능이 스타일 이미지 이전에 특정 이미지로 작동한다고 주장할 수 있다.  
또한 사용하는 다른 네트워크 아키텍처와 최적화 알고리즘으로 인해 이미지 합성에 약간의 차이가 있을 것으로 예상된다.  

## Conclusion
주요 발견은 CNN에서 content과 style의 표현이 잘 분리된다는 것이다.  
즉, 새롭고 perceptually meaningful한 이미지를 생성하기 위해 두 표현을 독립적으로 조작할 수 있다.  
이 발견을 입증하기 위해 두 개의 다른 source 이미지에서 content와 style 표현을 혼합하는 이미지를 생성한니다.  
특히, 우리는 독일 튀빙겐의 Neckar 강의 강변을 묘사한 사진의 내용 표현과  
다양한 예술 시대에서 가져온 여러 유명 예술품의 스타일 표현을 일치시킨다(그림 3).  
그림 3에 표시된 이미지는 아래의 표현을 일치시켜 합성했다.  
Content representation : 'conv4 2'   
Style representation : 'conv1 1', 'conv2 1', 'conv3 1', 'conv4 1', 'conv5 1'  
( wl = 해당 레이어에서 1/5, 다른 모든 레이어에서 wl = 0) 
![image](https://user-images.githubusercontent.com/40943064/147113114-2d34018b-71f0-4870-bd70-922dd664ace0.png)  

### 3.1. Trade-off between content and style matching
물론 이미지 content와 style이 완전히 분리될 수는 없다.  
한 이미지의 content와 다른 이미지의 style을 결합한 이미지를 합성할 때  
일반적으로 두 제약 조건이 동시에 완벽하게 일치하는 이미지는 존재하지 않는다.  
그러나 이미지 합성 시 최소화하는 손실 함수는 각각 content와 style에 대한 loss function 간의 선형 결합이므로  
content 또는 style reconstruction에 대한 강조를 원활하게 조절할 수 있다(그림 4).  
Style에 대한 강한 강조는 artwork의 모양과 일치하는 이미지를 생성하여 효과적으로 textuer 버전을 제공하지만  
사진의 내용은 거의 표시하지 않는다(α/β = 1 × 10−4, 그림 4, 왼쪽 상단).  
Content를 강하게 강조하면 사진을 명확하게 식별할 수 있지만 그림의 스타일이 잘 어울리지 않는다(α/β = 1 × 10-1, 그림 4, 오른쪽 하단).  
Content 및 style 이미지의 특정 쌍에 대해 content와 style 간의 균형을 조정하여 시각적으로 매력적인 이미지를 만들 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/147113077-ad3612e8-a038-445f-bbad-02d3cd6c9191.png)  

### 3.2. Effect of different layers of the Convolutional Neural Network
이미지 synthesis 프로세스의 또 다른 중요한 요소는 content와 style 표현에 맞는 layer를 선택하는 것이다.  
위에서 설명한 것처럼 style 표현은 NN의 여러 layer를 포함하는 다중 스케일 표현이다.  
이러한 layer의 수와 위치는 style이 일치하는 로컬 스케일을 결정하여 다양한 시각적 경험을 제공한다(그림 1, style 재구성).  
Style 표현을 네트워크의 상위 layer와 일치시키면 local 이미지 구조가 점점 더 큰 규모로 보존되어  
더 부드럽고 지속적인 시각적 경험을 제공한다는 것을 발견했다.  
따라서 시각적으로 가장 매력적인 이미지는 일반적으로 style 표현을 네트워크의 상위 layer와 일치시켜 생성되며,  
이것이 표시된 모든 이미지에 대해 layer 'conv1_1', 'conv2_1', 'conv3_1', 'conv4_1', 'conv5_1'의 style 기능을 일치시키는 이유이다.  

content 특성에 맞게 다른 layer를 사용하는 효과를 분석하기 위해 동일한 artwork과  
매개변수 구성(α/β = 1 × 10−3 )으로 사진을 스타일화하여 얻은 style transfer 결과를 제시한다.  
'conv2_2' layer의 feature와 'conv4_2' layer의 다른 feature(그림 5).  
네트워크의 하위 layer에 있는 content를 일치시킬 때 알고리즘은 사진의 세부 픽셀 정보 대부분을 일치시키고  
생성된 이미지는 마치 작품의 texture이 사진 위에 단순히 혼합된 것처럼 나타난다(그림 5, 중간).  
대조적으로, 네트워크의 상위 계층에서 content 기능을 일치시킬 때 사진의 세부 픽셀 정보는 크게 제한되지 않고  
artwork의 texture와 사진의 content가 적절하게 병합된다.  
즉, 이미지의 미세한 구조, 예를 들어 edge 및 colormap은 사진의 content를 표시하면서  
작품의 style과 일치하도록 변경된다(그림 5, 하단).
![image](https://user-images.githubusercontent.com/40943064/147114066-c4e1f7ef-373e-4e73-9d9b-ee2cc6086ad2.png)  

### 3.3. Initialisation of gradient descent
지금까지 보여진 모든 이미지를 white noise로 초기화했다.  
그러나 content 이미지나 style 이미지로 이미지 합성을 초기화할 수도 있다.  
우리는 이 두 가지 대안을 조사했다(그림 6 A, B): 비록 최종 이미지가 초기화의 공간 구조 쪽으로 다소 치우쳐 있지만,  
다른 초기화는 합성 절차의 결과에 강한 영향을 미치지 않는 것 같다.  
노이즈로 초기화하는 것만으로 임의의 수의 새 이미지를 생성할 수 있다는 점에 유의해야 한다(그림 6C).  
고정된 이미지로 초기화하면 항상 동일한 결과가 결정적으로 나타난다(경사하강법 절차에서 최대 확률).  

![image](https://user-images.githubusercontent.com/40943064/147114344-97a9f231-ee10-495e-926a-832ea0baee69.png)

### 3.4. Photorealistic style transfer
지금까지 이 논문의 초점은 artistic style transfer에 있었다.  
그러나 일반적으로 알고리즘은 임의의 이미지 간에 style을 전송할 수 있다.  
예를 들어 '밤의 뉴욕 사진' style을 '낮의 런던 이미지'로 전송한다(그림 7).  
포토리얼리즘이 완전히 보존되지는 않았지만 합성된 이미지는 style 이미지의 색상과  
번개를 많이 닮아 밤에 런던의 이미지를 어느 정도 표시한다.  
![image](https://user-images.githubusercontent.com/40943064/147114641-34c67866-1b5a-42c9-b193-5763c7faa0ec.png)

## 4. Discussion
여기서는 고성능 CNN의 feature representation을 사용하여 임의의 이미지 간에 style을 전송하는 방법을 보였고,   
높은 지각 품질의 결과를 보여줄 수 있지만 몇 가지 기술적 한계가 있다.  
가장 제한적인 요소는 합성 이미지의 해상도일 것이다.  
최적화 문제의 차원과 CNN의 unit 수는 모두 픽셀 수에 따라 선형적으로 증가한다.  
따라서 합성 절차의 속도는 이미지 해상도에 크게 의존한다.  
이 문서에 제시된 이미지는 약 512 × 512 픽셀의 해상도로 합성되었으며 합성 절차는 Nvidia K40 GPU에서  
최대 1시간이 소요될 수 있다(정확한 이미지 크기 및 경사하강법에 대한 중지 기준에 따라 다름).  
이 성능은 style 전송 알고리즘의 온라인 및 대화식 응용 프로그램을 금지하지만  
딥 러닝의 향후 개선으로 인해 이 방법의 성능이 향상될 가능성이 있다.  
또 다른 문제는 합성된 이미지가 때때로 낮은 수준의 노이즈에 노출된다는 것이다.  
이는 예술적 style 전달에서는 문제가 되지 않지만, content와 style 이미지 모두가 사진이고  
합성된 이미지의 사실성이 영향을 받는 경우 문제가 더 분명해진다.  
그러나 노이즈는 매우 특징적이며 네트워크의 장치 필터와 유사한 것으로 보인다.  
따라서 최적화 절차 후 이미지를 사후 처리하기 위해 효율적인 노이즈 제거 기술을 구성하는 것이 가능할 수 있다.  
이미지의 예술적 양식화는 전통적으로 비사실적 렌더링이라는 레이블 아래 CG에서 연구된다.  
texture transfer 작업을 제외하고 일반적인 접근 방식은 소스 이미지를 하나의 특정 style로 렌더링하는  
특수 알고리즘을 제공한다는 점에서 개념적으로 우리 작업과 상당히 다르다.  
이 분야의 최근 검토를 위해 우리는 독자에게 [21]을 참조한다.  
Style에서 이미지 content의 분리가 반드시 잘 정의된 문제는 아니다.  
이는 이미지의 style을 정확히 정의하는 것이 무엇인지 명확하지 않기 때문이다.  
그것은 그림의 붓놀림, 컬러 맵, 특정한 지배적인 형태와 모양일 수도 있지만,  
장면의 구성과 이미지 주제의 선택일 수도 있다.  
따라서 이미지 content와 style이 완전히 분리될 수 있는지, 그리고 그렇다면 어떻게 분리될 수 있는지 일반적으로 명확하지 않다.  
예를 들어, 별을 닮은 이미지 구조가 없으면 반 고흐의 "별이 빛나는 밤" style로 이미지를 렌더링할 수 없다.  
우리 작업에서는 생성된 이미지가 style 이미지와 유사하지만  
content 이미지의 대상과 풍경을 보여주는 경우 style 전달이 성공한 것으로 간주한다.  
우리는 이 평가 기준이 수학적으로 정확하지도 않고 보편적으로 동의하지도 않는다는 것을 충분히 알고 있다.  
그럼에도 불구하고 우리는 생물학적 시각의 핵심 계산 작업 중 하나를 수행하도록 학습된 신경 시스템이  
이미지 content를 style과 적어도 어느 정도는 분리할 수 있는 이미지 표현을 자동으로 학습한다는 사실이 정말 매력적이라는 것을 알게 되었다.  
한 가지 설명은 객체 인식을 학습할 때 네트워크가 객체 ID를 유지하는 모든 이미지 변형에 대해 불변해야 한다는 것이다.  
이미지 내용의 변화와 모양의 변화를 분해하는 표현은 이 작업에 매우 실용적이다.  
성능에 최적화된 인공 신경망과 생물학적 시각 사이의 현저한 유사점에 비추어,  
style에서 content를 추상화하는 인간의 능력, 따라서 창조하고 즐기는 우리의 능력 예술 또한  
우리 시각 시스템의 강력한 추론 기능의 탁월한 서명일 수도 있다.
