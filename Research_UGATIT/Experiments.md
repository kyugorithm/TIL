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
3. UGATIT + w UnetD : 40400 iterations * 4 mini_batch
 
</pre>

Unet의 Layer 수가 적어서 3개를 추가하여 재학습 수행
