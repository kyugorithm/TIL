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

<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124359308-55895700-dc5f-11eb-8cbd-adac6843a9ec.png" width=800 /></p>  
### main contribution
1) cGAN에서 mode collapse를 해결하기 위해 단순하지만 효과적인 mode seeking regularization 제안 : marginal training overheads and modifications에 잘 확장된다.  
2) 3가지 조건부 생성 task에 대한 제안한 정규화의 일반화를 보인다. : categorical  generation,  I2I translation, and text-to-image synthesis
3) 다양한 task에 대해 현존하는 모델에 대한 정규화 항 적용은 생성이미지 품질에 대한 희생 없이 더나은 다양성을 달성하도록 함을 보여준다.

# 2. Related Work
- **cGAN**
GAN은 영상 합성에 널리 사용되어 왔다. adversarial training을 통해 G는 실제 이미지 분포를 포착하도록 권장된다.  
cGAN은 GAN을 기반으로 다양한 컨텍스트를 기반으로 영상을 합성한다.  
e.x.,  
1) low-resolution -> high-resolution  
2) I2I translation  
3) styled 영상 생성  
4) TTI(text-to-image)  
  
cGAN은 다양한 애플리케이션에서 성공을 거두었지만 모드 축소 문제로 어려움을 겪는다. conditional 컨텍스트는 출력 이미지에 대한  
강력한 구조적 prior information을 제공하고 입력 noise 벡터보다 high-dimension이기 때문에 G는 생성된 영상의 변화를 일으키는  
입력 noise 벡터를 무시하는 경향이 있다. 따라서 G가 유사한 모양의 영상을 생성하게 된다.  
본 논문에서는 cGAN의 mode collapse 문제를 해결하는 것을 목표로 한다.  

- **Reducing mode collapse**
일부 방법은 학습을 안정화하기 위해 상이한 최적화 프로세스와 divergence metrics[1, 19]를 가진 D에 초점을 맞춘다.  
미니 배치 discrimination[26]을 통해 D는 개별 샘플이 아닌 전체 미니 배치 샘플을 구별할 수 있다.  
다른 방법에서는 모드 축소 문제를 완화하기 위해 auxiliary network를 사용한다.  
ModeGAN 및 VEEGAN은 입력 노이즈 벡터와 추가 인코더 네트워크를 사용하여 생성된 이미지 사이의 bijection mapping을 적용한다.  
multiple G와 weight 공유 G[18]는 더 많은 분포의 mode를 포착하기 위해 개발되었다.  
그러나, 이러한 접근법은 computing overhead를 수반하거나 network 구조수정이 필요하며, cGAN에 쉽게 적용되지 않을 수 있다.  

cGAN 분야에서는 최근 I2I transition task의 mode-collapse 문제를 해결하기 위해 몇 가지 방법이 제시되었다.  
Mode GAN 및 VEGAN과 유사하게, 생성된 이미지와 입력 noise 벡터 사이에 bijection constraint를 제공하기 위해 추가 encoder가 적용되었다.  
그러나 이러한 접근법은 다른 작업별 네트워크와 객관적 기능을 필요로 한다. 추가 구성 요소로 인해 방법의 일반화 가능성이 낮아지고  
학습에 추가적인 연산 부하가 발생합니다. 대조적으로, 우리는 학습 오버헤드를 없이 네트워크 구조의 수정을 필요로 하지 않는  
단순한 정규화 항을 제안한다. 따라서 제안된 방법은 다양한 조건부 생성 task에 쉽게 적용할 수 있다.  
최근, 동시 작업도 cGAN에 대한 모드 붕괴를 줄이기 위한 작업과 유사한 손실 조건을 채택하고 있다.  

# 3. Diverse Conditional Image Synthesis
## 3.1. Preliminaries

GAN 학습 과정은 min-max 문제로 공식화할 수 있다.  
D : 실제 데이터에 높은값을, 생성 데이터에 낮은값을 할당하여 분류능력을 향상한다.  
G : 그럴듯한 이미지를 합성하여 D를 속인다.  

적대적 학습을 통해 D의 gradient는 G가 실제 이미지 분포와 유사한 분포의 샘플을 생성하도록 가이드한다.  
GANs의 mode-collapse 문제는 잘 알려져 있다. 여러 방법은 이 문제가 발생할 때 penalty 부족이 missing 모드를 원인으로 삼는다.  
모든 모드는 대개 유사한 차별적 값을 가지므로 gradient descent에 기반한 학습 과정을 통해 다수샘플의 mode를 선호할 수 있다.  
반면, 소수샘플 mode에서는 샘플생성이 어렵다. cGAN에서 모드 누락 문제가 더 극적으로 발생한다.  
일반적으로, conditional context는 noise 벡터와 대조적으로 고차원적이고 구조화되어 있다.(예: 영상 및 문장).  
따라서 G는 context에 초점을 맞추고 다양성을 설명하는 noise 벡터를 무시할 가능성이 있다.  

## 3.2. Mode Seeking GANs
본 연구에서는 missing mode 문제를 G 관점에서 완화할 것을 제안한다. 그림 2는 본 방식의 주요 아이디어를 보여준다.  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124373239-869f7100-dccb-11eb-80c9-46cdfb556317.png" width=800 /></p>  

latent code space Z의 latent verctor z가 이미지 space I에 mapping되도록 한다. mode collapse가 발생하면  
mapping 이미지가 몇 가지 모드로 축소된다. 또한 두 개의 잠재 코드 z1과 z2가 가까울 경우 mapping 이미지 I1 = G(c, z1)와 I2 = G(c, z2)가  
동일한 모드로 축소될 가능성이 높다. 이 문제를 해결하기 위해 z1과 z2 사이의 거리에 대한 G(c, z1)와 G(c, z2) 사이의 거리 비율을  
직접적으로 최대화하기 위해 regularization term을 찾는 모드를 제안한다.  

<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124373279-e007a000-dccb-11eb-942e-62a1fcefce23.png" width=450 /></p>  

regularization 항은 cGAN 학습을 위한 선순환 구조를 제공한다. 이 항은 G가 image 공간을 탐색하도록 유도하고  
소수 모드의 샘플을 생성할 수 있는 기회를 향상시킨다. 반면에 D는 소수샘플 모드에서 생성된 샘플에 주의를 기울여야 한다.  
그림 2는 두 개의 가까운 샘플인 z1과 z2가 동일한 모드 M2에 매핑되는 mode-collapse 상황을 보여준다.  
그러나 제안된 정규화 조건을 사용하여 z1은 탐색되지 않은 모드 M1에 속하는 I1에 mapping되고 G는 다음의  
훈련에서 M1의 샘플을 생성할 수 있는 더 나은 기회를 갖게 된다.
  
F3에서 보는것처럼 제안한 정규화항은 기존 목적함수에 통합함으로써 cGAN에 쉽게 통합될 수 있다.  
여기서 Lori 는 기존의 loss항이고 Lambda_ms는 정규화 항의 중요도제어weight이다.  
3번 수식 : 일반 cGAN의 loss term이며 c, y, z는 각각 class label, 실제 이미지, noise vectord다.  
4번 수식 : I2I tranlation 문제이기 때문에 y도메인 사진과 생성 사진간 차이에 대한 loss항이 추가 된다.  
제안한 방법을 Mode Seeking GANs(MSGANs)라고 명명한다. 
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124373506-bb142c80-dccd-11eb-8de9-bd54034d2b41.png" width=450 /></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124373376-db8fb700-dccc-11eb-97a3-f63cce03c5a3.png" width=450 /></p>  


# 4. Experiments
## 4.1. Evaluation Metrics
- FID : Inception Network에 입력하여 얻어진 latent code간 분포 차이를 비교
- LPIPS : 생성 샘플간 평균 거리를 통해 다양성을 측정(높은값이 다양함을 나타냄)
- NDB and JSD : bin-based metrics, mode-missng을 평가  
- 실제 데이터 분포의 modes라 여기는 학습 샘플을 K-means로 군집을 분할하고  
- 생성 샘플의 가장 가까운 이웃의 빈에 할당  
- 그후 학습샘플과 생성샘플간 bin의 분포 차이를 비교하여 유사도를 측정  
- 낮은 NDB와 JSD는 분포가 유사함을 뜻함  
## 4.2. Conditioned on Class Label
**Categorical image generation + DCGAN + CIFAR-10(32x32) + LPIP 제외**
table을 보면 다양성과 품질 모두 향상된다.  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124373672-47731f00-dccf-11eb-8599-a4986e419cd2.png" width=800 /></p>  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124373674-4b06a600-dccf-11eb-9197-4484d1c94836.png" width=450 /></p>  

## 4.3. Conditioned on Image
**I2I translation + Pix2Pix(unimodal) and DRIT(multimodal)**
### 4.3.1  Conditioned on Paired Images
Pix2Pix(baseline), MSGAN vs BicycleGAN(paired image 셋에 diverse image 생성)  
dataset : facades, maps  
추가 구조를 필요로하는 MSGAN은 BicycleGAN과 동등하며 Pix2Pix보다는 훨씬 다양성이 있음  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124373925-97eb7c00-dcd1-11eb-8ded-defc62e859df.png" width=800 /></p> 

### 4.3.2  Conditioned on Unpaired Images
DRIT(baseline) : unpaired dataset에 대한 훌륭한 성능을 보이지만 mode-collapse 존재(e.g., cats to dogs).  
양 데이터셋에서 모든 meric에서 DRIT에 비해 나은 성능을 보임 (Table 4.)  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124374082-32988a80-dcd3-11eb-801a-0c5d7dd7e548.png" width=800 /></p> 

Figure6. dog to cat 변환에 대한 bin 비율을 보여주며 DRIT은 mode 분포가 매우 불균일한것을 확인할 수 있음   
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124374345-860bd800-dcd5-11eb-9e70-3a963a383cbc.png" width=600 /></p> 

정성적 평가로, Figure5는 MSGAN이 더 많은 mode들을 시각적 품질저하 없이 보여준다.  
<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124374382-c9fedd00-dcd5-11eb-8e40-49f23bfe938d.png" width=600 /></p> 


## 4.4. Conditioned on Text

**TTI 합성 + StackGAN++에 정규화항 추가 + CUB-200-2011 데이터 **
StackGAN++는 diversity 향상을 위해 Conditioning Augmentation module을 도입하여 텍스트 설명을 가우시안 분포의 text code에 re-parameterize 한다. semantically 의미있는 text code에 정규화항을 적용하는것 대신, prior 분포에서 latent code를 무작위로 뽑아 이용하는것에 집중한다. 정당한 평가를 위하여 다음 두개의 설정에 대해 MSGAN과 StackGAN++를 비교한다.  
1) 텍스트 설명에 대한 text code를 수정하지 않고 생성을 수행 : 이경우 text code는 출력이미지에 대한 다양성을 제공한다.  
2) 고정된 text 코드를 가지고 생성을 수행 : text code의 효과를 제거한다.

 테이블을 보면 text가 고정된 경우와 고정되지않은 경우 모두 다양성과 mode-collapse에 있어서의 성능향상을 확인 할 수 있다.  
 그림을 통해 더 이해를 할 수 있다.  
 <p align="center"><img src="https://user-images.githubusercontent.com/40943064/124374574-5f4ea100-dcd7-11eb-8a32-573e6f2969f0.png" width=750 /></p> 

## 4.5. Interpolation of Latent Space in MSGANs
2개의 Latent 사이를 interpolation 하는 경우 이미지가 부드럽게 변화하는것을 확인할 수 있다.  
mode-seeking이 발생한다면 latent 값의 차이에도 불구하고 이미지의 변화가 없을 것이다.  

<p align="center"><img src="https://user-images.githubusercontent.com/40943064/124374690-7346d280-dcd8-11eb-89ef-67ddac307df1.png" width=750 /></p> 


# 5. Conclusions
cGAN의 mode-collapse를 다루기 위하여 단순하지만 효과적인 mode seeking 정규화항을 G에 포함하는것을 제안한다.  
latent code 거리에 대한 이미지의 거리를 취대로 함으로써 정규화항은 G가 더 minor한 영역을 탐색하도록 한다.  
제안한 정규화항은 학습 오버헤드나 네트워크 구조의 수정 없이 현존하는 cGAN 방식에 대해 잘 통합될 수 있다.  
3가지 조건부 생성 작업(categorical 생성, I2I 변환,TTI 생성)에 대하여 제안 방식의 일반화 성능을 보여준다.  
양질의 결과는 정규화항을 통해 baseline framework으로 하여금 성능을 잃지 않으며 다양성을 향상시킴을 보여준다.  
