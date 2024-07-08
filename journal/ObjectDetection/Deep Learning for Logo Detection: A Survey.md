## Abstract
#### 1) Purpose:
To review the advancements in logo detection based on DL.

#### 2) Datasets: 
Discuss comprehensive public datasets for evaluating logo detection algorithms.  
Datasets are becoming more diverse, challenging, and reflective of real-life scenarios.  

#### 3) Learning Strategies: 
Analyze existing logo detection strategies with evaluating the strengths/weaknesses

#### 4) Future Directions: 
Analyze potential challenges in logo detection  
Present future directions for development in this field  

## Introduction

#### 1) Purpose of Logo Detection:
Determine the location and identity of specific logos in images/videos.  
Benefits applications in intelligent transportation, social media monitoring, and infringement detection.  

#### 1) Challenges:
Diverse contexts, varied scales, changes in illumination, size, resolution, non-rigid deformation.  

#### 2) Evolution of Logo Detection:
Early methods: Hand-crafted features (e.g., SIFT) and statistical classifiers.  
Recent advancements: Deep learning-based solutions.  

#### Advantages of Deep Learning Approaches:
Better robustness, accuracy, and speed  
More expressive feature representation capability  

#### Survey Focus:
Concentrates on DL based solutions for logo detection.  
Covers advances from 2015 onwards.  

#### Methodology:
In-depth analysis and discussion of existing studies.  
Covers various aspects: datasets, pipelines, task types, detection strategies, loss functions.  
Examines contributions and limitations of current approaches

#### Contributions of the Survey:
Provides a comprehensive review of DL based logo detection  
Analyzes potential research challenges  
Presents future research directions  
Aims to promote understanding and foster research in the field  

## Logo Datasets

##### 1. Introduction to Logo Datasets
DL has significantly improved object detection  
Datasets are crucial for comparing algorithms and supporting advanced detection methods  
Overview of logo datasets for detection and classification  

##### 2. Types of Logo Detection Datasets
Categorized into three scales: small/medium/large scale  
Created to solve the problem of large realistic datasets with accurate GT  
Enables qualitative and quantitative comparisons and benchmarking  


##### 3. Small-scale Datasets
**BelgaLogos, FlickrLogos-32**  
- BelgaLogos: First benchmark dataset, 10,000 images, 37 different logos  
- FlickrLogos-32: 32 classes, 70 images per class, real-world challenges  


##### 4. Medium-scale Datasets
**Logo-Net, QMUL-OpenLogo, FoodLogoDet-1500**  
- Logo-Net: For detecting logos and identifying brands from real-world product images  
- QMUL-OpenLogo: Aggregated from seven datasets, imbalanced distribution  
- FoodLogoDet-1500: First high-quality food logo dataset, 1,500 classes, 99,768 images  


##### 5. Large-scale Datasets
LogoDet-3K, PL8K  
- LogoDet-3K: 3,000 logo classes, nine super-classes, 158,652 images
- PL8K: 7,888 logo brands, 3,017,146 images, semi-automatically constructed


##### 6. Logo Classification Datasets
WebLogo-2M, Logo 2K+  
WebLogo-2M: Automatically acquired, weak annotation, noisy data, class imbalance
Logo 2K+: Large-scale, high-quality, diverse logo appearances, imbalanced categories


##### 7. Evaluation Metric
mAP (mean Average Precision) is the most common metric for logo detection

## Logo Detection

### A. Logo Classification
Logo classification aims to recognize the logo name from an input image  
Two main categories: ML based methods vs DL based methods  

1) Traditional Machine Learning-based Methods:

Use manual features like SIFT and HOG for feature extraction  
Classifiers include:  
a) SVM: Used in supervised learning for binary classification(Carvalho et al.'s self-learning and automatic detection method)  
b) KNN: Supervised learning algorithm for classification(Gopinathan et al.'s vehicle logo recognition system using KNN and HOG)  


2) Deep Learning-based Methods:  

Recent developments in DL applied to logo classification  
a) DCNN logo recognition algorithm(Karimi et al.):  
Uses pre-trained models for feature extraction and SVM for classification
Employs transfer learning to improve existing models  
b) DRNA-Net: Discriminative Region Navigation and Augmentation Network(Wang et al.):  
Discovers informative regions for logo classification  
Consists of navigator, teacher, region-oriented data augmentation, and scrutinizer sub-networks  
c) SeeTek(Li et al.):  
Multi-task learning architecture combining deep metric learning and scene text recognition  
Designed to distinguish visually similar logos  

### B. Logo Detection
A specific case of object detection  
Aims to detect logo instances of predefined classes in images or videos  

##### 1) Traditional Approaches:  
Based on hand-crafted visual features (e.g., SIFT, HOG) and traditional classification models (e.g., SVM)
Example: Sahbi et al.'s logo matching system (2013)
Limitations: Lack of pertinence in region-selective search and robustness to logo diversity


##### 2) Deep Learning-Based Approaches:
a) Region-based Convolutional Neural Network models (RCNNs)
b) YOLO-based models
c) Single Shot Detector-based models
d) Feature Pyramid Network-based models
e) Other models
Region-based Convolutional Neural Network models (RCNNs):

Evolution: R-CNN → Fast R-CNN → Faster R-CNN
Advantages: Improved performance and speed
Limitations: Computational redundancy and low efficiency for small object detection


##### RCNN-based Logo Detection Examples:
a) DeepLogo-DRCN by Hoi et al.:
Uses Selective Search for generating ROI. Employs FCNN and FC Layers. First work on DL based logo detection  

b) Oliveira et al.'s Fast R-CNN-based system:
Uses transfer learning and data augmentation. Robust to unconstrained imaging conditions.

c) Li et al.'s Faster R-CNN improvement:
Utilizes transfer learning, data augmentation, and clustering. Improves detection accuracy through hyperparameter optimization and precise anchors for RPN

##### YOLO-based models:
Single-stage detectors commonly used for logo detection
Directly detect images and output category and location information

Evolution of YOLO:  
Early YOLO: Fast but less accurate, especially for small objects  
Improvements: YOLOv2, YOLOv3, YOLOv4, YOLOF, YOLOR, YOLOX, YOLOv6, YOLOv7  
Balance between accuracy and speed  

Applications in Vehicle Logo Detection:  
a) Yin et al.'s system based on YOLOv2:  
High-efficiency vehicle logo detection  
Advantages: Self-learning features and direct image input  

b) Yang et al.'s data-driven enhanced training method:  
Based on YOLOv3  
Combined feature extraction network with multi-scale decision scheme  
Improved detection accuracy for small logos  

c) Zhang et al.'s lightweight network structure:
Uses separable convolutions  
Improves real-time performance and small-scale object detection accuracy  

Addressing Imbalanced Logo Classes:

Wang et al.'s Logo-Yolo based on YOLOv3:

Uses K-means clustering for anchor box selection  
Adopts Focal loss to address sample imbalance  
Introduces CIoU loss for improved bounding box regression  
Performs well on small objects and complex backgrounds  
Limitations: Poor performance on similar or occluded logos  

