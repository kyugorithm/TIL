## Abstract
StyleGAN 방식의 toonification의 비디오 수준 적용이 어려운 이유는 아래와 같다.   
- 프레임 사이즈가 고정됨
- 얼굴 alignment가 필요함
- 얼굴제외한 디테일 손실됨
- 시간 일관성이 떨어짐

### 목표
**controllable** + **high-resolution** + **portrait** + **video** + style transfer   

### 방법
StyleGAN의 중간이상 해상도 레이어를 이용해 고품질 artistic portrait을 render 하며 디테일을 보존하기 위해서 인코더에서 추출한 multi-scale feature를 활용한다.  
결과적인 FCN 구조는 다양한 해상도의 비디오에서 정렬되지 않은 얼굴을 입력으로 허용하여 전체 얼굴이 자연스럽게 움직이는데 기여한다.  
StyleGAN 기반의 이미지 toonification 모델을 비디오로 확장하는데 적합하며 매력적인 제어(스타일의 유연한 색상과 강도) 특징을 상속받는다.  
Collection 기반의 Toonify와 exemplar 기반의 DualStyleGAN 두가지에 대한 인스턴스화를 제시한다.  

## Introduction
### Paragraph1.
기존 이미지 기반 방식은 비디오 적용시 몇 가지 단점이 있어 제한된다.  
### Paragraph2.
StyleGAN은 1024의 얼굴 이미지를 생성할 수 있어 style transfer에 많이 활용되었다. 이미지를 inversion하여 latent를 얻고 이 latent를 다른 데이터셋에서 fine-tune된 다른 StyleGAN에 적용하여 결과를 얻을 수 있다. (Toonify)  
그러나 이 방법은 고정된 이미지 사이즈만 사용가능하며 정렬된 얼굴이 필요하다. 정렬되지 않은 얼굴 이미지 인코딩은 어려우며 부정확한 인코딩은 style transfer에 해로우며 성능이 떨어진다.  

### Paragraph3.
I2I 변환 방식은 이미지 크기와 얼굴 위치에 대한 엄격한 제한을 피하면서 FCN 구조의 enc-dec 구조로 종종 해결된다.  
훈련 데이터 쌍이 부족하기 때문에 프레임워크는 일반적으로 cycle consistency 방식을 사용하여 학습한다.  
그러나 복잡한 매핑으로 인해 모델이 256×256의 작은 이미지 크기로 제한된다.  
이러한 한계를 해결하기 위해 얼굴 속성 편집에 StyleGAN을 teacher로 이용하는 방식도 있다. 그러나 StyleGAN을 네트워크 설계에 통합하지 않기 때문에 유연한 스타일 제어 특성을 상속하지는 않는다.  
GLEAN은 StyleGAN의 prior를 효과적으로 사용하기 위해 네트워크 설계에 StyleGAN을 도입했지만 fixed-crop limitation는 해결하지 못했다.  
본 논문은 이러한 방식에서 영감을 얻는다.  

### Paragraph4.
정리해 보면 아래와 같은 요소를 고려해야 한다.
1) Variable Size 
2) High-Resolution  
3) Controllability  

### Paragpraph5. 
고정 사이즈 솔루션을 구성하는 StyleGAN의 translation equivariant를 분석한다.  
VToonify는 StyleGAN과 I2I 변환의 장점을 결합하여 제어 가능한 high-resolution portrait video style transfer를 달성한다.  
High-resolution style transfer를 위해 Toonify 방식을 채택하지만 고정 크기 입력 기능과 저해상도 레이어를 제거하여 I2I 방식과 유사하게 다양한 비디오 크기를 지원하는 새로운 완전 컨벌루션 인코더 생성기 아키텍처를 구성한다.  
원래의 high-level style code와 별도로, 생성기에 대한 추가 contents condition으로 입력 프레임의 multi-scale contents feature를 추출하도록 encoder를 학습시켜 style transfer 중에 프레임의 주요 시각적 정보가 더 잘 보존될 수 있도록 한다.  
Chen을 따라 합성된 paired 데이터에서 StyleGAN을 추출한다.  
또한 flickering을 제거하기 위해 단일 합성 데이터에 대한 카메라 모션 시뮬레이션을 기반으로 flicker supression loss를 제안한다.  
따라서 VToonify는 실제 데이터, 복잡한 비디오 합성 또는 명시적인 optical flow 없이 빠르고 일관된 비디오 번역을 학습할 수 있다.  
Chen의 표준 I2IT 프레임워크와 달리 StyleGAN 모델을 G에 통합하여 데이터와 모델을 모두 추출한다.  
따라서 VToonify는 StyleGAN의 스타일 조정 유연성을 상속할 수 있다.  
StyleGAN을 생성기로 재사용함으로써 인코더만 훈련하면 되므로 훈련 시간과 훈련 난이도가 크게 줄어든다.  

### Paragraph6. 
두 가지 대표적인 StyleGAN 백본인 Toonify 및 DualStyleGAN의 portrait video toonification을 위한 것이다.  
Toonify : 데이터셋의 전체 스타일을 기반으로 얼굴 스타일을 지정하고, DualStyleGAN : 데이터셋의 단일 이미지를 사용하여 그림 1의 오른쪽 상단과 같이 세부적인 스타일을 지정한다.  
DualStyleGAN의 스타일 제어 모듈을 적용하여 인코더의 기능을 조정하고 데이터 생성 및 교육 목표를 정교하게 설계하기 위해 VToonify는 DualStyleGAN의 유연한 스타일 제어 및 스타일 정도 조정을 상속하고 이러한 기능을 비디오로 확장한다(예: 그림 1의 오른쪽 상단). 실험에서 우리는 VToonify가 백본만큼 고품질의 양식화된 프레임을 생성할 뿐만 아니라 입력 프레임의 세부 사항을 더 잘 보존한다는 것을 보여준다.  

### 요약

• StyleGAN의 fixed-crop 제한을 분석하고 StyleGAN의 translation equivariant를 기반으로 해당 솔루션을 제안  
• 정렬되지 않은 얼굴과 다양한 비디오 크기를 지원하는 제어 가능한 고해상도 portraits video style transfer를 위한 새로운 fully convolution 프레임워크를 제안  
• Toonify/DualStyleGAN 백본을 기반으로 VToonify를 구축하고 데이터 및 모델 측면에서 백본을 추출하여 컬렉션 기반 및 예시 기반 세로 비디오 스타일 전송을 실현  
• 원칙에 입각한 데이터 친화적인 교육 체계를 설계하고 비디오 스타일 전송 모델을 교육하는 데 효율적이고 효과적인 시간적 일관성을 위한 optical flow 없는 flicker supression을 제안  
