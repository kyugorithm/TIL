## Abstract
GAN는 학습한 데이터 도메인에서는 사실적인 이미지를 생성할 수 있지만 창조적인 작업을 원하는 사람들은 GAN은 본질적으로는 불가능한 새로운 도메인으로의 이미지 생성을 원한다. 또한 무작위 결과를 순수하게 뽑는것 보다는 어느정도 예술적인 방향을 가지도록 제어 수준을 갖는것이 바람직하다. 해상도에 따라 StyleGAN를 보간하는 방법을 제시하며 이를통해 완전히 새로운 영역에서 이미지를 생성하며 어느정도의 제어가 가능하다.  

## Introduction
고품질 사전 학습모델의 가용성과 함께 StyleGAN 아키텍처의 훈련 안정성 덕분에 크리에이터와 아티스트는 전이 학습을 사용하여 제한된 컴퓨팅 리소스에만 액세스하여 고품질 생성 모델을 생성할 수 있게 되었다. Transfer learning으로 생성된 모델과 원래의 "base model"은 밀접한 관계를 가지며, 이러한 두 생성 모델의 가중치를 선형적으로 보간하면 학습된 두 영역을 거의 보간한 것과 같은 출력이 생성되는 것으로 나타났다(EsrGAN). 모델 파라미터 간에 선형 보간을 적용하는 것만으로는 StyleGAN에서 매우 중요한 제어 요소, 즉 모델의 서로 다른 해상도 레이어가 생성된 이미지의 서로 다른 특징(예: 저해상도는 헤드 포즈 제어, 고해상도는 조명 제어)을 담당한다는 점을 활용하지 못한다. 서로 다른 모델의 파라미터를 보간하되 특정 레이어의 해상도에 따라 보간을 수행하면 원하는 대로 여러 G의 feature를 선택하고 블렌딩할 수 있다.  
예를 들어 그림 1과 같이 우키요에 스타일(혹은 실제 인물)의 인물 사진에서 포즈와 머리 모양을 가져와도 사실적 렌더링을 유지한다.  

![image](https://github.com/kyugorithm/TIL/assets/40943064/042aa201-be6b-4644-a4ef-0c4e734daaba)



이 방법론은 사전 훈련된 기본 모델(Base model)과 이를 새로운 데이터셋으로 전이 학습하여 생성된 모델(Transferred model)을 결합하는 과정을 포함한다:

1) 기본 모델 구축(가중치: p_base): 사전 학습 모델을 시작점으로 한다.  
2) 전이 학습 모델 생성(가중치: p_transfer): 기본 모델을 새로운 데이터셋에 transfer learning을 수행한다.  
3) 가중치의 조합: 원래 모델과 새로운 모델의 가중치를 새로운 가중치 세트 p_interp로 결합한다. 두 모델 간 가중치를 결합하는 함수는 결합되는 conv. 레이어의 해상도 r에 따라 달라져야 한다. 여기에서는 각 모델의 가중치 중 하나를 선택하는 단순한 이진 선택 방법을 사용하는데, 이를 'layer swapping'이라고 한다.  
  
p_interp = (1-α)p_base + αp_transfer.  

여기서 α는 다음과 같다:  
α = 1 (r <= r_swap), 0 (r > r_swap)  
r_swap은 한 모델에서 다른 모델로 전환되는 해상도 수준을 나타낸다.  
4) 새로운 모델 생성: 새로 결합된 가중치 p_interp를 사용하여 보간된 모델을 생성한다.  
이 방법은 기존 모델과 새로운 데이터셋으로 두 모델의 특성을 조화롭게 결합하여 새로운 모델을 만드는 데 초점을 맞춘다.  

## 3. Results - Toonification

Cartoon 캐릭터의 구조적 특징을 가진 사실적인 얼굴 생성을 위한 해상도 의존적 보간을 실험한다. 고해상도 레이어의 FFHQ 모델과 애니메이션 캐릭터 얼굴로 전이된 모델의 저해상도 레이어를 결합한다. 이렇게 하면 만화적인 구조적 특징(예: 큰 눈, 작은 턱)을 가진 사실적인 얼굴 텍스처가 나타난다. 같은 잠재 벡터를 입력으로 주면, 기본 모델과 보간된 모델은 ID가 비슷한 넓은 특징을 가진 얼굴을 생성한다. 그 다음에 inversion encoder를 사용해서 w를 보간된 모델 입력으로 주어 원래 이미지의 "Toonified" 버전을 만들 수 있다(그림3).  
![image](https://github.com/kyugorithm/TIL/assets/40943064/92631b2a-d937-4acb-b042-d47fd23ba59d)

## Model Interpolation

모델 보간을 할 때 우리는 StyleGAN을 그 시점에 네트워크를 통과하는 활성화의 spatial resolution에 따라 layer set로 나눈다. 이것들은 StyleGAN에서 제시된 FFHQ 모델에서 4x4부터 1024x1024까지의 범위를 가진다. 매핑 네트워크에서 해상도에 의존하지 않는 학습 가능한 파라미터도 포함한다. 이 연구에서 우리는 매핑 네트워크의 파라미터를 기본 모델의 것과 동일하게 유지하기로 선택한다. 우리는 전이학습된 네트워크의 파라미터를 이 레이어들에 사용하는 것이 실제로는 거의 차이가 없다는 것을 발견했다. 이는 두 네트워크 간 매핑 레이어의 가중치 차이가 이 레이어들의 감소된 학습률로 인해 매우 작기 때문이다.