## Abstract
대부분의 FS 방법론은 지루한 network 및 loss 설계에 집중하지만 여전히 소스와 타겟의 정보 균형을 맞추는데 어려움을 겪고 있으며 결과물들은 artifact가 발생하는 경향이 있다. 본 연구에서 우리는 간결하고 효과적인 StyleSwap 프레임워크를 소개한다. 핵심은 StyleGAN2를 통해 high-fidelity & robust face swapping 부여하도록 하고 G의 이점이 identity 유사도를 최적하기 위해 사용될 수 있도록 하는 것이다. 최소의 수정 만으로 StyleGAN2를 이용해 소스와 타겟으로부터 바람직한 정보를 성공적으로 다룰 수 있음을 확인했다. ToRGB로부터 영감을 얻어 Swapping-Driven Mask Branch가 정보 blending을 더욱 향상하도록 고안되었다. 추가로 StyleGAN inversion의 이점이 채택될 수 있다. 부분적으로 Swapping-Guided ID Inversion 전략은 ID 유사도를 최적화하도록 고안된다.  

## Introduction
FS는 단일 소스를 이용하면서 다양한 시나리오를 목표로 사용하는 ID-agnostic 세팅에서 여전히 어렵다. 핵심 문제는 아래 두가지로 정리할 수 있다.  
1) ID 정보를 명시적으로 포착
2) 타겟의 implicit attribute를 보존하면서 흔적없이 변환 얼굴을 blending

이 문제를 해결하기 위해 기존 방법론은 아래 두가지 접근법을 택했다.  
1) 구조적 중간 표현 : 과거 컴퓨터 그래픽스 기반의 방법론들은 FS에 landmark나 3D 모델과 같은 구조적 중간 표현에 대한 강력한 prior를 포함시켰다. 최근 연구자들은 이러한 정보를 ID와 표정 추출을 위해 위의 정보들을 GAN에 결합했다. 그러나 구조적 정보(3D, landmark)가 부정확하면 특히 비디오와 같은 생성 결과물의 안정성과 통일성에 나쁜 영향을 주게 된다.  

2) 학습기반 파이프라인 : 대부분 방법은 소스와 타겟사이의 균형을 위해 지겨운 network와 loss 설계에 의존한다. 이러한 설계는 학습을 어렵게 만들고 이상적인 정보를 표현하는데 실패하며 유사하지 않거나 artifact를 만드는 문제가 발생한다.  

최근 StyleGAN 기반 방법론은 강력한 표현력과 latent space 조절의 이점으로 여러 얼굴 생성 테스크(attribute editting, enhancement, reeactment)에 그 효과가 입증되었다. 그러나 FS에서 StyleGAN 적용을 탐색하는 연구는 여전히 불충분하다. 특히, lighting 조건은 MegaFS에서 고정된 StyleGAN G가 표현할 수 있는 제한적인 분포로 인해 매우 성능이 부족하다. MegaFS의 feature blending procedure의 구조는 수작업의 layer-specific 방식으로 설계되었으며 복잡한 human tuning이 필요하다. 결국 High-resolution face swapping via latent semantics disentanglement은 StyleGAN2 feature와 함께 설계된 인디코더를 통합한다. 그러므로 자연스럽게 생기는 질문은 '**지루한 설계는 피하면서 최소한의 수정으로 다재다능한 StyleGAN을 사용할 수 있을까?**' 이다.

결국 우리는 StyleGAN을 통해 FS 능력을 부여하는 간결하고 효과적인 파이프라인의 **StyleSwap**을 제안한다. StyleSwap은 higher fidelity, identity similarity 결과를 만들고 기존 방법보다 다양한 시나리오에서 시각적 artifact를 생성하지 않는다는 점에서 더 robust하다. 또한 구현하기 쉬우며 학습에 친화적이다. 이의 핵심은 단순한 수정을 통해 StyleGAN2의 구조를 FS 데이터 흐름에 적용하는 것에 있으며 G의 id 최적화 이점을 적용하는 것이다. 상세하게, 우리는 단순한 layer-fusion 전략으로 타겟 이미지의 restoration을 얻는다. 동일 아이디어가 StyleGAN의 원래 capability를 유지하는것으로 GPEN을 통해 증명 되었다.  

그리고 우리는 ID정보는 추출된 ID feature를 W space로 mapping함으로써 주입될 수 있음을 주장한다. 이 방법으로 ID 정보는 implicit하게 Conv. 연산에서 attribute와 혼합 될 수 있다.  
또한 우리는 ToRGB와 동일한 Swapping-Driven Mask Branch를 제안 한다. 이는 자연스럽게 네트워크가 타겟의 high-level information에 덜 집중하도록 하고 최종 이미지 blending에 도움이 된다.

우리는 ID 유사도를 향상하기 위해 단순한 최적화 전략을 포함함으로써 구조의 이점을 기술한다. ID feature가 W 공간에 mapping 되듯이 최근 StyleGAN inversion 연구의 자연스러운 영감은 self-reconstruction을 통해 강력한 W+ 공간을 최적화 하는 것이다.  
Mode collapse를 피하기 위해 우리는 반복적으로 feature 최적화와 face swapping을 수행함으로써 새로운 Swapping-Guided ID Inversion 전략을 도입한다.  
이 도구로 무장하여 우리는 우리 방법이 high-fidelity 비디오 학습 패러다임 결과를 생성함을 보인다. 이는 부분적으로 robust하고 고해상도 결과를 위해 향상된 데이터로 지지될 수 있다. 

### Contribution 
1) StyleGAN을 간단하게 수정하고 Swapping-Driven Mask Branch를 설계하는 방법론을 제시한다. : 구현과 학습이 쉽다.
2) ID 유사도를 향상하기 위해 StyleGAN 이점을 통해 새로운 Swapping-Guided ID Inversion 전략을 설계한다.
3) 여러 실험을 통해 SOTA를 능가하고 robustness와 고품질 결과를 생성하는 능력을 가짐을 보인다. 
