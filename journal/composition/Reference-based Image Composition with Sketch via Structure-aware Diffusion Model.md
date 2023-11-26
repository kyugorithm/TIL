# Reference-based Image Composition with Sketch via Structure-aware Diffusion Model

## Abstract
최근 대규모 텍스트-이미지 생성 모델의 주목할만한 개선은 고화질 이미지 생성에서 유망한 결과를 보여주었습니다. 편집성을 강화하고 세밀한 생성을 가능하게 하기 위해, 참조 이미지와 함께 sketch를 새로운 모달로 결합하는 "multi-input-conditioned image composition model"을 소개합니다. Sketch를 사용한 에지 수준 제어 덕분에, 우리의 방법은 사용자가 원하는 구조(즉, sketch)와 내용(즉, 참조 이미지)을 가진 이미지의 하위 부분을 편집하거나 완성할 수 있게 해줍니다. 우리의 프레임워크는 참조 이미지를 사용하여 누락된 영역을 완성하는 동시에 sketch 가이드를 유지하는 사전 훈련된 diffusion model을 미세 조정합니다.

## Introduction

### 1. Diffusion 모델을 활용한 텍스트-이미지 생성의 발전
최근 대규모 텍스트-이미지 연구(DALL-E 2, Stable Diffusion, Imagen)에서 diffusion model의 발전은 주목할 만합니다. 이들은 텍스트 입력으로 복잡한 이미지를 생성하는 뛰어난 능력을 보여줍니다. 이러한 기본 생성 모델을 기반으로, 다양한 접근 방식이 개발되어 편집 가능성을 높이고 있습니다. 특히, 'Paint-by-Example' 방식은 시각적 힌트를 통해 텍스트 설명의 모호성을 줄이고, 사용자가 참조 이미지를 이용해 객체의 의미를 조작할 수 있게 합니다.  

### 2. 편집 가능성 향상을 위한 새로운 접근법
본 연구 목표는 sketch를 새로운 모달로 사용하여 generative diffusion model을 발전시키는 것입니다. sketch는 직관적이고 효율적인 도구로, 예술가와 대중에게 오랫동안 사랑받아 왔습니다. sketch의 주요 장점은 텍스트나 이미지와 달리 edge 수준에서의 제어를 통해 이미지 합성 중 기하학적 구조를 안내한다는 것입니다. 이런 기능은 텍스트 설명이나 단독 시각적 힌트보다 더 세밀한 이미지 생성 및 편집을 가능하게 합니다. 실제로, 만화 콘텐츠 생성에서 sketch의 유용성은 매우 높으며, 이 연구는 특히 만화 장면의 편집에 중점을 두고 있습니다.  

### 3. sketch 기반의 multi-input-conditioned image composition model
이 연구에서는 sketch와 참조 이미지를 결합하여 결과물을 생성하는 multi-input-conditioned image composition model을 제안합니다. 생성 과정에서 sketch는 대상 영역의 형태를 결정하는 structure prior로 작용합니다. 이를 위해, diffusion model을 훈련시켜 sketch 가이드를 유지하면서 참조 이미지로 누락된 영역을 완성하도록 합니다. 추론 단계에서는 'sketch plug-and-drop' 전략을 제안하여 모델에 유연성을 부여합니다. 이 방법은 기존 프레임워크와 비교하여 이미지 조작을 위한 독특한 사용 사례를 제공합니다. 제공된 예시들은 이 방법이 임의의 장면에서 사용자 주도의 수정을 가능하게 하는 효과를 잘 보여줍니다.  





![image](https://github.com/kyugorithm/TIL/assets/40943064/bed7298f-0656-4b37-8608-1899568b54d2)
