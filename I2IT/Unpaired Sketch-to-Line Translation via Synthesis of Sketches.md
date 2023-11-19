
## Abstract
**Task**.: Hand-drawn sketch -> line drawings  
**App**.: Product design & comics  
**Problem**: Collecting paired sketch and clean line pairs is diffucult.  
**Solution**:  
Propose training scheme that requires only unpaired sketch and line images for learning sketch-to-line translation.(trained on a limited number of handcrafted paired data.)  
1. Generate paired sample: Rule-based line augmentation and unsupervised texture conversion from unpaired images  
2. Supervised training (exclude the dependent on cycle loss)  
This method prove the supervised method shows better result at removing noisy strokes  

## Introduction
Work process of (cartoon, movie and product design) Artists:  
**Sketching**(quickly express artistic concepts w/o considering details) -> **clean lines**(time consuming process)  
For model, reasoning whether to remove(noisy strokes) or reserve(line to be preseved) is difficult.  


Learning to simplify(Simo-Serra)  
:Deep learning methods which simplify raster sketch images, learn useful features automatically from data, and show robust performance on various sketch images.  
: It Needs artist's expensive and time consuming to get paired training data for supervised learning.

A method for learning without paired data was later proposed in CycleGAN.  
But CycleGAN/MUNIT loss can't make clean line for undesired noisy sketch  

Thus, the authors proposes a method for "synthesizing paired data" to frame the problem in a supervised setting.

**1) Initial Synthetic Sketch Generation:**  
- **Produce initial synthetic sketches** rule-based line augmentation(individually perturbing each Bézier curve by adding noise to its control points.)  

**2) Sketch Refinement:**   
Refine the initial synthetic sketches using MUNIT. This step helps bridge the texture gap between synthetic and real sketch images.  

**3) Model Training:**  
Train a recent SPADE with the synthetic paired data for sketch-to-line translation.  

## Method

### 2.1 Rule-based Line Augmentation

1) Vectorize Clean Line Images(parametric curves using vectorization methods)  
2) Model using Quadratic Bézier Curves: Use simple quadratic Bézier curves, with three control points, for curve shaping.  
3) Perturb Control Points: Introduce noise to Bézier curve control points, mimicking real sketch strokes. Noise levels are based on Gaussian distribution and proportional to line length.  
4) Segment and Perturb Long Curves: Break longer curves into shorter segments, adding noise to each to emulate artists' sketching of long lines with short strokes.  
5) Repeat Noisy Strokes: Duplicate strokes multiple times as per artists' sketching style, controlled by a hyperparameter.
6) Adjust Background and Illumination: Modify background color and illumination for added realism in synthetic sketches.
7) Simulate Line-Filled Sketch Areas: Use watershed segmentation to create line-filled areas, typical in sketches.  
8) Hyperparameter Selection: Section 3.1 discusses the criteria for choosing appropriate hyperparameters.

### 2.2 Unsupervised Texture Conversion 
Initial synthetic sketches from Rule-based Line Augmentation mimic real sketches in shape but lack the **varied textures and colors of papers and pencils used in real sketches**.  
To solve this problem, author applied MUNIT to mimic texture style of sketch image as follows.  
Using MUNIT for Texture Conversion: Train MUNIT with synthetic sketches(2.1) and real sketches to convert the artificial textures of synthetic sketches.  

### 2.3 Learning to Simplify using Synthetic Data
Train SPADE(advancement in semantic image generation compared to the Pix2Pix)  
![image](https://github.com/kyugorithm/TIL/assets/40943064/d834d5b3-f102-49ac-b74b-096673792523)  

1) Encoding Sketch Images: Since sketch images are not semantically meaningful like the semantic labels in the original SPADE paper, they are first encoded using an cnn layer.  
2) Importance of Encoded Features: Emphasize the necessity of feeding encoded feature maps into the model, as the model struggles to find meaningful structures in sketch images without these features.  
3) Instance Norm.: Implement Instance Norm. for the generator within the model.  


## 3. Experiment

### 3.1 Experimental Details

**Data:**  
1300(130 line images and created 10 sketches for each.)  
Danbooru2018 (Gathered 20,000 sketches & 1,320 line arts)

**Hyperparameters for Synthetic Sketch Construction:**  
Used α values of 30, 40, 50.
Randomly sampled **Mc** and **Ms** values from a Poisson distribution with λ = 3.  

**Image Modification:**  
Set the ratio of colored or line-filled regions to 50% of the images.
Training MUNIT and SPADE Models:

ADAM optimizer(lr=0.0001, β1 = 0.5, and β2 = 0.9)  
Resized images to 512 × 512 and used 256 × 256 cropped patches for training.  
250,000iter + batch size: 16.  

**Line Width Preservation:**  
Line normalization module proposed by Simo-Serra et al. 2018b to prevent deformation of the line width in ground truth images.

### 3.2 Comparison with Existing Approaches

**Model Comparison:**  
MS [Simo-Serra et al. 2018a], SPADE(MS), Inker, CycleGAN, and MUNIT.  

**Methodology:**  

SPADE(MS) was trained with sketches from the line-to-sketch model in MS.
Pretrained models of MS and SPADE(MS) were used.  
CycleGAN and MUNIT codes were taken from their project sites.  
Inker results were obtained from their demo site.  
Test images were resized to 512 × 512.  

**Model Performance:**  

CycleGAN & MUNIT struggle with **noisy strokes** due to cycle consistency losses.  
Proposed model effectively removes noise and handles edge cases better(benefits from diverse and challenging sketch patterns.)  
  
**Evaluation Metrics:**  
The model had the lowest FID   

**Human Evaluation:**  
The proposed model was most preferred based on visual appeal. for 20 users comparing three models.  

**Data Used:**  
Evaluation involved 1000 sketch and 150 line images.  


![image](https://github.com/kyugorithm/TIL/assets/40943064/b5ecff5a-3e7c-4077-acb6-7679024dbd73)













