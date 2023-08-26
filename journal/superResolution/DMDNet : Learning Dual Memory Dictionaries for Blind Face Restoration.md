## Abstract
### 1. Complexity and Importance of Blind Face Restoration:
BFR is a challenging task due to unknown variables and complex degradation factors. Nevertheless, it has significant value across various practical applications.

### 2. Limitations of Existing Methodologies:

#### 1) Generic Restoration:  
While it relies on a general facial structure, it struggles to adapt to real-world degraded conditions. This is mainly due to the limitations of CNN-based mappings, which also miss out on capturing id-specific details.

#### 2) Specific Restoration:  
This aims to restore id-specific features using a reference image of the same id. However, the requirement for an appropriate reference image significantly restricts the applicable use-cases.

### 3. Innovative Approach of DMDNet
#### 1) Dual Dictionaries: 
Separates generic facial features and id-specific features, storing them in separate dictionaries  
- The generic dictionary learns from HQ images of various ids   
- The specific dictionary stores features unique to each individual id  

#### 2) Dictionary Transform Module:  
Whether or not a degraded input image has a specific reference, this module extracts relevant features from both dictionaries and fuses them into the input features. This enhances the flexibility and effectiveness of the restoration process.

#### 3) Multi-Scale Dictionaries:  
These are utilized to consider features at various resolutions, enabling restoration at multiple levels of detail, from fine to coarse.

### 4. Additional Technical Features:  
#### 1) End-to-End Optimization: 
The entire framework of DMDNet is optimized in an end-to-end manner, making it easily adaptable to a variety of application scenarios.

#### 2) CelebRef-HQ Dataset:  
A new HQ dataset has been constructed to foster research in specific face restoration at higher resolutions.  

## Introduction

## Tech flow
(2022-TPAMI) DMDNet: Learning Dual Memory Dictionaries for Blind Face Restoration  
(2020-CVPR) ASFFNet: Enhanced blind face restoration with multi-exemplar images and adaptive spatial feature fusion  
(2020-ECCV) DFDNet: Blind Face Restoration via Deep Multi-scale Component Dictionaries
(2019-CVPRW) GWAInet: Exemplar guided face image super-resolution without facial landmarks  
(2018-ECCV) GFRNet: Learning Warped Guidance for Blind Face Restoration  
