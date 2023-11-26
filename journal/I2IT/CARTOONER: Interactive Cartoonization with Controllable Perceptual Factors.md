## Abstract 
문제: 자연 이미지를 만화 스타일로 변경(Cartoonization)  
한계: 기존 방식은 end-to-end를 이용하기 때문에 제어가 불가능하다.  
목표: 만화 창작 과정을 기반으로 texture 및 color의 제어 기능을 제공  
해법: texture와 color 분리를 위해 개별 decoder를 사용하는 구조를 설계  
Texture decoder: 다양한 만화 질감을 만들기 위해서 stroke style 과 abstraction을 사용자가 제어  
Color decoder: 다양하고 제어가능한 색상 변형을 만들기 위해 HSV color augmentation  

## Introduction
만화 제작과정: Character drawing -> BG composition -> Post-processing(Shading 등)  
이러한 제작과정 하에서 전문가들도 만화 제작은 고된 작업이다.  
작가들은 캐릭터 생성에 집중하기 위해 배경 사진을 카툰화하는 방법을 활용한다. (Animegan, Cartoongan, Learning to Cartoonize Using White-box Cartoon Representation)  
<img width="994" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/2d427f3a-be72-4453-a03a-5ea61a633f7e">
예술가들은 사진으로부터 BG 이미지를 생성할때 아래의 단계를 거친다.  
1) Color stylization: 하늘 이미지 합성 -> 지역적/전역적으로 색상을 변경  
2) Texture stylization: 추가 스케치 선을 그리고 서로 다른 추상화를 얻기 위해 fine detail들은 선택적으로 제거  
3) Post-processing : 조명과 이미지 필터링 적용  

<img width="1145" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/690e4931-6771-447e-8259-f79762eddcee">

그러나 이 과정에서 end-to-end 방법을 사용하기 때문에 예술가들은 생성 과정에 대한 제어를 할 수 없고 입력 사진이나 최종 사진을 수정하는것만 가능하고 이는 제작 방식에 어려움이 있다.  

본 작업에서는 카툰화에서 효율적인 interactivity를 포함하는 방식을 제시한다.  
제안된 솔루션은 texture와 color를 제어할 수 있도록 하는데 집중한다.  
1) Texture 제어: stroke 두께와 abstraction 수준 조절 - 예술가는 자연스러운 시점을 묘사하거나 캐릭터 디테일을 강조하기 위해 먼거리 장면 디테일을 추상화할 수 있다. 제작자들은 마찬가지로 brush stroke의 미묘함을 수정해서 장면을 합성할 때 object 질감을 맞출 수 있다.  
2) Color 제어: 창작자가 자유롭게 임의 영역을 원하는 색상으로 조절할 수 있도록 한다.  
  
카툰화에서 사용자 제어를 위해, 텍스처와 색상 디코더를 별도로 구축해서 기능 간의 간섭을 최소화하고 분리된 아키텍처가 텍스처 스타일화의 강건함과 뛰어난 품질을 제공한다는 것을 발견했다.  
<img width="552" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/6964204a-863a-4773-9c6d-edaa2bade33e">
  
1) Texture 제어: 수용영역과 타겟 이미지 해상도가 stroke 두께와 추상화 수준에 어떤 역할을 하는지 조사한다. 이러한 관찰을 바탕으로, intermediate feature의 dynamic replacement를 통해 네트워크의 수용영역을 조절한다.  
2) Color 제어: 제안된 HSV augmentation에 기반한 paired dataset과 함께 지도학습으로 color decoder를 공동으로 학습한다. 이 전략으로 다양한 색상을 생성하는 능력을 얻는다.  
분리된 텍스처와 색상 모듈의 조합으로, 사용자의 제어에 따라 다양한 카툰화 결과를 만들 수 있는 두 차원의 제어 공간을 달성한다. 이러한 디자인은 robust하고 perceptually으로 고품질의 카툰화 결과를 제공한다.  

## 3. Method
Texture와 color decoder를 분리하는 작업은 전문 예술가의 작업방식을 관찰을 통해 정했다. (추가로 분리된 모델링은 신뢰할 수 있는 고품질 카툰화 결과를 만든다는것을 검사한다.)

#### 제어가능 특징
1) Texture=α  
2) Color=c  

#### 목표:
주어진 사진(Isrc)으로부터 사용자의 의도(α와 c)를 따르는 카툰화된 이미지(ˆItgt) 생성

#### 방법:
Eshared(공유 Encoder)를 통해 latent feature로 인코딩하고 개별 디코더인 S_texture와 S_color에 전달  

#### 색상 공간:
RGB 대신 Lab 색상 공간 사용 (텍스처 모듈: L-채널 텍스처 맵 생성 /  색상 모듈: ab-채널 색상 맵 생성)  

#### 최종 과정:
생성된 출력물을 RGB 공간으로 되돌림  


### 3.1. Texture module 

#### Analysis of texture level. 

이 모듈에서의 주요 목표는 세밀한 제어 메커니즘을 제공하는 것이며, texture 제어는 stroke 두께와 이미지 추상화를 변경하는 것으로 정의해. 이를 위해, stroke 두께와 추상화 변화에 영향을 미치는 구성 요소를 분석했어.  
실험에서 확인한 사항은 두가지임.  
1) Target cartoon 이미지의 해상도 - stroke 두께  
2) G의 수용 필드 -  abstraction 수준  
<img width="1268" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/d211463c-7868-4e89-80e4-e252841fa710">


#### Stroke thickness change:  
고정된 RF를 가진 손실 네트워크(예: VGG나 판별자)가 관련되어 있다고 주장해(그림 5a 참조). 고정된 손실 네트워크에서 카툰 이미지의 해상도를 높이면(녹색 상자), RF 창 내에서 stroke가 확대되어, G는 훈련 중에 두꺼운 stroke를 만들도록 학습해. 해상도를 낮추면(빨간 상자) 반대 현상이 일어나. 이는 카툰 이미지가 대부분 평평한 텍스처 영역을 가지고 있기 때문에 카툰화에 더 큰 영향을 미쳐.

#### abstraction change(이해 필요)  
장면의 복잡성이 이에 영향을 미친다고 주장해(그림 5b 참조). G의 RF를 확장하면(파란 상자), 네트워크는 콘텐츠 이미지의 더 넓은 영역을 인지할 수 있어서 장면 복잡성이 높아져. 반대로, 카툰 이미지의 해상도가 높아지면, 손실 네트워크가 상대적으로 작은 영역만 볼 수 있기 때문에 장면 복잡성이 낮아져(녹색 상자). 이렇게 해서, 고해상도 카툰 이미지 I^HR_tgt로 G를 훈련시키면(녹색과 파란 상자 각각), G는 고복잡성 장면의 복잡성을 줄이도록 유도돼. 이는 손실 네트워크에서 추출한 저복잡성 장면으로 손실 계산이 이루어지기 때문이야. 결과적으로, 큰 RF를 가진 G는 복잡한 디테일을 'Abstraction'할 수 있는 능력을 얻어. 낮은 RF(분홍색 창)의 경우 반대 현상이 일어나지만, 추상화 변화는 높은 것만큼 극적이지 않아, 일반적으로 카툰의 장면 복잡성이 콘텐츠 이미지보다 낮기 때문이야. 우리는 또한 G의 RF만 확장하는 시나리오를 분석했지만, 결과는 그림 4b처럼 극적이지 않아, G가 다른 복잡성의 카툰 장면에 의해 유도되지 않기 때문이야. Jing은 스타일 전송 문헌에서 해상도와 RF의 역할을 조사했지만, 우리의 심층적인 분석은 그들의 행동 패턴이 카툰화에서 상이하다는 것을 밝혀냈어.

#### Texture controller. 
위의 분석은 다양한 수준을 처리하기 위해 여러 네트워크가 필요하며, 서로 일관된 스타일을 생성할 수 없어. 또한, 이 방법은 discrete 제어만 지원해서 실제로 사용하기 어려워. 그래서 이 분석을 바탕으로, 우리는 간단하지만 효과적인 texture 제어 모듈인 texture controller(그림 6 참조)를 소개해. 이는 stroke와 abstraction 제어 유닛으로 구성되어 있고, 두 유닛 모두 multi-branch 구조로 설계되어 있어. Stroke 유닛에서는 각 브랜치가 연속된 3x3 컨볼루션(conv) 레이어 두 개로 구성되어 있고, 이들은 게이팅 모듈에 의해 결합돼. Abstraction 유닛은 stroke 유닛과 구조가 동일하지만, 큰 커널 사이즈 K1 < K2 < ... < KN을 사용하는 conv 레이어를 사용해.

Texture controller는 텍스처 레벨 α = {αs, αa}에 영향을 받는데, 특히 스트로크와 추상화 유닛은 각각 stroke 두께(αs)와 추상화 수준(αa)에  의해 조절돼. 인코더로부터의 특징 f와 함께 stroke 유닛은 conv 브랜치를 통해 feature 집합 gs = {g1 s, ..., gN s}를 생성하고, abstraction 유닛은 ga를 동일한 방식으로 생성해. 그 다음, 텍스처 레벨 α{s,a}에 따라, 텍스처 레벨에 가장 가까운 두 g{s,a} 특징이 선택돼. 선택된 특징들은 α{s,a}와 인덱스 간의 각 거리에 기반하여 보간(interpolated)되고, 이는 요소별(element-wise) 추가 연산을 통해 결합돼.

우리는 stroke 제어 유닛을 모두 3x3 conv 레이어로 설계했는데, 이는 texture 레벨 분석에서 G의 RF가 stroke 두께에 영향을 미치지 않는다는 것을 보여주기 때문이야. 대신, 각 브랜치는 타겟 카툰 이미지의 다른 해상도로 훈련되어 있어. 추론 시, αs를 통한 특징 보간은 스트로크 두께에 대한 연속적인 제어를 가능하게 해. 추상화 유닛에 대해서는 분석을 바탕으로 단일 모듈을 구축했지만, stroke 유닛과 달리, 각 브랜치는 커널 사이즈가 증가하는 순서로 다른 conv 레이어를 포함해. 이는 G의 RF와 타겟 이미지의 해상도를 변경하면 추상화가 변경되기 때문이야. 출력 특징은 αa를 통해 스트로크 유닛과 동일하게 보간돼. stroke와 abstraction를 병렬로 분리된 구조로 설계함으로써, 각 유닛은 다른 측면에 집중할 수 있고, texture를 두 차원 공간으로 제어할 수 있는 능력을 제공해.

<img width="541" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/ffbdc7c6-ab18-4ec0-886c-50fd6cdd5a96">  
<img width="556" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/fb6a124d-e128-4af1-904e-ed15990ea991">  

### 3.2. Color module
목표: 주어진 I^Lab_src 색상을 사용자의 색상 의도에 맞게 카툰 이미지로 전달하면서, 타겟 카툰의 색상 뉘앙스를 반영  

#### 입력과 처리:
Input: 1) Lab 입력 사진(ILab src), 2) 입력 색상 맵(¯CLab src)  
Output: ab-채널 이미지(ˆIab src)  
* 텍스처 디코더에서 출력인 텍스처 맵(ˆIL tgt)과 결합  

#### 색상 맵 생성:
실제 사진(IRGB src)에서 슈퍼픽셀 알고리즘을 적용해 초기 색상 맵(CRGB src)을 생성합니다.  
슈퍼픽셀은 입력 이미지의 세부 사항에서 노이즈를 줄이는 데 사용됩니다.  

#### HSV 증강:
HSV 증강을 통해 IRGB src와 CRGB src의 색상을 변경하여 색상 조작된 이미지(¯IRGB src와 ¯CRGB src)를 만듭니다.  
이러한 이미지들은 Lab 공간으로 변환됩니다.  

#### L 캐싱 트릭:
색상 증강 전에 L 캐싱 트릭을 적용하여 이미지의 밝기(L)를 캐시하고, 증강된 이미지의 밝기를 캐시된 것으로 되돌립니다.  
이는 색상 변화가 인지적으로 비현실적인 결과를 생성하는 것을 방지하기 위함입니다.  

<img width="373" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/1bf0ff96-7312-457c-8897-633f9d74e36e">  
  
<img width="367" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/a1d7554e-1b78-4f9e-899e-463a54bae7e8">  

### 3.3. Model training
이전의 깊은 카툰화 방법과 달리, CARTOONER에서는 network warm-up을 수행하지 않는다.  
전체 프레임워크를 abstraction 제어 유닛을 제외하고 L = L_texture + L_color로 훈련  
abstraction 유닛은 L_texture를 통해 훈련되며, 다른 구성 요소는 모두 고정 상태로 유지  
G에 다양한 해상도의 이미지를 제공하기 위해, IRGB tgt를 α(텍스처 레벨)에 따라 크기 조정(그림 7 참조)  
abstraction 유닛의 kernel 사이즈 {K1, K2, ..., KN}를 각각 {3, 7, 11, 15, 19}로 설정  
CARTOONER 훈련 시, α{s,a} ∈ {1, ..., 5}를 무작위로 선택하여 IRGB tgt를 각각 {2562, 3202, 4162, 5442, 8002} 해상도로 조정하지만, 추론 시 α{s,a}는 임의의 숫자로 확장  
