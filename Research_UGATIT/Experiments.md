U-GAT-IT ablation study for Cat2Dog in the wild(https://www.kaggle.com/c/dogs-vs-cats)

### 성공  
<pre>
1. Baseline   
2. w/o D cam and D local discriminator  : 47300 iterations * 4 mini_batch
</pre>
<img src="https://user-images.githubusercontent.com/40943064/132364652-4836c4a9-da3c-4b8e-b4da-666eb892207e.png" width="400" height="250">  
### 실패  
<pre>
1. Our Structure : 21875 iterations * 4 mini_batch
2. 1 + layer norm on G : 21875 iterations * 4 mini_batch
</pre>
