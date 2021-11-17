# Feature matching loss
  
## Introduction
In GAN-related papers that perform image to image translation tasks, feature matching loss term is often used.  
The cases and explanations used in several papers are summarized to help understand Feature Matching Loss.  

## 1. FUNIT : Few-Shot Unsupervised Image-to-Image Translation
Explanation : The feature matching loss **regularizes** the training.  
Process :  
1. **Df** : Remove the last layer of D and construct feature extractor   
2. Use **Df** to extract features from the translation output **x¯** and the class images {y1, ..., yK} and minimize  
  
![image](https://user-images.githubusercontent.com/40943064/142168442-9d1faff8-5e98-4541-a854-0ff4d38114af.png)  

Unlike other papers, the target class is set to K, not one.  
Therefore, for each target image, the value obtained through the **Df** is forced to be equal to the average of all other classes's feature.  
Furthermore other papers utilize feature matching loss by using feature values of all layers of Discriminator 
