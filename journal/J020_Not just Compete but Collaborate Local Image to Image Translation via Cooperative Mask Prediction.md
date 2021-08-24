Not just Compete, but Collaborate: Local Image-to-Image Translation via Cooperative Mask Prediction
## Abstract 
얼굴 속성 편집은 원하는 속성으로 이미지를 조작하면서 다른 디테일은 보존하는 것을 목표로 한다.  
최근, GAN, Encoder-Decoder architecture가 현실적인 이미지를 만들 수 있는 능력 때문에 이 작업에 활용되고 있다.  
그러나 unpaired dataset에 대한 기존 방법은 ground truth image가 없기 때문에 attribute-irrelevant regions를 제대로 보존할 수 없다.  
본 연구는 CAM-consistensy loss라는 새롭고 직관적인 손실 함수를 제안하며, 이는 이미지 변환에서 입력 이미지의 일관성을 향상시킨다.  
기존의 cycle consistency loss는 이미지를 다시 변환할 수 있도록 보장하지만, 우리의 접근방식은 모델이 판별기에서 계산한 Grad-CAM 
출력을 사용하여 다른 도메인에 대한 단일 변환에서도 속성 무관 영역을 더욱 보존하도록 한다.  
우리의 CAM-consistensy loss는 다른 영역을 변경하지 않으면서 발전기가 변경해야 하는 로컬 영역을 적절히 캡처하기 위해 학습 중에  
판별기에서 이러한 Grad-CAM 출력을 직접 최적화한다.  
이러한 방식으로, 우리의 접근방식은 이미지 변환 품질을 향상시키기 위해 생성자와 판별자가 서로 협력할 수 있도록 한다.  
실험에서는 StarGAN, AttGAN, STGAN과 같은 대표적인 얼굴 이미지 편집 모델에 CAM 일관성 손실 제안의 효과와 다용성을 검증한다.
