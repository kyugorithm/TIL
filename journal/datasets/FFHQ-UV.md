## Abstract

다양한 조명 조건에서 사실적 3D 얼굴 모델 렌더링하는 데 필요한 특성인 균일한 조명, 중립적인 표정 및 깨끗한 얼굴 영역이 포함된 50,000개 이상의 고품질 텍스처 UV 맵을 포함하는 대규모 얼굴 UV 텍스처 데이터 세트를 제공한다.  

아래의 완전한 자동 및 강력한 UV 텍스처 생산 파이프라인으로 FFHQ 세트에서 파생된다.  
1) StyleGAN 기반 face image editing으로 단일 이미지 입력에 대해 multi-view normalized face image 생성
2) 정교한 UV texture 추출/수정/완성을 통해 정규화된 얼굴 이미지에서 고품질 UV 맵을 생성  
(기존 UV 텍스처 데이터셋과 비교하여 다양하고 고품질의 텍스처 맵을 가진다.)  
Parametric fitting 기반 3D face reconstruction을 위한 비선형 텍스처 기반으로 GAN 기반 texture decoder를 추가로 학습한다. 

## Introduction
대부분의 3DMM based reconstruction은 shape 추정 정확도 향상에 중점을 두었지만 texture UV map recon 문제를 해결한 작업은 적었다.  
이 문제에서는 결과 texture map의 fidelity와 quality가 중요하다. 입력 이미지의 id를 보존하는 high-fidelity texture map을 복구하려면 3DMM의 texture basis는 더 큰 표현력을 가져야 한다.  
반면 high quality texture map은 다양한 조명에서 rendering하기 위한 얼굴 자산으로 texture map을 사용할 수 있도록 얼굴 영역이 고르게 조명되고 원하지 않는 머리카락이나 액세서리가 없어야 한다.  

GANFIT : 표현력을 높이기 위해 3DMM의 선형 texture basis를 대체하는 texture 디코더로 10,000개의 UV map에서 GAN을 학습한다. 학습 데이터의 UV map 조명이 고르지 않은 얼굴 이미지에서 추출되어 결과 텍스처 맵에는 명백한 그림자가 포함되어 있으며 조명이 다른 렌더링에는 적합하지 않다.  
AvatarMe : (UV-GAN을 기반의 다른 작업) 통제된 조건에서 200명의 인물에 대한 고품질 texture map에서 학습된 초고해상도 네트워크와 선형 texture 기반 피팅을 결합한다.  
HiFi3DFace : 200개의 texture map에서 학습된 regional fitting 접근 방식과 세부 정제 네트워크를 도입하여 선형 텍스처 기반의 표현 능력을 향상시킨다.  
Normalized Avatar : 고품질 스캔 데이터와 합성 데이터로 구성된 5,000개 이상의 대상이 있는 더 큰 texture map 데이터에서 texture decoder를 학습한다.  

위 결과 texture map의 quality는 높지만 재구성 충실도는 훈련 데이터 세트의 인물 수에 따라 크게 제한되며 공개되지도 않는다.  
* Facescape : 공개적으로 액세스할 수 있는 최신 고품질 texture map 데이터셋(통제된 환경 취득 했으며 847개의 ID만 있음)    

이 논문에서는 다양한 인물에서 추출한 고품질 texture map으로 구성된 대규모의 공개적으로 사용 가능한 얼굴 UV 텍스처 데이터 세트를 제공한다.  
이를 위해 대규모 "wild" face image 데이터 세트에서 고품질 texture UV map을 생성할 수 있는 완전 자동의 강력한 파이프라인이 필요하다.  
생성된 텍스처 맵의 경우 균일한 조명, 중립적인 표정, 머리카락이나 액세서리와 같은 가려짐 없이 완전한 얼굴 텍스처가 될것으로 기대되어진다.  
이것은 간단치 않고 몇 가지 문제가 있다.  
1) Wild face iamge의 제어되지 않은 조건은 고품질의 normalized texture를 제공할 수 없다.  
2) single-view face image에서 전체 얼굴 texture를 추출할 수 없다.  
3) 얼굴 이미지와 추정된 3D 모양 사이의 불완전한 정렬은 래핑되지 않은 texture UV-map에서 만족스럽지 못한 아티팩트를 유발할 수 있다.  

이를 해결하기 위해 StyleGAN 기반 이미지 편집 접근 방식을 활용하여 단일 wild 이미지에서 multi-view normalized 얼굴을 생성한다.  
이후 texture unwrapping에서 불완전한 3d shape 추정으로 인한 불만족스러운 아티팩트를 수정하여 고품질의 texture UV map을 안정적으로 제작할 수 있도록 UV texture 추출/보정/완성 과정을 개발한다.  
제안된 파이프라인을 사용하여 FFHQ를 기반으로 FFHQ-UV라는 대규모 정규화된 얼굴 UV 텍스처 데이터 세트를 구성한다.  
FFHQ-UV 데이터 세트는 FFHQ의 데이터 다양성을 상속하며 사실적인 digital human rendering을 위한 face asset으로 직접 사용할 수 있는 high-quality texture UV map으로 구성된다.  
FFHQ를 사용하여 GAN based texture decoder를 추가로 학습하고 texture decoder로 재구성된 3D 얼굴의 fidelity 및 qaulity 모두 크게 향상함을 보여준다.  

• 공개적으로 사용 가능한 최초의 대규모 정규화된 face UV 텍스처 데이터 세트, 즉 FFHQ-UV에는 사실적인 digital human을 rendering하기 위한 face-asset으로 직접 사용할 수 있는 50,000개 이상의 고품질의 균일하게 조명된 face texture UV map이 포함되어 있다.  
• StyleGAN 기반 face image editing, elaborate UV texture extraction/editing/completion 절차로 구성된 대규모 wilt face image 데이터 세트에서 제안된 UV texture 데이터 세트를 생성하기 위한 완전 자동 및 강력한 파이프라인.  
• FFHQ로 학습된 GAN 기반 texture decoder를 기반으로 fidelity와 quality 측면에서 SOTA를 능가하는 3D face recon. 알고리즘.
