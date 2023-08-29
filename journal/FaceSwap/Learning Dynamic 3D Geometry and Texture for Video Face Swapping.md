
## Abstract

기존의 방법은 2D 기반의 접근 방법을 활용하여 개선된 성능을 획득 했으나, 얼굴의 기하적인 특성이나 텍스쳐 특성을 참고하지 않아 새로운 시점이나 약간의 제어하해서의 일반화 성능을 얻을 수 없었다.

소스와 타겟의 특정적인 기하적 feature에 잘 적응할 수가 없는 사전 학습된 facial priors에 의존한다.  
Methods incorporating geometry rely on pre-learned facial priors that do not adapt well to particular geometric features of the source and target faces. 


FS 문제를 
We approach the problem of face swapping from the perspective of learning simultaneous convolutional facial autoencoders for the source and target identities using a shared encoder network with identity-specific decoders.  ()
The key novelty in our approach is that each decoder first lifts the latent code into a 3D representation, comprising a dynamic face texture and a deformable 3D face shape, before projecting this 3D face back onto the input image using a differentiable renderer. 
The coupled autoencoders are trained only on videos of the source and target identities without requiring 3D supervision. 
By leveraging the learned 3D geometry and texture, our method achieves face swapping with higher quality than off-the-shelf monocular 3D face reconstruction and an overall lower FID score than state-of-the-art 2D methods. 
Furthermore, our 3D representation allows for efficient artistic control over the result, which can be hard to achieve with existing 2D approaches.
