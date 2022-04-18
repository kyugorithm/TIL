# FaceShifter: Towards High Fidelity And Occlusion Aware Face Swapping

## Abstract
FaceShifter는 높은 충실도와 함께 occlusion을 고려하여 face swapping 하는 두 단계로 구성된 framework이다. Swap된 얼굴을 합성할 때 target 이미지로부터 제한된 정보만을 이용하는 여러 face swapping 방식과는 달리 target attribute를 이용하고 통합하여 완전히 적응적으로 충실도 높은 swapped face를 생성한다.  
다음 두가지를 제안한다.  
1) Attribute encoder : Multi-level의 target 얼굴 attribute를 추출하기 위한 새로운 
2) Generator : 얼굴 합성을 위한 ID와 attribute를 적응적으로 통합하기 위해 신중하게 설계된 AAD(Adaptive Attentional Denormalization) 레이어로 구성

또한, 까다로운 얼굴 occlusion을 다루기 위해 두단계를 구성하는 새로운 Heuristic Error Acknowledging Refinement Network (HEAR-Net)을 추가한다. Annotation 없이 self-supervised 방식으로 이상 영역을 복구하도록 학습한다. Wild face에 대한 광범위한 실험은 우리의 얼굴 교환 결과가 SOTA와 비교하여 훨씬 더 지각적으로 매력적일 뿐만 아니라 더 나은 ID 보존을 보여준다.  

## 1. Introduction
Faceswap 설명 > Faceswap의 활용 > Faceswap 기술에서 어려운 점 > 

1) Replacement 기반 : 얼굴 내부 픽셀만 대체하여 pose/perspective 변화에 민감
2) 3D 기반 : pose/perspective 차이를 다루기 위해 3D 모델을 사용 했지만 3D reconstruction의 정확성과 견고성은 부족
3) GAN 기반 : 성능은 상대적으로 향상되었으나 현실적인 결과와 높은 충실도의 결과를 모두 합성하는 것은 여전히 어려움  
본저는 결과의 **충실도** 향상에 데 중점을 둔다. 지각적으로 매력적으로 만들기 위해서 합성이 target의 **포즈/표정**을 공유할 뿐만 아니라 촘촘하게 target 이미지에 원활하게 맞아야 한다. 렌더링은 target scence의 조명(방향, 강도, 색상)에 충실해야 하며, 픽셀 해상도는 target 이미지 해상도와 일치해야 한다. 이 두 가지 모두 단순한 alpha 또는 Poisson blending으로는 잘 처리되지 않는다. 대신, 조명 또는 이미지 해상도를 포함한 target 이미지의 attr.를 스왑된 얼굴을 보다 사실적으로 만드는 데 도움이 될 수 있도록 스왑된 얼굴의 합성 중에 target 이미지 attr.의 철저하고 적응적인 통합이 필요하다. 그러나 이전의 얼굴 교환 방법은 이 통합의 요구 사항을 무시하거나 철저하고 적응적인 방식으로 수행할 수 있는 능력이 부족하다.  

(FSGAN) 기존의 방법들은 target 이미지의 포즈 및 표현 지침만 사용하여 스왑된 얼굴을 합성하고, 이후 target 얼굴의 마스크를 사용하여 target 이미지에 얼굴을 혼합한다. 이 프로세스는 아래 이유로 아티팩트를 일으키기 쉽다.  
1) 포즈나 표정 이외에 target 이미지에 대한 정보를 합성 시에 활용하지 않기 때문에 장면 조명이나 이미지 해상도와 같은 target의 attr.을 반영하기 어렵다.  
2) 이러한 blending은 모든 src.의 주변지역을 버린다. 그러므로 이러한 방법론들은 src. 정체성에 대한 얼굴 형태를 보존하지 못한다.  
Fig.2에 전형적인 실패 케이스들을 보인다.
![image](https://user-images.githubusercontent.com/40943064/163660709-a62a5a6b-3c3b-4e17-8acc-a4a64ba582ff.png)

높은 충실도의 얼굴 교환 결과를 달성하기 위해, 프레임워크의 첫 번째 단계에서는 target attr.의 철저하고 적응적인 통합을 위해 적응형 임베딩 통합 네트워크(AEI-Net)라는 GAN 기반 네트워크를 설계한다. 
다음고 같이 네트워크 구조를 두 가지 개선했다.
1) Attr. encoder : RSGAN/IPGAN으로 단일 벡터로 압축하는 대신 다양한 공간 해상도에서 target attr.을 추출하기 위한 새로운 다단계 구조
2) Generator : attr.이나 id 임베딩을 통합할 위치를 적응적으로 학습하는 신중하게 설계된 Adaptive Attentional Denormalization(AAD) 레이어 구조

이러한 적응형 통합은 RSGAN, FSNet 및 IPGAN에서 사용하는 단일 수준 통합보다 상당한 개선을 가져온다. 이 두 가지 개선으로 제안된 AEI-Net은 그림 2와 같이 조도와 얼굴 모양이 일정하지 않은 문제를 해결할 수 있다. 또한 얼굴 교환에서 얼굴 폐색을 처리하는 것은 항상 어렵다. 폐색 인식 안면 마스크를 얻기 위해 얼굴 분할을 훈련하는 Nirkin과 달리, 우리의 방법은 수동 주석 없이 자체 감독 방식으로 얼굴 이상 영역을 복구하는 방법을 배울 수 있다. 잘 학습된 AEI-Net에 대상 및 소스와 동일한 얼굴 이미지를 제공할 때 재구성된 얼굴 이미지가 여러 영역의 입력에서 벗어난다는 것을 관찰한다. 이러한 편차는 얼굴 폐색 위치를 강하게 암시한다. 따라서, 재구성 오류의 guide에 따라 결과를 더욱 세분화하기 위해 새로운 Heuristic Error Acknowledging Refinement Network(HEAR-Net)를 제안한다. 제안된 방법은 더 일반적이므로 안경, 그림자 및 반사 효과, 기타 흔치 않은 폐색 등과 같은 더 많은 이상 유형을 식별한다. 제안된 2단계 얼굴 교환 프레임워크인 FaceShifter는 주제에 구애받지 않는다. 일단 훈련되면, 이 모델은 딥페이크 및 코르슈노바와 같은 주제별 훈련 없이 모든 새로운 얼굴 쌍에 적용될 수 있다. 실험은 우리의 방법이 다른 최첨단 방법에 비해 상당히 현실적이고 입력에 충실한 결과를 달성한다는 것을 보여준다.

## 2. Related Works
Face swapping ㅇ
이러한 적응형 통합은 RSGAN, FSNet 및 IPGAN에서 사용하는 단일 수준 통합보다 상당한 개선을 가져온다. 이 두 가지 개선으로 제안된 AEI-Net은 그림 2와 같이 조도와 얼굴 모양이 일정하지 않은 문제를 해결할 수 있다. 또한 얼굴 교환에서 얼굴 폐색을 처리하는 것은 항상 어렵다. 폐색 인식 안면 마스크를 얻기 위해 얼굴 분할을 훈련하는 Nirkin과 달리, 우리의 방법은 수동 주석 없이 자체 감독 방식으로 얼굴 이상 영역을 복구하는 방법을 배울 수 있다. 잘 학습된 AEI-Net에 대상 및 소스와 동일한 얼굴 이미지를 제공할 때 재구성된 얼굴 이미지가 여러 영역의 입력에서 벗어난다는 것을 관찰한다. 이러한 편차는 얼굴 폐색 위치를 강하게 암시한다. 따라서, 재구성 오류의 guide에 따라 결과를 더욱 세분화하기 위해 새로운 Heuristic Error Acknowledging Refinement Network(HEAR-Net)를 제안한다. 제안된 방법은 더 일반적이므로 안경, 그림자 및 반사 효과, 기타 흔치 않은 폐색 등과 같은 더 많은 이상 유형을 식별한다. 제안된 2단계 얼굴 교환 프레임워크인 FaceShifter는 주제에 구애받지 않는다. 일단 훈련되면, 이 모델은 딥페이크 및 코르슈노바와 같은 주제별 훈련 없이 모든 새로운 얼굴 쌍에 적용될 수 있다. 실험은 우리의 방법이 다른 최첨단 방법에 비해 상당히 현실적이고 입력에 충실한 결과를 달성한다는 것을 보여준다.
