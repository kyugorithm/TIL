# FSGAN: Subject Agnostic Face Swapping and Reenac

Created: 2022년 1월 2일 오후 8:05
Property: 2022년 1월 3일
Property 1: 이규철
Tags: 3Dface, Synthesis

![Untitled](https://user-images.githubusercontent.com/40943064/148788039-f18ac0c4-8850-47fe-b25e-52361ff6b4c0.png)
의문사항  
1) perceptual loss는 high-frequency 관련 loss이다? -> high-level feature loss 이다.
2) perceptual loss에 l2가 아닌 l1을 사용한 이유가 무엇인지? 

## Abstract

---

**Functional Novelty**

1. **Reenactment →** **Swapping** 순서로 pipeline을 구성하여 두 가지 task 모두 가능
2. 특정 얼굴에 대해 학습 없이 임의 얼굴에 대해 **Swapping** 가능

### **Methodological Novelty**

1. RNN 활용 **단일 이미지 혹은 단일 비디오 sequence**에 대한 Reenactment(**자세, 표정)**
(landmark 필요)
2. **Video Sequences 사용 시 interpolation**(**reenactment, Delaunay triangulation, 무게중심**)을 통해  ****더 나은 결과 획득
3. face completion network(in-paint network)를 통해 Occluded 영역  처리
4. 얼굴 색상이나 조명 조건을 보존하기 위해 Perceptual loss에 Poisson blending loss(Poisson optimization)를  추가한 blending network 활용

**Keyword : RNN using reenactment, interpolation, in-painting NN, Poisson blending**

## 5. **Experiment Results**

---

### **1) Qualitative face reenactment results**

- 제안한 기본 방법론을 이용해 얻은 결과
- 일반적인 정성적 결과  : 4번째 열의 극단적 차이(Pose와 Expression이 매우 큼)에도 대응가능
- Yaw 크기에 따른 결과  : 큰 angle 변화에 대해 iterative 방식으로 접근하면 ID와 texture가 더 잘 보존 (의견 : 큰 차이는 없어 보임)

![Untitled 1](https://user-images.githubusercontent.com/40943064/148788056-0835b479-9d08-4d3c-8efc-0f7dc083a488.png)

### 2) **Qualitative face swapping results**

실험데이터 : FaceForensics++

다양한 표정, 얼굴, occlusion 케이스 사용 [35]와 대등한 비교를 위해 target과 가장 유사한 자세의 source 선택( KC 이해안됨)

![Untitled 2](https://user-images.githubusercontent.com/40943064/148788077-06cadd71-3f5d-4ed2-9ea4-7b5ab6060f09.png)

### **3) Comparison to Face2Face**

Face2Face와 동일하게 입만 전송하는 문제로 정의 Face2Face는 전반적으로 artifact가 나타나며 target 입 모양을 잘 표현하지 못함

![Untitled 3](https://user-images.githubusercontent.com/40943064/148788086-6843f5d3-48ca-42c7-a16c-653199262d14.png)

### **4) Quantitative results**

source의 ID 보존 & target의 자세/표정 반영 1, 2) 품질  비교    : ID, SSIM(dlib 얼굴인식/탐지등 관련 라이브러리) (ID : Face Recognition 모델을 통과한 값의 차이로 계산할 듯) (SSIM : 우리눈은 artifact를 잘 발견하지만 SSIM은 제대로 반영하지 못해서 수치의 차이가 발견되지 않음)

3) 자세 정확도 : Euler angle의 유클리드 거리 ; 단위 degree(Fb vs It) 4) 표정 정확도 : 2D landmark 유클리드 거리; 단위 pixel (Fb vs It) (FaceForensics++에서 500개의 비디오의 첫 100개 프레임 관측값에 대한 평균과 분산 추출)  ID와 SSIM읜 유사하지만 자세와 표정이 잘 반영

(규철 : SSIM이 알맞은 performance measure인가?)

![Untitled 4](https://user-images.githubusercontent.com/40943064/148788099-1d83f94f-4311-43a7-9f8d-3ccf8249c959.png)

### **5) Ablation Study**

아래 4가지 케이스 비교 
(Gs는 고정 사용)

모든 경우 ID 동일 

자세와 표정에서 가장 성능이 좋음

SSIM 성능 하락 : 추가 네트워크와 처리단계가 추가가 원인

![Untitled 5](https://user-images.githubusercontent.com/40943064/148788109-f699bf50-f696-4762-aa9e-c90175ac4f44.png)

## 6. Conclusion

---

### **Limitations.**

1) iteration을 많이 분할 하면 texture blur가 심해짐

2) 아래 그림에서 보는 것과 같이 포즈의 차이가 커질 수록 ID와 texture 품질이 저하됨

3) Face2Face 처럼 이미지로부터 texture를 warp하는 3DMM 기반 방법과 달리 본 방식은 학습데이터 해상도의 한계에 품질이 제한됨

4) Landmark를 사용하기 때문에 landmark 가 sparse한 경우 복잡한 표정을 잘 따라가지 못할 수 있음
