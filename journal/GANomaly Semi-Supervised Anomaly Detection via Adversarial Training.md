# GANomaly: Semi-Supervised Anomaly Detection via Adversarial Training
## Abstract
Anomaly detection은 컴퓨터 비전의 고전적인 문제이다. 비정상 샘플이 적어 정상샘플에 크게 치우쳤을 때 비정상에서 정상을 결정하는 것이다.  
지도학습보다 어려운 것은 문제를 한 클래스 semi-supervised 학습 패러다임의 공간으로 데려가는 알려지지 않은/보이지 않는 이상 사례를 감지하는 것이다.  
**1) 고차원 이미지 공간 생성**과 **2)latent space 추론**을 공동으로 학습하는 cGAN을 사용하여 새로운 이상 탐지 모델을 소개한다.  
G에서 enc-dec-enc sub 네트워크를 사용하면 이미지를 낮은 차원 벡터에 매핑하며, 이 벡터는 생성된 출력 이미지를 재구성하는 데 사용된다.  
추가 encoder 네트워크를 사용하면 생성이미지를 latent 표현에 매핑한다. 훈련 중 이러한 이미지와 latent 벡터 사이의 거리를 최소화하면  
정규 샘플에 대한 데이터 분포를 학습하는 데 도움이 된다.  
결과적으로 inference 시 이 학습된 데이터 분포에서 더 큰 거리 메트릭은 해당 분포의 이상값(이상)을 나타낸다.  
다양한 도메인의 여러 벤치마크 데이터 세트에 대한 실험은 과거 SOTA대비 모델 효능과 우수성을 보여준다.    

## 1. Introduction
supervised approaches heavily depend on large, labeled datasets. In many of the real world problems, however, samples from the more unusual classes of interest are of insufficient sizes to be effectively modeled. Instead, the task of anomaly detection is to be able to identify such cases, by training only on samples considered to be normal and then identifying these unusual, insufficiently available samples (abnormal) that differ from the learned sample distribution of normality. For example a tangible application, that is considered here within our evaluation, is that of X-ray screening for aviation or border security — where anomalous items posing a security threat are not commonly encountered, exemplary data of such can be difficult to obtain in any quantity, and the nature of any anomaly posing a potential threat may evolve due to a range of external factors. However, within this challenging context, human security operators are still competent and adaptable anomaly detectors against new and emerging anomalous threat signatures. As illustrated in Figure 1, a formal problem definition of the anomaly detection task is as follows: given a dataset D containing a large number of normal samples X for training, and relatively few abnormal examples Xˆ for the test, a model f is optimized over its parameters θ. f learns the data distribution pX of the normal samples during training while identifying abnormal samples as outliers during testing by outputting an anomaly score A(x), where x is a given test example. A Larger A(x) indicates possible abnormalities within the test image since f learns to minimize the output score during training. A(x) is general in that it can detect unseen anomalies as being non-conforming to pX. There is a large volume of studies proposing anomaly detection models within various application domains [2–4,23,39]. Besides, a considerable amount of work taxonomized the approaches within the literature [9, 19, 28, 29, 33]. In parallel to the recent advances in this field, Generative Adversarial Networks (GAN) have emerged as a leading methodology across both unsupervised and semi-supervised problems. Goodfellow et al. [16] first proposed this approach by co-training a pair networks (generator and discriminator). The former network models high dimensional data from a latent vector to resemble the source data, while the latter distinguishes the modeled (i.e., approximated) and original data samples. Several approaches followed this work to improve the training and inference stages [8, 17]. As reviewed in [23], adversarial training has also been adopted by recent work within anomaly detection. Schlegl et al. [39] hypothesize that the latent vector of a GAN represents the true distribution of the data and remap to the latent vector by optimizing a pre-trained GAN based on the latent vector. The limitation is the enormous computational complexity of remapping to this latent vector space. In a follow-up study, Zenati et al. [40] train a BiGAN model [14], which maps from image space to latent space jointly, and report statistically and computationally superior results albeit on the simplistic MNIST benchmark dataset [25]. Motivated by [6, 39, 40], here we propose a generic anomaly detection architecture comprising an adversarial training framework. In a similar vein to [39], we use single color images as the input to our approach drawn only from an example set of normal (non-anomalous) training examples. However, in contrast, our approach does not require two-stage training and is both efficient for model training and later inference (run-time testing). As with [40], we also learn image and latent vector spaces jointly. Our key novelty comes from the fact that we employ adversarial autoencoder within an encoder-decoder-encoder pipeline, capturing the training data distribution within both image and latent vector space. An adversarial training architecture such as this, practically based on only normal training data examples, produces superior performance over challenging benchmark problems. The main contributions of this paper are as follows:
지도학습방식은 대규모 데이터에 의존 하지만 실제에서는 관심 클래스의 샘플은 항상 적어 효과적으로 모델링할 수 없다.  
대신, 비정상 탐지의 임무는 정상으로 간주되는 샘플에 대해서만 교육한 다음 학습된 정규성 샘플 분포와 다른 비정상적이고 불충분하게 사용 가능한  
비정상 샘플을 식별하여 이러한 사례를 식별할 수 있도록 하는 것이다.  
예를 들어, 여기에서 우리의 평가에서 고려하는 유형의 응용 프로그램은 항공 또는 국경 보안을 위한 X선 검사이다.  
보안 위협을 제기하는 변칙적 항목이 일반적으로 발생하지 않는 곳에서 그러한 모범적인 데이터는 어느 곳에서나 얻기 어려울 수 있다.  
잠재적인 위협을 제기하는 모든 변칙의 특성은 다양한 외부 요인으로 인해 진화할 수 있다.  
그러나 이러한 어려운 상황에서 인간 보안 운영자는 새롭고 새로운 변칙 위협 서명에 대해 여전히 유능하고 적응 가능한 변칙 감지기이다.  
그림 1에서 볼 수 있듯이 이상 탐지 작업의 공식적인 문제 정의는 다음과 같다.  
![image](https://user-images.githubusercontent.com/40943064/130700993-bfa10430-76a6-45b6-9299-32d909609a43.png)
학습을 위한 많은 수의 정상 샘플 X를 포함하는 데이터 세트 D와 테스트를 위한 상대적으로 적은 비정상 예 Xˆ가 주어지면 모델 f는 θ에 대해 최적화된다.  
f는 학습 중 정상 샘플의 데이터 분포 p**X**를 학습하고 테스트 중 비정상 샘플을 이상치로 식별하는 이상 점수 **A(x: given test sample)** 를 출력한다.  
더 큰 A(x)는 f가 훈련 중에 출력 점수를 최소화하도록 학습하기 때문에 테스트 이미지 내에서 가능한 비정상을 나타낸다.  
A(x)는 **pX** 를 따르지 않음으로써 보지못한 이상을 감지할 수 있다는 점에서 일반적이다.  

**GAN 이상탐지 선행 연구 사례**
1) **AnoGAN** : GAN의 latent 벡터가 데이터의 실제 분포를 나타낸다고 가정하고 latent 벡터를 기반으로 pretrained GAN을 최적화하여 latent 벡터에 다시 매핑한다.  
(잠재 벡터 공간에 다시 매핑하는 엄청난 계산 복잡성이 존재)  
2) **EGBAD** : 이미지 공간에서 잠재 공간으로 공동으로 매핑하는 BiGAN을 학습하고 단순한 MNIST 벤치마크 데이터 세트에도 불구하고 통계 및 계산적으로 우수한 결과를 보고한다.  

본 논문은 GAN을 포함하는 일반적인 이상 탐지 아키텍처를 제안한다.  
AnoGAN과 유사한 맥락에서 단일 컬러 이미지를 입력으로 사용하며, 이는 정상 학습 예제 세트에서만 가져온 것이다.  
그러나 이와 대조적으로 우리의 접근 방식은 2단계 학습이 필요하지 않으며 모델 학습과 이후 추론에 모두 효율적이다.  
EGBAD와 마찬가지로 이미지와 잠재 벡터 공간을 함께 학습한다.  
주 novelty는 enc-dec-enc 파이프라인 내에서 적대적 autoencoder를 사용하여 이미지와 latent vector 공간 내에서 학습 데이터 분포를 포착한다는 사실에서 비롯된다.  
이와 같은 적대적 훈련 아키텍처는 실제로 정상적인 훈련 데이터 예제에만 기반을 두고 있어 까다로운 벤치마크 문제보다 우수한 성능을 제공한다.  
이 논문의 주요 기여는 다음과 같다.  
1) semi-supervised anomaly detection : enc-dec-enc 파이프라인 내의 새로운 adversarial auto encoder로, 이미지와 latent vector space 모두에서 훈련 데이터 분포를 포착하여 최신 GAN 기반 및 기존 autoencoder 기반 접근 방식보다 우수한 결과를 제공한다.
2) Efficacy : 통계적으로나 계산적으로 더 나은 성능을 제공하는 이상 감지에 대한 효율적이고 새로운 접근 방식이다.  
3) Reproducibility : 공개적으로 사용 가능한 코드를 통해 결과를 재현할 수 있는 간단하고 효과적인 알고리즘.  

