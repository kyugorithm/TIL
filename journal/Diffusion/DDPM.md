## Abstract
Nonequilibrium thermodynamics에서 온 고려사항에 영감을 받은 잠재 변수 모델인 diffusion probabilistic models을 사용하여 고품질 이미지 합성 결과를 제시한다. 최고의 결과는 diffusion probabilistic models과 Langevin dynamics를 이용한 denoising score matching 사이의 새로운 연결에 따라 설계된 가중된 변분 경계에 대한 학습을 통해 얻어진다. 그리고 우리의 모델은 점진적인 손실 압축 해제 방식을 자연스럽게 수용하는데, 이는 autoregressive decoding의 일반화로 해석될 수 있다.

## 1. Introduction
### 다양한 딥 생성 모델들의 최근 진보
최근 다양한 데이터 형식에서 모든 종류의 딥 생성 모델들이 고품질 샘플을 선보였다. GANs, autoregressive models, flows, VAEs는 인상적인 이미지와 오디오 샘플을 합성했으며, 에너지 기반 모델링과 score matching 분야에서도 주목할 만한 발전이 있었다. 이러한 기술로 GANs와 비교할 수 있는 이미지를 생성하는 데 성공했다.

### Diffusion Probabilistic Models의 발전
본 논문은 diffusion probabilistic models의 발전을 소개한다. Variational inference 사용하여 학습된 매개변수화된 Markov chain이다. 이 체인의 전환은 데이터에 점차적으로 노이즈를 추가하는 diffusion process를 역으로 진행하도록 학습된다. Diffusion이 작은 양의 Gaussian 노이즈로 구성될 때, 샘플링 체인 전환을 조건부 Gaussian으로 설정하는 것으로 충분하며, 이를 통해 간단한 신경망 매개변수화가 가능하다. 

### 고품질 샘플 생성 및 특정 매개변수화의 중요성
Diffusion models는 간단하고 효율적으로 학습할 수 있지만, 고품질 샘플을 생성할 수 있다는 사실이 입증되지 않았다. 이 논문에서는 diffusion models가 실제로 고품질 샘플을 생성할 수 있음을 보여주며, 때로는 다른 생성 모델들의 결과보다 더 나은 결과를 보여준다. 또한, diffusion models의 특정 매개변수화가 학습 중 다중 노이즈 레벨에 대한 denoising score matching과 샘플링 중 annealed Langevin dynamics와 동등함을 밝혀낸다. 이 매개변수화를 사용하여 최고의 샘플 품질 결과를 얻었으며, 이는 주요 기여 중 하나로 간주된다.  

### 로그 우도 및 이미지 세부사항에 대한 분석
우리의 모델은 샘플 품질에도 불구하고 다른 우도 기반 모델들과 비교할 때 경쟁력 있는 로그 우도를 가지고 있지 않다. 하지만 에너지 기반 모델과 score matching에 대해 보고된 것보다는 더 나은 로그 우도를 가진다. 우리 모델들의 대부분의 손실 없는 코드 길이는 눈에 띄지 않는 이미지 세부사항을 설명하는 데 사용된다. 이 논문에서는 이 현상에 대한 더 정교한 분석을 the language of lossy compression으로 제시하며, diffusion models의 샘플링 절차가 autoregressive decoding과 유사한 형태의 점진적 디코딩이라는 것을 보여준다. 이는 autoregressive models에서 일반적으로 가능한 것보다 훨씬 더 광범위하게 일반화된 비트 순서를 따른다.



## 4 Experiments
T = 1000 (이전 논문들과의 동등한 비교를 위해)  
beta(forward process variances)는 constant로 세팅 : np.linspace(0.0001, 0.02, 1000) - (linear, quadratic 중 최적 선정)

아래 두가지를 위해 데이터 스케일 [-1, 1]에 비해 beta값을 작게 설정
1) Forward/backward process를 근사적으로 같은 functional form이 되도록 함
2) xT에서의 snr을 최대한 낮춤


<img width="250" alt="image" src="https://user-images.githubusercontent.com/40943064/167233335-8aa18016-01dd-476c-9f89-06db11932386.png">  
(KLD scale이 매우작음 ~ 10^-5)  
  
  
Reverse process를 구현하기 위해 아래 논문의 U-net backbone과 유사한 구조를 사용하며 전체적으로 group-norm 사용  
(PixelCNN++: Improving the PixelCNN with discretized logistic mixture likelihood and other modifications)

<img width="561" alt="image" src="https://user-images.githubusercontent.com/40943064/167233517-c44d1942-6ded-49a5-9a3a-c76e3eb6935a.png">
<img width="561" alt="image" src="https://user-images.githubusercontent.com/40943064/167233591-be007a5c-a751-4836-ae43-1ca9e59eb1e1.png">  
  
t(Transfomer의 sinusoidal position embedding에 적용)에 따른 parameter는 공유  
16x16 featuremap level에서는 self-attention 구조를 사용함  
<img width="834" alt="image" src="https://user-images.githubusercontent.com/40943064/167242029-b987d5c8-c870-4a8b-821e-ad57201c7742.png">

### Appendix B.  
<img width="834" alt="image" src="https://user-images.githubusercontent.com/40943064/167242030-24db6af4-c271-4a1d-bb96-bec6544124b7.png">


#### Parameter number
CIFAR10 : 35.7M
LSUN and CelebA-HQ : 114M (256M for larger variant of the LSUN Bedroom by increasing filters)

#### 학습량
TPU v3-8 GPU를 이용하여 10시간(CIFAR-10) ~ 2주(256)가량 소요

#### Hyperparameter
<img width="919" alt="image" src="https://user-images.githubusercontent.com/40943064/167234542-197a4621-0742-46bf-a41a-5756dbcd423d.png">  
<img width="918" alt="image" src="https://user-images.githubusercontent.com/40943064/167234548-781f6c20-8641-4c57-bd2a-473d28c407b0.png">  

#### Additional detail
Sample quality를 판단하기 위해 최종 실험은 1회 수행하며 학습동안 지속적으로 샘플 품질 평가를 수행  
품질 수치는 학습동안 최소 FID 값을 가지는 iteration 기준으로 추출  
(CIFAR10)OpenAI/TTUR의 original code를 이용해 50k 샘플에 대해 FID와 IS를 계산  
(LSUN) StyleGAN2 repo 이용하여 계산  
CIFAR10 & CelebA-HQ은 Tensforflow 로드 방식 사용하였으며 LSUN은 StyleGAN 코드를 사용  
train/test split은 일반적인 생성모델에서 사용하는 방식을 사용

## 4.1 Sample quality

Conditional 모델을 포함한 대부분의 모델보다 더 나은 FID 달성  
학습 데이터(3.17), 테스트 데이터(5.24) : 표준 테스트는 학습 데이터에 대하여 수치를 계산  

**Object function 비교**  
1) True variational bound : NLL 
2) Simplified traning object : Qualitative quality

#### Table : IS, FID, NLL for CIFAR10**   
<img width="450" alt="image" src="https://user-images.githubusercontent.com/40943064/167179030-1542096d-5037-41ee-b5e8-e2cce43fdece.png">  

#### Figure : CelebA-HQ 256(left) / unconditional CIFAR10 (right)
<img width="1292" alt="image" src="https://user-images.githubusercontent.com/40943064/167175144-3d366411-9638-46fb-bf5b-f35ab0234e95.png">  
  
#### Figure : SNGAN(Spectral normalization GAN)  
<img width="1231" alt="image" src="https://user-images.githubusercontent.com/40943064/167235512-ec58cc3f-29ed-4c71-9e2a-49378bec56d0.png">

#### Figure : LSUN
<img width="1492" alt="image" src="https://user-images.githubusercontent.com/40943064/167180022-23931877-33f0-47c8-bc5d-321ef880c501.png">

## 4.2 Reverse process parameterization and training objective ablation
<img width="600" alt="image" src="https://user-images.githubusercontent.com/40943064/167181166-dd6ea436-e509-4a23-ae06-2045bd8e8c1e.png">

Table 2: Unconditional CIFAR10 reverse process parameterization and training objective ablation.  
(빈 부분은 불안정하고 품질이 매우 낮은 경우)  

Parameterizations 방법과 objective 차이에 따른 영향을 본다.
**1) baseline**  
baseline parameterization : true variational bound >> (불안정)unweighted MSE(simplified와 유사한 방식)  

**2) propose**  
Variational bound + parameterized diagonal Σθ(xt) : 불안정 << Variational bound + fixed variance Σ

fixed variance를 이용하는경우 ε는 μ~에 근사하지만 simplified objective를 사용하는 경우 월등한 성능을 보인다.

### 4.3 Progressive coding
CIFAR 10에 대한 결과에서 보면 codelengths의 train-test 차이가 0.03으로 매우 작으며 타 방법론에 절대 떨어지지 않는다.  
Overfitting이 일어나지 않음을 의미하기도 한다. 
Figure. col1(생성샘플)  
<img width="1266" alt="image" src="https://user-images.githubusercontent.com/40943064/167238277-ef483abb-a9dc-4d73-a4de-0fa357959228.png">

Energy based와 score matching(annealed importance sampling 사용)보다 lossless codelength가 낫지만 다른종류보다는 낮다.
그럼에도 불구하고 FID, IS와 같은 수치는 높은것으로 보아 inductive bias를 가지는것으로 결론 내릴 수 있다.  
  
<img width="1264" alt="image" src="https://user-images.githubusercontent.com/40943064/167238582-367be0af-dc98-4914-8965-86002b558b15.png">  
  
#### Progressive lossy compression

<img width="1355" alt="image" src="https://user-images.githubusercontent.com/40943064/167238690-0a93bed2-33f9-4dda-91dd-3ba20babd93f.png">
<img width="1275" alt="image" src="https://user-images.githubusercontent.com/40943064/167238753-f80af552-b2c6-41d1-807a-90ebd8ea59cc.png">


#### Progressive generation
random bit로부터 점진적 복원을 통해 생성과정을 수행한다. 

그림을 보면 초기 단계는 large scale 후기 단계는 detail 이미지 생성 작업이 수행된다.  
(직관적으로는 구조에 관계없이 생성될것으로 생각 되었으나 일반적인 CNN 생성 방식대로 구조가 연결됨)  
Figure : Unconditional CIFAR10 progressive generation  
<img width="700" alt="image" src="https://user-images.githubusercontent.com/40943064/167239462-53edad34-f789-4e99-9081-16db5622d29f.png">  
Figure : 추가 이미지  
<img width="700" alt="image" src="https://user-images.githubusercontent.com/40943064/167241994-8aeae793-4597-414c-907f-12eda01332d1.png">

Figure : Unconditional CIFAR10 progressive sampling quality over time. 
<img width="500" alt="image" src="https://user-images.githubusercontent.com/40943064/167239516-51216457-aba6-44af-a692-9c92dccfb129.png">  

동일한 t로부터 얻어진 서로다른 이미지에 대해 비교를 해보면 high-level feature는 보존됨을 알 수 있다. 즉, t=1000로 갈 수록 높은 수준의 feature가 공유된다.  
(Conceptual comppresion에 대한 hint)
<img width="900" alt="image" src="https://user-images.githubusercontent.com/40943064/167239587-ad689f6f-a195-4f23-94ff-6769afc6696b.png">  

#### Connection to autoregressive decoding
<img width="550" alt="image" src="https://user-images.githubusercontent.com/40943064/167240057-3b780e40-9651-4c8b-8714-d72ee6f9b4bf.png">

<img width="800" alt="image" src="https://user-images.githubusercontent.com/40943064/167239998-dd27bbf6-5c88-4c7d-9c3b-aa351fcb01c7.png">

#### 4.4 Interpolation
Image interpolation은 잘 되지 않기 때문에 diffusion process로 corrupt시킨 latent에 interpolation을 하고 다시 decoding을 하여 semantic한 interpolation 구현  
(단, r을 적용할때 random noise는 동일하게 고정하여 사용)  
* 재밌는 아이디어 인데 일부분만 interpolation 하면 어떻게 되는지 궁금  
* t=1000 까지 corrupt-decoding 한 이미지의 semantic한 차이가 어떤 의미인지 궁금  
* (recon도 되지 않으므로 의미가 있는지 모르겠음..)  
Figure. Interpolations and reconstructions of original CelebA-HQ 256x256 images (t = 500)  
<img width="900" alt="image" src="https://user-images.githubusercontent.com/40943064/167240572-7d97c4de-6a54-4421-bcb2-cc50f758c609.png">  
Figure. Coarse-to-fine interpolations that vary the number of diffusion steps prior to latent mixing.
<img width="900" alt="image" src="https://user-images.githubusercontent.com/40943064/167240734-2c04a1db-4521-406f-b33f-5f19dce8c905.png">  

