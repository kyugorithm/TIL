## Abstract
학습된 G를 사용해 image editing을 수행하는 다양한 방법이 시도되고 있다.  
이러한 방법을 실제 이미지에 적용하는 것은 이미지를 latent space로 inversion시켜야 하기 때문에 어렵다.  
이미지를 성공적으로 inversion하려면 이미지를 정확하게 reconstruct 하고 더 중요하게는 의미 있는 manipulation을 허용하는 latent code를 찾아야 한다.  
본 논문에서는 SOTA G인 StyleGAN의 latent space를 주의 깊게 연구한다.  
StyleGAN latent space 내에서  distortion-editability tradeoff 및 distortion-perception tradeoff의 존재를 식별하고 분석한다.  
그런 다음 StyleGAN이 원래 학습된 영역에 대한 inversion의 근접성을 제어할 수 있는 방식으로 encoder를 설계하기 위한 두 가지 원칙을 제안한다.  
이러한 균형을 유지하여 실제 이미지를 쉽게 편집할 수 있도록 특별히 설계된 두 가지 원칙을 기반으로 하는 encoder를 제시한다.  

## 1. Introduction

StyleGAN은 놀라운 사실성을 넘어 학습된 intermediate latent space W를 사용한다.  
이는 standard Gaussian latent space와 비교하여 학습 데이터의 분포를 더 충실하게 반영한다.  
많은 연구에서 W가 학습된 StyleGAN을 활용하여 다양한 이미지 조작을 수행할 수 있도록 하는 흥미로운 얽힌 속성을 가지고 있음을 보여주었다.  

이러한 조작을 적용하기 위해 먼저 주어진 이미지를 latent로 invert 해야한다.  
(즉, 획득한 style code를 사전학습된 StyleGAN에 대한 입력으로 제공하면 원본 이미지가 반환되도록 latent code를 되찾는다.  
따라서 이러한 편집 기술에는 고품질 inversion이 필수적이다.  
고품질 inversion은 아래 두 가지 특징이 있다.  
1) G는 inversion에서 얻은 style code로 주어진 이미지를 적절하게 reconstruct 해야한다.  
2) 주어진 이미지의 **의미 있고 사실적인** 편집을 얻기 위해 latent space의 editing 기능을 최대한 활용할 수 있어야 한다.(편집 가능성)  
적절한 재구성을 정의하기 위해 두가지 속성을 구별한다.  
(i)  Distortion(↓)          : 입출력 이미지의 유사성  
(ii) Perceptual quality(↑) : 재구성된 이미지의 사실성

Distortion, perceptual quality 및 editability 사이에는 밀접한 관계가 있다.  
W latent space의 expressiveness는 모든 이미지가 W에 정확하게 매핑될 수 없다는 점에서 제한적인 것으로 나타났다.  
이러한 제한을 완화하기 위해 Abdal은 모든 이미지가 W+로 표시된 W의 확장으로 inversion될 수 있음을 보여준다.  
여기서 style code는 여러 style vector로 구성된다.  
공간 W+는 더 많은 자유도를 가지기 때문에 W보다 훨씬 더 표현력이 뛰어나다.  
비록 이 확장이 이미지 표현력은 높지만, 원래의 W 공간에서 떨어져서 이미지를 inversion 하면 편집이 잘 되지 않고 지각 품질이 낮은 latent space에 도달한다.  
Distortion, perceptual quality 및 editability 사이의 이러한 균형이 이 문서에서 제시되고 광범위하게 분석된다.  
(W+ : 표현력 강함, 편집력 떨어짐)  (W : 표현력 떨어짐, 편집력 강함)  

Image inversion의 주요 동기가 downstream editing task임을 인식하고 inversion된 실제 이미지의 editability를 이해하는 데 중점을 둔다.  
우리의 핵심 통찰력은 W에 가까운 이미지를 inversion하여 editability와 perceptual quality를 가장 잘 달성할 수 있다는 것이다.  
다음에서 "close"라는 용어는 두 가지 주요 속성을 특징으로 한다.  
1) 서로 다른 style vector간 분산이 낮다.  
2) 각 스타일 벡터가 분포 W 내에 있다.  

W에 가까운 이미지를 반전하도록 명시적으로 권장되는 새로운 encoder를 설계한다.  
이 인코더는 두 가지 목적을 제공한다.  
1) Distortion-editability와 distortion-perception tradeoff가 W에 대한 latent code의 근접성에 의해 제어됨을 증명  
2) 이미지를 편집하기 위한 효과적인 encoder를 구성  
따라서 인코더 이름을 e4e(Encoder for editing)로 정한다.  

특히, 우리는 주어진 이미지를 mapping하도록 encoder를 설계한다.  
이미지를 각각 W의 분포에 가까운 분산이 낮은 일련의 style vector로 구성된 style code로 변환한다.  
W의 분포는 명시적으로 모델링할 수 없기 때문에 Nitzan에서 도입된 style code의 adversarial training을 확장하고  
이를 여러 code에 적용하여 각각을 W로 적절하게 인코딩하도록 권장한다.
편집 가능한 영역에 머무르는 것을 추가로 지원하기 위해 style vector간의 분산이 학습 중에 점진적으로 증가하는 progressive training scheme을 추가로 제시한다.  

우리는 Distortion-editability 및 distortion-perception tradeoff와 W에 "close"한 inversion의 이점을 보여주는 양적 및 정성적 결과를 제시한다.  
우리는 우리의 접근 방식의 일반화와 얼굴 영역과 달리 공통 구조가 없고 수많은 모드를 포함할 수 있는 다양한 도전 영역에 대한 적용 가능성을 보여주는 인코더를 평가한다.  
그림 1에서는 인코더가 여러 도메인에서 얻은 inversion과 다양한 편집 방법을 사용하여 수행된 여러 조작을 보여준다.  
보시다시피 왜곡이 약간만 감소하면 원본 이미지의 내용과 품질을 유지하면서 그럴듯하게 편집된 이미지를 얻을 수 있다.  

### Contribution 
• StyleGAN의 복잡한 latent space 분석및 구조에 대한 새로운 관점 제안  
• 왜곡, 인식 및 편집 가능성 간의 본질적인 절충점을 제시  
• 절충점을 특성화하고 encoder가 이를 제어할 수 있는 두 가지 수단을 설계  
• inverted real image의 editing을 허용하도록 특별히 설계된 새로운 encoder e4e 제시

