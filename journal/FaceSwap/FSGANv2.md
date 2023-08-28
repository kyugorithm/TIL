## Abstract

### 1) Subject Agnostic Swapping
Swapping does not require training on specific face pairs, making it more flexible.

### 2) Iterative Deep Learning for Reenactment(Iterative Gr)
Employs a new iterative DL approach to adjust significant variations in pose and facial expressions.

### 3) Application on Single Images and Video
Can be applied to either a single image or a sequence of video frames.

### 4) Continuous Interpolation for Video(Delaunay triangle)
Uses continuous interpolation, Delaunay Triangulation, and barycentric coordinates for smoother face views for video sequences.

### 5) Handling Occluded Regions(Gc: inpainting)
A face completion network is used to handle occlusions in the facial region.

### 6) Seamless Face Blending(Gb: blending)
Uses a face blending network that leverages a novel **Poisson blending loss** for a smooth transition while preserving skin color and lighting.

## Introduction

### 1) Existing Methods
Most prior works have focused on either face swapping or reenactment, using 3D face representations to transfer facial features. These approaches could either estimate face shapes from input images or keep them fixed.  

### 2) Limitations of Current Methods  
Current methods often require specific training sets for each subject and may need to handle occluded faces better. Also, there is significant information loss when encoding identity as latent feature vectors.

### Contribution
1) A **face landmarks transformer network** for interpolating between face landmarks without 3D information  
2) Improved **inpainting generator** that utilizes symmetry and face landmark cues  
3) A demonstration of an additional use case for the new face reenactment method for pose-only face reenactment  
4) Completely revised preprocessing and an additional postprocessing step for reducing jittering and saturation artifacts  
5) Introduction of a **new metric **for facial expression comparison

## 3 FACE SWAPPING GAN

### 1) Objective
The goal is to seamlessly replace (Ft​ in It) with (Fs ​in Is) while maintaining the same **pose and expression**.

### 2) Three Major Components

![image](https://github.com/kyugorithm/TIL/assets/40943064/f9af7f5b-a29f-46c8-90b5-6c4f2dcf0ca0)

Gs : U-Net with bilinear interpolation upsampling
Gr, Gc, Gb : pix2pixHD with Coarse-to-fine generator and Multi-scale discriminator
Global Generator of Gr, Gc, Gb
- Net with bottleneck blocks (Concatenation in place of Summation) with bilinear interpolation upsampling
- Characteristics: Smaller channels with better convergence
### 3) Issue of Subject-Agnostic Face Reenactment
Problem: Difficulty in reenactment with large pose changes
Solution: Break down large pose changes into smaller reenactment steps and interpolate between the closest available source images corresponding to the target's pose.

### 3.1 Detection and tracking

1) Face Detection : Videos are processed by the dual-shot face detector (DSFD), which is more accurate than the previously used SFD.  
2) Detection Grouping: Detections from successive frames are grouped into sequences based on Intersection over Union (IoU) calculations, with IoUs > 0.75 considered to belong to the same sequence.  
3) Facial Expression Tracking: 2D landmarks trained on WLFW(consisting of 98 points) are used for tracking facial expressions. (The previous method used both 2D and 3D landmarks with 68 points.)  
4) Sub-Pixel Inaccuracy: Despite SOTA face detection and landmark extraction, bounding boxes and landmarks are not sub-pixel accurate, leading to frame-to-frame inconsistencies and noticeable jittering.  
- Temporal Averaging: While this method can reduce jittering, it introduces lag.  
- 1e Filter Extension: To address the jittering and lag, the 1e filter is extended. This is based on human sensitivity to jittering in small motions and lag in large motions.  
- Motion Estimation: The level of motion is estimated and used as per-frame weights for a 1D temporal averaging filter. Larger motions get less averaging.  
- Smoothing Applications: Smoothing is applied separately to the center and dimensions of bounding boxes and each face part in face landmarks.  

### 3.2 Generator architecture
Gr = Gc = Enhancer(Global(2; 2; 3); 2)  
Gb = Enhancer(Global(1; 1; 1); 1)  
![image](https://github.com/kyugorithm/TIL/assets/40943064/9d593c76-2e24-47f2-bdf7-41daedb200d8)

### 3.3 Training losses
(Reconstruction Loss : Domain specific perceptual loss + Reconstruction loss) + Adversarial Loss
Trained model to compare high-frequency details using multiple face recognition and attribute classification datasets instead of a generic ImageNet-based CNN  

### 3.4 Face Segmentation
Improvements: The inclusion of hair information and data augmentation techniques aim to improve the model's stability and accuracy.

### 3.5 Face reenactment
