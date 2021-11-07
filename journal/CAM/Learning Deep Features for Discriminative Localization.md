## Abstract
Global average pooling(GAP) layer는 network in network 논문에서 제안된 바 있으며 regularizing training을 위해 사용 되었다.  
그러나 본 논문에서는 GAP를 사용하여 image-level label에 학습됨에도 놀라운 localization 능력을 가지는것을 보인다.  
GAP의 명확한 단순성에도 불구하고 localization 성능이 매우 뛰어나며 기존 fully supervised 방식의 SOTA에 꽤 가까운 성능을 보여준다.  
다양한 task에서 localization을 위한 학습이 이루어지지 않음에도 불구하고 localize가 가능함을 보인다.  

## 핵심구조
![image](https://user-images.githubusercontent.com/40943064/124291821-ef81ce80-db8f-11eb-97cd-19a8ea7d980a.png)  
  
본 논문이 제안하는 핵심 구조는 매우 간단하다. FC대신 GAP를 사용함으로써 Feature 특성을 살리고 이를 이용하는 것으로 판단된다.  
이로써 CAM이 생성되며 어떤 부분이 활성화되어 Class가 선택되었는지를 Visually 이해할 수 있으며 localization에 활용 할 수도 있다.
