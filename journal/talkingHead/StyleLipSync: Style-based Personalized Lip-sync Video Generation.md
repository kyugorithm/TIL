StyleLipSync: Style-based Personalized Lip-sync Video Generation

## Abstract
Generate "ID-agnostic lip-sync. video from arbitrary video"

### StyleGAN
The robust prior inherent in StyleGAN's latent space can be utilized, which is particularly valuable due to its semantically rich information. 
Traversing this latent space allows for the generation of photorealistic images with video consistency.

### 3D parametric mesh predictor
Used to make mask dynamically which is effective for improving the natrualness  

### Adaptation
Introduce sync regularizer that preserves lip-sync quality while enhancing person-specific information(ID, ...)
