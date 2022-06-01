# Abstract
FOV(field-of-view)가 넓은 사진은 distortion이 강하게 발생한다.  
이를 전문가의 manual한 수정이 아닌 알고리즘 접근을 통해 해결한다.  
알고리즘은 다른 부분은 왜곡하지 않고 되돌려야하는 얼굴만 수정하도록 한다.  
최적화 문제를 구성하여 얼굴 부위의 stereographic projection에 로컬하게 적응하고 배경을 통한 perspective projection으로 seamlessly evolve 하는 content-aware warping mesh를 생성한다.  
제안하는 새로운 energy function은 효과적으로 작동하며 다양한 사진에 대해 신뢰성 있게 적용된다. 

## Introduction
**문단1. 배경  : 최신 카메라는 많은 object를 담을 수 있음**  
**문단2. 문제점 : 많은 왜곡 발생**  
**문단3. 해결방법 :**  
입력 이미지가 주어지면 대상 마스크를 계산하여 coarse mesh 위에 vertex 별 weight를 할당한다.  
구와 평면 사이의 conformal mapping인 stereographic projection을 국소적으로 emulate 하도록 facial vertex를 encourage하는 energy term을 구성한다.  
방법론의 출력은 stereographic & perspective projections를 단일 이미지에 대해 결합한다.  
제안하는 energy function은 얼굴 경계에서 충돌하는 두개의 projection들 사이에서 부드러운 transition을 장려한다.  
**문단4. 성능검증 : 다양한 이미지에 대해 검증**  

**Contribution**  
왜곡을 자동적으로 해결하는 알고리즘을 제안하며, stereographic & perspective projection을 얼굴과 배경에 대해 통합한다.  

## Related Work


