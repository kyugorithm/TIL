# Abstract
Discriminative 모델과 GAN generated training data를 end-to-end 공동으로 학습하기 위한 프레임워크인 GAN-지도 학습을 제안한다.  
프레임워크를 dense visual alignment 문제에 적용한다. **Congealing**에서 영감을 받아, GANgealing은 정렬되지 않은 데이터에 대해 학습된 GAN의 무작위 샘플을 공통으로 학습된 대상 모드로 mapping하기 위해 spatial transformer를 학습시킨다.  
GAN gealing은 과거의 self-supervised correspondance algorithm을 크게 능가하며, **correspondense algorithm**이나 **data augmentation** 없이 GAN 생성 데이터에 대해서만 학습되어 여러 데이터 세트에서 SOTA supervised correspondense에 필적했다. 정확한 대응을 위해 supervised 방법을 최대 3배 향상시킨다. 우리는 AR, 이미지 편집 및 다운스트림 GAN 훈련을 위한 이미지 데이터 세트의 자동화된 전처리를 위한 방법의 응용 프로그램을 보여준다.

# 1. Introduction
Correspondence 또는 registration 문제라고도 알려진 visual alignment은 광학 흐름, 3D 매칭, 의료 영상, 추적 및 AR을 포함한 많은 컴퓨터 비전에서 중요한 요소이다. pairwise alignment(이미지 A를 이미지 B에 정렬)에 대해 최근 많은 진전이 있었지만 global joint alignment(데이터셋에 걸쳐 모든 이미지를 정렬) 문제는 많은 관심을 받지 못했다. 그러나 공동 정렬은 auto keypoint annotation, AR 또는 edit progation와 같은 common refernce frame을 필요로 하는 작업에 중요하다(그림 1 맨 아래 행 참조). 또한 jointly aligned datasets(FFHQ, AFHQ, CelebA-HQ)에 대한 교육이 정렬되지 않은 데이터에 대한 훈련보다 고품질 생성 모델을 생성할 수 있다는 증거가 있다.

본 논문에서는 automatic joint image set alignment에 대한 과거연구에서 영감을 얻는다. 특히, Learned-Miller의 비지도 congealing 방법에 의해 동기부여가 되는데, 이는 일련의 이미지가 공통 업데이트 모드로 지속적으로 변형됨으로써 정렬될 수 있음을 보여준다. Congealing은 MNIST 숫자와 같은 간단한 이진 이미지에서 놀라울 정도로 잘 작동할 수 있지만, 직접적인 픽셀 수준 정렬은 모양과 포즈 변화가 큰 대부분의 데이터 세트를 처리할 만큼 강력하지 않다.   
  
이러한 한계를 해결하기 위해 입력 이미지의 변환을 학습하여 더 나은 관절 정렬로 가져오는 GAN-감독 알고리듬인 GAN galing을 제안한다. 핵심은 공간 변환기에 대한 쌍체 훈련 데이터를 자동으로 생성하기 위해 GAN(미정렬 데이터에 대해 훈련된)의 잠재 공간을 사용하는 것이다[35]. 결정적으로, 우리가 제안한 GAN 지도 학습 프레임워크에서, 공간 변환기와 대상 이미지는 모두 공동으로 학습된다. 우리의 공간 변환기는 GAN 이미지로만 훈련되고 테스트 시 실제 이미지로 일반화된다. 8개의 데이터 세트에 걸친 결과를 보여 줍니다.LSUN 자전거, 고양이, 자동차, 개, 말 및 TV[88], In-The-Wild CelevA[52] 및 CUB[84]—우리의 GAN 게일링 알고리듬이 데이터 세트 전체에서 정확하고 밀도 높은 대응을 발견할 수 있음을 보여준다. 우리는 공간 변환기가 이미지 편집 및 증강 현실 작업에 유용하다는 것을 보여준다. 정량적으로 GAN 게일링은 많은 SPair71K [60] 범주에서 키 포인트 전송 정확도(PCK[4])를 거의 두 배로 늘리면서 과거의 자체 감독 밀도 대응 방법을 크게 능가한다. 더욱이, GAN gealing은 때때로 최첨단 통신 감독 방법과 일치하고 심지어 초과한다.
