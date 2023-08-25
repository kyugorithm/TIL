![image](https://github.com/kyugorithm/TIL/assets/40943064/5b0df474-5856-423c-be34-686eaa283069)## Abstract
**Two-stage** framework for controllable Identity Guided Face Inpainting (IGFI) under heterogeneous domains.  


1. _**SFI-Net**_ :  
Explicitly disentangle FG and BG of target face image.  
Adaptively fit the target face onto BG, leveraging ID(src) and 3D/texture(trg).
3. _**JR-Net**_ :  
Refine swapped image.  
Leverage AdaIN(stylizing ID and multi-scale texture codes) to transform the decoded face from SFI-Net with facial occlusions.  
(**Challenge**: The boundary of BG and swapped FG is inconsistent.)  

## 1. Introduction

### ID Swapping and its Challenges
(DeepFakes, FaceSwap, FaceShifter, SimSwap) enable the manipulation of facial features.  
However, they lack performance control and visual realism.  
Face forensics also benefit from the challenging and diverse samples. (in terms of fake detection)  

### Evaluation Criteria for Face Swapping
FSs are assessed on ID and Attr. fidelity.  
FaceShifter uses SPADE and AdaIN for metrics but struggles with **redundancy**.  
Some redundant identity features of the source, e.g., hair, make it difficult to preserve attributes in some challenging cases.(figure)  
SimSwap preserves attributes well but is limited to paired data learning.  

![image](https://github.com/kyugorithm/TIL/assets/40943064/7f354e85-4d83-4a66-b738-cbc38a3abc25)


### The Heterogeneous ID Swapping Problem
The challenge lies in swapping identities across pose, expression, and lighting conditions.  
An IGFI framework is proposed for better **control and generalization**.  

### Extracting Identity and Attribute Features
ID from src via ArcFace, and Attr. from trg via 3D fitting models. These are used to control the IGFI process.  

###  SFI-Net for Texture and Shape
Combines various factors from both the source and target to achieve efficient and controllable IGFI, particularly preserving high-fidelity non-face areas like background and hair.  

### JR-Net for Final Adjustments
Refines **identity, attributes, and boundary fusion** using AdaIN and multi-scale texture codes. It optimizes **visual and occlusion perception**.  

### Results and Adaptability
The method produces high-quality swapped faces adaptable to various **heterogeneous domains**, including non-photorealistic styles **like cartoons**.

### Contribution
1. First heterogeneous ID swapping solution using  IGFI. Archives more controllable and higher quality considering (HI-FI ID and Attr.)
2. Two-stage : SFI-Net(map fs using priors including 3D and ID) and JR(refine attr and id with generating occlusion-aware and high-resolution results with naturally fused boundary.)

## 3. Approach
IGFI task aims to generate a modified foreground face that preserves Attr. while naturally fusing with the background.  
Three key factors—expression, pose, and texture—are considered. ArcFace, 3DMM, and texture encoders are used to create **style codes** that guide the face synthesis in SFI-Net. However, this result results in inconsistencies between the new face and the original BG. The JR-Net later refines these inconsistencies.

### 3.1. Styled Face Inpainting Network
Since 3DMM facial expressions and IDs are entangled, we don't use the 3DMM's ID, but instead utilize the Recognition Network.
1) ArcFace : zid(Xs)
2) 3DMM Expression : zexp(Xt)
3) 3DMM Pose : zpos(Xt)
4) VGG19 texture : ztex(Xt^fg)  
C = [zid(Xs), zexp(Xt), zpos(Xt), ztex(Xfgt )],  

Ic(StyleGAN output) and bg fused to maintain Hi-fi scene.  
<img src="https://github.com/kyugorithm/TIL/assets/40943064/4858f1b3-dd1c-4edc-80d9-bef3986dacdb" width=300>

### Loss
Lid: Cosine Similarity between Xs and Y^st  
Lexp: expression 3dmm param. loss between Xt and Y^st  
Lpos: pose 3dmm param. loss between Xt and Y^st  
LGAN: pass  
Lrec: applied when Xs and Y^st are same  
LCX: Contextual loss to avoid artifacts where ArcFace causes hair in the source to appear. It allows for shape deformation while preserving the texture.  
Lppl:  
The technique commonly used in StyleGAN to improve **the diversity and consistency of generated images**.  
It ensures that small changes in the latent code result in proportionate changes in the output image, **preventing extreme variations**.   
When applied to face-swapping models like FaceSwap, it allows for more nuanced and natural adjustments to facial features and styles.  
By capturing subtle differences between the original and target faces more effectively creates more natural-looking results.  
Additionally, this regularization prevents the model from over-focusing on specific features, promoting better generalization across various styles and attributes.  
Overall, using Path Length Regularization in SFI-Net training can lead to more stable and natural face-swapping outcomes for a variety of inputs.


<img src="https://github.com/kyugorithm/TIL/assets/40943064/0396e151-4eac-4687-827b-781e741c82ff" width=500>    

## 3.2. Joint Refinement Network
The result cannot handle occlusions. It also struggles with low-resolution situations and produces boundary artifacts.  
To make the generated image occlusion-aware, a **residual map** representing the occlusions between Xt and ˆYt,t is fed into JR-Net.  
This approach aims to improve **the finesse and adaptability of the face-swapping process**.  

<img src="https://github.com/kyugorithm/TIL/assets/40943064/d30779ce-116d-4b78-b781-9ad7e8654d91" width=500>    



Embeddings(Attribute: 512 and extracted using VGG. + ID embedding of Xs) => AdaIN to transfer feature styles of swapped, delta Xt
![image](https://github.com/kyugorithm/TIL/assets/40943064/8199dbdb-72bf-41ab-b677-9222c085f361)


Moreover, model uses DFDnet based SR shcematic based on multi-scale component dictionaries from high-quality reference images.

Specifically, in DFT, the offline generated dictionaries are modulated via AdaIN, based on texture features of the corresponding eye, nose, and mouth from { ˆYs,t, △Xt}. Then the matched restored features are used for feature modulation in Dec, via the corresponding SFT.

### Loss
LCX: Contextual loss to avoid artifacts where ArcFace causes hair in the source to appear. It allows for shape deformation while preserving the texture.  
Lid: Cosine Similarity between Xs and Yst  
Lrec: applied when Xs and Y^st are same  
Lvgg: VGG19 feature l2 loss between Xt and Yst(if Xs=Xt) otherwise 0  
LGAN: pass  

## 4. Experiment

### SFI-Net
Datasets: CelebA-HQ, FFHQ, VGGFace(256×256)  
Face Alignment: Five point landmarks (Joint cascade face detection and alignment).
Get 3DMM Parameters using 3DDFA2
Dimensionality: zexp(Xt): 10, zpos(Xt): 12, zid(Xs) & ztex(Xfg t) & ztex(Xt): 512
Fusion Module Output Dimension: 1024  
Equation Weights: 'id'=20, other weights=10  

### JR-Net
Datasets: CelebA-HQ, FFHQ, VGGFace(512x512)
Warping: Warps ˆYt,t according to facial landmarks of Xt. Focuses more on occlusion via △Xt.
Architecture Blocks: 8 AdaIN residual blocks + Downsampling Blocks: 3 + Upsampling Blocks: 4  
Data Augmentation: Cropping, flipping, rotation, blur, variations in brightness, saturation, contrast, and color jittering  



### Notable items

1) Perceptual Path Length Loss
2) Residual map of JR-Net to refine the result.

