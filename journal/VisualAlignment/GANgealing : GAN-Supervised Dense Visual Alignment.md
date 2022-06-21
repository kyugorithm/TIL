# Abstract
Discriminative 모델과 GAN generated training data를 end-to-end 공동으로 학습하기 위한 프레임워크인 GAN-지도 학습을 제안한다.  
프레임워크를 dense visual alignment 문제에 적용한다. 고전적인 **Congealing** 방법에서 영감을 받아, 우리의 GANgealing 알고리듬은 정렬되지 않은 데이터에 대해 학습된 GAN의 무작위 샘플을 공통으로 학습된 대상 모드로 mapping하기 위해 spatial transformer를 학습시킨다.  
GAN gealing은 과거의 self-supervised correspondance algorithm을 크게 능가하며, correspondense algorithm이나 데이터 증강을 사용하지 않고 GAN 생성 데이터에 대해 독점적으로 학습되었음에도 불구하고 여러 데이터 세트에서 SOTA supervised correspondense 알고리듬과 대등하게(때로는 초과) 수행한다. 정확한 대응을 위해 supervised 방법을 최대 3배 향상시킨다. 우리는 AR, 이미지 편집 및 다운스트림 GAN 훈련을 위한 이미지 데이터 세트의 자동화된 전처리를 위한 방법의 응용 프로그램을 보여준다.


대응 또는 등록 문제라고도 알려진 visual alignment은 광학 흐름, 3D 매칭, 의료 영상, 추적 및 증강 현실을 포함한 많은 컴퓨터 비전에서 중요한 요소이다. 쌍방향 정렬(이미지 A를 이미지 B에 정렬)에 대해 최근 많은 진전이 있었지만 전역 공동 정렬(데이터셋에 걸쳐 모든 이미지를 정렬) 문제는 많은 관심을 받지 못했다. 그러나 공동 정렬은 자동 키포인트 주석, 증강 현실 또는 편집 전파와 같은 공통 참조 프레임을 필요로 하는 작업에 중요하다(그림 1 맨 아래 행 참조). 또한 공동으로 정렬된 데이터 세트(예: FFHQ, AFHQ, CelebA-HQ)에 대한 교육이 정렬되지 않은 데이터에 대한 훈련보다 고품질 생성 모델을 생성할 수 있다는 증거가 있다.
