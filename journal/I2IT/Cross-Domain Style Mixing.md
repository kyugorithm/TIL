## Abstract
이전 방법들은 많은 학습 이미지가 필요하거나 추상적인 cartoon 얼굴을 지원하지 못하는 등 중요한 제약들을 제대로 해결하지 못했다. 최근에 Toonify는 제한된 수의 트레이닝 이미지 사용하도록 개선됐지만 기존의 문제들을 그대로 물려받았기 때문에 여전히 제한된 사용 사례를 가지고 있다.  

### Solution
Cross-Domain Style Mixing(CDSM): 두 가지 다른 domain의 두 가지 latent codde를 결합  
많은 트레이닝 이미지를 사용하지 않고 하나의 G만 사용하면서도 다양한 cartoon 캐릭터 얼굴을 효과적으로 스타일화할 수 있다.  

## 1. Introduction
Cartoongan, U-GAT-IT 같은 I2IT는 주목할 만한 접근법인데, cartoon 이미지가 많이 필요하고 광범위한 GPU 자원을 소모하며 특정한 cartoon 특징을 표현하는 데 종종 부족해서 한계가 있다.

이 문제들을 완화하기 위해,
Toonify는 2개의 StyleGAN을 사용한 레이어 스왑과 수백 개의 트레이닝 이미지를 사용해 학습하는데, 여기서 중요한 품질 문제(세부적으로 표현이 안 되거나 출력 이미지의 일부 색상 왜곡)가 있다. 또한 cartoon domain의 추상화가 클수록(예를 들어, 일본 애니메이션 스타일에서 자주 보이는 것처럼) 더 심해진다.  

### Solution
두 다른 domain의 잠재 코드를 결합한다. 입력된 실제 얼굴(source domain)과 cartoon(target domain) 이미지들에 대한 latent code를 얻고, later swap된 G의 같은 latent space에서 스타일 혼합을 수행한다.  
즉, source/target domain에 대한 latent code를 생성하기 위해 신중한 inversion을 설계한다. source domain에는 사전 학습 인코더(예를 들어, ReStyle)를 사용하고, target domain에는 projection protocol**을 사용한다.(모두 표현력 있는 W+ 공간에서 작업).  
이렇게 해서 latent code를 결합하기에 적합하게 만들고 S(style space) space에서 각 스타일 혼합한다.  

이 방법은 성공적으로 cartoon의 세부적인 특징들을 유지하지만, Tonify의 layer swap에서도 발생하는 문제와 동일하게 출력에서 색상 왜곡이 있다는 걸 발견한다. 분석하면, layer swapped G는 사전 트레이닝된 인코더로부터 입력받은 잠재 코드를 사용할 때 domain 차이 때문에 색상 아티팩트가 있는 이미지를 만들어내는 경향이 있기 때문에 tRGB replacement 방법을 적용한다. 이는 입력 이미지의 스타일 파라미터(s∈S)의 일부를 조작해서, 출력 이미지가 목표 cartoon domain 색상 분포를 따르게 하고, 결국 색상 아티팩트를 성공적으로 제거하게 해준다.  

제안 방법은 품질과 안정성 측면에서 간단하지만 효과적이며 단일 G가 다양한 추상화 수준에서 cartoon 얼굴에 대한 일괄 스타일화를 수행할 수 있게 한다(Figure 1 참고). 이전 방법들은 캐릭터별 “G”를 준비해야 했지만 제안 방법이 character별 “latent”를 활용하기 때문이다. 우리 프레임워크는 추가적인 학습 트릭(예를 들어, 보조 손실이나 정규화 같은)이나 StyleGAN2 G의 미세 조정 외에 다른 아키텍처 조정이 필요하지 않다는 점도 강조한다. 그래서, 학습및 배포에서의 높은 효율성 덕분에 활용성이 높다.

### Contribution

• 다양한 추상적 얼굴과 스타일을 가진 cartoon 스타일화로서 layer swap 방식의 한계 조사  
• cartoon domain에 특화된 단순하지만 고품질 stylization 프레임워크를 제안한다. 최소한의 학습과 데이터셋(<100)만 필요해하며 이때 단일 G가 캐릭터 ID를 바꿔주는 것만으로 여러 cartoon 캐릭터 얼굴을 스타일화할 수 있다.  
• 몇 가지 추가 모듈과 결합하면, 심지어 더 우수한 사진이나 비디오 cartoon화 결과를 제공할 수 있다는 걸 보인다.

## 2. Background
### Portrait Stylization

Neural style transfer 기반 접근법은 사전 트레이닝된 네트워크를 사용해서 이미지 스타일화를 수행하지만 대부분은 얼굴 특징의 기하학적 변형에 한계가 있다(예를 들어 만화나 캐리커처에서의 과장된 표현). 또한 GAN 기반 I2I 패러다임도 이 분야에서 활발히 연구되고 있다. 이 방법들은 매력적인 스타일화 결과를 만들어내지만 표현력의 한계가 있고(한정된 범위의 대상이나 입력 특징만 표현) 많은 수의 학습 이미지에 의존해서 활용이 어려워. 최근에 Toonify는 I2I을 사용하지 않고 앞의 문제를 해결하기 위해 layer swapping 방법을 제안했다. 이 방식은 적은 수의 트레이닝 이미지를 사용하여 그럴듯한 스타일화 결과를 보여주지만, 매우 추상적인 카툰 얼굴의 경우, 세밀한 카툰 텍스처를 표현하는 데 한계가 있고 색상 artifact가 발생해서 활용 가능한 도메인의 한계가 있다. 반면 제안 방법은 다양한 카툰 캐릭터의 세밀한 텍스처와 특징을 성공적으로 생산하면서 불쾌한 색상 아티팩트를 해결한다.  

### GAN inversion
두 가지 접근 방식이 있다.  
1) 최적화 기반: 최적화 알고리즘을 사용해서 합성된 이미지와 타겟 이미지 사이의 손실을 최소화하도록 잠재 코드를 업데이트
2) Encoder 기반: Encoder 네트워크를 사용해서 이미지를 deterministic하게 latent space에 mapping하는 방법이다. 본 논문은 source domain에 ReStyle 인코더를 사용하는데, 이건 W+ space를 사용해서 더 우수한 recon. 및 표현 능력을 가지고 있다.

## 3. Motivation & Pre-analysis
Toonify 방식은 괜찮은 stylization 결과를 얻지만 cartoon domain에 적용하면 두 가지 품질 문제가 있다.  

첫째, layer swapped G는 high-fidelity cartoon characteristic image를 생성하지 못한다.  
StyleGAN2 G가 원래의 W 공간에서 샘플링된 이미지를 만들 때, 이 공간은 학습 이미지에 대한 분포를 나타내기 때문에 높은 fidelity를 가지지만 layer swapped G의 경우, 원래의 W space는 FFHQ fine-tuned G에서 온 low-resolution layer와 mapping network와만 정렬되어 있다. 하지만, 같은 W 공간은 cartoon domain에서 학습된 고해상도 레이어와는 정렬되지 않는다. 따라서 고해상도 레이어에서 합성될 필요가 있는 세밀한 카툰 특징이 부족한 결과가 만들어지고 캐릭터별 ID가 사라진다(Figure 2c).  
<img src = "https://github.com/kyugorithm/TIL/assets/40943064/326bb9ac-1573-4eaa-9d33-dbdede477ad4" width=350>

둘째, 출력 이미지에서 색상 왜곡  
Layer swap 방식은 inversion을 활용하는데 이 때문에 색상에 한정된 예상치 못한 품질 저하를 일으킬 수 있다. 왜냐하면 FFHQ 데이터셋으로 사전 트레이닝된 인코더는 source domain의 색상 범위만 표현하도록 학습되어 있지 target cartoon domain의 색상 범위는 고려하지 못한다(Figure 4a).  
<img src = "https://github.com/kyugorithm/TIL/assets/40943064/220b4477-f826-451a-a98b-7f8bdd0aa549" width=350>


문제를 완화하기 위해, 이전 연구들은 latent-consistent fine-tuning과 VAE 인코더를 사용하거나 layer swapped G를 위해 학습한 encoder를 사용했다. 하지만, 이런 접근법들은 cartoon과 실제 이미지가 많은 특징과 texture를 공유한다고 가정하기 때문에 실제 얼굴과 cartoon 얼굴 사이의 유사성 손실(e.x., perceptual loss)을 강한 정규화로 사용한다. 우리는 이런 정규화가 고도로 추상적이거나 flat한 cartoon 얼굴에 적용되지 않고, 실제 얼굴의 texture와 특징을 과도하게 보존함을 확인했다(Figure 6d 참고).  
![image](https://github.com/kyugorithm/TIL/assets/40943064/efd623fd-890c-4d3f-8a93-c1c15736a592)  

## 4. Method

I2I 방법의 한계를 극복하고 layer swap 방법의 두 가지 주요 문제를 해결하는 새로운 portrait stylization, 즉 CDSM을 제안한다. 이전 방법들과 달리, 단일의 G로 다양한 cartoon 스타일을 표현하기 때문에 실용성이 높다.  
이전 스타일 혼합 방법들(Encoding in style, AgileGAN)은 같은 domain에서 두 개의 잠재 코드를 가져와 사전 학습된 G를 통해 출력을 해석하지만 우리는 서로 다른 domain에 속하는 latent code를 결합하고 layer swap된 G를 사용해서 결과를 해석한다. 이를 위해, 각 domain에 대해 각기의 inversion을 사용하고 S(style) space에서 style mixing을 수행한다. 색상 왜곡 문제를 해결하기 위해 tRGB swapping을 적용한다(Figure 3 참고).  

### 4.1. Framework  
xf(real), xc(대상 cartoon 캐릭터 ID)  
목표: 입력(xf)을 원하는 캐릭터(c)로 스타일화하여 ^xc를 생성  
1) 먼저 layer swap 방법(Toonify)의 G_swap를 구성한다.
2) Cartoon 데이터셋에서 각 캐릭터 ID c에 대해 무작위로 k개의 카툰 이미지 xc_(1, 2,...,k)를 샘플링하고, target domain의 inversion(Invtgt(.))을 사용하여 Gswap의 latent space로 변환하고 이를 평균화 하여 Character ID별 latent code wc를 준비한다.  
3) inference에서, xf는 FFHQ 데이터셋에 학습된 source domain 특정 encoder를 사용하여 latent code wf로 먼저 변환되어, Invsrc(:)로 표시되어 인코더는 wf를 생성하는데, wc는 Gswap을 사용하여 변환되었기 때문에 wc와 같은 잠재 공간에서 생성돼. 따라서 wf와 wc는 domain 차이에도 불구하고 스타일 혼합에 적합해. 마지막으로, 우리는 제안된 크로스-도메인 스타일 혼합 방법(CDSM(:))을 사용하여 출력 ^xc(=Gswap(CDSM(wf;wc;m)))를 생성한다. 

여기서 m은 출력 이미지에서 카툰 스타일의 강도를 결정하는 스타일 혼합 레벨이야. CDSM(:)은 StyleSpace에서의 스타일 혼합 방법 SM(:)과 tRGB 교체 방법 R(:)으로 구성되어 있고 다음과 같이 정의돼:
CDSM(wf;wc;m) = SM(R(sf;sc),sc,m)
sf = A(wf), sc = A(wc)

여기서 A는 StyleGAN2 생성기의 레이어별 affine 레이어를 나타내며, StyleSpace에서 제안된 것처럼 덜 엉킨 스타일 파라미터 s(∈S)를 제공해.

### 4.2. StyleSpace에서의 스타일 혼합
프레임워크에서 StyleSpace에서의 스타일 혼합 방법 SM(:)에 대해 먼저 설명한다. 기존의 SM과 달리, 우리 방법은 두 가지 다른 inversion을 사용한 다음 S 공간에서 스타일 혼합을 수행한다.  

#### Inversion for the natural image.
특히, 프레임워크에서 wf를 얻기 위해 Restyle 인코더를 선택했는데, 이 인코더는 우수한 재구성과 특징 보존으로 알려진 W+ 공간을 기반으로 하고 feed-forward 추론 특성은 많은 실용적인 애플리케이션에 이상적이다. 그러나, 이 인코더를 사용하면, 레이어 스왑된 생성기가 예상치 못하게 색상 왜곡 이미지를 만들어낼 수 있다. 이 문제는 tRGB 교체 방법(Section 4.3)에 의해 완전히 해결되어, 품질 저하 없이 인코더를 견고하게 사용할 수 있도록 한다.  

#### Inversion for the cartoon image.
wc를 생성하는 것은 다른 inversion 방식을 필요로 하다. 먼저, 코드는 모두 look-up table에 저장되어 있고 나중에 원하는 캐릭터 ID로 요청할 때 조회되도록 사전에 처리된다. 둘째, 각 캐릭터 ID에 대해 제한된 수의 학습 이미지만 존재하기 때문에 인코더를 트레이닝하는 것은 단순하지 않다.  
누군가는 StyleGAN2에 대해 높은 충실도를 가진 이미지를 생성하는 직관적인 방법으로 Gswap의 원래 잠재 공간에서 wc를 샘플링하는 경향이 있을 수 있어. 그러나, 우리는 이것이 Gswap에 대해 다르게 동작한다는 것을 발견했다(Figure 2 참고). Gswap의 저해상도 레이어는 cartoon 이미지에 fine-tuned된 고해상도 레이어에 적합하지 않은 자연 얼굴에 대한 feature map을 생성한다는 것을 이해해야 해. 따라서 대신 cartoon 이미지를 반전하고 W+ 공간에서 각 캐릭터 ID별로 평균을 내어 명시적으로 wc를 생성한다(eq 1). 이 연산을 통해 wc는 pose 및 noise 불변성이 높아지며, 이는 다음 style mixing 절차에 바람직한 특성이다.

#### Style mixing.  
주어진 입력 코드 wf와 wc를 섞는다. 이를 위해 affine layer A를 통과시켜 해당 스타일 파라미터 sf, sc를 S 공간에서 얻는다 (Equation 4). 그 다음 sf의 일부를 sc로 tRGB 교체 방법(4.3절에서 논의)을 사용해 바꾼다. 결국 두 세트의 스타일 파라미터, sf와 sc는 S 공간에서 다음과 같이 스타일 믹싱된다.  
SM(sf; sc; m) = {sf_1,...t(m)-1} ∪ {sc_t(m),...26}
여기서 t(m)은 잠재 코드 w(∈W+)의 인덱스를 해당 스타일 파라미터 s ∈ S로 매핑하는 함수야.

### 4.3 tRGB 교체
본 방법에서는 source domain의 encoder가 Gswap의 W+ 공간에 있는 latent code를 생성하도록 설정돼 있어. 우리는 이 공간을 사용하는 것이 색상 왜곡을 일으킬 수 있다고 가정한다. 왜냐하면 원래 W 공간은 색상 아티팩트가 전혀 없는 것으로 나타났거든 (Figure 4b). StyleGAN2에서 tRGB 레이어를 제어하는 스타일 파라미터 stRGB의 일부만 조작하여 이미지의 지역적 또는 전역적인 영역의 색상만 변경할 수 있다고도 제안돼 (24). 이런 맥락에서, 우리는 인코더가 tRGB 레이어에 대해 분포 벗어난 s_tRGB를 생성하며 심각한 색상 왜곡을 일으키는 것을 발견했어 (Figure 4a). 이를 바탕으로, 우리는 색상 왜곡의 원인을 style parameter에 국한시키고, 출력 이미지의 색상 분포를 변경하기 위해 오직 s_tRGB만 조작하는 tRGB 교체 방법을 개발했어. 구체적으로, 자연스러운 얼굴 이미지 sf의 tRGB 스타일 파라미터 부분 sf tRGB은 대상 카툰 캐릭터 sc의 tRGB 부분 sc tRGB으로 교체되어, sf가 대상 캐릭터 이미지의 색상 분포를 나타내는 tRGB 부분을 가지도록 해 (Figure 3). 우리는 이 방법이 색상 왜곡 문제를 해결할 뿐만 아니라 (Figure 7b), 스타일 믹싱 구성 요소와 함께 적용될 때 캐릭터 특정 세밀한 특징을 전달하는 데도 도움이 된다는 것을 보여줘 (Figure 5).

## 5. 실험 & 응용
FFHQ 사전 학습된 StyleGAN2를 ADA와 함께 기본 설정을 사용하여 카툰 dataset에서 fine-tuning한다(스타일 믹싱 확률은 0으로 설정). Fine-tuned된 generator는 FFHQ 사전 학습된 generator와 32x32 해상도에서 layer-swapped 한다. 기본적으로 스타일 믹싱 레벨 m은 6으로 설정한다. 캐릭터별 ID에 대해 우리는 훈련 dataset에서 무작위로 k = 50 이미지를 샘플링하고 이들을 W+ 공간에 invert하여 캐릭터 ID별 latent code wc를 준비했어.





