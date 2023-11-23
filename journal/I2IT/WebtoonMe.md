## Abstract

<img width="728" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/e9a31425-6d5d-4cd2-89bd-27177d953034">

### Problem
Translate images into cartoon style with full-body stylization  

### Limitations
Focusing solely on the face, existing methods are limited in achieving a natural look for body stylization.
Recent 2-stage methods consider full bodies but with sensitive and less plausible outputs + Fail to accomodate diverse skin tone   

### Solution
Proposes a **data-centric** approach to develop a full-body portrait stylization system by building the two-stage method with advanced dataset preparation paradigm.  
New approach effectively addresses **the quality issues in non-face** regions and **skin tone problem**   

## Introduction
Full-body portrait stylization, transforming user portraits into Webtoon characters, is important.  

### Previous Studies and Limitations
#### Prior Approaches:  
Use of StyleGAN2 for face region stylization with high visual quality. (JoJoGAN & U-GAT-IT)  

#### Challenges:  
Difficulty in real-world application due to limitations to face regions and the requirement of face alignment, which affects pose and non-face synthesis.
Spirin's Approach: A two-stage scheme using StyleGAN2 fine-tuned with cartoon faces and an image-to-image translation network trained on a blended photo-cartoon dataset. This method aimed at full-body stylization but faced several drawbacks, like less appealing face quality, unsatisfactory non-face regions, and ignorance of diverse skin tones.

### Proposed Solution
#### Data-Centric Approach
Focus on creating a synthetic training dataset with advanced preparation and augmentation methods.

#### Methodology
Separation of source portrait images into head & background, stylizing each individually, specialized modeling for cartoon faces, and background stylization.

#### Color Correction and Augmentation: 
1) Maintain input portrait color tone for racial diversity
2) Increase quality robustness using CutFace augmentation
3) 
#### Training and Inference: 
Training the stylization network with a paired dataset in a supervised manner, with no additional cost at inference.

### Contributions

#### Natural Stylization: 
Achieves natural and high-quality stylization of face, body, and background with a limited Webtoon face images(<100).  

#### Diversity in Skin Color: 
Reflects skin color diversity, addressing a limitation of previous methods.

#### Robustness in Real-World Applications: 
Produces fewer distortions, fulfilling robustness criteria for real-world applications.

## 2. Approach


### Core Approach
2-Stage Stylization Framework: Adopts ArcaneGAN's two-stage method, which involves:
#### 1) Synthetic-Paired Dataset Creation: 
Synthesize a dataset that pairs of real and stylized (Fig. 2a).

<img width="200" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/6f97167d-7417-417d-aad2-6b3652f6690d">  

#### 2) Supervised Training of Stylization Network: 
Training the network using this paired dataset to achieve stylization (Fig. 2c).

<img width="250" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/381e3fa8-fcd3-4749-9fd9-c22f32dc40ea">  


### Data-Centric Procedures
Aim: Construct a more sophisticated training dataset using data-centric approaches.  
#### Key Modules:
1) Full-Body Aware Data Synthesis: Focusing on generating data that is conscious of the full-body requirements of the stylization process.  
2) Input Color Correction: Adjusting the color of the input images to ensure consistency and quality in the final stylized output.  
3) Full-Body Aware Data Augmentation: Enhancing the dataset with additional information relevant to full-body characteristics (Fig. 2b).  
<img width="710" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/9281b00f-cf09-4dd5-bb5b-6d03679edb98">

### Enhancements over the Previous Approach
Modification of the First Phase: The initial stage of the 2-stage(ArcaneGAN) (Fig. 2a) is altered to improve the target domain images while leaving the source domain images unaffected.
Efficiency: The proposed method achieves natural and high-quality stylization of the input portraits using <100 images.

### 2.1 Full-Body Aware Data Synthesis
The two-stage method produces unsteady outputs when  
#### (1) Target image has severe **geometric deformations**  
#### Problem 
We observe that the layer blending-based method(Toonify) is often vulnerable to the **geometric changes** of facial parts.  
So, the portrait stylization framework based on this method is also affected. 
#### Solution
Thus, we employ a cross-domain style-mixing (CDSM), which is known to be robust to geometric deformation.  
With this, we generate source domain images 𝑋𝑠𝑟𝑐 through FFHQ pre-trained StyleGAN2 and initial target domain images 𝑋𝑐𝑑𝑠𝑚 𝑡𝑔𝑡 via CDSM.

### (2) the pixel distribution of background regions in the target domain images are diverged from that of the real source domain images. 

#### Problem
The previous method trains the stylization network using only face images. Accordingly, the background regions received at the inference phase become out-ofdistribution, resulting in an unexpected result. 
Fig. 3(d,e) show that the baseline (two-stage) method undesirably alters the shape of the original (FFHQ) pixel distribution. 
Consequently, it shifts the color and texture of the background while pursuing the distribution of head regions (e.g., purplish and flattened).
<img width="750" alt="image" src="https://github.com/kyugorithm/TIL/assets/40943064/482c3cb6-c3fd-4e10-980b-3323ac424949">
#### Solution
Divide image to face and bg region. -> Extract 𝑀ℎ𝑒𝑎𝑑(head masks: face+hair,neck using bisenet v2) form Xsrc  
**Face**: Mhead is used to get head regions of the Xcdsm(Xcdsm_tgt ⊙ Mhead).  
**Bg.**: Create synthetic bg imgs. Xsty_tgt by translating Xsrc via AnimeGAN(the background stylization model) (Xsty_tgt ⊙ (1 − Mhead)).  
Xfb_tgt(full-body aware images.) = Xcdsm_tgt ⊙ Mhead + (Xsty_tgt ⊙ (1 − Mhead)) / instead of baseline method which is layer blending Toonify.  
 
 Note that AnimeGAN(the background stylization network) is trained on diverse Webtoon images to translate the input to the universal Webtoon background style while adequately maintaining the input color (Fig. 3f).  
 It also shows that our method ensures that the distribution is not markedly diverged from that of FFHQ (Fig. 3d).  
 
 ### 2.2 Input Color Correction
Problem. Color correction to head regions to improve the stylization **quality of facial parts** and increase the capability to **handle racial diversity**.  
The former inspiration regards relaxing the unaligned pixel distribution of head and background regions. 
Xfb_tgt is composed of background regions, which are stylized while preserving the input color (Fig. 3f) and head regions, which are stylized by referring to the color/texture of the target character (Fig. 3b). 

**와닿지 않는 부분**
It means that "1) Color of the background should be retained & 2) The facial part should be substantially changed."  
Such a complex mapping is difficult to learn without an explicit guide of the head position.  
Therefore, we relax the complication of this mapping function by simply changing to at least preserve noticeable color information of source image for head regions (i.e., Fig. 3b→c).  

#### Data distribution
#### Problem  
To preserve a user's skin tone is important.*(not for a cartoon character's skin color which is biased)  
#### Challenges with Data Bias  
In the synthetic dataset, facial parts often appear whitewashed, particularly when the target character has light skin color. This issue arises from a bias in data handling and is significant to address.  
#### Color Reflection Algorithm
Calculate the average color of facial parts in both source and target images. Images and average colors are converted to Lab color space, and color adjustments are made to reflect the input color tone in the target images ( � � � � � � X crtgt ​ ). The images are then converted back to RGB space. Outcome of the Algorithm: The algorithm effectively preserves the color tone of the input portrait, enabling the achievement of color diversity. This is visually represented in Fig. 4g. 

#### Training the Stylization Network
The stylization network is trained using a paired dataset of (Xsrc, Xcr_tgt), which helps in preserving the source domain images' color distribution while accommodating the geometric deformation typical in cartoon characters.  
This training is essential for the final product in the inference phase, as illustrated in Fig. 2c.

### 2.3 Full-Body Aware Data Augmentation
#### Problem
In the synthetic dataset, bg. only accounts for 35%, with blurry images.(no complex patterns in the dataset).  
As a result, this limits the stylization quality and the robustness regarding the background.  
#### Solution
One method to address this is to incorporate landscapes generated using AnimeGAN into the dataset. 
However, since bg. do not include faces, simply adding them can compromise the quality of facial regions. 
Therefore, the stylization network cannot implicitly localize the head position.

##### CutFace
A data augmentation to build a robust and high-quality full-body stylization framework.  
It generates augmented images ~𝑋cr_tgt by integrating  𝑋𝑠𝑡𝑦_𝑏𝑔(stylized landscape images) and  𝑋𝑐𝑟_𝑡𝑔𝑡(color reflected face images) (Fig. 2b).  
In particular, 𝑘 face images are randomly pasted on the landscape images (without overlapping).  
Using CutFace, we guide the stylization network to implicitly learn the position of head regions without explicit information from the user;  
the stylization quality is improved, and the robustness of the background region also increases significantly (Fig. 4d, g) producing fewer distortions for all cases.
