## 3. Method
고해상도 이미지 합성을 위한 DM 학습에 필요한 계산 부담을 줄이기 위해, DM이 해당하는 손실 항목을 언더샘플링함으로써 인지적으로 중요하지 않은 세부사항을 무시할 수 있음을 관찰했다. 하지만 이러한 모델들은 여전히 픽셀 공간에서 비용이 많이 드는 함수 평가를 필요로 하며, 이는 계산 시간과 에너지 자원에 거대한 요구를 가져온다.
이러한 단점을 피하기 위해, 압축 단계와 생성 학습 단계를 명확히 분리하는 방법을 제안한다(그림 2 참조). 이를 위해, 이미지 공간과 인지적으로 동등하지만 계산 복잡성이 훨씬 줄어든 공간을 학습하는 autoencoding 모델을 활용한다.  
  
### 접근 방법의 장점  
1. 고차원의 이미지 공간을 벗어남으로써, 저차원 공간에서 샘플링이 수행되기 때문에 계산적으로 훨씬 효율적인 DMs를 얻을 수 있다.  
2. DMs의 UNet 구조로부터 상속받은 inductive bias를 활용함으로써, 공간 구조를 가진 데이터에 특히 효과적이며, 이전 접근법들이 요구한 공격적이고 품질을 저하시키는 압축 수준의 필요성을 완화한다.  
3. 다양한 생성 모델을 학습하고 단일 이미지 CLIP 유도 합성과 같은 다른 downstream application에도 사용될 수 있는 일반 목적의 compression models의 latent space를 얻는다.

 ## 3.1. Perceptual Image Compression
perceptual compression model은 이전 연구 [23]를 기반으로 하며, perceptual loss(LPIPS)과 패치 기반(pix2pix) adversarial objective 조합으로 학습된 AE로 구성된다. 이는 local realism을 강화함으로써 재구성이 이미지 매니폴드에 제한되도록 하고, L2나 L1 목표와 같은 픽셀 공간 손실에만 의존함으로써 도입되는 흐릿함을 피한다. 보다 정확히 말하면, RGB 공간의 이미지 x가 주어지면, 인코더 E는 x를 잠재 표현 z = E(x)로 인코딩하고, 디코더 D는 잠재 표현에서 이미지를 재구성하여 ~x = D(z) = D(E(x))를 생성한다, 여기서 z는 R^ h x w x c  차원이다. 중요하게, 인코더는 이미지를 f = H/h = W/w 비율로 다운샘플링하며, 다양한 다운샘플링 비율 f = 2^m을 조사한다.  
  
임의로 높은 분산을 가진 잠재 공간을 피하기 위해, 두 가지 다른 종류의 regularization을 실험한다. 첫 번째 변형인 KL-reg는 VAE와 유사하게 학습된 잠재 공간에 표준 정규 분포에 대한 약간의 KL-페널티를 부과한다. 반면, VQ-reg.는 디코더 내부에 vector quantization 레이어를 사용한다. 이 모델은 디코더에 의해 흡수된 quantization 레이어를 가진 VQGAN으로 해석될 수 있다. 우리의 후속 DM은 학습된 잠재 공간 z = E(x)의 이차원 구조와 함께 작동하도록 설계되었기 때문에, 비교적 온건한 압축률을 사용하고 매우 좋은 재구성을 달성할 수 있다. 이는 잠재 공간 z의 분포를 자기회귀적으로 모델링하기 위해 학습된 공간 z의 임의적인 1D 순서에 의존하고 z의 본질적인 구조를 대부분 무시한 이전 연구들 [23, 66]과 대조적이다. 따라서, 우리의 압축 모델은 x의 세부 사항을 더 잘 보존한다(표 8 참조). 전체 목표와 학습 세부 사항은 보충 자료에서 찾을 수 있다.


이미지의 디테일을 유지하기 위해 인지적 손실과 적대적 목표를 결합한 특별한 학습 방식을 사용한다.:이는 이미지가 흐릿해지는 것을 방지하고 더 현실적인 재구성을 가능하게 한다.
#### 잠재공간품질을 유지하기 위해  두가지 정규화 방법 실험  
1. KL-정규화: 잠재 공간이 표준 정규 분포를 따르도록 한다.   
2. VQ-정규화: 벡터 양자화를 사용한다. 잠재 공간이 너무 복잡해지거나 불규칙해지는 것을 방지한다.  

### 3.2. Latent Diffusion Models

#### Diffusion Models
Diffusion Models은 데이터 분포 p(x)를 배우기 위해 설계된 확률적 모델입니다. 이들은 정규 분포된 변수를 점차적으로 노이즈 제거함으로써 작동하며, 이는 고정된 arkov Chain의 역과정을 배우는 것과 동일합니다. 이 체인의 길이는 T입니다. 이미지 합성에서 가장 성공적인 모델들(Classifier guidance, DDPM, SR3)은 p(x)에 variational lower bound의 재가중 버전에 의존합니다. 이는 denoising score-matching을 반영합니다.
이 모델들은 노이즈가 제거된 자신의 입력 xt를 예측하도록 훈련된 일련의 노이즈 제거 AE인 𝝐_𝜃(xt, t), t = 1, ..., T의 동등하게 가중된 시퀀스로 해석될 수 있습니다. 여기서 xt는 입력 x의 노이즈 버전입니다. 해당 목표는 다음과 같이 단순화될 수 있습니다.  
<img width="300" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/7d67347a-36d8-4915-bda2-f2ebdb3f4d85">  
여기서 t는 {1, ..., T}에서 균등하게 샘플링됩니다.

간단히 말해, Diffusion Models는 데이터를 이해하기 위해 노이즈를 단계적으로 제거하는 방식으로 학습하는 모델입니다. 이들은 마르코프 체인의 역과정을 모방하여 이미지의 노이즈를 제거하는 다수의 오토인코더들을 시퀀스로 사용합니다. 이 과정을 통해 고도로 정교한 이미지 생성이 가능해집니다.

#### Generative Modeling of Latent Representations
이 내용은 생성 모델링과 관련된 논문의 일부로 보입니다. 여기에서는 훈련된 인지적 압축 모델(오토인코더의 인코더 E와 디코더 D로 구성)을 사용하여 저차원의 효율적인 잠재 공간(latent space)에 접근하는 방법에 대해 설명하고 있습니다. 이 잠재 공간은 높은 주파수와 인지하기 어려운 세부사항을 추상화하여 제거합니다. 이 저차원 공간은 고차원 픽셀 공간에 비해 가능성 기반의 생성 모델(likelihood-based generative models)에 더 적합합니다. 이는 생성 모델이 (i) 데이터의 중요하고 의미 있는 부분에 집중할 수 있고 (ii) 계산적으로 훨씬 더 효율적인 저차원 공간에서 학습할 수 있기 때문입니다.

이전 연구들은 압축된 이산 잠재 공간에서 자기회귀적, 주의 기반 변환 모델(autoregressive, attention-based transformer models)에 의존했지만, 이 연구에서는 모델이 제공하는 이미지 특정 유도 편향(image-specific inductive biases)을 활용할 수 있습니다. 이는 주로 2D 컨볼루셔널 레이어로 구성된 UNet을 사용하고, 재가중된 경계(reweighted bound)를 통해 인지적으로 가장 관련 있는 부분에 목표를 집중하는 능력을 포함합니다. 이렇게 수정된 식은 다음과 같습니다:

<img width="451" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/2b3fa82e-dce7-4c1d-8733-d1c1cd418de5">
여기서 모델의 neural network backbone은 time-conditional UNet으로 구현됩니다. forward process가 고정되어 있으므로, zt는 훈련 중 𝜺을 통해 효율적으로 얻을 수 있으며, p(z)에서 샘플을 뽑아 Decoder를 통해 한 번의 패스로 이미지 공간으로 decode할 수 있습니다.  

### 3.3. Conditioning Mechanisms
이 내용은 디퓨전 모델(Diffusion Models, DMs)이 조건부 분포(conditional distributions)를 모델링하는 능력에 대해 설명하고 있습니다. 다른 종류의 생성 모델들처럼 [56, 83], 디퓨전 모델도 원칙적으로 p(z|y)형태의 조건부 분포를 모델링할 수 있습니다. 여기서 z는 잠재 공간에서의 요소를, y는 조건을 나타냅니다. 이것은 conditional denoising autoencoder 𝜺(zt, t, y)를 통해 구현할 수 있으며, 텍스트(Generative adversarial text to image synthesis), 의미 지도(semantic maps) 또는 I2IT 작업(pix2pix)과 같은 입력  y를 통해 합성 과정을 제어하는 길을 엽니다.

이미지 합성의 맥락에서, DMs의 생성력을 클래스 라벨 [15]이나 입력 이미지의 흐릿한 변형 [72]과 같은 다른 유형의 조건들과 결합하는 것은 아직까지 탐구되지 않은 연구 분야입니다. 연구팀은 DMs를 더 유연한 조건부 이미지 생성기로 변환하기 위해 기본 UNet backbone에 cross-attention mechanism을 추가합니다(다양한 입력 형태의 attention 기반 모델을 학습하는 데 효과적).언어 프롬프트와 같은 다양한 모달리티의 를 전처리하기 위해, 연구팀은 τ𝜃
y를 중간 표현 τ𝜃(y) in R ^M x d_tau 로 투영하는 도메인 특정 인코더를 도입합니다. 이 중간 표현은 cross-attention layer를 통해 UNet의 중간 레이어로 매핑되며, 이 레이어는 아래 수식을 구현합니다.  
  
  <img width="505" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/4a4f2df9-242d-4315-8a7e-db9a0fb14136">  


Image-conditioning pairs를 기반으로 우리는 conditional LDM을 아래와 같이 정의한다.  
<img width="504" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/f8233b7b-4e89-4f9d-a203-6dcbb58c6f89">  
tau와 e(encoder와 diffusion 모델은 동시에 최적화된다.)  
여기서, τθ는 특정 도메인에 맞춘 전문가들에 의해 매개변수화될 수 있습니다. 예를 들어, y가 텍스트 프롬프트인 경우에는 transformers와 같은 도메인별 전문가를 사용합니다. 이 변환기는 마스킹되지 않은(unmasked) 형태일 수 있습니다.  
  
요약: DMs을 통해 다양한 조건(예: 텍스트, 의미 지도 등)에 따라 이미지를 생성하는 방법을 탐구합니다. UNet에 cross-attention mechanism을 추가함으로써, 다양한 입력 형태에 대한 더 유연한 조건부 이미지 생성을 가능하게 합니다.
