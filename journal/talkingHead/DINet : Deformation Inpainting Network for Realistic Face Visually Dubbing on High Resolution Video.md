![image](https://github.com/kyugorithm/TIL/assets/40943064/e351cdbd-bd0f-41e8-a64d-a0caa4d3407a)
**Concept**  
디테일 보존을 위해 5개의 레퍼런스 이미지의 feature map으로부터 sptial deformation을 수행  
1) Feature-map deformation
- (5개의 ref. 이미지에 adaptive 하게 spatial deform을 적용)하여 (각 프레임의 입모양을 encoding하는 deformed feature 맵 생성). 이와 함께 입력 오디오와 헤드 포즈에 맞도록 정렬된다.
2) Inpainting
- 얼굴 시각 더빙을 생성하기 위해 Decoder는 변형된 feature map의 입 움직임과 source feature map의 head pose나 위쪽 얼굴 표정 등을 적응적으로 결합

## Introduction

### Talking head Generation
1. One shot talking face 
2. person-specific talking face
3. few-shot face visually dubbing(여러 업샘플링 레이어가 있는 conv. net을 통해 implicit embedding mouse pixel을 직접 생성)
- Wav2Lip(2020) : 6개의 conv. 레이어로 face decoder 설계  
- TRVD(2021) : Face decoder에서 upsample 레이어와 AdaIN 결합
이러한 간단한 방법은 고해상도 데이터를 사용하더라도 고해상도 비디오를 생성하는 데 어려움을 겪는다. (1:wav2lip구조 2:wav2lip 결과, 3:DINet결과)
<img height=200 src="https://github.com/kyugorithm/TIL/assets/40943064/7914b2dd-76f4-46ab-bf20-a77f704edc7b">

<img height= 200 src="https://github.com/kyugorithm/TIL/assets/40943064/e6f71f74-83a3-4bf8-8798-ab2af45a7338">
<img height= 200 src="https://github.com/kyugorithm/TIL/assets/40943064/bd40dcef-3748-4f49-bc14-f536e9bc9a77">  
  
디테일 부족의 이유는 few-shot 조건에서 입의 디테일은 입력 오디오와 상관성이 없기 때문에 디테일을 직접 생성하기 어렵기 때문이다.  
네트워크 입장에서, 다양한 발화방식을 가지는 수많은 인물의 복잡한 오디오-입 동기화 매핑을 하는것은 매우 어렵기 때문에 textural detail은 쉽게 무시된다.  
이러한 이유로 인해 person-specific dubbing 방식과 비교해서 더 블러한 결과를 생성하게 된다.  
이를 해결하기 위해 레퍼런스 얼굴 이미지의 feature map에 spatial transformation을 적용하여 mouse pixel을 inpaint 한다.  
특히 spatial transformation은 입 모양을 오디오와 sync를 맞추고 head-pose를 source 얼굴과 정렬할 수 있다.  
변형 작업은 픽셀을 처음부터 생성하지 않고 적절한 위치로 이동하므로 모든 텍스처 디테일을 거의 보존할 수 있다.  

![image](https://github.com/kyugorithm/TIL/assets/40943064/a1faa57b-25b1-46be-99fe-15a02f840c2b)  

## Related work
### Talking Fac Generation
오디오/텍스트에 따라 얼굴 이미지를 합성하는 것을 목표로 한다.  
이는 아래 세 가지 주요 방향으로 구성된다: 
#### One-shot
하나의 ref 얼굴 이미지를 다음 요소들을 고려하여 생성한다. : Synchronic lip movements, realistic facial expressions, rhythmic head  
일부 작업은 잠재 임베딩을 사용하여 구현한다. 먼저 ref. 이미지와 오디오를 latent embedding으로 encoding하고 네트워크를 사용하여 embedding을 합성 이미지로 decoding한다.  
Deblur loss, audio-visual correlation loss, audio-visual disentangled loss, spatial-temporal adversarial loss 같은 추가 손실은 품질을 향상시키는 데 사용된다.  
 
#### Few-shot face visually dubbing
오디오에 따라 소스 face의 입 영역을 복구하는 데 초점을 맞춘다. 기존 연구는 소스 얼굴에서 입 영역의 픽셀을 직접 생성하기 위해 유사한 방식의 얼굴 디코더, 다중 업샘플 레이어를 사용한다.  
시각적 품질을 향상시키기 위해 face landmark를 중간 구조적 표현으로 사용한다.  
1. 유효 SSIM 손실을 사용  
2. 입술 동기화를 개선하기 위해 사전 훈련된 동기화 장치에서 감독하는 동기화 손실을 추가  
3. 하나의 오디오 립 메모리를 사용하여 동기식 립 모양을 정확하게 검색.  
그러나 이러한 직접 생성 기반 방법은 고해상도 비디오에서 얼굴 더빙을 시각적으로 실현하지 못한다. 본 방법은 더 현실적인 결과를 얻기 위해 직접 생성 패션을 변형으로 대체한다.  

#### Person-specific talking face
학습 데이터에 ID가 특정되어 있다. 초기 작업은 audio-lip mapping 학습에 16시간의 영상이 필요하다.  
Fried는 rule-base 선택으로 교육 데이터를 1시간 미만으로 줄인다.  
Song은 공유 애니메이션 생성기 또는 Nerf를 사용하여 몇 분 분량의 영상만 사용할 수 있도록 한다.  
라히리는 변화 가능한 빛의 극한 조건을 처리하기 위해 조명 정규화를 사용한다.  
지씨는 표정, 눈 깜빡임과 같은 현실적인 얼굴 표정에 주의를 기울인다.

### Spatial Transformation
#### Affine transformation : 
아핀 변환의 계수를 먼저 계산한 후 모든 아핀 변환을 결합하여 이미지의 특징 맵에 변형을 적용합니다.
Jaderberg는 아핀 변환을 CNN 네트워크에 첫번째로 도입하였습니다. 이들은 각 특징 레이어에서 하나의 글로벌 아핀 변환을 계산합니다.
변형의 복잡성을 향상시키기 위해, Siarohin 등과 Wang, Mallya & Liu는 2D 또는 3D 영역에서 다른 계수를 계산함으로써 아핀 변환의 수를 증가시켰습니다.
더 복잡한 변형을 시뮬레이션하기 위해 Zhang & Ding는 AdaAT를 제안하였습니다. 이들은 채널별 특정 계수를 계산하여 아핀 변환의 수를 수백개로 늘립니다.

#### Dense flow : 
네트워크를 직접 사용하여 완전한 dense flow를 계산한 후 이를 이용해 feature map을 워핑하여 spatial transformation을 달성한다.  
Dense flow는 GCN, enc-dec 네트워크, weighted demodulation decoder에서 계산될 수 있다.  
본 연구에서는 가장 좋은 결과를 합성하기 때문에 AdaAT를 사용하여 spatial transformation을 사용한다.  

## Method
<img src="https://github.com/kyugorithm/TIL/assets/40943064/387fda8b-b32f-4782-b13e-5ebfba6ff55a">
