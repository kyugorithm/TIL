# FaceShifter: Towards High Fidelity And Occlusion Aware Face Swapping

## Abstract
FaceShifter는 높은 충실도와 함께 occlusion을 고려하여 face swapping 하는 두 단계로 구성된 framework이다. Swap된 얼굴을 합성할 때 target 이미지로부터 제한된 정보만을 이용하는 여러 face swapping 방식과는 달리 
본 방식은, 첫단계로 target attribute를 이용하고 통합하여 완전히 적응적으로 충실도 높은 swapped face를 생성한다. 본 연구에서 다음 두가지를 제안한다.  
1) multi-level의 target 얼굴 attribute를 추출하기 위한 새로운 attribute encoder
2) 얼굴 합성을 위한 ID와 attribute를 적응적으로 통합하기 위해 신중하게 설계된 AAD(Adaptive Attentional Denormalization) 레이어가 있는 새로운 G  

까다로운 얼굴의 occlusion을 다루기 위해 두단계를 구성하는 새로운 Heuristic Error Acknowledging Refinement Network (HEAR-Net)을 추가한다. 수동 주석 없이 self-supervised 방식으로 이상 영역을 복구하도록 학습한다. Wild face에 대한 광범위한 실험은 우리의 얼굴 교환 결과가 SOTA와 비교하여 훨씬 더 지각적으로 매력적일 뿐만 아니라 더 나은 ID 보존을 보여준다.
