## Abstract 
Cartoonization은 자연이미지를 만화 스타일로 변경하는 작업이다.  
이전 딥러닝 방식은 end-to-end를 이용하기 때문에 editability가 지원되지 않는다. 이를 해결하기 위해 대신 만화 창작 과정을 기반으로 texture 및 color의 편집 기능을 갖춘 참신한 솔루션을 제안한다.  
이를 위해 texture와 color 속성 분리를 위해 개별 decoder를 사용하는 구조를 설계한다.  
Texture decoder: 다양한 만화 질감을 만들기 위해서 stroke style 과 abstraction을 사용자가 제어할 수 있도록 texture controller를 제안한다.  
Color decoder: 다양하고 제어가능한 색상 변형을 만들기 위해 HSV color augmentation을 제안한다.  
* 최초의 딥러닝 기반 cartoonization 제어를 위한 첫 방법이다.

## Introduction
보편적 만화 제작과정: Character drawing -> BG composition -> Post-processing(Shading 등)  
이러한 제작과정 하에서 전문가들도 만화 제작은 고된 작업이다.  
작가들은 캐릭터 생성에 집중하기 위해 배경 사진을 카툰화하는 방법을 활용한다. (Animegan, Cartoongan, Learning to Cartoonize Using White-box Cartoon Representation)  
그러나, 이전 딥러닝 방식은 카툰 제작 과정에 대한 중간 과정을 생략해서 작가들이 결과물을 제어할 수가 없다.
예술가들은 사진으로부터 BG 이미지를 생성할때 일련의 단계를 거친다.  
Color stylization()
<img width="1145" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/690e4931-6771-447e-8259-f79762eddcee">


1) Color stylization: 저자는 지역적/전역적으로 색상을 변경하고 하늘을 합성한다.  
2) Texture stylization: 추가 스케치 선들을 그리고 서로다른 추상화를 얻기 위해 fine detail들은 선택적으로 제거한다.  
3) Post-processing : 조명과 이미지 필터를 포함한다.  
그러나 이 과정에서 end-to-end 방법을 사용하기 때문에 예술가들은 생성 과정에 대한 제어를 할 수 없고 입력 사진이나 최종 사진을 수정하는것만 가능하고 이는 제작 방식에 어려움이 있다.

본 작업에서는 카툰화에서 효율적인 interactivity를 포함하는 방식을 제시한다.  
제안된 솔루션은 texture와 color를 제어할 수 있도록 하는데 집중한다.  
Texture 제어: stroke 두깨와 추상화에 대한 조절로 정의한다. 이 컨셉은 많은 시나리오에서 활용될 수 있다. 예를들어 예술가는 자연스러운 시점을 묘사하거나 캐릭터 디테일을 강조하기 위해 먼거리 장면 디테일을 추상화할 수 있다. 제작자들은 마찬가지로 brushstroke의 미묘함을 수정해서 장면을 합성할 때 object 질감을 맞출 수 있다.  
Color 제어: 창작자가 자유롭게 임의 영억을 원하는 색상으로 조절할 수 있는 시스템을 만든다. 이것은 color stylization과정에서 예술가를 돕도록 설계했다.  

카툰화에서 사용자 조절성을 얻기 위해, 우리는 텍스처와 색상 디코더를 별도로 구축해서 기능 간의 간섭을 최소화해(그림 3 참조). 우리는 또한 분해된 아키텍처가 텍스처 스타일화의 강건함과 뛰어난 품질을 제공한다는 것을 발견했어.

텍스처 컨트롤에 대해, 우리는 수용 필드(receptive field, RF)와 타겟 이미지 해상도가 스트로크 두께와 추상화 수준에 어떤 역할을 하는지 조사했어. 이러한 관찰을 바탕으로, 우리는 네트워크의 수용 필드를 중간 특징의 동적 교체를 통해 조절하는 텍스처 컨트롤러를 제시해.

색상 컨트롤에 대해서는, 제안된 HSV 증강에 기반한 쌍 데이터셋과 함께 감독 방식으로 색상 디코더를 공동으로 훈련해. 이 훈련 전략을 통해 색상 모듈은 다양한 색상을 생성하는 능력을 얻게 돼.

분리된 텍스처와 색상 모듈의 조합으로, 우리는 사용자와의 의사소통에 따라 다양한 카툰화 결과를 만들 수 있는 두 차원의 컨트롤 공간을 달성해. 이러한 디자인은 강건하고 인지적으로 고품질의 카툰화 결과를 제공해.

우리가 아는 한, 우리의 프레임워크는 깊은 학습 기반 카툰화에 인터랙티비티를 제시하는 첫 번째 접근 방법이야. 제안된 솔루션을 바탕으로, 사용자의 의도에 따라 다양한 설정으로 카툰화된 이미지를 생성할 수 있는 응용 시나리오를 보여줘. 광범위한 실험들은 제안된 솔루션이 인지적 품질 측면에서 이전 카툰화 방법들을 능가하며, 사용자의 텍스처와 색상 선택에 따라 다수의 이미지를 생성할 수 있음을 보여줘.







To obtain user controllability in cartoonization, we separately build texture and color decoders to minimize interference across the features (Figure 3). 
We also found that the decomposed architecture provides a robust and superb quality of texture stylization. 
For texture control, we investigated the role of the receptive field and the target image resolution in the level of stroke thickness and abstraction. 
Based on these observations, we present a texture controller, which adjusts the receptive field of the network through a dynamic replacement of the intermediate features. 
For color control, we jointly train the color decoder in a supervised manner with the paired dataset that is built based on the proposed HSV augmentation. 
Throughout this training strategy, the color module gains the ability to produce diverse colors. 
With the combination of the decoupled texture and color modules, we achieve a two-dimension of control space that can create a variety of cartoonized results upon user communication. 
Such a design also provides robust and perceptually high-quality cartoonized outcomes. 

To the best of our knowledge, our framework is the first approach that presents interactivity to deep learning-based cartoonization. Based on the proposed solution, we demonstrate application scenarios that permit user intentions to create cartoonized images with diverse settings. Extensive experiments demonstrate that the proposed solution outperforms the previous cartoonization methods in terms of perceptual quality, while also being able to generate multiple images based on the user’s choices of texture and color.
