CCN
충분히 학습된 모델로 부터 transfer learning을 수행하여 (몇개의 샘플이 가지는 편향된 분포)를 calibrate한다.
StyleGAN2와 inversion방법의 결합이 필요한 기존 방법과는 달리 
향상된 content symmetry를 가진채로 target domain을 재건하기 위해 StyleGAN2의 강력한 사전 능력을 이용한다.

1. Dt를 이용해 생성 결과가 target domain에 속하도록 하고
2. ArcFace를 통해 xt와 xs의 identity 유사도가 가깝도록 학습된다.

추론 시에는 Gs의 앞부분 k 레이어의 weight를 사용한다.

TTN
Learns cross-domain correspondense between calibrated domains.
Because CCN learns global mapping, it only make roughly aligned pairs and cannot preserves content details
Further CCN cannot manage to transfer style for arbitrary input image without inversion method.
Sufficient for texture information / but inaccurate  for texture mapping
(그럴듯 하지만 fidelity가 떨어진다는 의미로 해석됨)
Global domain mapping —> Local texture transformation: Fine-grained texture mapping in the pixel level

*
To get away from overfitting, do not align xs and xt pair but train unsupervised manner.
1. Multi-representation constraints Representation decomposition: Learning to Cartoonize Using White-Box Cartoon Representations 1) Lsty(style loss) :  Distance between the style representation distributions of (real stylized images) and (generated images) + uses texture and surface decomposition and 2) Ds to synthesize xg in the similar style of xt~ 2) Lcon(content loss): L1 between xg and xs~ in the VGG feature space

2. Facial perception constraints : use expression regressor to get exaggerated structural deformation  on the top of feature extractor ef, Rexp uses n(=3) regression heads. * ef uses PatchGAN discriminator architecture  (uses learned regressor to estimate the expression score 

