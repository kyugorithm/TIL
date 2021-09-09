U-GAT-IT ablation study for Cat2Dog in the wild(https://www.kaggle.com/c/dogs-vs-cats)

### 성공  
<pre>
1. UGATIT Baseline   
2. w/o D cam and local D  : 47300 iterations * 4 mini_batch
3. w/o D cam and local D + / w dec G IN(not AdaLIN) : 47300 iterations * 4 mini_batch
</pre>
<img src="https://user-images.githubusercontent.com/40943064/132364652-4836c4a9-da3c-4b8e-b4da-666eb892207e.png" width="400" height="250">     <img src="https://user-images.githubusercontent.com/40943064/132522298-bbee9056-4cf0-4a12-b0b4-0fc8868b4a57.png" width="400" height="250">  


### 실패  
<pre>
1. Our Structure : 21875 iterations * 4 mini_batch
2. 1 + layer norm on G : 21875 iterations * 4 mini_batch
</pre>

### 정리
1) **D cam과 local D 없이 / IN 만으로 변경 가능**  
 D의 구조를 단순화 해도 변경은 가능 == G의 역할이 강하게 동작해서 변경 가능한 것으로 판단
2) **CycleGAN + G Decoder [IN > LN] 적용시 변경 불가 ** 

변경 성공했던 UGATIT baseline에 **G는 유지**하고 **D만 변경**해서 U-net Discriminator의 효과 확인 실험 수행중  
