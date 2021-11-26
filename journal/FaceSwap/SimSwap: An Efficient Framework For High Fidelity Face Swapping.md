# SimSwap: An Efficient Framework For High Fidelity Face Swapping

## Abstract

일반화된 고성능의 face swapping을 목적으로 하는 효율적 framework를 제안  
임의 ID를 일반화하는 능력이 부족하거나 표정/시선등의 특성들을 보존하지 못하는 과거 연구결과와 달리  
임의의 source face의 **ID**를 전달하면서 target face의 attribute를 보존할 수 있다.
다음의 두가지 방법으로 문제를 해결한다.  
  
1) ID Injection Module (IIM) : feature level의 source ID 정보를 target으로 전송  
- 특정 ID에 한정으로 학습되는 방식을 임의 ID 적용 방식으로 확장할 수 있다.

2) Weak Feature Matching Loss : Implicit 방식으로 attribute를 보존

여러 wild face set에 대한 다양한 실험은 SOTA 대비 attribute 보존/ID 적용 성능의 경쟁력을 보여준다.  
![image](https://user-images.githubusercontent.com/40943064/143544606-8516eb6f-982c-402c-9f6e-f631a53ea930.png)


## Introduction
Face swapping은 target의 attribute(표정, 자세, 조명)는 보존하면서 source ID를 전달하는 유망한 기술이다.  
이 기술은 존재하지 않는 쌍둥이를 생성하는 영화산업에서 광범위하게 사용된다.  


The industrial face swapping method utilizes advanced equipment to reconstruct the actor’s face model and rebuild the scene’s lighting condition, which is beyond the reach of most people. Recently, face swapping without high-end equipment [2, 7, 20, 26] has attracted the researcher’s attention. The main difficulties in face swapping can be concluded as follows: 1). A face swapping framework with a strong generalization ability should be adapted to arbitrary faces; 2). The identity of the result face should be close to the identity of the source face; 3). The attributes(e.g. expression, posture, lighting etc.) of the result face should be consistent with the attributes of the target face. There are mainly two types of face swapping methods, including source-oriented methods that work on the source face at image level and target-oriented methods that work on the target face at feature level. Source-oriented methods [3, 4, 26, 27] transfer attributes(like expression and posture) from the target face to the source face and then blend the source face into the target image. These methods are sensitive to the posture and lighting of the source image and are not able to reproduce the target’s expression accurately. Targetoriented approaches [2, 7, 18, 20] directly modify the features of the target image and can be well adapted to the variation of the source face. The open-source algorithm [7] is able to generate face swapping results between two specific identities, but lacks the ability for generalization. The GAN-based work [2] combines the source’s identity and the target’s attributes at the feature level and extends the application to arbitrary identity. A recent work [20] utilizes a two-stage framework and achieves high fidelity results. However, these methods focus too much on identity modification. They apply weak constrain on attribute preservation and often encounter mismatch in expression or posture. To overcome the defects in generalization and attribute preservation, we propose an efficient face swapping framework, called SimSwap. We analyze the architecture of an identity-specific face swapping algorithm [7] and find out the lack of generalization is caused by the integration of identity information into the Decoder so the Decoder can be only applied to one specific identity. To avoid such integration, we present the ID Injection Module. Our module conducts modifications on the features of the target image by embedding the identity information of the source face, so the relevance between identity information and the weights of Decoder can be removed and our architecture can be applied to arbitrary identities. Furthermore, identity and attribute information are highly coupled at feature level. A direct modification on the whole features will lead to a decrease in attribute performance and we need to use training losses to alleviate the effect. While explicitly constraining each attribute of the result image to match that of the target image is too complicated, we propose the Weak Feature Matching Loss. Our Weak Feature Matching Loss aligns the generated result with the input target at high semantic level and implicitly helps our architecture to preserve the target’s attributes. By using this term, our SimSwap is capable of achieving competitive identity performance while possessing a better attribute preservation skill than previous state-of-the-art methods. Extensive experiments demonstrate the generalization and effectiveness of our algorithm.
