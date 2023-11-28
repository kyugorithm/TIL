## 3. Method
고해상도 이미지 합성을 위한 DM 학습에 필요한 계산 부담을 줄이기 위해, DM이 해당하는 손실 항목을 언더샘플링함으로써 인지적으로 중요하지 않은 세부사항을 무시할 수 있다. 하지만 이러한 방법은 여전히 픽셀 공간에서 비용이 많이 드는 함수 평가를 필요로 하며, 계산 시간및 에너지 자원에 거대한 요구를 가져온다. 이러한 단점을 피하기 위해, compression 단계와 생성 학습 단계를 명확히 분리하는 방법을 제안한다(그림 2 참조). 이를 위해, 이미지 공간과 인지적으로 동등하지만 계산 복잡성이 훨씬 줄어든 공간을 학습하는 autoencoding 모델을 활용한다.  
  
### 접근 방법의 장점  
1. 고차원의 이미지 공간을 벗어남으로써, 저차원 공간에서 샘플링이 수행되기 때문에 계산적으로 훨씬 효율적인 DM을 얻을 수 있다.  
2. DM의 UNet 구조로부터 상속받은 inductive bias를 활용하여 공간 구조를 가진 데이터에 특히 효과적이며, 이전 접근법들이 요구한 공격적이고 quality-reducing compression levels의 필요성을 완화한다.  
3. 다양한 생성 모델을 학습하고 downstream application(e.x., single-image CLIP-guided synthesis)에도 사용될 수 있는 일반 목적의 compression models의 latent space를 얻는다.  
  
 ## 3.1. Perceptual Image Compression
Perceptual compression model은 VQGAN를 기반으로 하며, LPIPS와 패치 기반(pix2pix) adversarial objective 조합으로 학습된 AE로 구성된다. 이는 local realism을 강화함으로써 reconstruction이 image manifold에 제한되도록 하고, L2나 L1 목표와 같은 픽셀 공간 손실에만 의존함으로써 도입되는 흐릿함을 피한다. 정확하게, RGB 공간의 이미지 x가 주어지면, 인코더 E는 x를 잠재 표현 z = E(x)(R^ hxwxc)로 인코딩하고, 디코더 D는 잠재 표현에서 이미지를 재구성하여 ~x = D(z) = D(E(x))를 생성한다. 중요하게, 인코더는 이미지를 f = H/h = W/w 비율로 다운샘플링하며, 다양한 다운샘플링 비율 f = 2^m을 조사한다.  
  
임의로 높은 분산을 가진 잠재 공간을 피하기 위해, 두 가지 다른 종류의 regularization을 실험한다. 첫 번째 변형인 KL-reg는 VAE와 유사하게 학습된 잠재 공간에 표준 정규 분포에 대한 약간의 KL-페널티를 부과한다. 반면, VQ-reg.는 디코더 내부에 vector quantization 레이어를 사용한다. 이 모델은 디코더에 의해 흡수된 quantization 레이어를 가진 VQGAN으로 해석될 수 있다. 우리의 후속 DM은 학습된 잠재 공간 z = E(x)의 이차원 구조와 함께 작동하도록 설계되었기 때문에, 비교적 온건한 압축률을 사용하고 매우 좋은 재구성을 달성할 수 있다. 이는 잠재 공간 z의 분포를 자기회귀적으로 모델링하기 위해 학습된 공간 z의 임의적인 1D 순서에 의존하고 z의 본질적인 구조를 대부분 무시한 이전 연구들 [23, 66]과 대조적이다. 따라서, 우리의 압축 모델은 x의 세부 사항을 더 잘 보존한다(표 8 참조). 전체 목표와 학습 세부 사항은 보충 자료에서 찾을 수 있다.


이미지의 디테일을 유지하기 위해 인지적 손실과 적대적 목표를 결합한 특별한 학습 방식을 사용한다.:이는 이미지가 흐릿해지는 것을 방지하고 더 현실적인 재구성을 가능하게 한다.
#### 잠재공간품질을 유지하기 위해  두가지 정규화 방법 실험  
1. KL-정규화: 잠재 공간이 표준 정규 분포를 따르도록 한다.   
2. VQ-정규화: 벡터 양자화를 사용한다. 잠재 공간이 너무 복잡해지거나 불규칙해지는 것을 방지한다.  

### 3.2. Latent Diffusion Models

#### Diffusion Models
Diffusion Models은 데이터 분포 p(x)를 배우기 위해 설계된 확률적 모델이다. 이들은 정규 분포의 변수를 점차적으로 노이즈 제거함으로써 작동하며, 이는 고정된 Markov Chain의 역과정을 배우는 것과 동일하다. 이 체인의 길이는 T이다. 이미지 합성에서 가장 성공적인 모델들(Classifier guidance, DDPM, SR3)은 p(x)에 variational lower bound의 재가중 버전에 의존한다. 이는 denoising score-matching을 반영한다.  
이 모델들은 노이즈가 제거된 자신의 입력 xt를 예측하도록 훈련된 일련의 노이즈 제거 AE인 𝝐_𝜃(xt, t), t = 1, ..., T의 동등하게 가중된 시퀀스로 해석될 수 있다. 여기서 xt는 입력 x의 노이즈 버전이다. 해당 목표는 다음과 같이 단순화될 수 있다.  
<img width="300" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/7d67347a-36d8-4915-bda2-f2ebdb3f4d85">  
여기서 t는 {1, ..., T}에서 균등하게 샘플링된다.

요약: 데이터를 이해하기 위해 노이즈를 단계적으로 제거하는 방식으로 학습하는 모델이며 Markov Chain의 역과정을 모방하여 이미지의 노이즈를 제거하는 다수의 AE들을 시퀀스로 사용한다. 이 과정을 통해 고도로 정교한 이미지 생성이 가능해진다.  

#### Generative Modeling of Latent Representations
학습된 perceptual compression model(AE더의 인코더 E와 디코더 D로 구성)을 사용하여 저차원의 효율적인 잠재 공간(latent space)에 접근하는 방법에 대해 설명하고 있다. 이 잠재 공간은 높은 주파수와 인지하기 어려운 세부사항을 추상화하여 제거한다. 이 저차원 공간은 고차원 픽셀 공간에 비해 likelihood-based generative models에 더 적하다. 이는 생성 모델이 (i) 데이터의 중요하고 의미 있는 부분에 집중할 수 있고 (ii) 계산적으로 훨씬 더 효율적인 저차원 공간에서 학습할 수 있기 때문이다.  

이전 연구들은 압축된 discrete latent space에서 autoregressive, attention-based transformer models에 의존했지만, 본 연구에서는 모델이 제공하는 image-specific inductive biases을 활용할 수 있다. 이는 주로 2D 컨볼루셔널 레이어로 구성된 UNet을 사용하고, reweighted bound를 통해 인지적으로 가장 관련 있는 부분에 목표를 집중하는 능력을 포함한다. 이렇게 수정된 식은 다음과 같다:

<img width="451" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/2b3fa82e-dce7-4c1d-8733-d1c1cd418de5">
모델의 neural network backbone은 "time-conditional UNet"으로 구현된다. Forward process가 고정되어 있으므로, zt는 훈련 중 𝜺을 통해 효율적으로 얻을 수 있으며, p(z)에서 샘플을 뽑아 Decoder를 통해 한 번의 패스로 이미지 공간으로 decode할 수 있다.  

### 3.3. Conditioning Mechanisms
DMs이 조건부 분포를 모델링하는 능력에 대해 설명하고 있다. cGAN, cVAE처럼 DM도 원칙적으로 p(z|y)형태의 조건부 분포를 모델링할 수 있다. 여기서 z는 잠재 공간에서의 요소를, y는 조건을 나타낸다. 이것은 conditional denoising autoencoder 𝜺(zt, t, y)를 통해 구현할 수 있으며, 텍스트(Generative adversarial text to image synthesis), 의미 지도(semantic maps) 또는 I2IT 작업(pix2pix)과 같은 입력  y를 통해 합성 과정을 제어하는 길을 연다.  
  
이미지 합성의 맥락에서, DM의 생성력을 클래스 라벨(Class guided)이나 입력 이미지의 흐릿한 변형(SR3)과 같은 다른 유형의 조건들과 결합하는 것은 아직까지 탐구되지 않은 연구 분야이다. 연구팀은 DM를 더 유연한 조건부 이미지 생성기로 변환하기 위해 다양한 입력 형태의 attention 기반 모델을 학습하는 데 효과적인 기본 UNet backbone에 cross-attention mechanism을 추가한다. 언어 프롬프트와 같은 다양한 모달리티를 전처리하기 위해, 연구팀은 y를 중간 표현 τ𝜃(y) in R ^ M x d_tau 로 투영하는 도메인 특정 인코더를 도입한다. 이 중간 표현은 cross-attention layer를 통해 UNet의 중간 레이어로 매핑되며, 이 레이어는 아래 수식을 구현한다.  
  
<img width="505" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/4a4f2df9-242d-4315-8a7e-db9a0fb14136">  


Image-conditioning pairs를 기반으로 우리는 conditional LDM을 아래와 같이 정의한다.  
<img width="504" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/f8233b7b-4e89-4f9d-a203-6dcbb58c6f89">  
Domain specific encoder와 diffusion 모델은 동시에 최적화된다.  
여기서, τθ는 특정 도메인에 맞춘 전문가들에 의해 매개변수화될 수 있다. 예를 들어, y가 텍스트 프롬프트인 경우에는 transformers와 같은 도메인별 전문가를 사용한다. 이 변환기는 마스킹되지 않은(unmasked) 형태일 수 있다.  
  
요약: DMs을 통해 다양한 조건(예: 텍스트, 의미 지도 등)에 따라 이미지를 생성하는 방법을 탐구한다. UNet에 cross-attention mechanism을 추가함으로써, 다양한 입력 형태에 대한 더 유연한 조건부 이미지 생성을 가능하게 한다.


## 4. Experiments
LDM은 다양한 이미지 모달리티에 대한 유연하고 계산적으로 처리 가능한 diffusion 기반 이미지 합성 수단을 제공한다.  
성능을 보이기위해 학습과 추론에서 pixel-based DM과 비교하여 우리 모델의 이점을 분석한다. 흥미롭게도, VQ-reg. latent space에서 학습된 LDMs는 때때로 더 나은 샘플 품질을 달성하며, 이는 VQ-req. 첫 단계 모델의 재구성 능력이 연속된 대응물보다 약간 뒤떨어진다는 점에도 불구하고 그렇다. 표 8과 부록 D.1에서 LDM 학습 및 고해상도 이미지에서의 일반화 능력에 대한 첫 단계 정규화 방식의 영향에 대한 시각적 비교를 찾을 수 있다. E.2에서는 이 섹션에서 제시된 모든 결과에 대한 아키텍처, 구현, 학습 및 평가 세부사항을 나열한다.  

### 4.1. On Perceptual Compression Tradeoffs
이 섹션에서는 다운샘플링 요소 f가 {1, 2, 4, 8, 16, 32}(1인 경우 DM)인 LDM의 거동을 분석한다.  
비교 가능한 실험 환경을 위해, NVIDIA A100 한 대로 모든 실험을 고정하고 모든 모델을 같은 단계 수와 매개변수로 학습한다.  
표 8에는 이 섹션에서 비교한 LDMs에 사용된 첫 단계 모델의 하이퍼파라미터와 재구성 성능이 확인 가능하다.  
<img width="400" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/b9f3f7d7-363f-46ef-8761-2995d4b99bcc">   

그림 6은 ImageNet 데이터셋에서 클래스 조건부 모델의 2M 학습 단계에 따른 샘플 품질을 보여주고 있어. 작은 다운샘플링 요소인 LDM-f1,2는 학습 진행이 느리고, 큰 f 값은 적은 학습 단계 후에 품질이 정체되는 것을 볼 수 있어. 이는 DM에 perceptual compression 대부분을 맡기고 첫 단계 압축이 너무 강해 정보 손실이 발생하여 품질이 제한된다는 걸 의미해. LDM-f4-16은 효율성과 인지적으로 충실한 결과 사이에서 좋은 균형을 맞추는데, 이는 2M 학습 단계 후에 DM(LDM-1)과 LDM-8 사이에 FID 점수 차이가 38이라는 것으로 나타난다.  
<img width="745" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/c32d5fe0-6490-4061-835d-e623e839ff36">  


그림 7에서는 CelebA-HQ와 ImageNet에서 학습된 모델들을 DDIM 샘플러로 노이즈 제거 단계 수에 따른 샘플링 속도와 FID 점수를 비교해. LDM-f4-8은 perceptual and conceptual 압축 비율이 적절하지 않은 모델들보다 성능이 좋아. 특히 DM에 비교해서 훨씬 낮은 FID 점수를 달성하면서 샘플 처리량도 크게 증가시켜. ImageNet 같은 복잡한 데이터셋은 품질을 줄이지 않기 위해 압축률을 줄여야 해. 요약하자면, LDM-4와 -8이 고품질 합성 결과를 얻는데 최적의 조건을 제공한다.  
<img width="763" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/651d5a18-01db-417f-8696-b0270f80dbfe">  

### 4.3. Conditional Latent Diffusion
#### 4.3.1 Transformer Encoders for LDMs
LDMs에 cross-attention을 도입하여 이전에 DM에서 탐구되지 않았던 다양한 조건부 모달리티 적용  


##### Text2Image 모델링:
LAION-400M 데이터셋에서 1.45B 매개변수 KL-reg LDM 학습.
언어 프롬프트에 기반한 학습.
BERT 토크나이저와 transformer 사용.
Latent code를 UNet으로 매핑하기 위해 cross-attention 적용.

##### 성능 평가:
사용자 정의 텍스트 프롬프트에 잘 일반화됨(MS-COCO 검증 세트에서 AR 및 GAN 기반 방법보다 뛰어남)  
Classifier free  Diffusion guide로 샘플 품질이 크게 향상됨  
<img width="700" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/0fe643f0-8d5d-4e9c-ac2f-9eb78385fc6e"> 

<img width="300" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/083e66ab-d63d-42a5-8418-40db481c74d0"> 

<img width="300" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/ee05dfa3-09bb-4d45-a5b7-70f8deb6d2af">  



##### cross-attention의 유연성 추가 분석:
OpenImages에서 의미적 레이아웃 기반 이미지 합성 모델 학습.
COCO에서 미세 조정.
정량적 평가와 구현 세부사항은 섹션 D.3 참조.
![image](https://github.com/kyugorithm/TIL/assets/40943064/c8329ac2-6c48-4a41-ad40-a210a4cfc3a9)  
![image](https://github.com/kyugorithm/TIL/assets/40943064/7a03e090-6497-408d-9988-b04b588b2ba1)  



##### 클래스 조건부 ImageNet 모델 평가:
Section 4.1의 f ∈ {4, 8}인 모델 평가  
계산 요구 사항과 매개변수 수 줄이면서 최신 디퓨전 모델 ADM 능가  


#### 4.3.2 Convolutional Sampling Beyond 256^2
Spatially aligned 조건부 정보를 ϵ𝜃의 입력에 concatenate 함으로써 LDMs는 효율적인 범용 I2IT 모델로 활용될 수 있다. 이를 활용해 semantic synthesis, super-resolution, inpainting을 위한 모델을 학습했다. 의미론적 합성을 위해, 풍경 이미지와 의미 지도를 짝지어 사용하고, 의미 지도의 다운샘플된 버전을 f = 4 모델의 잠재 이미지 표현과 연결했어(VQ-정규화, 표 8 참조). 입력 해상도는 256(384 크롭에서)로 학습했지만, 모델이 더 큰 해상도로 일반화되어 메가픽셀 범위의 이미지를 컨볼루셔널 방식으로 생성할 수 있음을 발견했어(그림 9 참조).   
<img width="400" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/55d3847d-086f-44c8-9be8-00b39183eb30">   
이런 행동을 활용해 SR(Sec. 4.4) 모델과 inpainting(Sec. 4.5) 모델도 512에서 1024 사이의 큰 이미지를 생성하는 데 적용했어. 이러한 응용에서 잠재 공간의 스케일에 의해 유발되는 SNR이 결과에 크게 영향을 미쳐. Sec. D.1에서 이를 보여주는데, (i) f = 4 모델(KL-정규화, 표 8 참조)에 의해 제공되는 잠재 공간을 학습하고, (ii) 구성 요소별 표준 편차로 스케일된 버전을 사용하는 것을 비교했어. 후자는 classifier-free guidance와 함께 256 이상 이미지를 직접 합성하는 데도 사용될 수 있어, 예를 들어 text-conditional LDM-KL-8-G에서 그림 13과 같이 말이야.   
  
![image](https://github.com/kyugorithm/TIL/assets/40943064/df22cd74-90a4-4c9f-af03-86f3bf95c636)  

### 4.4. SuperResolution with Latent Diffusion
Concat을 통해 저해상도 이미지에 conditioning을 직접적으로 함으로써 SR에 효율적으로 학습 될 수 있다. 
첫 실험은 SR3를 따르고 image degradation은 "bicubic interpolation with 4 -downsampling"로 수정하고 SR3의 데이터 처리 파이프라인을 따라 ImageNet에서 학습했다. OpenImages에 학습된 모델 "f=4 & VQ-reg"을 사용한다. (tau_theta = the identity)  
정성/정량 평가는 SR3과 상응하는 결과를 보여준다. (FID는 높고 IS는 낮음)

<img width="300" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/bb0f682b-da02-4749-9f38-6c92acbc292e">   
<img width="300" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/eb37246e-4eb4-4233-8174-561bac499ead">   

단순 이미지 회귀 모델이 가장 높은 PSNR 및 SSIM 점수를 달성하지만, 이러한 지표들은 인간의 지각과 잘 일치하지 않고, 완벽하게 정렬되지 않은 고주파수 세부사항보다 흐릿함을 선호한다. 또한 DM과 우리 모델을 비교하기 위해 user study를 수행한다.  
![image](https://github.com/kyugorithm/TIL/assets/40943064/158f13e4-09fe-49d7-8b54-855c2d7a8ca0)
* User study는 저해상도 좌우에 각 고해상도 이미지를 배열한 사람이 있는 SR3의 방식을 따라 수행했다.  
Post-hoc guiding mechanism(classifier guidance)을 사용하여 PSNR과 SSIM을 개선할 수 있으며, 우리는 지각 손실을 통해 이 image-based guider를 구현합니다(Section D.6 참조). Bicubic degradation process는 이러한 전처리를 따르지 않는 이미지에는 잘 일반화되지 않기 때문에 보다 다양한 열화를 사용하여 일반 모델인 LDM-BSR도 학습한다. 결과는 섹션 D.6.1에 나와 있습니다.

### 4.5. Inpainting with Latent Diffusion
#### 1. Inpainting Task and Evaluation Method  
이미지의 마스킹된 부분을 새로운 내용으로 채우는 작업을 인페인팅이라고 한다. 이미지의 일부가 손상되었거나 이미지 내 원치 않는 내용을 대체하기 위해 수행된다. 우리는 일반적인 조건부 이미지 생성 방법이 이 작업을 위한 더 전문화되고 최신의 접근법들과 어떻게 비교되는지 평가한다. 우리의 평가는 최근 인페인팅 모델인 LaMa(Fast Fourier Convolutions 아키텍쳐)의 프로토콜을 따른다. 정확한 학습 및 평가 프로토콜은 Places에서 설명된 바와 같다.  

#### 2. Design Choices and Their Impact on Inpainting  
첫 번째 단계의 다양한 디자인 선택이 인페인팅 효율에 미치는 영향을 분석한다. 특히, 픽셀 기반 조건부 Diffusion Model인 LDM-1과 LDM-4를 KL 및 VQ 정규화와 함께 비교한다. 또한, 첫 번째 단계에서 어떠한 attention도 사용하지 않는 VQLDM-4도 비교한다(표 8 참조). 후자는 높은 해상도에서 GPU 메모리를 줄인다. 비교를 위해 모든 모델의 매개변수 수를 고정한다. 표 6은 256 및 512 해상도에서의 학습 및 샘플링 처리량, 에포크당 총 학습 시간(시간 단위) 및 6 에포크 후 검증 분할에서의 FID 점수를 보고한다. 전반적으로, 픽셀 기반과 잠재 기반 Diffusion Model들 사이에서 최소 2.7배의 속도 향상을 관찰하며, FID 점수는 최소 1.6배 개선된다.

#### 3. Comparative Analysis with Other Inpainting Approaches
다른 인페인팅 접근법과의 비교에서, 우리의 attention 기반 모델은 LaMa에 비해 FID로 측정된 전반적인 이미지 품질을 향상시킨다. 마스크가 없는 이미지와 우리 샘플 사이의 LPIPS는 LaMa보다 약간 높다. 이는 LaMa가 평균 이미지를 더 많이 복구하는 경향이 있는 단일 결과만 생성하는 반면, 우리의 LDM은 다양한 결과를 생성하기 때문이라고 추정한다. 또한 사용자 연구(표 4)에서 인간 참가자들은 LaMa의 결과보다 우리의 결과를 선호한다.  
<img width="100" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/46397ae4-3597-48fb-bb99-8b99ccfced39">
<img width="300" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/a799f56f-2ff3-4be3-824a-701f7f0da3e4">

## 5. Limitations & Societal Impact
### Limitations
LDM은 픽셀 기반 접근 방식에 비해 계산 요구 사항을 크게 줄이지만, 순차 샘플링 프로세스로 인해 GAN에 비해 느리다.  
높은 정밀도가 요구되는 경우 LDM의 사용에 의문이 생길 수 있다. f = 4 자동 인코딩 모델에서는 이미지 품질 손실이 매우 작지만(그림 1 참조), 픽셀 공간에서 세밀한 정확도가 필요한 작업에서는 재구성 기능이 병목 현상이 될 수 있다.  
초해상도 모델(4.4절)은 이러한 측면에서 이미 어느 정도 한계가 있다.

### Societal Impact
이미지와 같은 미디어를 위한 생성 모델은 양날의 검과도 같다: 한편으로는 다양한 창의적인 애플리케이션을 가능하게 하고, 특히 훈련 및 추론 비용을 절감하는 저희와 같은 접근 방식은 이 기술에 대한 접근을 용이하게 하고 그 탐구를 민주화할 수 있는 잠재력을 가지고 있다. 반면 조작된 데이터를 생성하고 유포하거나 잘못된 정보와 스팸을 퍼뜨리는 것이 더 쉬워진다는 의미이기도 하다. 특히 이미지의 고의적인 조작("딥페이크")은 이러한 맥락에서 흔히 발생하는 문제이며, 특히 여성은 불균형적으로 영향을 받고 있습니다. 생성 모델은 학습 데이터를 공개할 수도 있는데, 데이터에 민감하거나 개인 정보가 포함되어 있고 명시적인 동의 없이 수집된 경우 큰 우려가 된다. 그러나 이것이 이미지의 DM에도 어느 정도 적용되는지는 아직 완전히 이해되지 않았으며, 마지막으로 딥러닝 모듈은 데이터에 이미 존재하는 편향을 재생산하거나 악화시키는 경향이 있다. DM이 GAN 기반 접근 방식보다 데이터 분포에 대한 더 나은 커버리지를 달성하지만, 적대적 학습과 확률 기반 목표를 결합한 2단계 접근 방식이 데이터를 얼마나 왜곡하는지는 중요한 연구 문제로 남아 있다.  

## 6. Conclusion 
품질 저하 없이 노이즈 제거 DM의 훈련 및 샘플링 효율을 크게 향상시킬 수 있는 간단하고 효율적인 방법인 LDM을 제시했다. 이 모델과 cross attention conditioning mechanism을 기반으로 한 실험을 통해 작업별 아키텍처 없이도 광범위한 조건부 이미지 합성 작업에서 최첨단 방법과 비교했을 때 유리한 결과를 얻을 수 있었다.
