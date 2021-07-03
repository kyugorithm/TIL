# Abstract 

대부분의 조건부 생성작업들은 주어진 단일 조건부 context에서 다양한 출력을 만들어낼 것으로 기대된다.  
그러나 cGAN 때로 사전 조건부 정보에 집중하여 출력의 다양성을 만들 수 있는 입력 노이즈벡터를 무시하게된다.  
mode collapes 문제를 해결하기 위한 최근 연구들은 보통 task에 특정적이며 계산적으로 매우 비싼 작업이다.  
본 연구에서 cGAN에 대한 mode collapse를 다루기 위한 단순하지만 효과적인 정규화 항을 제안한다.  
제안하는 방법은 명확하게 생성된이미지에 대한 그에 상응하는 latent code에 사이의 거리비율을 최대화하며,  
그에 따라 G가 더욱더 세밀한 모드들을 탐험할 수 있도록 한다. 이러한 mode seeking 정규화항은 학습에 대한 overhead나  
기존 네트워크 구조 변경 없이 조건부 생성작업에 대해서 잘 적용될 수 있다. 우리는 3개의 조건부 이미지합성 task  
(categorical generation, I2I translation, and text-to-image synthesis)에 대하여 다른 baseline 모델과 비교하며  
제안한 알고리즘을 검증한다. 질적양적 결과들은 품질손실없이 다양성을 향상하는 제안한 정규화 방법의 효과를 보여준다.  

# 1. Introduction
 GAN은 복잡한 고차원 이미지 데이터를 여러 사례에 효과적으로 포착해왔다.  
GAN에 기반하여 만들어진 cGAN은 외부 정보를 추가 입력으로 취한다. 이미지 합성에서 cGAN은 조건부 방식의 여러 task에 적용 될 수 있다.  
1) class 라벨 : 카테고리별 이미지 생성 가능  
2) 텍스트 문장 : text-to-image 합성에 사용  
3) 이미지 : I2I translation, 의미론적 변경, style transfer에 적용  
  
 대부분의 조건부 생성 작업들에 대해서 mapping들은 본질적으로 multimodal(단일 입력 -> 그럴듯한 다양한 출력)이다.  
multimodality를 다룰 직관적 접근방식은 조건부 context(주요 내용물 결정)와 함께 random noise(다양한 변이) 입력을 취하는 것이다.   
예를들면, 개>고양이 I2I translation task에서 입력의 개 이미지들은 머리의 방향, 얼굴 landmark 위치 등의 내용물을 결정한다.  
반면 noise vector는 여러종의에 대한 생성을 돕는다.  
그러나 cGAN은 보통 단일의 혹은 매우 적은 방식의 분포를 생성하거나 다른 모드를 무시하는 mode collapse 문제를 만나게 된다.  
cGAN이 고차원의 그리고 구조화된 조건부 context로부터 학습하는데 집중함으로써 noise vector가 무시되거나 매우 작은 영향을 주게된다.  
  
 GAN에서 mode collapse 문제를 다루기 위한 주요 2가지 접근 방식이 있다.  
여러가지 방법들은 divergence metric과 최적화 등을 도입하여 Discriminator에 집중한다.  
다른 방법은 여분의 네트워크 예를들어 여러개의 생성자모델을 만들거나 추가 encoder들을 사용한다.  
그러나 mode collapse는 cGAN에서 상대적으로 덜 연구되어 왔다.  
I2I 변환작업에서 다양성을 향상시키기 위해 여러 연구가 수행되어 왔다.  
조건 없는 설정의 두 번째 category와 유사하게, 이러한 접근법들은 출력과 latent code 사이의 일대일 관계를 장려하는  
추가적인 encoder나 loss 함수들을 도입한다. 이러한 방법은 교육에 막대한 컴퓨팅 오버헤드를 수반하거나 종종 다른  
프레임워크로 쉽게 확장될 수 없는 특정 태스크인 보조 네트워크를 필요로 한다.
  
 제안한 정규화 알고리즘에 대하여 여러가지 baseline 모델들과 함께 3가지 조건부 이미지 합성 task에 대한  
면밀한 평가를 수행한다.  
1) categorical image 생성 : CIFAR-10                         / DCGAN
2) I2I translation        : facades, maps, Yosemite, cat-dog / Pix2Pix, DRIT
3) text-to-image 합성     : CUB-200-2011                     / StackGAN++  

이미지의 다양성 평가는 perceptual distance metric을 이용한다.  
그러나 diversity metric 하나만으로 생성 이미지 분포와 실제 이미지 분포 사이 유사성을 보장할 수는 없다.  
그러므로 두가지 bin 기반 metric을 제안한다.  
- *theNumber  ofStatistically-Different Bins(NDB) metric* : 실제 데이터에 의해 사전 결정된 클러스터들로 배정된 샘플의 상대적 비율  
- *ensen-Shannon  Diver-gence(JSD)  distance* : bin 분포 사이 유사성을 측정  
추가로 현실성을 희생하고 다양성을 얻지 못함을 검증하기 위해 품질에 metric으로써 FID를 가지고 검증한다.  
실험결과는 제안 정규화 방법론이 현존모델에 대해 여러 task에 대해 품질 손실 없이 나은 다양성을 달성함을 보여준다.  
F1은 현존하는 모델에 대하여 정규화 방식의 효율성을 보여준다.(모드붕괴 없이 다양한 품질의 이미지가 생성됨)  
![image](https://user-images.githubusercontent.com/40943064/124359308-55895700-dc5f-11eb-8cbd-adac6843a9ec.png)

### main contribution
1) cGAN에서 mode collapse를 해결하기 위해 단순하지만 효과적인 mode seeking regularization 제안 : marginal training overheads and modifications에 잘 확장된다.  
2) 3가지 조건부 생성 task에 대한 제안한 정규화의 일반화를 보인다. : categorical  generation,  I2I translation, and text-to-image synthesis
3) 다양한 task에 대해 현존하는 모델에 대한 정규화 항 적용은 생성이미지 품질에 대한 희생 없이 더나은 다양성을 달성하도록 함을 보여준다.

# 2. Related Work
- cGAN
- Reducing mode collapse

# 3. Diverse Conditional Image Synthesis
## 3.1. Preliminaries
## 3.2. Mode Seeking GANs

# 4. Experiments
## 4.1. Evaluation Metrics
## 4.2. Conditioned on Class Label
## 4.3. Conditioned on Image
### 4.3.1  Conditioned on Paired Images
### 4.3.2  Conditioned on Unpaired Images
## 4.4. Conditioned on Text
## 4.5. Interpolation of Latent Space in MSGANs
# 5. Conclusions
