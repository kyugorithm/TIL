## Abstract
**Two-stage** framework for controllable Identity Guided Face Inpainting (IGFI) under heterogeneous domains.  


1. _**SFI-Net**_ :  
Explicitly disentangle FG and BG of target face image.  
Adaptively fit the target face onto BG, leveraging ID(src) and 3D/texture(trg).
3. _**JR-Net**_ :  
Refine swapped image.  
Leverage AdaIN(stylizing ID and multi-scale texture codes) to transform the decoded face from SFI-Net with facial occlusions.  
(**Challenge**: The boundary of BG and swapped FG is inconsistent.)  

## 1. Introduction

**ID Swapping and its Challenges:**  
(DeepFakes, FaceSwap, FaceShifter, SimSwap) enable the manipulation of facial features.  
However, they lack performance control and visual realism.  
Face forensics also benefit from the challenging and diverse samples. (in terms of fake detection)  

**Evaluation Criteria for Face Swapping:**  
FSs are assessed on ID and Attr. fidelity.  
FaceShifter uses SPADE and AdaIN for metrics but struggles with **redundancy**.  
SimSwap preserves attributes well but is limited to paired data learning.  

**The Heterogeneous ID Swapping Problem:**  
The challenge lies in swapping identities across pose, expression, and lighting conditions.  
An IGFI framework is proposed for better **control and generalization**.  

**Extracting Identity and Attribute Features:**  
ID from src via ArcFace, and Attr. from trg via 3D fitting models. These are used to control the IGFI process.  

SFI-Net for **Texture and Shape**:
Combines various factors from both the source and target faces to achieve efficient and controllable IGFI, particularly preserving high-fidelity non-face areas like background and hair.  

JR-Net for **Final Adjustments**:
Refines **identity, attributes, and boundary fusion** using AdaIN and multi-scale texture codes. It optimizes **visual and occlusion perception**.  

**Results and Adaptability:**
The method produces high-quality swapped faces adaptable to various **heterogeneous domains**, including non-photorealistic styles **like cartoons**.




