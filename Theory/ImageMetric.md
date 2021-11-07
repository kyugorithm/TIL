## 1. PSNR : Peak Signal-to-noise ratio
**신호가 가질 수 있는 최대 전력**에 대한 **잡음의 전력** : 영상/동영상 손실 압축에서 화질 손실 정보를 평가할때 사용  
신호의 전력에 대한 고려 없이 평균 제곱 오차(MSE)를 이용해서 계산
  
![image](https://user-images.githubusercontent.com/40943064/140645154-d0ac01fe-68f7-4c83-88ed-eb9fdece4043.png)  
  
MAX_I = 채널의 최대값 - 최솟값 (e.x., 8bit gray scale : 255 (255 - 0))

Log scale이기 때문에 단위는 db이다.  
손실이 적을수록 높은 값을 가지며 무손실 영상의 경우에는 MSE가 0이기 때문에 PSNR은 정의되지 않는다.  

## 2. SSIM : Structural Similarity Indexed Measure  
영상/동영상에 대한 지각적 품질 측정방식  
(이미지 품질저하 == 구조적 정보의 지각 변화)로 간주하는 인식 기반 모델이며  
**luminance masking** 및 **constrast masking** 항을 포함한 중요한 **perceptual phenomenon**을 통합한다.  
MSE 또는 PSNR과 다른 점은 **절대적인 에러를 추정**한다는 것이다.  
구조 정보는 특히 픽셀이 공간적으로 가까울 때 강력한 상호 의존성을 가지고 있다는 개념이다.  
이러한 종속성은 시각적 장면에서 **물체의 구조에 대한 중요한 정보**를 전달한다.  
Luminance masking : 밝은 영역에서 이미지 왜곡(이러한 맥락에서)이 덜 보이는 경향이 있는 현상  
Contrast masking : 이미지에 중요한 활동이나 "혼합물"이 있을 때 왜곡이 덜 보이는 현상이다.  
  
**_SSIM의 핵심 가설_**  
인간의 시각은 구조적 정보 추론에 특화되었기 때문에 구조의 왜곡 정도가 지각적 품질 인식에 큰 영향을 준다.  


![image](https://user-images.githubusercontent.com/40943064/140647689-e17998b4-a3b8-45b9-89be-5062c507dc81.png)  
  
![image](https://user-images.githubusercontent.com/40943064/140647698-2c117439-9dfb-4c5a-9300-da77c9b46420.png)  

_**논문**_   
저자 : Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli.   
제목 : Image quality assessment: from error visibility to structural similarity  

## MS-SSIM : Multiscale SSIM  
초기 vision 시스템의 multi-scale 처리를 연상시키는 서브샘플링의 여러 단계의 과정을 통해 여러 척도에 걸쳐 수행된다.  
다른 주관적 이미지와 비디오 DB에서 SSIM보다 성능이 동등하거나 우수한 것으로 나타났다.
MS-SSIM은 SSIM에 스케일 스페이스의 개념을 추가시킨 것이다.  
여러 스케일에서 SSIM 점수를 산출한 다음에 가중곱으로 최종 스코어를 얻는다.  
![image](https://user-images.githubusercontent.com/40943064/140648116-8862d947-4d63-42cf-87eb-530ece3df694.png)


설명참조 : https://bskyvision.com/396  
