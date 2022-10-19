## Abstract
대부분의 현존 FS 방법론은 지루한 네트워크 및 손실항 설계에 집중하지만 여전히 소스와 타겟의 정보 균형을 맞추는데 어려움을 겪고 있으며 결과물들은 artifact가 발생하는 경향이 있다.  
본 연구에서 우리는 간결하고 효과적인 StyleSwap이라는 이름의 프레임워크를 소개한다. 
핵심 아이디어는 StyleGAN2 G 통해 high-fidelity & robust face swapping 부여하도록 하고 G의 이점이 identity 유사도를 최적하기 위해 사용될 수 있도록 하는 것이다.  
우리는 최소의 수정 만으로 StyleGAN2를 이용해 소스와 타겟으로부터 바람직한 정보를 성공적으로 다룰 수 있음을 확인했다.  
ToRGB로부터 영감을 얻어 Swapping-Driven Mask Branch가 정보 blending을 더욱 향상하도록 고안되었다.  
추가로 StyleGAN inversio의 이점이 채택될 수 있다. 
부분적으로 Swapping-Guided ID Inversion 전략은 ID 유사도를 최적화하도록 고안된다.  
