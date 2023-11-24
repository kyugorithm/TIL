# Cross-Domain Style Mixing for Face Cartoonization

## Abstract

Previous methods not properly addressed the critical constraints, such as requiring a large number of training images or the lack of support for abstract cartoon faces. 
Recently, Toonify required only a limited number of training images; however, its use cases are still narrow as it inherits the remaining issues.  

#### Solution
Cross-domain Style mixing(CDSM): combines two latent codes from two different domains.  
Effectively stylizes faces into multiple cartoon characters at various face abstraction levels using **only a single G without even using a large number of training images.**cartoons  

## 1. Introduction
**Portrait stylization to the cartoon domain**  
I2IT is a notable approach (Cartoongan, U-GAT-IT) but requires many of cartoon images and exhaustive GPU resources.  
In addition, it often lacks the ability to express **character-specific cartoon features**, thus limiting its practical application.  

To mitigate these issues,  
Toonify:  
Toonify uses layer swapping using 2 StyleGANs and is trained on hundreds of training images.  
But the method suffers from critical quality issues(cannot be expressed in fine detail and the colors may be distorted in some parts of the output images.)  
These problems deteriorate when the texture and abstraction level of the target cartoon character are vastly different from those of human faces, as commonly seen in the style of Japanese animation.
레이어 스왑을 쓰고 수백장 이미지를 이용하여 학습하나 상세하게 표현될 수 없거나 출력 이미지 일부분의 색상이 왜곡된다. 이러한 문제는 특히 카툰 도메인의 추상화(e.x., 데포르메)가 클 수록(일본 애니메이션) 커진다.

#### Solution
CDSM combines latent codes from two different domains. 
We obtain the latent codes for both the input natural face (source domain) and the cartoon (target domain) images and perform style mixing in the same latent space of the layer-swapped generator (Figure 3). 
In detail, we first carefully design inversion strategies for generating the latent codes for the source and target domains. 
We employ a pretrained encoder (e.g., ReStyle [2]) for the source domain and a projection protocol for the target domain, both in the expressiveW+ space [1]. 
This makes the latent codes suitable for combining. Then, we perform style mixing on them in the S space (StyleSpace [24]).
