## Abstract
실제 이미지와 분간되지 않는 모양과 질감이 전역적이고 지역적으로 일관된 이미지를 합성하기 위한 **capacity**가 GAN의 주요 과제이다.  
이를 위하여 논문은 segmentation분야의 통찰력을 빌려 대안의 **U-Net기반 Discriminator** 구조를 제안한다.  
U-Net 구조는 합성이미지에 대한 전역적 feedback를 제공하여 전역적 일관성을 유지하고 생성기에 상세 per-pixel feedback을 전달한다.  
분별기의 픽셀당 응답에 힘입어 CutMix 데이터 augmentation에 기반한 per-pixel consistency regularization 기법을 사용하며  
U-Net 판별기가 실제와 가짜가 이미지 사이의 semantic하고 구조적인 변화에 더욱 집중하도록 장려하여  
학습 성능을 향상시키며 생성 샘플들의 이미지 품질을 향상시킨다.  
새로운 판별기는 SOTA 방법들에 걸쳐 표준분포와 이미지품질 metrics 항목을 향상시킨다.
이는 생성기가 전역적이고 지역적인 현실성을 유지한채로 변화하는 구조, 외모, 디테일 수준을 가진 이미지를 합성할 수 있도록 한다.  
BigGAN baseline과 비교하여 우리는 평균 2.7FID 향상을 얻었다.  

## Introduction

Large-scale 학습, 구조변경, 정규 기법적용으로 향상된 학습 안정성등은 GAN의 품질 향상에 기여했으나   
1)전체 semantic 일관성, 2)long-range structure, 3) 디테일 정확성의 문제로 학습 한계가 있어왔다.  
잠재적 문제중 하나는 D에 있는데, 데이터 분포를 목표로 합성이미지에 대한 학습 신호를 G에 제공하는 loss function의 역할을 한다.  
D가 강할수록 G의 성능도 향상된다. 현 SOTA GAN 모델에서 D는 단지 실제 이미지와 합성이미지 사이의 가장 분별되는 차이에  
기반하여 효율적으로 G를 penalize하는 표현만을 배운다. 따라서, D는 때때로 global 혹은 local중 하나에만 집중한다.  
D가 non-stationary 환경에서 학습을 해야함에 따라 이 문제가 증폭된다. : 
학습에 따라 G가 지속적으로 변화하며 합성이미지 샘플 분포는 이동하게 되며 이때문에 과거 task를 까먹게 되기 쉽다.  
(D학습관점에서 semantic, 구조, 질감등 학습은 다른 task로 여겨질 수있다.)  
따라서 이러한 D는 더 global, local 이미지 차이를 학습하는 강력한 D를 유지하는데 incentive를 받지 않게 된다.  
이는 때로 합성 이미지가 일관적이지 않고 부분적으로 얼룩덜룩하게 되도록 하거나 기하적이고 구조적 패턴이 일관적이지 않게 된다.  

전술한 문제를 해결하기 위해 우리는 global/local 결정을 동시에 출력하는 대안의 D 구조를 제안한다.  
![image](https://user-images.githubusercontent.com/40943064/125013911-a1952b00-e0a7-11eb-96c5-15f3a8fab7b0.png)

sementation 분야로부터 아이디어를 얻어, 우리는 D의 역할을 classifier와 segmenter 두개 부여하도록 재설계한다.
D를 U-net으로 설정하며 encoder는 이미지에 대한 분류, decoder는 perpixel 분류역할을 부여한다.  



This architectural change leads to a stronger discriminator, which is encouraged to maintain a more powerful data representation, making the generator task of fooling the discriminator more challenging and thus improving the quality of generated samples (as also reflected in the generator and discriminator loss behavior in Figure 8). Note that we do not modify the generator in any way, and our work is orthogonal to the ongoing research on architectural changes of the generator [20, 27], divergence measures [25, 1, 37], and regularizations [40, 15, 34]. The proposed U-Net based discriminator allows to employ the recently introduced CutMix [47] augmentation, which is shown to be effective for classification networks, for consistency regularization in the two-dimensional output space of the decoder. Inspired by [47], we cut and mix the patches from real and synthetic images together, where the ground truth label maps are spatially combined with respect to the real and fake patch class for the segmenter (U-Net decoder) and the class labels are set to fake for the classifier (U-Net encoder), as globally the CutMix image should be recognized as fake, see Figure 3. Empowered by per-pixel feedback of the U-Net discriminator, we further employ these CutMix images for consistency regularization, penalizing per-pixel inconsistent predictions of the discriminator under the CutMix transformations. This fosters the discriminator to focus more on semantic and structural changes between real and fake images and to attend less to domain-preserving perturbations. Moreover, it also helps to improve the localization ability of the decoder. Employing the proposed consistency regularization leads to a stronger generator, which pays more attention to local and global image realism. We call our model U-Net GAN. We evaluate the proposed U-Net GAN model across several datasets using the state-of-the-art BigGAN model [5] as a baseline and observe an improved quality of the generated samples in terms of the FID and IS metrics. For unconditional image synthesis on FFHQ [20] at resolution 256 × 256, our U-Net GAN model improves 4 FID points over the BigGAN model, synthesizing high quality human faces (see Figure 4). On CelebA [29] at resolution 128×128 we achieve 1.6 point FID gain, yielding to the best of our knowledge the lowest known FID score of 2.95. For class-conditional image synthesis on the introduced COCOAnimals dataset [28, 24] at resolution 128×128 we observe an improvement in FID from 16.37 to 13.73, synthesizing diverse images of different animal classes (see Figure 5).
