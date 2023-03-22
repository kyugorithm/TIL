## Abstract
(Generative/geometric) prior로 인해 개선이 있었으나 입력에 faithful detail 생성은 개선필요.  
Dictionary-based method & VQ 기법에 착안하여 방법론 제안.  

High-quality low-level feature bank를 사용하므로 사실적인 얼굴 세부정보 복구에 도움  
그러나 VQ codebook 단순 적용만으로는 좋은 faithfull detail과 id 보존에 도움되지 않는다.  

따라서 두 가지 특별한 네트워크를사용한다.

1) VQ codebook의 compression patch size를 조사하고 적절한 크기로 설계된 VQ codebook이 quality/fidelity 균형을 맞추는데 중요하다.  
2) VQ codebook에서 생성된 사실적인 세부 사항을 "오염"시키지 않으면서 입력 low-level feature를 추가로 융합하기 위해 texture decoder와 main decoder로 구성된 parallel decoder 제안
이 두 디코더는 deformable conv.가 있는 texture warping module과 상호 작용한다.  
Facial detail dictionary인 VQ codebook과 parallel decoder 설계를 갖춤으로써 이전 방법의 충실도를 유지하면서 복원된 얼굴 디테일의 품질을 크게 향상시킬 수 있다.  

## 1. Introduction
BFR :  노이즈, 블러, 다운 샘플링 등과 같은 알 수 없는 저하가 있는 LQ 얼굴을 복구  
복잡한 저하, 다양한 얼굴 포즈 및 표정이 있는 실제 시나리오에서 더욱 어려워진다. 이전 작업은 일반적으로 generative geometric/facial/reference prior를 이용한다.  

### Geometric prior
일반적으로 face (landmark, parsing maps, heatmap) 등으로 구성된다.  
정확한 얼굴 모양을 복원하기 위한 global guidance 제공할 수 있지만 사실적인 세부 정보 생성에 도움은 되지 않는다.  
게다가, 기하 사전은 저하된 이미지에서 추정되므로 심각한 저하가 있는 입력에 대해 부정확하다.  
이러한 속성은 연구자가 나은 prior를 찾도록 동기부여한다.  
(ECCV/2018) Face super-resolution guided by facial component heatmaps
(CVPR/2018) FSRnet: End-to-end learning face superresolution with facial priors  
(CVPR/2021) PSFR-GAN : Progressive semantic-aware style transformation for blind face restoration  

### Generative prior 
일반적으로 StyleGAN의 강력한 생성 기능을 활용하여 사실적인 텍스처를 생성한다. 저하된 이미지를 GAN 잠재 공간으로 projection하고 사전 학습된 StyleGAN으로 HQ를 디코딩한다.  
언뜻 보기에 괜찮은 전체 복원 품질을 달성하지만 미세한 얼굴 detail, 특히 가는 머리카락과 섬세한 얼굴 구성 요소를 생성하지 못하며 이는 부분적으로 잘 학습된 GAN의 불완전한 latent space 때문일 수 있다.   
![image](https://user-images.githubusercontent.com/40943064/226795143-440a57fb-15fa-4bf9-8f25-5022c1b8ff44.png)

(CVPR/2021) GFPGAN : Towards real-world blind face restoration with generative facial prior
(CVPR/2021) GPEN : Gan prior embedded network for blind face restoration in the wild

### Reference prior
High-quality guided faces 또는 facial component dictionary를 탐색하여 얼굴 복원 문제를 해결한다.  
DFDNet은 동일한 id의 얼굴에 접근할 필요가 없는 대표적인 방법이다.  
여러 얼굴 구성 요소에 대해 고품질 "texture bank"를 명시적으로 설정한 다음 LQ 얼굴 구성 요소를 dictionary에서 가장 가까운 HQ 얼굴 구성 요소로 대체한다.  
이러한 개별 교체 작업은 low-quality와 high-quality facial component 간의 격차를 직접 연결하여 적절한 facial detail을 제공할 수 있는 잠재력을 갖는다.  
그러나 DFDNet의 얼굴 구성 요소 사전에는 여전히 두 가지 약점이 있다.  

1) (얼굴인식에 최적화되고 복원에는 그렇지 않은) 사전 학습된 VGGFace로 facial component dictionary를 오프라인에서 생성한다.  
2) 얼굴의 여러 부분(예: 눈, 코, 입)에만 초점을 맞추며 머리카락과 피부와 같은 다른 중요한 부분은 포함하지 않는다.  

(CVPR/2019) GWAInet : Exemplar guided face image super-resolution without facial landmarks
(ECCV/2020) DFDNet : Blind face restoration via deep multiscale component dictionaries
(ECCV/2018) Learning warped guidance for blind face restoration

Facial component dictionary 한계는 전체 얼굴 영역에 대해 구축된 dictionary인 VQ codebook을 탐구하도록 동기를 부여한다.  
VQFR은 dictionary와 GAN training 둘다 활용하지만 geometric/GAN prior는 필요없다.  
Facial component dictionary와 비교할 때 VQ codebook은 제한된 얼굴 구성요소에 국한되지 않는 보다 포괄적인 low level feature bank를 제공할 수 있다.  
또한 face reconstruction task 방식을 통해 end-to-end로 학습된다. 게다가 vector quantization mechanism은 다양한 저하에 대해 더욱 강력하다.  
그럼에도 불구하고 VQ codebook을 적용하는 것만으로는 좋은 결과를 얻기가 쉽지 않다.  

세부 정보 생성과 ID 보존 모두에서 이전 방법을 능가할 수 있는 두 가지 특별한 네트워크는 아래와 같다.  

1) 현실적인 세부 정보를 생성하려면 적절한 압축 패치 크기 f를 선택하는 것이 중요하다.   
그림 2에서 볼 수 있듯이 f가 클수록 시각적 품질은 좋아지지만 충실도는 나빠질 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/226797093-5af9cce6-7ec6-4799-b5b2-022bfa752c5d.png)
(포괄적인 조사 후 입력 이미지 크기 512×512에 대해 f = 32를 사용하는 것이 가장 좋다.)  

그러나 이러한 선택은 품질과 충실도 사이의 trade-off일 뿐이다.  
적절한 압축 패치 크기로도 expression and identity이 많이 바뀔 수 있다.  
간단한 해결책은 GFP-GAN에서와 같이 low-level feature를 입력이 아닌 디코더 레이어에 융합하는 것이다.  
입력 feature가 더 충실한 정보를 가져올 수 있지만 VQ codebook에서 생성된 현실적인 세부 정보가 "오염"될 수 있다.  
이 문제는 두 번째 네트워크 설계인 parallel decoder로 이어진다. 구체적으로, parallel decoder 구조는 texure decoder와 main decoder로 구성된다.  
Texture decoder는 VQ codebook의 latent representation 정보만 수신하는 반면, main decoder는 저하된 입력의 정보와 일치하도록 texture decoder feature를 왜곡한다.  
고품질 디테일의 손실을 제거하고 저하된 face와 더 잘 일치시키기 위해 메인 디코더에서 deformable conv.가 있는 texture warping 모듈을 추가로 채택한다.  
VQ codebook을 얼굴 dictionary로 사용하고 parallel decoder 설계를 통해 얼굴 복원을 위한 fidelity를 유지하면서 더 높은 품질의 얼굴 디테일을 얻을 수 있다.

### 기여사항
1. HQ detaill 정보를 가지는 VQ dcitionary를 제안한다. FR에서 compression patch size의 중요성과 함께 VQ 분석을 통해 잠재성과 한계를 보인다.
2. VQ codebook(HQ의 디테일을 손상시키지 않으면서 fidelity를 유지하는)으로부터 입력과 texture feature를 점진적으로 fuse 하기위해 Parallel decoder를 제안한다.

## 2. Related Works
### Vector-Quantized Codebook
VQVAE(NIPS/2017) : VQ codebook은 VQ-VAE에서 도입되었다. 인코더 네트워크 출력이 discrete하며 코드북에 캡슐화된 prior가 정적이 아니라 학습된다.  
VQVAE2(NIPS/2019) : 더 나은 이미지 생성을 위한 멀티스케일 코드북을 도입했다.  
VQGAN(CVPR/2021) : 적대적 목적으로 코드북을 훈련하므로 코드북은 높은 지각 품질을 달성할 수 있다.  

코드북 사용을 개선하기 위해 일부 연구에서는 L2 normalization 혹은 periodically re-initialization 같은 학습 기술을 탐색한다.  
이러한 VQ codebook은 patch tokenizer이며 이미지 생성, 다중 모달 생성 및 대규모 사전 훈련과 같은 여러 작업에 채택될 수 있다.  
VQ codebook을 사용하여 토큰 기능을 얻는 이전 작업과 달리 VQ 코드북을 HQ 얼굴 세부 정보 사전으로 탐색한다.
