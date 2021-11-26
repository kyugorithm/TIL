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
Face swapping은 target attribute(표정, 자세, 조명)는 보존하면서 source ID를 전달하는 유망한 기술이다.  
이 기술은 존재하지 않는 twin을 생성하는 영화산업에서 광범위하게 사용된다.  
산업에서의 face swapping 방식은 배우의 얼굴모델을 재현하기 위한 최신 장비를 이용하고  
대부분의 사람이 접근할 수 없는 장면의 조명조건을 재구성한다.  
최근, 최신 장비 없이 face swapping을 수행하는 방식은 연구자들의 관심을 끌어왔다.  

face swapping에서 고려되는 주요 어려움들은 다음과 같다.  
1) 강력한 일반화 능력을 가진 페이스 스왑 프레임워크를 임의의 페이스에 맞게 조정해야 한다.  
2) 결과 face의 ID는 source의 것과 가까워야 한다.  
3) 결과 face의 attribute(표정, 자세, 조명)는 target의 것과 가까워야 한다.  

swapping 방법은 주로 두가지로 나뉜다. 
1) Source-oriented : image level로 source에서 작업  
2) Target-oriented : feature level로 target에서 작업  

Source-oriented methods transfer attributes(like expression and posture) from the target face to the source face and then blend the source face into the target image. 
These methods are sensitive to the posture and lighting of the source image and are not able to reproduce the target’s expression accurately. 
Targetoriented approaches [2, 7, 18, 20] directly modify the features of the target image and can be well adapted to the variation of the source face. 
The open-source algorithm [7] is able to generate face swapping results between two specific identities, but lacks the ability for generalization.
The GAN-based work [2] combines the source’s identity and the target’s attributes at the feature level and extends the application to arbitrary identity.
A recent work [20] utilizes a two-stage framework and achieves high fidelity results. However, these methods focus too much on identity modification.
They apply weak constrain on attribute preservation and often encounter mismatch in expression or posture. 
To overcome the defects in generalization and attribute preservation, we propose an efficient face swapping framework, called SimSwap.
We analyze the architecture of an identity-specific face swapping algorithm [7] and find out the lack of generalization is caused by 
the integration of identity information into the Decoder so the Decoder can be only applied to one specific identity. 
To avoid such integration, we present the ID Injection Module.
Our module conducts modifications on the features of the target image by embedding the identity information of the source face, 
so the relevance between identity information and the weights of Decoder can be removed and our architecture can be applied to arbitrary identities. 
Furthermore, identity and attribute information are highly coupled at feature level.
A direct modification on the whole features will lead to a decrease in attribute performance and we need to use training losses to alleviate the effect. 
While explicitly constraining each attribute of the result image to match that of the target image is too complicated, we propose the Weak Feature Matching Loss.
Our Weak Feature Matching Loss aligns the generated result with the input target at high semantic level and implicitly helps our architecture
to preserve the target’s attributes. By using this term, our SimSwap is capable of achieving competitive identity performance 
while possessing a better attribute preservation skill than previous state-of-the-art methods. Extensive experiments demonstrate 
the generalization and effectiveness of our algorithm.
