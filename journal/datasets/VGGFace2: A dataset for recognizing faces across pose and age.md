Github link : https://github.com/ox-vgg/vgg_face2

## Abstract
Larget scale 얼굴 데이터셋 VGGFace2를 소개한다.  
데이터셋은 **9131명**으로부터 **331만장**의 이미지를 포함하며 1인당 **362.6**장의 이미지가 있다.  
이미지는 구글에서 수집하였고 자세, 나이, 조도, 인종, 직업(배우, 운동선수, 정치인)에 있어 매우 큰 다양성을 가진다.  
  
데이터셋은 다음 세가지를 염두해두고 수집되었다.  
1) 많은 인물로부터 수집하고 개별 인물당 많은 수의 이미지를 가질것  
2) 다양한 자세, 나이, 인종을 포함할것  
3) 라벨의 노이즈를 최소화 할것

데이터를 어떻게 수집했는지 특히 각 인물에 대한 이미지들에 대해 높은 정확도를 보장하기 위해 자동화된 그리고 수기 필터링단계에서 묘사한다.  

새 데이터셋을 사용하여 얼굴인식성능을 평가하기 위해 ResNet-50 모델을 1) VGGFace에 2) MS-Celeb-1M, 3) 1, 2 통합에 대하여 학습하고  
자세/나이에 대해 향상된 인식 성능을 이끄는것을 보인다.  

## 1. Introduction
일반적으로 최근 데이터 세트(표 I 참조)는 **클래스 내 및 클래스 간 변화의 중요성**을 탐구했다. 
전자는 깊이(한 하위 영역의 많은 이미지)에 초점을 맞추고 후자는 폭(주체당 이미지가 제한된 많은 주제)에 초점을 맞춘다.  
그러나 이러한 데이터 세트 중 포즈와 연령 변화를 탐색하기 위해 특별히 설계된 것은 없었다.  
여기서는 인간 얼굴의 광범위한 포즈, 나이, 조명 및 민족적 변화를 가진 이미지를 명시적으로 수집하기 위한 데이터 세트 생성 파이프라인을 설계하여 이를 다룬다.  
  
다음 네 가지 기여를 했다.  
1) 각 정체성에 대해 80개 및 800개 이상의 이미지를 가진 9,000개 이상의 정체성과 총 3M개 이상의 이미지를 포함
2) 각 피험자에 대한 포즈와 연령 다양성을 장려하고 라벨 노이즈를 최소화하기 위해 자동 및 수동 필터링의 여러 단계를 포함
3) 포즈 및 연령 인식 성능을 명시적으로 탐색하기 위해 테스트 세트에 대한 template annotation을 제공한다.  
4) 새로운 데이터 세트에 대한 심층 CNN 교육이 IJB 벤치마크 데이터 세트의 SOTA 훨씬 능가  

특히, 우리는 최근의 Squeeze and Excitation 네트워크[9]를 실험하고 폭이 있는 데이터 세트(MS-Celeb-1M[7])에 대한 첫 번째 사전 훈련과 VGGFace2에 대한 미세 조정의 이점을 조사한다.
논문의 나머지 부분은 다음과 같이 구성된다.  
S.2  : 이전 데이터 세트 검토, 표 I에서 기존 공개 데이터 세트에 대한 요약
S.3 : 새 데이터 세트에 대한 개요를 제공하고 포즈 및 나이에 대한 template annotation 설명. 
S.4  : 데이터 세트 수집 프로세스 설명
S.5   : IJB-A, IJB-B, IJB-C 벤치마크에서 여러 아키텍처의 최신 성능 보고
![image](https://user-images.githubusercontent.com/40943064/157663639-67409380-dc0c-4223-8b91-321366717cb5.png)

## 3. An overview of the VGGFace2

#### A. Dataset Statistics
VGFace2 데이터 세트에는 광범위한 인종에 걸쳐 있는 9131명의 유명인의 331만 개의 이미지가 포함되어 있다.  
예를 들어, VGFace보다 더 많은 **중국 및 인도** 얼굴이 포함되어 있다. (인종 간 균형은 여전히 유명인사 및 공인의 분포에 의해 제한됨),  
직업(예: 정치인 및 운동선수) 이미지는 Google 이미지 검색에서 다운로드되었으며 자세, 연령, 조명 및 배경에 큰 차이가 있다.  
데이터 세트는 대략적으로 성별 균형을 이루며, 59.3%의 남성이 각 정체성에 대해 80개에서 843개의 이미지 사이에서 변화하며 평균 362.6개의 이미지가 있다.  
여기에는 얼굴 주위의 인간 검증된 경계 상자 및 [27] 모델에 의해 예측된 5개의 기준 요점이 포함된다. 또한 자세(요, 피치 앤 롤링) 및 외관
나이 정보는 사전 학습된 포즈와 나이 분류기로 추정
데이터 세트는 8631개의 클래스가 있는 학습용과 500개의 클래스가 있는 평가(테스트)용 두 개로 나뉜다.  

#### B. Pose and Age Annotations
VVGFace2는 두 가지 시나리오, 즉 서로 다른 포즈에 걸친 얼굴 일치와 서로 다른 연령에 걸친 얼굴 일치를 평가할 수 있는 주석을 제공한다.
템플릿을 포즈합니다. 여기 템플릿은 동일한 피사체의 면 5개와 일관된 포즈로 구성되어 있습니다. 이 자세는. 정면, 3쿼터 또는 종단 뷰일 수 있습니다. 평가 세트의 300명의 피험자 하위 집합에 대해 각 포즈 보기에 대해 2개의 템플릿(템플릿당 5개의 영상)이 제공됩니다. 결과적으로 총 9K 이미지가 있는 1.8K 템플릿이 있습니다. 그림 2(왼쪽)에 예가 나와 있습니다.
기간 템플릿. 여기서 템플릿은 겉보기 나이가 34세 미만(젊은 것으로 간주) 또는 34세 이상(성숙한 것으로 간주)인 동일한 피험자의 5개의 면으로 구성된다. 이러한 템플릿은 각 연령 기간마다 두 개의 템플릿이 포함된 평가 세트에서 100명의 피험자 하위 집합에 대해 제공되므로 총 2K 영상이 포함된 템플릿은 400개입니다. 예는 그림 2(오른쪽)에 나와 있습니다.

![image](https://user-images.githubusercontent.com/40943064/157669332-d4940dfe-2e2a-41ab-9adc-29c66d08ba63.png)
