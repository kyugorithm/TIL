## Publish
<pre>
CycleGAN  : ICCV 2017  
discoGAN  : ICML 2017  
UNIT      : NIPS 2017 (MUNIT : ECCV 2018)  
Drit      : ECCV 2018  
StarGANv1 : CVPR 2018  
DMIT      : NIPS 2019  
StarGANv2 : CVPR 2020  
U-GAT-IT  : ICLR 2020  
</pre>
## Batch Size
<pre>
CycleGAN  : 1  
discoGAN  : 1  
UNIT      : 1  
Drit      : 2   
StarGANv1 : 16  
StarGANv2 : 16  
U-GAT-IT  : 1  
</pre>  

## Image Resolution
<pre>
CycleGAN  : 256  
discoGAN  : 256
UNIT      : 256, 512  
Drit      : 360  
StarGANv1 : 128  
StarGANv2 : 256  
U-GAT-IT  : 256  
</pre>  

## Normalization 
<pre>
CycleGAN  : D(BN or IN) / G(BN or IN)  
discoGAN  : D(BN)       / G(BN)  
UNIT      : D(X)        / G(IN + AdaIN)  
Drit      : D(IN or SN) / G(IN + LN)  
StarGANv1 : D(X)        / G(IN)  
StarGANv2 : D(IN)       / G(IN + AdaIN)  
U-GAT-IT  : D(SN)       / G(IN  + **AdaLIN**)  
</pre>  

## Transform
<pre>
CycleGAN  : RandomCrop > Resize > ToTensor > Normalize(0.5)  
discoGAN  : Scale > ToTensor > Normalize(0.5)
UNIT      : ToTensor > Normalize(0.5) > RandomCrop > Resize > RandomHorizontalFlip
Drit      : Resize > ToTensor > Normalize(0.5)  
StarGANv1 : RandomHorizontalFlip > CenterCrop > Resize > ToTensor > Normalize(0.5)  
StarGANv2 : rand_crop > Resize > RandomHorizontalFlip > ToTensor > Normalize(0.5)  
U-GAT-IT  : RandomHorizontalFlip > Resize > RandomCrop > ToTensor > Normalize(0.5)  
</pre>

## Key Concept
CycleGAN  : Cycle consistency  
discoGAN  : Shared encoder  
UNIT      :  
Drit      :  
StarGANv1 : G(class input), cycle consistency   / D(real/facke + domain classifi.)
StarGANv2 : G(style input, AdaIN), D : multiple output branches 
U-GAT-IT  : CAM on Gen./Dis. & Adaptive Linear Instance Norm.  

## Pros and Cons

![image](https://user-images.githubusercontent.com/40943064/132003919-6d313c16-7aa6-4f06-8f08-93283cef810d.png)
 
