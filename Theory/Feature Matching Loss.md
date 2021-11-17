# Feature matching loss
  
## Summary
In GAN-related papers that perform image to image translation tasks, feature matching loss term is often used.  
The cases and explanations used in several papers are summarized to help understand Feature Matching Loss.  
  
---
  
### (2016) Generating Images with Perceptual Similarity Metrics based on Deep Networks
Named loss **Perceptual Similarity Metrics**  
Instead of image space distances, compute distances between features extracted by deep neural networks.  
**C** is feature extractor pretrained for classification task.  
This paper used **L2 loss** for the loss term.  
![image](https://user-images.githubusercontent.com/40943064/142176306-368c09d2-b1a0-467e-b9f4-6bf897d7b915.png)  
![image](https://user-images.githubusercontent.com/40943064/142176421-152742b1-c882-459e-8533-848f22bbc879.png)  
This loss term alone does not provide a good loss for training. It is known (Mahendran & Vedaldi, 2015) that optimizing just  
for similarity in the feature space typically leads to **high-frequency artifacts**.  
This is because for each natural image there are many non-natural images mapped to the same feature vector.  
Therefore, a natural image prior is necessary to constrain the generated images to the manifold of natural image.  

---
  
### (ECCV 2018) MUNIT : Multimodal Unsupervised Image-to-Image Translation

  
---
  
### (ECCV 2019) FUNIT : Few-Shot Unsupervised Image-to-Image Translation
Explanation : The feature matching loss **regularizes** the training.  
Process :  
1. **Df** : Remove the last layer of D and construct feature extractor   
2. Use **Df** to extract features from the translation output **x¯** and the class images {y1, ..., yK} and minimize  
  
![image](https://user-images.githubusercontent.com/40943064/142168442-9d1faff8-5e98-4541-a854-0ff4d38114af.png)  

Unlike other papers, the target class is set to K, not one.  
Therefore, for each target image, the value obtained through the **Df** is forced to be equal to the average of all other classes's feature.  
Furthermore other papers utilize feature matching loss by using feature values of all layers of Discriminator 
This paper's contribution is to extend feature matching loss's use to the more challenging and novel few-shot unsupervised image-to-image translation setting.  
  
---
  
19
29
37
50
