U-GAT-IT ablation study for Cat2Dog in the wild(https://www.kaggle.com/c/dogs-vs-cats)

### 성공  
<pre>
1. Baseline   
2. w/o D cam and local D  : 47300 iterations * 4 mini_batch
3. w/o D cam and local D + / w dec G IN(not AdaLIN) : 47300 iterations * 4 mini_batch
</pre>
<img src="https://user-images.githubusercontent.com/40943064/132364652-4836c4a9-da3c-4b8e-b4da-666eb892207e.png" width="400" height="250">     <img src="https://user-images.githubusercontent.com/40943064/132501532-427bfc50-37fe-48ca-9a22-ad83c48c3e0d.png" width="400" height="250">  

### 실패  
<pre>
1. Our Structure : 21875 iterations * 4 mini_batch
2. 1 + layer norm on G : 21875 iterations * 4 mini_batch
</pre>
