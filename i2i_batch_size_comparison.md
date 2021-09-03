DiscoGAN, DMIT

## Publish
CycleGAN  : ICCV 2017  
discoGAN  : ICML 2017  
UNIT      : NIPS 2017 (MUNIT : ECCV 2018)  
Drit      : ECCV 2018  
StarGANv1 : CVPR 2018  
DMIT      : NIPS 2019  
StarGANv2 : CVPR 2020  
U-GAT-IT  : ICLR 2020  
  
## Batch Size
CycleGAN  : 1  
discoGAN  : 1  
UNIT      : 1  
Drit      : 2   
StarGANv1 : 16  
StarGANv2 : 16  
U-GAT-IT  : 1  
  
## Image Resolution
CycleGAN  : 256  
discoGAN  : 256
UNIT      : 256, 512  
Drit      : 360  
StarGANv1 : 128  
StarGANv2 : 256  
U-GAT-IT  : 256  
  
## Normalization 
CycleGAN  : D(BN or IN) / G(BN or IN)  
discoGAN  : D(BN)       / G(BN)  
UNIT      : D(X)        / G(IN + AdaIN)  
Drit      : D(IN or SN) / G(IN + LN)  
StarGANv1 : D(X)        / G(IN)  
StarGANv2 : D(IN)       / G(IN + AdaIN)  
U-GAT-IT  : D(SN)       / G(IN  + **AdaLIN**)  

### D에 Spectral Norm.을 사용하는것을 추천
  
## Transform
CycleGAN  : RandomCrop > Resize > ToTensor > Normalize(0.5)  
discoGAN  : Scale > ToTensor > Normalize(0.5)
UNIT      : ToTensor > Normalize(0.5) > RandomCrop > Resize > RandomHorizontalFlip
Drit      : Resize > ToTensor > Normalize(0.5)  
StarGANv1 : RandomHorizontalFlip > CenterCrop > Resize > ToTensor > Normalize(0.5)  
StarGANv2 : rand_crop > Resize > RandomHorizontalFlip > ToTensor > Normalize(0.5)  
U-GAT-IT  : RandomHorizontalFlip > Resize > RandomCrop > ToTensor > Normalize(0.5)  

## Pros and Cons
![image](https://user-images.githubusercontent.com/40943064/132003919-6d313c16-7aa6-4f06-8f08-93283cef810d.png)
