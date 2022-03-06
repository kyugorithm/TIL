
## Abstract
Deep fake technology became a hot field of research in the last few years. 
Researchers investigate sophisticated GAN, autoencoders, and other approaches to establish precise and robust algorithms for face swapping. 
Achieved results show that the deep fake unsupervised synthesis task has problems in terms of the visual quality of generated data. 
These problems usually lead to high fake detection accuracy when an expert analyzes them. 
The first problem is that existing image-to-image approaches do not consider video domain specificity 
and frame-by-frame processing leads to face jittering and other clearly visible distortions. 
Another problem is the generated data resolution, which is low for many existing methods due to high computational complexity. 
The third problem appears when the source face has larger proportions (like bigger cheeks), 
and after replacement it becomes visible on the face border. 
Our main goal was to develop such an approach that could solve these problems and outperform existing solutions on a number of clue metrics. 
We introduce a new face swap pipeline that is based on FaceShifter architecture and fixes the problems stated above. 
With a new eye loss function, super-resolution block, and Gaussian-based face mask generation leads to improvements 
in quality which is confirmed during evaluation.
