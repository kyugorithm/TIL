## GFPGAN : Towards Real-World Blind Face Restoration with Generative Facial Prior

## Abstract
Blind face restoration은 보통 사실적이고 신뢰할 수 있는 디테일을 복원하기 위해 facial prior(geometry face prior 혹은 reference prior)에 의존한다. 그러나, 고품질 reference는 획득하기 어려워 실제 상황에서 적용이 어려운 반면 저품질의 입력은 정확한 기하적 prior를 제공할 수 없다. 본 연구는 blind face restoration을 위해 사전학습된 face GAN에 캡슐화된 풍부하고 다양한 prior를 이용하는 GFP-GAN을 제안한다. GFP는 spatial feature transform 레이어를 통해 얼굴 복원 프로세스에 통합되며 이 레이어는 우리의 방법이 사실성과 충실성의 좋은 균형을 달성하도록 한다. 강력한 generative facial prior와 섬세한 설계 덕분에, 추론 시에 GAN inversion 같은 image-specific 최적화 없이 얼굴 디테일을 복원함과 동시에 단일의 forward pass를 이용해 색상을 복원할 수 있다.  

## 1. Introduction
Blind face restoration은 저해상도, 노이즈 블러, 압축 아티팩트 등 알 수 없는 열화를 겪고 있는 저품질 얼굴로부터 고품질 얼굴을 복구하는 것을 목적으로 한다. 실제 시나리오에 적용하면 성능 저하, 다양한 포즈 및 표현으로 인해 더욱 어려워진다. 과거 연구는 facial landmark, parsing map, facial component heatmap과 같은 얼굴 복원에서 얼굴 고유의 prior를 이용하며, 이러한 geometry face prior가 정확한 얼굴 모양과 세부 정보를 복구하는 데 중추적이라는 것을 보여준다. 그러나 이러한 우선 순위는 일반적으로 입력 이미지에서 추정되며 실제 환경에서는 매우 낮은 품질의 입력으로 인해 필연적으로 저하된다. 또한, semantic guidance에도 불구하고, 위의 이전 항목들은 얼굴 세부사항(예: 눈동자)을 복원하기 위한 제한된 텍스처 정보를 포함하고 있다.  

또 다른 범주의 접근방식은 reference prior(예: 고품질 high-quality guided faces 또는 facial component dictionaries)을 조사하여 현실적인 결과를 생성하고 저하된 입력에 대한 의존성을 완화한다. 그러나 고해상도 참조의 접근성은 실제 적용 가능성을 제한하지만, prior의 제한된 용량은 얼굴 디테일의 다양성과 풍부함을 제한한다.  

본 연구는 사실적 face restoration을 위해 GFP를 활용한다(StyleGAN과 같은 사전 학습된 얼굴 GAN 모델에 암묵적으로 캡슐화됨). 이러한 face GAN은 가변성이 높은 충실한 얼굴을 생성할 수 있기 때문에 geometry, face texture, 색채 등 풍부하고 다양한 prior를 제공할 수 있어 얼굴 디테일을 공동으로 복원하고 색을 강화할 수 있다(그림 1). 그러나 이러한 generative prior를 복원 과정에 포함시키는 것은 어렵다. 이전 시도에서는 일반적으로 GAN inversion을 사용한다. 먼저 저하된 이미지를 사전 학습된 GAN의 latent로 다시 'invert'한 다음, 계산량이 많은 이미지 특정 최적화를 수행하여 이미지를 재구성한다. 사실적인 결과에도 불구하고 저차원 latent code가 정확한 복원을 유도하기에 불충분하기 때문에 대개 낮은 충실도로 이미지를 생성한다.  
![image](https://user-images.githubusercontent.com/40943064/161587243-a6151a07-7134-4c5b-8e91-93eb256b4004.png)  


이를 해결하기 위해, 단일 forward pass로 현실성과 충실성의 균형을 잘 맞출 수 있는 섬세한 디자인의 GFP-GAN을 제안한다. 구체적으로는 열화 제거 모듈과 face prior로서의 pretrained face GAN으로 구성된다. 이들은 직접 latent code mapping과 여러 Channel-Split Spatial Feature Transform(CS-SFT; 채널 분할 공간 feature 변환) 레이어에 의해 대략적으로 세밀하게 연결된다. CS-SFT latyer는 feature 분할에 공간 변조를 수행하고 더 나은 정보 보존을 위해 왼쪽 feature가 직접 통과하도록 하여, 높은 충실도를 재교육하면서 generative prior feature를 효과적으로 통합할 수 있게 한다. 또한 local discriminator로 facial compenent loss를 도입하여 perceptual facial detail을 더욱 강화하는 한편, ID preserving loss를 사용하여 충실도를 더욱 향상시킨다.  

다음과 같이 기여도를 정리한다.  
1. Blind face recovery에 풍부하고 다양한 generative prior를 활용한다. Prior는 충분한 얼굴 텍스처와 컬러 정보를 포함하므로, 얼굴 복원과 색조 향상을 공동으로 실시할 수 있다.  
2. Generative facial prior를 통합하기 위한 구조와 섬세한 loss 설계로 GFP-GAN 프레임워크를 제안한다. CS-SFT 레이어를 사용하는 GFP-GAN은 단일 포워드 패스로 충실도와 텍스처 충실도의 균형을 달성한다.  
3. 광범위한 실험을 통해 합성 데이터 세트와 실제 데이터 세트 모두에서 이전 기술보다 뛰어난 성능을 달성한다는 것을 알 수 있다.

StyleGAN2의 latent를 prior로 활용 + 사용할 때 구조를 잘 맞도록 설계 + CS-SFT로 최적화 없이 단일 포워드로 얻어냄(이미지>latent>이미지). 

## 2. Related Work
#### Image Restoration
일반적으로 image restoration에는 SR, denoising, deblurring 및 compression removal이 포함된다. 만족스러운 결과를 얻기 위해, GAN은 보통 natural manifold에 solution을 더 가깝게 하기 위해 loss supervision으로 사용되는 반면, 우리의 작업은 사전 학습된 face GAN을 GFP로 활용하려고 시도한다. 
#### Face Restoration.
일반적인 face hallucination을 기반으로 geometry prior와 refernce prior의 두 가지 전형적인 얼굴 고유 prior가 통합되어 성능을 더욱 향상시킨다. **Geometry prior**는 face landmark, face parsing map과 face component heatmap을 포함한다. 그러나 1) 그러한 우선 사항은 저품질 입력으로부터의 추정을 필요로 하며 실제 시나리오에서는 필연적으로 저하된다. 2) 주로 기하학적 제약에 초점을 맞추고 복원을 위한 적절한 세부사항을 포함하지 않을 수 있다. 대신 GFP는, 열화된 이미지로부터 명시적인 geometric 추정을 수반하지 않고, 사전학습된 네트워크 내에 적절한 텍스처를 포함하고 있다.  
**Reference prior**는 일반적으로 동일한 ID의 reference image에 의존한다. 이 문제를 극복하기 위해, DFDNet은 복원을 안내하는 CNN feature로 각 구성 요소(예: 눈, 입)의 얼굴 prior를 구성할 것을 제안한다. 그러나 DFDNet은 주로 prior의 구성 요소에 초점을 맞추고 prior 범위를 벗어난 영역(예: 머리카락, 귀 및 얼굴 윤곽)에서 저하되며, 대신 GFP-GAN은 복원하기 위해 얼굴 전체를 처리할 수 있다. 게다가, GFP는 기하학, 텍스처, 색채 등 풍부하고 다양한 prior를 제공할 수 있는 반면, prior의 크기가 한정되어 있기 때문에 diversity와 richness가 제한된다.  

#### Generative Priors
사전 학습된 GAN의 generative prior는 입력 이미지가 주어진 가장 가까운 latent code를 찾는 것이 주된 목표인 GAN inversion에 의해 이전에 이용되었다. PLUST는 출력과 입력 사이의 거리가 임계값 미만이 될 때까지 StyleGAN의 latent code를 반복적으로 최적화한다. mGAN prior는 reconstruction 품질을 개선하기 위해 여러 code를 최적화하려고 시도한다. 그러나 이러한 방법은 저차원 latent code가 reconstruction을 안내하기에 불충분하기 때문에 일반적으로 낮은 fidelity 이미지를 생성한다. 이와는 대조적으로, 제안한 CS-SFT modulation 레이어는 높은 fidelity를 달성하기 위해 다중 해상도 공간 feature에 prior 통합을 가능하게 한다. 또한 추론 중에 GFP-GAN에서 높은 계산량의 최적화가 필요하지 않다. 

#### Channel Split Operation
일반적으로 소형 모델을 설계하고 모델 표현 능력을 향상시키기 위해 탐색된다. MobileNet은 깊이 있는 conv.를 제안하고 GhostNet은 conv.를 두 부분으로 분할하여 본질적인 feature map을 생성하기 위해 더 적은 수의 filter를 사용한다. DPN의 dual path 구조에서는, 각 패스의 기능의 재이용과 새로운 feature의 탐색이 가능하게 되어, 그 표현 능력이 향상된다. SR에서도 비슷한 아이디어가 사용된다. 델의 CS-SFT 레이어는, 같은 정신을 공유하지만, 운용과 용도는 다르다. Realness와 fidelity의 균형을 맞추기 위해 하나의 분할에 공간적 feature 변환을 채택하고 왼쪽 분할을 ID 남긴다.

#### Local Component Discriminators.
로컬 패치 분포에 초점을 맞추도록 제안된다. 얼굴에 적용될 때, 그러한 discriminative loss는 별개의 semantic facial 영역에 부과된다. 우리가 도입한 facial component loss도 그러한 디자인을 채택하지만 학습된 discriminative feature에 기초한 추가적인 스타일의 supervision을 가지고 있다.

## 3. Methodology
### 3.1. Overview of GFP-GAN
이 섹션에서는 GFP-GAN 프레임워크에 대해 설명한다. 불명확한 열화에 시달리는 입력 얼굴 화상 x에 대해 blind face restoration의 목적은 realness나 fidelity 면에서 GT image y와 가능한 한 유사한 고품질 이미지 y^를 추정하는 것이다.  

GFP-GAN의 전체적인 프레임워크는 그림2와 같다. GFP-GAN은 이전과 같이 열화 제거 모듈(U-Net)과 사전 훈련된 face GAN으로 구성되어 있다. 이들 레이어는 latent code mapping과 여러 Channel-Split Spatial Feature Transform(CS-SFT; 채널 분할 공간 feature 변환) layer에 의해 브리징된다. 특히 열화 제거 모듈은 복잡한 열화를 제거하고 두 가지 종류의 feature를 추출하도록 설계되어 있다. 
1) **F_latent** : 입력 이미지를 StyleGAN2의 가장 가까운 latent code에 mapping하기 위한 feature  
2) **F_spatial** : StyleGAN2 feature를 변조하기 위한 다중 해상도 공간 feature   

![image](https://user-images.githubusercontent.com/40943064/161704873-4c5507a7-11dd-41b8-a9fc-7c3ad2e1e1e8.png)


그 후 **F_latent**는 몇 개의 선형 레이어에 의해 중간 latent code W에 매핑된다. 입력 이미지에 근접한 latent code를 지정하면 StyleGAN2는 F_GAN으로 나타나는 중간 conv. feature를 생성할 수 있다. 이러한 feature는 사전 학습된 GAN의 weight로 캡처된 풍부한 얼굴 디테일을 제공한다. F_spatial은 face GAN feature F_GAN을 제안된 CS-SFT 레이어와 함께 공간적으로 조정하여 높은 fidelity를 유지하면서 현실적인 결과를 달성한다.  

학습 중에, global discriminative loss를 제외하고, 눈 및 입과 같이 지각적으로 중요한 얼굴 구성 요소를 강화하기 위해 discriminator를 사용하여 facial component loss를 도입한다. ID 재교육을 위해 ID preserving guidance도 채용한다.  

### 3.2. Degradation Removal Module
Blind face restoration은 복잡하고 심각한 열화(low-resolutionm blur, noise, JPEG artiface)에 직면한다.  
열화 제거 모듈은 위의 열화를 명시적으로 제거하고 F_latent/F_spatial의 '깨끗한' feature를 추출하여 후속 모듈의 부담을 완화하도록 설계되었다. U-Net 구조를 열화 제거 모듈로 채택했는데, 1) 큰 흐림을 제거하기 위해 receptive field를 증가시키고 2) 다중 해상도 feature를 생성할 수 있기 때문이다. 공식은 다음과 같다.  
![image](https://user-images.githubusercontent.com/40943064/161691819-a4c2a58c-7da2-4e84-96aa-e3ab2cb4c643.png)

F_latent는 입력 이미지를 StyleGAN2(Sec. 3.3)에서 가장 가까운 latent code에 매핑하는 데 사용된다. F_spatial은 StyleGAN2 feature를 변조하는 데 사용된다(3.4절).  

열화 제거에 대한 중간 supervision을 수행하기 위해 학습 초기에 각 해상도 스케일에서 L1 restoration loss를 사용한다. 특히 UNet 디코더의 각 해상도 스케일에 대한 이미지를 출력한 다음 이러한 출력을 GT 이미지 피라미드에 가깝게 제한한다.  

### 3.3. Generative Facial Prior and Latent Code Mapping
사전 학습된 face GAN은 conv. weight, 즉 generative prior에서 얼굴에 대한 분포를 캡처한다. 우리는 사전 학습된 face GAN을 활용하여 작업에 다양하고 풍부한 얼굴 세부 정보를 제공한다. Generative prior를 배포하는 일반적인 방법은 입력 이미지를 가장 가까운 latent code Z에 매핑한 다음 사전 학습된 GAN에 의해 해당 출력을 생성하는 것이다. 그러나 이러한 방법은 일반적으로 fidelity를 유지하기 위해 시간이 많이 소요되는 반복 최적화가 필요하다. 최종 이미지를 직접 생성하는 대신 더 많은 세부 사항을 포함하고 더 나은 fidelity를 위해 입력 feature에 의해 추가로 변조될 수 있기 때문에 가장 가까운 얼굴의 중간 conv. feature FGAN을 생성한다(3.4절 참조).

특히, 입력 이미지의 인코딩된 벡터 F_latent가 주어지면 semantic property, 즉 Z에서 여러 MLP로 변환된 중간 공간을 더 잘 보존하기 위해 먼저 중간 latent code W에 매핑한다. Latent code W는 사전 학습된 GAN의 각 conv. 레이어를 통과하고 각 해상도 스케일에 대한 GAN feature를 생성한다.  
![image](https://user-images.githubusercontent.com/40943064/161693415-6b7990c6-09cf-4229-9d75-e7334e76809c.png)
#### Discussion: Joint Restoration and Color Enhancement.
생성 모델은 사실적인 디테일과 생생한 질감을 넘어 다양하고 풍부한 prior를 포착한다. 예를 들어, 그들은 또한 joint 얼굴 복원 및 색상 향상을 위한 작업에 사용할 수 있는 색상 prior를 캡슐화한다. 실제 얼굴 이미지(예: 오래된 사진)는 일반적으로 흑백, 빈티지 노란색 또는 흐릿한 색상이다. Generative facial prior에서 생생한 컬러 prior를 통해 채색을 포함한 색상 향상을 수행할 수 있다. 우리는 generative face prior가 복원 및 조작을 위해 기존의 geometric prior, 3D prior 등을 통합한다고 믿는다.

### 3.4. Channel-Split Spatial Feature Transform
Fidelity를 더 잘 보존하기 위해 F_spatial를 추가로 사용하여 F_GAN을 변조한다. 입력에서 공간 정보를 보존하는 것은 얼굴 복원에 매우 중요하다. 일반적으로 fidelity 보존을 위한 local characteristics와 얼굴의 다른 공간 위치에서의 적응 복원이 필요하기 때문이다. 따라서 우리는 공간적 feature 변조를 위한 affine transformation 매개변수를 생성하는 공간 특징 변환(SFT)을 사용하고 이미지 복원 및 이미지 생성에 다른 조건을 통합하는 데 그 효과를 보여주었다. 특히, 각 해상도 스케일에서 여러 conv. 레이어에 의해 입력 feature F_spatial에서 한 쌍의 affine transformation 매개변수(a, b)를 생성한다. 그 후, 변조는 다음과 같이 공식화된 GAN feature FGAN을 스케일링 및 이동하여 수행된다.  
![image](https://user-images.githubusercontent.com/40943064/161694858-95514f01-0db6-484d-ae04-ff7f94e1ffdd.png)  
(Fsplit0_GAN/Fsplit1_GAN:채널 방향에서의 F_GAN으로부터의 split feature)  
결과적으로 CS-SFT는 prior 정보를 직접 통합하고 입력 이미지를 효과적으로 변조하여 질감의 faithfullness와 fidelity 사이의 균형을 잘 이루는 이점을 누립니다. 게다가 CS-SFT는 GhostNet[23]과 유사하게 변조를 위해 더 적은 수의 채널을 필요로 하기 때문에 복잡성을 줄일 수도 있다. 각 해상도 스케일에서 채널 분할 SFT 레이어를 수행하고 최종적으로 복원된 얼굴 ^y를 생성한다.

### 3.5. Model Objectives
GFP-GAN 학습의 목적함수:  
#### 1) Reconstruction loss : 출력 ^y를 실제 y에 가깝게 제한
널리 사용되는 L1 loss와 perceptual loss를 다음과 같이 정의된 reconstruction loss **Lrec**로 채택한다.  
![image](https://user-images.githubusercontent.com/40943064/161695806-1c9404eb-8ca8-4194-9c8b-ec265b51f9ef.png)  
Phi : pretrained VGG-19 & use (conv1 ~ conv5) feature map before activation

#### 2) Adversarial loss : 사실적 texture restoration
적대적 손실 Ladv를 사용하여 GFP-GAN이 자연 이미지 manifold의 솔루션을 선호하고 사실적인 질감을 생성하도록 권장한다. StyleGAN2와 유사하게 logistic loss를 사용한다.  
![image](https://user-images.githubusercontent.com/40943064/161696403-5ee69783-8408-4ac5-84c0-aa161086aa99.png)  

#### 3) facial compenet loss : 얼굴 세부 사항을 더욱 향상
지각적으로 중요한 얼굴 구성 요소를 더욱 향상시키기 위해 왼쪽 눈, 오른쪽 눈 및 입에 대한 local discriminator를 사용하여 얼굴 구성 요소 손실을 도입한다. 그림 2와 같이 먼저 관심 영역을 ROI 정렬로 자른다. 각 영역에 대해 우리는 복원 패치가 실제인지 여부를 구별하기 위해 별도의 작은 local discriminatator를 학습하여 패치를 자연스러운 얼굴 구성 요소 분포에 가깝게 밀어 넣는다.  

[62]에서 영감을 받아 학습된 discriminator를 기반으로 feature style loss를 추가로 통합한다. 공간제약이 있는 이전 feature matching loss 손실과 달리 우리의 feature sytle loss는 실제 패치와 복원된 패치의 Gram 행렬 통계를 일치시키려고 시도한다. Gram 행렬은 feature 상관 관계를 계산하고 일반적으로 텍스처 정보를 효과적으로 캡처한다. 학습된 local discriminator의 여러 레이어에서 feature를 추출하고 실제 패치와 복원된 패치에서 중간 표현의 이러한 Gram 통계를 일치시키는 방법을 배운다. 경험적으로, feature style loss가 사실적인 얼굴 세부 사항을 생성하고 불쾌한 인공물을 줄이는 측면에서 이전 feature matching loss보다 더 나은 성능을 보인다는 것을. 발견했다.  
얼굴 구성요소 손실은 다음과 같이 정의된다. 첫 번째 항은 discriminative loss, 두 번째 항은 feature style loss이다.  

![image](https://user-images.githubusercontent.com/40943064/161697319-bb656370-d1fa-43a3-8338-8da063028b48.png)  
(ROI : region of interest for {left-eye, right_eye, mouth} / D_ROIs : 각 영역에 대한 local discriminator)  

#### 4) Identity preserving loss
[31]에서 영감을 얻고 ID preserving loss를 적용한다. Perceptual loss와 유사하게, 입력 얼굴의 feature embedding을 기반으로 loss를 정의한다. 특히, ID 식별을 위해 가장 두드러진 feature를 포착하는 사전 학습된 얼굴 인식 ArcFace 모델을 채택한다. Loss를 보존하는 ID는 복원된 결과를 compact deep feature 공간에서 GT와 작은 거리를 갖도록 강제한다.  

![image](https://user-images.githubusercontent.com/40943064/161698274-b8a42cab-b447-47d8-804f-519152a05a79.png)  
(n : feature extract;ArcFace)
전체 모델의 목적함수는 아래와 같다.  
![image](https://user-images.githubusercontent.com/40943064/161698496-91f40801-1ae7-47a0-b902-498879d4402b.png)   
![image](https://user-images.githubusercontent.com/40943064/161698524-a55fa922-5335-4041-8a5f-d33617c5b9f0.png)  


## 4 Experiments
### 4.1. Datasets and Implementation
#### Training Datasets.
70k 이미지가 있는 FFHQ를 이용하여 학습하며 512x512로 이미지를 조정한다. 실제 세계의 저품질 이미지에 근사하는 합성 데이터에 대해 학습되며 추론동안 실제 세계 이미지에 일반화 한다.  [46, 44]에서 사용하는 방식을 적용하고 다음의 degradation model를 학습데이터를 합성하기 위해 사용한다.  
![image](https://user-images.githubusercontent.com/40943064/161707446-17e87f4b-0506-41a7-80ec-3357622e5452.png)  
고품질 이미지 y -> gaussian blur kernel k𝛔 convolution -> r 비율만큼 downsampling  
-> nδ gaussian noise 추가 -> q압축율로 JPEG 압축  
[44]와 유사하게 각 파라미터를 무작위로 샘플한다. 𝛔,r,δ,q : {0.2:10},{1:8},{0:15},{60:100}  
Color enhancement 학습시에 color jittering도 적용한다. 
#### Testing Datasets.
하나의 합성 데이터셋과 세개의 실제 이미지 데이터셋을 서로 다른 소스로 구성한다. 모든 데이터 셋은 학습 데이터셋과 겹치지 않는다. 간략한 소개를 한다. 
CelebA-Test는 테스트 파티션에서 3,000개의 CelebA-HQ 이미지가 포함된 합성 데이터 세트이다. 생성 방식은 학습과 같다.

LFW-Test. LFW에는 야생의 저품질 이미지가 포함되어 있다. 검증 파티션의 각 ID에 대한 모든 첫 번째 이미지를 그룹화하여 1711개의 테스트 이미지를 형성한다.

Celeb Child-Test에는 인터넷에서 수집한 연예인의 180명의 어린이 얼굴이 포함되어 있다. 품질이 낮고, 많은 것들이 흑백의 오래된 사진이다.

Web Photo-테스트. 인터넷에서 실생활에서 188장의 저품질 사진을 크롤링하고 407장의 얼굴을 추출하여 WebPhoto 테스트 데이터 세트를 구성했다. 이 사진은 다양하고 복잡한 열화가 있으며 일부는 디테일과 색상 모두 매우 심각하게 열화된 오래된 사진이다.

#### Implementation.
사전학습된 512 출력의 StyleGAN2을 face prior로 사용한다. StyleGAN2의 채널 승수는 소형 모델 크기에 대해 1로 설정된다. 열화 제거를 위한 UNet은 7xdownsample/7 x upsample로 구성되며, 각 다운샘플에는 residual block이 있다. 각 CS-SFT 레이어에 대해 2개의 conv. 레이어를 사용하여 각각 affine parameter를 생성한다. 미니 배치 사이즈는 12이다. Horizontal flip, color jitter로 학습 데이터를 증강한다. 얼굴의 구성 요소가 지각적으로 중요하므로 왼쪽 눈, 오른쪽 눈, 입의 세 가지 구성 요소를 고려한다. 각 구성요소는 원본 학습 데이터 세트에 제공된 얼굴 랜드마크와 ROI 정렬[24]로 잘린다. Adam Optimizer를 사용하여 모델을 총 800k 반복 학습한다. 학습 속도는 2 10^-3으로 설정되었고 700k번째, 750k번째 반복에서 2배 감소하였다. PyTorch 프레임워크로 모델을 구현하고 4대의 NVIDIA Tesla P40 GPU를 사용하여 모델을 학습한다.

### 4.2. Comparisons with State-of-the-art Methods
GFP-GAN을 몇 가지 최신 얼굴 복원 방법과 비교한다. : HiFaceGAN, DFDNet, PSFRGAN, Super-FAN, Wan.  
얼굴 복원을 위한 GAN 반전 방법: 비교를 위해 PLUST 및 mGAN prior도 포함되어 있다. 또한 GFP-GAN을 이미지 복원 방법인 RCAN, ESRGAN 및 DeblurGANv2와 비교하고 얼굴 트레이닝 세트를 미세 조정하여 공정하게 비교한다. Super-FAN을 제외하고 공식 코드를 채택하며 Super-FAN의 경우 re-implementation 한다.  

평가를 위해 널리 사용되는 비기준 지각 지표인 FID와 NIQE를 사용한다. CelebA-Test with GT를 위해 픽셀 단위 메트릭(PSNR 및 SSIM)과 지각 메트릭(LPIPS)을 채택한다. 작은 값이 GT에 가까운 식별성을 나타내는 ArcFace feature 임베딩에서 angle과 식별 거리를 측정한다.  

#### Synthetic CelebA-Test.
비교는 1) 입력과 출력이 동일한 해상도를 갖는 블라인드 얼굴 복원과 2)2) 4x face SR 두가지에서 수행한다. 이 방법은 얼굴 SR 입력으로 upsampling 이미지를 가져올 수 있다.  

각 설정에 대한 정량적 결과는 표 1과 표 2에 나와 있다. 두 가지 설정 모두에서 GFP-GAN은 가장 낮은 LPIPS를 달성하며, 이는 우리의 결과가 지각적으로 GT에 가깝다는 것을 나타낸다. 또한 GFP-GAN은 최저 FID 및 NIQE를 취득하여 각각 실제 얼굴 분포 및 자연 화상 분포에 근접한 거리를 가지고 있음을 보여준다. 지각적 성능 외에도, 우리의 방법은 얼굴 feature 삽입에서 가장 작은 정도로 나타나는 더 나은 identity를 유지한다. 주의: 1) FID 및 NIQE가 GT보다 낮다고 해서 성능이 GT보다 우수하다는 것은 아니다. 이러한 'perceptual' 메트릭은 대략적인 척도의 인간-오피니언 점수와 잘 상관되어 있지만, 항상 세밀한 척도로 잘 상관되어 있는 것은 아니기 때문이다. 2) 픽셀 단위의 메트릭 PSNR 및 SSIM은 상관 관계가 없다. 인간 관찰자에 대한 평가와 우리의 모델은 이 두 가지 지표에 능숙하지 않다.  

![image](https://user-images.githubusercontent.com/40943064/161723812-16c00232-0252-41a5-a01b-0906d06863b9.png)  

![image](https://user-images.githubusercontent.com/40943064/161723845-1e1bcbcb-794b-4e5e-bed6-bf108e773aa5.png)  


정성적 결과는 그림3과 그림4에 제시되어 있다. 
1) 강력한 generative facial prior 덕분에 눈(부골, 속눈썹), 치아 등의 충실한 디테일을 회복하고 
2) 복원 시 얼굴 전체를 처리하여 사실적인 모발을 발생시킬 수 있는 방법이며, 이전 방법은 component dictionaries (DFDNet)에 의존했다. Parsing maps (PSFRGAN)은 충실한 모발 텍스처를 생성하지 못한다(2번째 줄, 그림3). 
3) 충실도를 유지한다. PSFRGAN과 같이 강제로 치아를 추가하지 않고 자연스럽게 입을 닫게 된다(2번째 열, 그림3). 그림4에서는, GFP-GAN에 의해서, 합리적인 시선 방향이 복원된다. 

![image](https://user-images.githubusercontent.com/40943064/161721420-e7271ba8-4cf5-4192-a058-008f538a7d07.png)  
![image](https://user-images.githubusercontent.com/40943064/161721450-231d795e-1b22-480f-b28b-a5c1db61b4bd.png)  


#### Real-World LFW, CelebChild and WedPhoto-Test.
일반화 능력을 테스트하기 위해 세 가지 실제 데이터셋에서 모델을 평가한다. 정량적 결과는 표 3과 같다. GFP-GAN은 세 가지 실제 데이터셋 모두에서 뛰어난 성능을 달성하여 탁월한 일반화 능력을 보인다. PLUST는 높은 perceptual quality(낮은 FID 점수)를 얻을 수 있었지만 그림 5와 같이 얼굴 정체성을 유지할 수 없었다.  

![image](https://user-images.githubusercontent.com/40943064/161723940-aa859fb2-69d2-451f-8466-c5d0dab58e80.png)  


정성적 비교는 그림 5와 같다. GFPGAN은 기존의 강력한 generative prior와 함께 얼굴 복원 및 실제 사진 color enhancement를 공동으로 수행할 수 있었다. 복잡한 현실 세계 열화에서 그럴듯하고 현실적인 얼굴을 만들어 낼 수 있는 반면, 다른 방법은 충실한 얼굴 디테일을 회복하지 못하거나 artifact를 생성한다(특히 그림 5의 WebPhoto-Test에서). GFP-GAN은 눈과 치아와 같은 일반적인 얼굴 구성 요소 외에도, 분리된 부분보다는 얼굴 전체를 고려하기 때문에 머리카락과 귀에서 더 좋은 성능을 발휘한다. SC-SFT 레이어를 통해 당사의 모델은 높은 충실도를 달성할 수 있다. 그림 5의 마지막 줄에서 보듯이, 대부분의 이전 방법은 감은 눈을 복구하지 못했지만, 우리의 방법은 적은 아티팩트로 성공적으로 복원할 수 있었다.

![image](https://user-images.githubusercontent.com/40943064/161721507-cef82e53-fd32-4112-9ebb-f3695941aa89.png)  


### 4.3. Ablation Studies
#### CS-SFT layers.
표 4(a)와 그림 6에서 볼 수 있듯이 공간 변조 계층을 제거하면(즉, 공간 정보 없이 latent code mapping만 유지) 복원된 얼굴은 identity 보존 loss를 획득하지 못한다. (높은 LIPS 및 큰 degree). 따라서 CS-SFT 레이어에 사용되는 다중 해상도 공간 feature는 fidelity를 유지하는 데 중요하다.  

![image](https://user-images.githubusercontent.com/40943064/161721612-1c4b026e-f69c-462e-ab2f-300b343fca7f.png)


CS-SFT 레이어를 간단한 SFT 레이어로 전환할 때 [표 4b], 1) 모든 메트릭에서 perceptual 품질이 저하되고 2) 입력 이미지 feature가 모든 메트릭에 영향을 미치기 때문에 더 강한 ID(더 작은 Deg.)를 유지한다는 것을 관찰했다. 변조된 feature와 출력은 저하된 입력으로 바이어스되어 perceptual 품질이 낮아진다. 대조적으로 CSSFT layer는 feature split 을 조정하여 realness와 fidelity의 좋은 균형을 제공한다.

#### Pretrained GAN as GFP.
사전 학습된 GAN은 복원을 위한 풍부하고 다양한 feature를 제공한다. 표4(c)와 Fig. 6과 같이 generative face prior를 사용하지 않으면 성능 저하가 관찰된다.

#### Pyramid Restoration Loss.
열화 제거 모듈에 피라미드 복원 손실을 적용하여 실제 복잡한 열화에 대한 복원 능력을 강화한다. 이 중간 감독이 없으면 후속 변조를 위한 다중 해상도 공간 feature가 여전히 저하되어 표에 표시된 것처럼 성능이 저하될 수 있다. 표4(b) 및 그림 6.

#### Facial Component Loss.
1) 모든 facial compnent loss를 제거하고, 2) component discriminator만 유지하고, 3) 에서와 같이 추가 feature matching loss를 추가하고, 4) Gram 통계를 기반으로 추가 feature style loss를 채택한 결과를 비교한다. Feature style loss가 있는 구성 요소 discriminator가 눈 분포를 더 잘 포착하고 그럴듯한 세부 사항을 복원할 수 있음을 그림 7에서 볼 수 있다.  
![image](https://user-images.githubusercontent.com/40943064/161702092-2e6646d1-97b2-4ef9-b422-f9de1b69ab14.png)  

![image](https://user-images.githubusercontent.com/40943064/161702121-fe381b9d-8a98-4ed4-b427-cfd6e991f6fc.png)  

![image](https://user-images.githubusercontent.com/40943064/161702174-5943495b-d1aa-45dc-8f15-a947492d8c24.png)  



### 4.4. Discussion and Limitations

#### Training bias. 
변조를 위해 사전 학습된 GAN과 입력 이미지 feature을 모두 사용하기 때문에 대부분의 어두운 피부 얼굴과 다양한 인구 그룹에서 잘 수행된다(그림 8). 입력에 대한 fidelity를 유지하기 위해 출력을 제한하는 reconstruction loss 및 ID preserving loss를 사용한다. 그러나 입력 이미지가 회색조일 때 입력에 충분한 색상 정보가 포함되어 있지 않기 때문에 얼굴 색상에 바이어스가 있을 수 있다(그림8의 마지막 예). 따라서 다양하고 균형 잡힌 데이터 세트가 필요하다.  
![image](https://user-images.githubusercontent.com/40943064/161699699-67c6cf84-1298-4ba5-aa9d-8140e01356e5.png)  

#### Limitations.
그림9와 같이 실제 이미지 열화가 심할 경우 GFPGAN에 의해 복원된 얼굴 디테일이 아티팩트로 뒤틀린다. 또한 매우 큰 포즈에 대해 부자연스러운 결과를 생성한다. 합성 열화 및 학습 데이터 분포가 실제와 다르기 때문이다. 한 가지 방법은 미래 작업으로 남겨진 합성 데이터를 사용하는 대신 실제 데이터에서 이러한 분포를 배우는 것이다.  
![image](https://user-images.githubusercontent.com/40943064/161699664-8ec90e02-6fd6-4585-89ca-459c75527e7c.png)  

## 5. Conclusion
어려운 blind face restoration 작업에 대해 풍부하고 다양한 generative facial prior를 이용하는 GFP-GAN 프레임워크를 제안했다. 이 prior는 channel-split 공간 feature transform 레이어를 사용하여 복원 프로세스에 통합되어 realness와 fidelity의 좋은 균형을 얻을 수 있다.  
