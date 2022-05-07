## DeepFaceLab: Integrated, flexible and extensible face-swapping framework

## Abstract
딥페이크 방어는 탐지 연구뿐만 아니라 발생 방법의 노력도 필요하다. 그러나 현재의 딥페이크 방식은 불분명한 워크플로우와 저조한 성능의 영향을 받는다. 이 문제를 해결하기 위해, 우리는 페이스 스왑을 위한 현재 지배적인 딥 페이크 프레임워크인 DeepFaceLab을 제시한다. 필요한 도구와 사용하기 쉬운 방법으로 고품질의 페이스 스와핑을 할 수 있습니다. 또한 복잡한 complicated boilerplate 코드를 작성하지 않고 파이프라인과 다른 기능을 강화해야 하는 사용자를 위해 유연하고 느슨한 결합 구조를 제공합니다. DeepFaceLab의 구현을 추진하는 원리에 대해 자세히 설명하고 파이프라인을 소개합니다. 파이프라인의 모든 측면을 사용자가 쉽게 수정하여 맞춤형 목적을 달성할 수 있습니다. DeepFaceLab이 높은 fidelity로 영화 품질의 결과를 얻을 수 있었던 것은 주목할 만하다. 우리는 우리의 접근 방식을 다른 페이스 스왑 방법과 비교함으로써 우리 시스템의 장점을 입증한다.

## 1. Introduction
최근 몇 년 동안 딥 러닝이 컴퓨터 비전 영역을 강화한 이후 디지털 이미지, 특히 인물 초상 이미지 조작이 빠르게 개선되어 대부분의 경우 사실적인 결과를 얻었습니다. 
페이스 스와핑은 원본 얼굴을 대상에게 이전하면서 대상자의 얼굴 움직임과 표정 변형을 유지시켜 가짜 콘텐츠를 생성하는 데 있어 눈길을 끄는 작업이다. 
얼굴 조작 기술의 근본적인 동기는 GAN이다. Style에 의해 합성되는 얼굴이 점점 더 많아진다.
GAN, styleGAN2는 점점 더 현실화되고 있으며 인간의 시각 시스템에 대해 완전히 구별할 수 없다. 
GAN 기반의 페이스 스왑 방식으로 합성된 수많은 스푸핑 비디오가 YouTube 및 기타 동영상 웹사이트에 게시되어 있습니다. 
일반 네티즌들이 쉽게 가짜 이미지와 동영상을 만들 수 있게 해주는 ZAO와 FaceApp과 같은 상용 모바일 애플리케이션은 딥페이크라고 불리는 이러한 스와핑 기술의 확산을 크게 촉진한다. 
특히 딥페이크가 잘못된 정보, 조작, 괴롭힘 및 설득의 원천으로 악의적으로 사용될 수 있다는 점에서 이러한 콘텐츠 생성 및 수정 기술은 공개 담론의 질에 영향을 미치고 시민들의 초상권을 침해할 수 있습니다. 
조작 미디어를 특정하는 것은 기술적으로 요구가 높고 빠르게 진화하는 과제이며, 기술 산업 전체 및 그 이상의 분야에서 협업이 필요합니다. 
미디어 위조 방지 연구에 박차를 가하고 위조 얼굴 탐지에 전념하고 있다. DFDC는 페이스북과 마이크로소프트(MS)가 시작한 100만 달러 규모의 대회다. 
강력한 위조 탐지 모델을 교육하려면 고품질의 가짜 데이터가 필요합니다. 우리의 방법으로 생성된 데이터는 DFDC 데이터셋에 포함된다. 
그러나 공격을 받은 후 적발되는 것이 딥페이크의 악의적인 영향을 줄이는 유일한 방법은 아니다. 스푸핑 콘텐츠의 확산을 감지하기에는 항상 너무 늦습니다. 
학계와 일반인 모두에게 딥페이크가 무엇인지, 어떻게 영화 품질의 스왑 비디오가 생성되는지 네티즌들이 알 수 있도록 돕는 것이 훨씬 더 좋습니다. 
옛말에도 있듯이"최고의 수비는 좋은 공격이다" 일반 네티즌들에게 딥페이크의 존재를 깨닫게 하고 소셜네트워크에 게재된 스푸핑 매체에 대한 식별 능력을 강화하는 것이 
스푸핑 매체의 사실 여부를 고민하는 것보다 훨씬 중요하다. 
인간의 시각 체계로는 전혀 구별이 안 돼 GAN 기반의 페이스 스왑 방식으로 합성된 수많은 스푸핑 비디오가 YouTube 및 기타 동영상 웹사이트에 게시되어 있습니다. 
일반 네티즌들이 쉽게 가짜 이미지와 동영상을 만들 수 있게 해주는 ZAO와 FaceApp과 같은 상용 모바일 애플리케이션은 딥페이크라고 불리는 이러한 스와핑 기술의 확산을 크게 촉진한다. 
특히 딥페이크가 잘못된 정보, 조작, 괴롭힘 및 설득의 원천으로 악의적으로 사용될 수 있다는 점에서 이러한 콘텐츠 생성 및 수정 기술은 공개 담론의 질에 영향을 미치고 시민들의 초상권을 침해할 수 있습니다. 
조작 미디어를 특정하는 것은 기술적으로 요구가 높고 빠르게 진화하는 과제이며, 기술 산업 전체 및 그 이상의 분야에서 협업이 필요합니다. 미디어 위조 방지 연구에 박차를 가하고 위조 얼굴 탐지에 전념하고 있다. 
DFDC는 페이스북과 마이크로소프트(MS)가 시작한 100만 달러 규모의 대회다. 
강력한 위조 탐지 모델을 교육하려면 고품질의 가짜 데이터가 필요합니다. 
우리의 방법으로 생성된 데이터는 DFDC 데이터 세트에 포함된다[5]. 
DeepFakes는 2018년 눈동자 움직임, 얼굴 근육 움직임 등 동일한 표정과 함께 소스 인물의 얼굴을 타깃 인물의 얼굴로 대체하는 완벽한 제작 파이프라인을 도입했다. 
하지만, Deep Fakes에 의해 만들어진 결과는 다소 형편없고, 현대 Nirkin 등의 자동 얼굴 교환에 의한 결과도 그렇다. 
얼굴 조작 동영상에 대한 사람들의 인식을 높이고 위조 탐지 연구자들의 편의를 제공하기 위해 엔터테인먼트용 고품질 동영상 제작 및 위조 탐지 개발에 크게 도움이 되는 오픈 소스 딥페이크 프로젝트인 Deepface Lab(DFL)을 설립하였습니다. 고품질 위조 데이터를 제공함으로써요.