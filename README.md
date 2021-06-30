# TIL
- 기록은 모든것의 기본이다. 보고 배운것과 해본것들을 꾸준히 남기도록 한다.
- [namjunemy][nam] 님의 Github TIL을 참고했고 많은 부분을 배울 수 있었다.
# Principles
- Contribution을 목표로 하지 않는다. 보여주기 위한것이 아니라 나를 위한 것을 잊지 말자.
- 파일, 폴더, 변수등 모든 명명 규칙은 이해하기 쉽게 정의한다.
- 다시 보았을 때 불편함이 없도록 명료하게 작성한다.
# Categories
### Coursera : IBM Machine Learning
- Week#1-Module#1. Introduction, History
- Week#1-Module#2. Retrieving Data, Data Cleaning, EDA, Feature Engineering


# 학습할 논문
### Image Generation and etc.

#### Generative Adversarial Nets (2014)
#### Conditional Generative Adversarial Nets (2014)
#### A Neural Algorithm of Artistic Style (2015)
###### : Content image와 style image를 이용하여 이미지를 생성 / [논문링크][j_link001]
#### Improved training of wasserstein gans (2017)
#### Arbitrary Style Transfer in Real-time with Adaptive Instance Normalization (2017)
#### StyleGAN2  : Analyzing and Improving the Image Quality of StyleGAN (2019)
#### StyleMapGAN: Exploiting Spatial Dimensions of Latent in GAN for Real-time Image Editing
#### PIE: Portrait Image Embedding for Semantic Control (2020) / [논문링크][j_link008]
#### U-GAT-IT: UNSUPERVISED GENERATIVE ATTENTIONAL NETWORKS WITH ADAPTIVE LAYERINSTANCE NORMALIZATION FOR IMAGE-TO-IMAGE TRANSLATION



# 학습완료 논문
### Anomaly Detection
#### 1. DeepAnT: A Deep Learning Approach for Unsupervised Anomaly Detection in Time Series(2018)
##### CNN 구조 time series predictor와 error threshold 기반 anomaly detector를 이용하여 여러 형태의 anomaly 탐지 / [논문링크][j_link002]

### Image Generation and etc.
#### StyleGAN1  : A Style-Based Generator Architecture for Generative Adversarial Networks (2019) [정리][j_link007]
#### MoFA: Model-based Deep Convolutional Face Autoencoder for Unsupervised Monocular Reconstruction (2017)
#### StyleRig: Rigging StyleGAN for 3D Control over Portrait Images [논문링크][j_link009]
#### CycleGAN : Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks [정리][j_link008]
#### RTUG : Real-Time User-Guided Image Colorization with Learned Deep Priors[논문링크][j_link010]
#### DRIT++: Diverse Image-to-Image Translation via Disentangled Representations


# 그외의 이론및 모델

[Graphical Model?][b_link001] : 상태를 가지는 모델에서 directed/indirected graphical model의 개념이 자주 등장한다.  
[Restricted Boltzmann Machine][b_link002] : 깊은 신경망에서 학습이 잘 되지 않는 문제를 해결하기 위해 Geoffrey Hinton 교수님이 제안하신 방법론  
Gradient vanishing을 사전학습으로 풀어낸다. 이를 통해 DL이 다시 활기를 되찾았다. Generative 계열을 이해하기 위해서는 이해 필수
[MCMC(Monte Carlo Markov Chain)][b_link003] : 샘플링 방법론
[Pytorch Manual][b_link004] : 파이토치 사용매뉴얼
 # Text book 
 [Machine Learning : A Probabilistic Perspective][t_link001] : ML의 바이블이라고 생각하는 책이다. 언젠간 보고 정리해야겠다고 생각했는데, 언제 다볼 수 있을지... 
 
 
[j_link001]: <https://arxiv.org/pdf/1508.06576.pd>
[j_link002]: <https://ieeexplore.ieee.org/document/8581424>
[j_link003]: <https://ieeexplore.ieee.org/document/9171158>
[j_link004]: <https://www.technicaljournalsonline.com/ijeat/VOL%20V/IJAET%20VOL%20V%20ISSUE%20I%20JANUARY%20MARCH%202014/IJAETVol%20V%20Issue%20I%20Article%207.pdf>
[j_link005]: <https://ieeexplore.ieee.org/document/1542519>
[j_link006]: <https://arxiv.org/abs/1711.04322>
[j_link007]: <https://github.com/kyugorithm/TIL/blob/main/journal/PG_GAN.md>
[j_link008]: <https://github.com/kyugorithm/TIL/blob/main/journal/J006_cycleGAN.md>
[j_link008]: <https://dl.acm.org/doi/abs/10.1145/3414685.3417803>
[j_link009]: <https://arxiv.org/pdf/2004.00121.pdf>
[j_link010]: <https://github.com/kyugorithm/TIL/blob/main/journal/J007_RTUG.md>
[b_link001]: <https://medium.com/@chullino/graphical-model%EC%9D%B4%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%EC%9A%94-2d34980e6d1f>
[b_link002]: <https://github.com/kyugorithm/TIL/blob/main/Theory/RestrictedBoltzmannMachine.md>
[b_link003]: <https://github.com/kyugorithm/TIL/blob/main/Theory/MCMC.md>
[b_link003]: <https://github.com/kyugorithm/TIL/blob/main/ML_APP.md>
[b_link004]: <https://pytorch.org/tutorials/beginner/pytorch_with_examples.html#nn-module>

[nam]: <https://github.com/namjunemy/TIL#%EC%9E%91%EC%84%B1-%EA%B7%9C%EC%B9%99>
