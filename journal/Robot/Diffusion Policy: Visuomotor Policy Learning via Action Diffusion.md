## Abstrct
####Proposal
Propose robot action generation using conditional DDPM of visuomotor policy of robots  
  
####Performance
4 robot manipulation benchmarks, 15 Tasks에서 기존 State-of-the-art 대비 평균 46.9% 성능 향상  
  
####Technics
• Conditional DDPM으로 action 분포의 score function gradient 학습  
• Inference 시 Langevin dynamics 기반 스텝을 통해 반복 최적화  

####Strong points
• Multi-modal 동작 분포 처리  
• 고차원 동작 공간에 적합  
• 학습 안정성 우수  
  
####Contribution
• RHC(Receding Horizon Control) 통합  
• Visual Input 기반 조건부 생성  
• Time-series Diffusion Transformer 아키텍처 도입  
  
####Goal
Diffusion 기반 robot policy 학습이 새로운 표준이 되도록 동기부여  
