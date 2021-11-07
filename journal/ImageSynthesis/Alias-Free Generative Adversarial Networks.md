## Abstract
우리는 계층적 Convolutional 특성에도 불구하고 전형적인 GAN의 합성 프로세스는 불건전한 방식으로 절대 픽셀 좌표에 의존한다고 본다.  
이는 예를 들어 묘사된 객체의 표면 대신 이미지 좌표에 접착된 세부 사항으로 나타난다.  
G에서 aliasing을 유발하는 부주의한 신호 처리로 근본 원인을 추적한다.  
네트워크의 모든 신호를 연속 신호로 해석하여 원하지 않는 정보가 계층적 합성 프로세스로 유출되지 않도록 보장하는 일반적으로 적용 가능한 작은 아키텍처 변경을 도출한다.  
결과 네트워크가 StyleGAN2의 FID와 일치하지만 내부 표현 방식이 크게 달라 subpixel 스케일에서도 translation과 roation에 버금간다.  
결과는 비디오와 애니메이션에 더 적합한 생성 모델을 위한 기반을 제공한다.

## 1. Introduction

## 2. Equivariance via continuous signal interpretation
### 2.1 Equivariant network layers
#### Convolution
#### Upsampling and downsampling
#### Nonlinearity

## 3 Practical application to generator network
### 3.1 Fourier features and baseline simplifications (configs B–D)
### 3.2 Step-by-step redesign motivated by continuous interpretation
#### Boundaries and upsampling (config E)
#### Filtered nonlinearities (config F)
#### Non-critical sampling (config G)
#### Transformed Fourier features (config H) 
#### Flexible layer specifications (config T) 
#### Rotation equivariance (config R)

## 4 Results
#### Ablations and comparisons
#### Internal representations

## 5 Limitations, discussion, and future work
