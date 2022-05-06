
## 4.1 Sample quality

**표 1 : IS, FID, negative log liklihood for CIFAR10**   
<img width="450" alt="image" src="https://user-images.githubusercontent.com/40943064/167179030-1542096d-5037-41ee-b5e8-e2cce43fdece.png">  


**FID :** 
Conditional 모델을 포함한 대부분의 모델보다 더 나은 품질을 달성  
학습 데이터(3.17), 테스트 데이터(5.24)  
(표준 테스트는 학습 데이터에 대하여 수치를 계산함)  

<img width="1292" alt="image" src="https://user-images.githubusercontent.com/40943064/167175144-3d366411-9638-46fb-bf5b-f35ab0234e95.png">  
Fig. 1: CelebA-HQ 256(left) / unconditional CIFAR10 (right)  

<img width="1492" alt="image" src="https://user-images.githubusercontent.com/40943064/167180022-23931877-33f0-47c8-bc5d-321ef880c501.png">

**Object function 비교**  
1) True variational bound : NLL 
2) Simplified traning object : Qualitative quality

Fig. 1 (CIFAR10, CelebA-HQ 256)
Fig. 3/4 (LSUN 256)
Appendix D for more.

## 4.2 Reverse process parameterization and training objective ablation
<img width="600" alt="image" src="https://user-images.githubusercontent.com/40943064/167181166-dd6ea436-e509-4a23-ae06-2045bd8e8c1e.png">

Table 2: Unconditional CIFAR10 reverse process parameterization and training objective ablation.  
(빈 부분은 성능이 낮았던 경우임)  

reverse process parameterizations과 학습 목적함수(3.2)의 샘플품질에 대한 영향을 본다.

We find that the baseline option of predicting ~  works well only when trained on the true variational bound instead of unweighted mean squared error, a simplified objective
akin to Eq. (14). We also see that learning reverse process variances (by incorporating a parameterized
diagonal   (xt) into the variational bound) leads to unstable training and poorer sample quality
compared to fixed variances. Predicting  , as we proposed, performs approximately as well as
predicting ~  when trained on the variational bound with fixed variances, but much better when trained
with our simplified objective.
