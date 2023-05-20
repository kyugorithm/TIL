FVD: A new Metric for Video Generation
비디오 생성 모델은 시각적 표현뿐 아니라 temporal dynamic에 대한 품질을 평가할 수 있는 메트릭이 없어 한계가 있다.  
본 논문은 FVD가 생성된 비디오의 질적인 관점에서 인지적 판단과 매우 밀접함을 확인하는 대규모 인간 연구에 기여한다.  

1. Introduction

2 FR´ECHET VIDEO DISTANCE

3 EXPERIMENTS
비디오에 대한 noise 추가에 대한 품질 평가 결과를 제시
sample size에 대한 민감도와 해상도를 분석하는 추가 실험(Appendix B & D)

3.1 NOISE STUDY
비디오에 노이즈를 추가하여 FVD가 기본 왜곡에 얼마나 민감한지 테스트.  
**고려 범위**
1) 개별 프레임에 추가된 정적 노이즈  
2) 프레임의 전체 시퀀스를 왜곡하는 시간적 노이즈  

비디오와 노이즈가 많은 비디오 사이의 FVD와 KVD를 계산  
노이즈 강도 : 6  
데이터셋 : BAIR, Kinetics-400, HMDB51  
모델 변형 : latent embedding으로, Kinetics-400/600에서 pretrained I3D 모델의 최상위 pooling과 logit  
기준으로 비디오에 대한 단일 임베딩을 얻는 비디오에 대한 순진한 FID 확장과 비교
  
모든 변형은 pretrained Inception 네트워크가 일반적으로 예상했던 대로 시간적 왜곡을 감지하는 데 열세인 가운데 주입된 다양한 왜곡을 어느 정도 감지할 수 있다.  

그림 2 : "the logits layer of the I3D model pre-trained on Kinetics-400"가 가장 높은 평균 상관관계를 가짐  
그림 3 : Noise 실험에 대한 score overview  


3.2 HUMAN EVALUATION

4 CONCLUSION
