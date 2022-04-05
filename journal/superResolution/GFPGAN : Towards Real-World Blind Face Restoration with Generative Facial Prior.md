## GFPGAN : Towards Real-World Blind Face Restoration with Generative Facial Prior

## Abstract
Blind face restoration은 보통 사실적이고 신뢰할 수 있는 디테일을 복원하기 위해 facial prior(얼굴 기하적 prior 혹은 reference prior)에 의존한다. 그러나, 고품질 reference는 획득하기 어려워 실제 상황에서 적용이 어려운 반면 저품질의 입력은 정확한 기하적 prior를 제공할 수 없다. 본 연구는 blind face restoration을 위해 사전학습된 face GAN에 캡슐화된 풍부하고 다양한 prior를 이용하는 GFP-GAN을 제안한다. GFP는 spatial feature transform 레이어를 통해 얼굴 복원 프로세스에 통합되며 이 레이어는 우리의 방법이 사실성과 충실성의 좋은 균형을 달성하도록 한다. 강력한 생성적 facial prior와 섬세한 설계 덕분에, 추론 시에 GAN inversion 방법은 image-specific 최적화를 요구하지만, 우리의 GFP-GAN은 얼굴 디테일을 복원함과 동시에 단일의 forward pass를 이용해 색상을 복원할 수 있다.

## 1. Introduction
Blind face restoration은 저해상도, 노이즈 블러, 압축 아티팩트 등 알 수 없는 열화를 겪고 있는 저품질 얼굴로부터 고품질 얼굴을 복구하는 것을 목적으로 한다. 실제 시나리오에 적용하면 성능 저하, 다양한 포즈 및 표현으로 인해 더욱 어려워진다. 이전 작품들은 일반적으로 facial landmark, parsing map, facial component heatmap과 같은 얼굴 복원에서 얼굴 고유의 prior를 이용하며, 이러한 기하학적 얼굴 prior가 정확한 얼굴 모양과 세부 정보를 복구하는 데 중추적이라는 것을 보여준다. 그러나 이러한 우선 순위는 일반적으로 입력 이미지에서 추정되며 실제 환경에서는 매우 낮은 품질의 입력으로 인해 필연적으로 저하된다. 또한, semantic guidance에도 불구하고, 위의 이전 항목들은 얼굴 세부사항(예: 눈동자)을 복원하기 위한 제한된 텍스처 정보를 포함하고 있다.  

또 다른 범주의 접근방식은 reference prior(예: 고품질 high-quality guided faces 또는 facial component dictionaries)을 조사하여 현실적인 결과를 생성하고 저하된 입력에 대한 의존성을 완화한다. 그러나 고해상도 참조의 접근성은 실제 적용 가능성을 제한하지만, Prior의 제한된 용량은 얼굴 디테일의 다양성과 풍부함을 제한한다.  

본 연구에서는 사실적 face restoration을 위해 GFP를 활용한다(StyleGAN과 같은 사전 학습된 얼굴 GAN 모델에 암묵적으로 캡슐화됨). 이러한 face GAN은 가변성이 높은 충실한 얼굴을 생성할 수 있기 때문에 geometry, face texture, 색채 등 풍부하고 다양한 prior를 제공할 수 있어 얼굴 디테일을 공동으로 복원하고 색을 강화할 수 있다(그림 1). 그러나 이러한 generative prior를 복원 과정에 포함시키는 것은 어렵다. 이전 시도에서는 일반적으로 GAN inversion을 사용한다. 먼저 저하된 이미지를 사전 학습된 GAN의 latent로 다시 'invert'한 다음, 계산량이 많은 이미지 특정 최적화를 수행하여 영상을 재구성한다. 시각적으로 사실적인 출력에도 불구하고 저차원 latent code가 정확한 복원을 유도하기에 불충분하기 때문에 대개 낮은 충실도로 이미지를 생성한다. 
![image](https://user-images.githubusercontent.com/40943064/161587243-a6151a07-7134-4c5b-8e91-93eb256b4004.png)  


이러한 과제에 대처하기 위해, 우리는 하나의 forward pass로 현실성과 충실성의 균형을 잘 맞출 수 있는 섬세한 디자인의 GFP-GAN을 제안한다. 구체적으로는 GFPGAN은 열화 제거 모듈과 face prior로서의 pretrained face GAN으로 구성된다. 이들은 직접 latent code mapping과 여러 Channel-Split Spatial Feature Transform(CS-SFT; 채널 분할 공간 기능 변환) 레이어에 의해 대략적으로 세밀하게 연결된다. 제안된 CS-SFT latyer는 feature 분할에 공간 변조를 수행하고 더 나은 정보 보존을 위해 왼쪽 feature가 직접 통과하도록 하여, 우리의 방법이 높은 충실도를 재교육하면서 생성적 prior feature를 효과적으로 통합할 수 있게 한다. 또한 local discriminator로 facial compenent loss를 도입하여 perceptual facial detail을 더욱 강화하는 한편, ID preserving loss를 사용하여 충실도를 더욱 향상시킨다.  

다음과 같이 기여도를 정리한다.  
1. Blind face recovery에 풍부하고 다양한 generative prior를 활용한다. Prior는 충분한 얼굴 텍스처와 컬러 정보를 포함하고 있기 때문에, 얼굴의 복원과 색조 향상을 공동으로 실시할 수 있다.  
2. Generative facial prior를 통합하기 위한 구조와 loss의 섬세한 설계로 GFP-GAN 프레임워크를 제안한다. CS-SFT 레이어를 사용하는 GFP-GAN은 단일 포워드 패스로 충실도와 텍스처 충실도의 균형을 달성한다.  
3. 광범위한 실험을 통해 합성 데이터 세트와 실제 데이터 세트 모두에서 이전 기술보다 뛰어난 성능을 달성한다는 것을 알 수 있다.

## 2. Related Work
#### Image Restoration
일반적으로 image restoration에는 SR, denoising, deblurring 및 compression removal이 포함된다. 시각적으로 만족스러운 결과를 얻기 위해, GAN은 보통 natural manifold에 solution을 더 가깝게 하기 위해 loss supervision으로 사용되는 반면, 우리의 작업은 사전 학습된 face GAN을 GFP로 활용하려고 시도한다. 
#### Face Restoration.
일반적인 얼굴 환각을 기반으로 geometry prior와 refernce prior의 두 가지 전형적인 얼굴 고유 prior가 통합되어 성능을 더욱 향상시킨다. Geometry prior는 face landmark, face parsing map과 face component heatmap을 포함한다. 그러나 1) 그러한 우선 사항은 저품질 입력으로부터의 추정을 필요로 하며 실제 시나리오에서는 필연적으로 저하된다. 2) 주로 기하학적 제약에 초점을 맞추고 복원을 위한 적절한 세부사항을 포함하지 않을 수 있다. 대신에, 채용되고 있는 GFP는, 저하된 이미지로부터의 명시적인 geometric 추정을 수반하지 않고, 사전 검증된 네트워크내에 적절한 텍스처를 포함하고 있다.  
Reference prior는 일반적으로 동일한 ID의 reference image에 의존한다. 이 문제를 극복하기 위해, DFDNet은 복원을 안내하는 CNN feature로 각 구성 요소(예: 눈, 입)의 얼굴 prior를 구성할 것을 제안한다. 그러나 DFDNet은 주로 prior의 구성 요소에 초점을 맞추고 prior 범위를 벗어난 영역(예: 머리카락, 귀 및 얼굴 윤곽)에서 저하되며, 대신 GFP-GAN은 복원하기 위해 얼굴 전체를 처리할 수 있다. 게다가, GFP는 기하학, 텍스처, 색채 등 풍부하고 다양한 선험을 제공할 수 있는 반면, prior의 크기가 한정되어 있기 때문에 diversity와 richness가 제한된다. 

#### Generative Priors
사전 학습된 GAN의 generative prior는 입력 이미지가 주어진 가장 가까운 latent code를 찾는 것이 주된 목표인 GAN inversion에 의해 이전에 이용되었다. PLUST는 출력과 입력 사이의 거리가 임계값 미만이 될 때까지 StyleGAN의 latent code를 반복적으로 최적화한다. mGAN prior는 reconstruction 품질을 개선하기 위해 여러 code를 최적화하려고 시도한다. 그러나 이러한 방법은 저차원 latent code가 reconstruction을 안내하기에 불충분하기 때문에 일반적으로 낮은 fidelity로 이미지를 생성한다. 이와는 대조적으로, 우리가 제안한 CS-SFT modulation 레이어는 높은 fidelity를 달성하기 위해 다중 해상도 공간 feature에 prior 통합을 가능하게 한다. 또한 추론 중에 GFP-GAN에서 높은 계산량의 반복 최적화가 필요하지 않다. 

#### Channel Split Operation
일반적으로 소형 모델을 설계하고 모델 표현 능력을 향상시키기 위해 탐색된다. MobileNet은 깊이 있는 conv.를 제안하고 GhostNet은 conv.를 두 부분으로 분할하여 본질적인 feature map을 생성하기 위해 더 적은 수의 filter를 사용한다. DPN의 dual path 구조에서는, 각 패스의 기능의 재이용과 새로운 feature의 탐색이 가능하게 되어, 그 표현 능력이 향상된다. SR에서도 비슷한 아이디어가 사용된다. 델의 CS-SFT 레이어는, 같은 정신을 공유하지만, 운용과 용도는 다르다. Realness와 fidelity의 균형을 맞추기 위해 하나의 분할에 공간적 feature 변환을 채택하고 왼쪽 분할을 ID 남긴다.

#### Local Component Discriminators.
로컬 패치 분포에 초점을 맞추도록 제안된다. 얼굴에 적용될 때, 그러한 discriminative loss는 별개의 semantic facial 영역에 부과된다. 우리가 도입한 facial component loss도 그러한 디자인을 채택하지만 학습된 discriminative feature에 기초한 추가적인 스타일의 supervision을 가지고 있다.

## 3. Methodology
### 3.1. Overview of GFP-GAN
이 섹션에서는 GFP-GAN 프레임워크에 대해 설명한다. 불명확한 열화에 시달리는 입력 얼굴 화상 x에 대해 blind face restoration의 목적은 realness나 fidelity 면에서 GT image y와 가능한 한 유사한 고품질 이미지 y^를 추정하는 것이다.  

GFP-GAN의 전체적인 프레임워크는 그림 2와 같다. GFP-GAN은 이전과 같이 열화 제거 모듈(U-Net)과 사전 훈련된 face GAN으로 구성되어 있다. 이들 레이어는 latent code mapping과 여러 Channel-Split Spatial Feature Transform(CS-SFT; 채널 분할 공간 기능 변환) layer에 의해 브리징된다. 특히 열화 제거 모듈은 복잡한 열화를 제거하고 두 가지 종류의 feature를 추출하도록 설계되어 있다. 1) latent feature **F_spatial**는 입력 이미지를 Style의 가장 가까운 StyleGAN2에서의 latent code에 mapping한다. 그리고 2) StyleGAN2 feature를 변조하기 위한 다중 해상도 공간 feature **F_spatial** 

그 후 **F_latent**는 몇 개의 선형 레이어에 의해 중간 latent code W에 매핑된다. 입력 이미지에 근접한 latent code를 지정하면 StyleGAN2는 FGAN으로 나타나는 중간 conv. feature를 생성할 수 있다. 이러한 feature는 사전 학습된 GAN의 weight로 캡처된 풍부한 얼굴 디테일을 제공한다. F_spacial은 face GAN feature FGAN을 제안된 CS-SFT 레이어와 함께 공간적으로 조정하여 높은 fidelity를 유지하면서 현실적인 결과를 달성한다.  

학습 중에, 전체적인 discriminative loss를 제외하고, 눈 및 입과 같이 지각적으로 중요한 얼굴 구성 요소를 강화하기 위해 discriminator를 사용하여 facial component loss를 도입한다. ID 재교육을 위해 ID 보존 가이던스도 채용한다.  

### 3.2. Degradation Removal Module
실제 blind face restoration은 복잡하고 심각한 열화(low-resolutionm blur, noise, JPEG artiface)에 직면한다.  
열화 제거 모듈은 위의 열화를 명시적으로 제거하고 Flatent 및 Fspatial의 '깨끗한' 기능을 추출하여 후속 모듈의 부담을 완화하도록 설계되었다. 우리는 U-Net 구조를 열화 제거 모듈로 채택했는데, 1) 큰 흐림을 제거하기 위해 receptive field를 증가시키고 2) 다중 해상도 feature를 생성할 수 있기 때문이다. 공식은 다음과 같다.  
![image](https://user-images.githubusercontent.com/40943064/161691819-a4c2a58c-7da2-4e84-96aa-e3ab2cb4c643.png)

Latent feature Flatent는 입력 이미지를 StyleGAN2(Sec. 3.3)에서 가장 가까운 latent code에 매핑하는 데 사용된다. 다중 해상도 공간 feature Fspatial은 StyleGAN2 feature를 변조하는 데 사용된다(3.4절).

열화 제거에 대한 중간 supervision을 수행하기 위해 교육 초기 단계에서 각 해상도 스케일에서 L1 restoration loss를 사용한다. 특히 우리는 또한 UNet 디코더의 각 해상도 스케일에 대한 이미지를 출력한 다음 이러한 출력을 GT 이미지 피라미드에 가깝게 제한한다.

### 3.3. Generative Facial Prior and Latent Code Mapping
사전 학습된 face GAN은 conv. 가중치, 즉 generative prior에서 얼굴에 대한 분포를 캡처한다. 우리는 사전 학습된 얼굴 GAN을 활용하여 작업에 다양하고 풍부한 얼굴 세부 정보를 제공한다. Generative prior를 배포하는 일반적인 방법은 입력 이미지를 가장 가까운 latent code Z에 매핑한 다음 사전 학습된 GAN에 의해 해당 출력을 생성하는 것이다. 그러나 이러한 방법은 일반적으로 fidelity를 유지하기 위해 시간이 많이 소요되는 반복 최적화가 필요하다. 최종 이미지를 직접 생성하는 대신 더 많은 세부 사항을 포함하고 더 나은 fidelity를 위해 입력 feature에 의해 추가로 변조될 수 있기 때문에 가장 가까운 얼굴의 중간 conv. feature FGAN을 생성한다(3.4절 참조).

특히, 입력 이미지의 인코딩된 벡터 F_latent(U-Net, Eq. 1에 의해 생성됨)가 주어지면 semantic property, 즉 Z에서 여러 MLP로 변환된 중간 공간을 더 잘 보존하기 위해 먼저 중간 latent code W에 매핑한다. Latent code W는 사전 학습된 GAN의 각 conv. 레이어를 통과하고 각 해상도 스케일에 대한 GAN feature를 생성한다.  
![image](https://user-images.githubusercontent.com/40943064/161693415-6b7990c6-09cf-4229-9d75-e7334e76809c.png)
#### Discussion: Joint Restoration and Color Enhancement.
생성 모델은 사실적인 디테일과 생생한 질감을 넘어 다양하고 풍부한 사전을 포착한다. 예를 들어, 그들은 또한 joint 얼굴 복원 및 색상 향상을 위한 작업에 사용할 수 있는 색상 prior를 캡슐화한다. 실제 얼굴 이미지(예: 오래된 사진)는 일반적으로 흑백, 빈티지 노란색 또는 흐릿한 색상이다. Generative facial prior에서 생생한 컬러 prior를 통해 채색을 포함한 색상 향상을 수행할 수 있다. 우리는 generative face prior가 복원 및 조작을 위해 기존의 geometric prior, 3D prior 등을 통합한다고 믿는다.

### 3.4. Channel-Split Spatial Feature Transform
Fidelity를 더 잘 보존하기 위해 입력 공간 feature Fspatial(U-Net에서 생성, Eq. 1)을 추가로 사용하여 Eq.2의 GAN feature FGAN을 변조한다. 입력에서 공간 정보를 보존하는 것은 얼굴 복원에 매우 중요하다. 일반적으로 fidelity 보존을 위한 local characteristics와 얼굴의 다른 공간 위치에서의 적응 복원이 필요하기 때문이다. 따라서 우리는 공간적 feature 변조를 위한 affine transformation 매개변수를 생성하는 공간 특징 변환(SFT)을 사용하고 이미지 복원 및 이미지 생성에 다른 조건을 통합하는 데 그 효과를 보여주었다. 특히, 각 해상도 스케일에서 여러 conv. 레이어에 의해 입력 feature Fspatial에서 한 쌍의 affine transformation 매개변수(a, b)를 생성한다. 그 후, 변조는 다음과 같이 공식화된 GAN feature FGAN을 스케일링 및 이동하여 수행된다.  
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
ROI : region of interest for {left-eye, right_eye, mouth} / D_ROIs는 
#### 4) Identity preserving loss



#### Reconstruction Loss.
#### Adversarial Loss.
#### Facial Component Loss.
#### Identity Preserving Loss.

## 4 Experiments
### 4.1. Datasets and Implementation
#### Training Datasets.
#### Testing Datasets.
#### Implementation.

### 4.2. Comparisons with State-of-the-art Methods
#### Synthetic CelebA-Test.
#### Real-World LFW, CelebChild and WedPhoto-Test.

### 4.3. Ablation Studies
### 4.4. Discussion and Limitations
