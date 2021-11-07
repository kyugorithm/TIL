# Arbitrary Style Transfer in Real-time with Adaptive Instance Normalization

## Abstract
기존의 style tranfter 방법론은 2가지 한계를 가진다.  
1. 느린 최적화 프로세스로 인한 사용성 제약 (Gatys.)  
2. 단일의 style 표현 학습 : 고정 스타일에 제한되며 새로운 style 반영이 어려움  

본 논문은 문제를 아래 개념을 도입하여 해결한다.  
'Adaptive instance normalziation layer' : style feature의 평균분산으로 content의 평균분산을 align  

이로써 새로운 style에 대한 적응없이 실시간으로 처리가 가능하며 단일 feedforward NN을 통해 아래 요소를 지원한다.  
1) content/style trade-off  
2) style 보간  
3) 색상 및 공간 제어와 같은 유연한 사용자 제어  


## 1. Introduction 

**style transfer 방법론의 한계**  
Gatys는 유연한 style transfer 방법론을 제시하였다.  
DNN을 통해 content와 style을 분리하여 encoding 하는 방법을 보여주었고 content를 유지하고 style을 변경할 수 있다.  
임의의 이미지의 content과 style을 결합할 수 있을 정도로 유연하지만 최적화 프로세스로 인해 엄청나게 느리다.  
이후 neural style 전달을 가속화하기 위해 많은 연구가 진행되어왔다.  
보통의 방법은 단일 forward 방향의 stylization을 수행하는 feedforward 방법은 단일 style만 반영할 수 있다는 제한이 있다.  
최근 연구도 style의 유한 집합으로 제한되어 있거나 단일 style 전송 방법보다 훨씬 느리다.  

**해결책**  
위의 **유연성-속도 딜레마**를 해결하는 최초의 neural style  transfer 알고리즘을 제시한다.  
최적화 기반 프레임워크의 유연성과 가장 빠른 feedforward 방식과 유사한 속도를 결합하여  
임의의 새로운 style을 실시간으로 전송할 수 있다.  
본 방법은 feedforward style 전송에 놀라울 정도로 효과적인 인스턴스 정규화(IN) [52, 11] 레이어에서 영감을 받았다.  
IN의 성공을 설명하기 위해 IN이 이미지의 style 정보를 전달하는 것으로 밝혀진 특징 통계를 정규화하여  
style 정규화를 수행한다는 새로운 해석을 제안한다.  
이에 영감을 받아 IN에 대한 간단한 확장, 적응형 인스턴스 정규화(AdaIN)를 도입한다.  
content 입력과 style 입력이 주어지면 AdaIN은 단순히 content 입력의 평균과 분산을 style 입력과 일치하도록 조정한다.  
실험을 통해 AdaIN이 feature 통계를 전송하여 전자와 style의 content를 효과적으로 결합함을 발견했다.  
그런 다음 decoder는 AdaIN 출력을 다시 이미지 공간으로 반전하여 최종 style화된 이미지를 생성하도록 학습된다.  
본 방법은 입력을 임의의 새 style로 전송하는 유연성을 희생하지 않으면서 [16]보다 거의 3배나 빠르다.  
또한 학습 프로세스를 수정하지 않고도 런타임에 풍부한 사용자 제어를 제공한다.
