# A Chat with Andrew on MLOps: From Model-centric to Data-centric AI
AI 시스템은 code와 data로 구성되어있다.  
![image](https://user-images.githubusercontent.com/40943064/136804151-1b676523-9ff4-4d34-b0d6-a31d2b4d504f.png)  

code : 구현하는 네트워크 구조같은 모델/알고리즘을 지난 수십년간 ML이 발전된 방식으로 데이터에 학습하는것  
학습 알고리즘이 원하는 하는 성능을 얻는데 도움을 주기 위해서는 일반적으로 **code**를 향상하는것 보단  
시스템적 방식으로 **data**를 향상시키도록 마인드셋을 변화시키는것이 유용할 것이다.  
예로부터 시작해보자,  
자 프로젝트의 결함 검사시트에 대한 예를 보자, 
![image](https://user-images.githubusercontent.com/40943064/136804755-b4fe9a7c-9bb4-4562-81a6-6c720412aa23.png)  
아래 사진은 당신의 부엌에서 볼 수 있는 커다란 알루미늄 재질의 롤이며 무척이나 얇다.  
생산과정에서 발생하는 다양한 defect가 존재할 수 있다.  
공정에는 총 39가지의 결함 유형이 있으며 CV를 통해 결함을 검출하고 싶다.  
튜닝된 뉴럴넷을 학습하여 baseline은 76.2%의 정확도를 가진다.  
오퍼레이터는 사람의 수준의 기준이되는 90%의 정확도 수준이 되길 원한다.  
내가 구입하는 차에 이런 결함이 존재하길 원하지 않기 때문에 당연히 이러한 문제는 중요하다.  
지금까지는 상대적으로 제한된 정보를 전달받았지만 단순한 질문 한가지를 해보겠다.  
만일 당신이 팀을 리드하고 있다면 code/data 중 어떤것을 향상하는데 노력을 기울이겠는가?  
![image](https://user-images.githubusercontent.com/40943064/136805621-aab6e83b-a0c4-45f4-8f73-f68bf09011cf.png)  
많은 사람들이 본능적으로 데이터를 향상시키는게 더 옳다고 이야기한다.  
code를 향상하는것에도 가치가 있지만 많은 역사와 문화 그리고 AI 팀들의 dna와 본능은 data보다는 NN구조의 code에 대해 이야기한다.  

Ivan의 baseline은 76.2%을 얻었고 다른팀은 Model 중심적 개발을 수행했다. github의 최신 모델을 찾고 다운받아  
사용했으나 성능의 진전은 없었다. 실제로 71 ~ 75에 대부분의 모델 성능이 결정됐다.  
이런 방식으로 접근하는것은 매우 어렵지만 데이터 중심 접근 방식을 사용하면서 약 2주만에 17%정도의 향상으로
데이터 품질을 개선하여 93%의 성능을 달성한다.  
Solar panel의 사례도 유사한 결과를 얻었다. 데이터 중심으로 분석을 수행한 팀은 데이터에 더욱더 집중했고  
다른 결함의 예를 찾을 수 있었기에 성능 향상을 얻을 수 있었다.  

![image](https://user-images.githubusercontent.com/40943064/136816618-f2a46b42-ff6a-4c26-bf4d-ce89f7e1b443.png)  
농담처럼 이야기 해왔지만 위의 음식과의 비교를 통해 데이터의 중요성이 얼마나 큰지 알 수 있다.  
결국 data는 AI를 위한 재료이기에 훌륭한 재료로부터 훌륭한 음식이 나온다는 직관은 AI의 사례와 매우 동일하다.  
따라서, machine learning engineer에게 있어 데이터를 중요하는것은 가장 중요한 작업이다.  
  
데이터의 중요성을 이야기했으니 이제 데이터에 접근하는 방법을 보다 체계적으로 만드는 것에 관심을 기울여보자  
80대 20 룰에 영감을 받아 몇주전에 아카이브에서 100개 정도의 최신 ML 논문의 abstract를 훑어보았다.  
완전히 비과학적이지만 99%의 논문이 모델 성능 향상을 위한 주제였다.  
99%의 연구가 20%의 성능을 위한 것이라면 80% 성능을 향상하는 연구로 변화하는것이 더 가치 있는것 같다.  

**Lifecycle of an ML project**  
ML 프로젝트를 만들때,  보통 모델 학습을 대부분 강조한다. 학습, 모델구조 등 중요하지만  
학습에러분석, 반복적 향상등은 단지 전체 ML 프로젝트의 일부분에 지나지 않는다.  

**1. Define project**  
바른방향으로의 업무를 결정하기 위해 프로젝트를 샅샅히 살핌  
(e.x., 나는 바른 음성을 찾기 위한 음성인식 프로젝트를 결정한다. )  
얼마나 많은 데이터/자원/엔지니어링/계산이 필요한지를 결정 한다.  
  
**2. Define and collect data**  
데이터를 정의하고 수집  
AI에 대한 데이터 중심적 접근이라고 하는것은 당신이 물어야하는 가장 중요한 질문중 하나인데,  
하나는 데이터 레이블 지속성이다.  
**Example 1**  
만약 충분한 고품질의 데이터를 가지고 있다면, 한가지예를 이야기해보자.  
쉽게 찾을 수 있는 audio clip이 하나 있다. 틀어보면 (today's weather)  
예를들어 당신이 이 목소리를 듣고 script로 변환을 완벽하게 훌륭하게 하고자 한다면  
Um, today's weather / Um... today's weather / Today's weather  
이중 어떤 것을 label로 사용해도 상관없으나 함께 사용하면 알고리즘에 혼동이 될 수 있으며  
따라서 이는 알고리즘 성능에 부정적인 영향이 될 것이다.  
  
**Example 2**  
 ![image](https://user-images.githubusercontent.com/40943064/136820627-48bac7fd-eead-4a5f-977b-833c8bd4b565.png)  
3가지의 bounding box 중 다른 방법을 혼동하여 사용하면 데이터의 일관성이 사라지고 알고리즘이 혼동하게 된다.  
  
![image](https://user-images.githubusercontent.com/40943064/136820989-c676f756-8cc9-4830-a339-3ebc80fa90b5.png)  
**Tip**  
1. 두 독립적인 laber에게 레이블을 sampling 하도록 해라.  
2. 둘이 어디에서 동의하지 않는지를 탐색하기 위해 그들 사이에서의 일치성을 측정해라  
3. 동의하지 못하는 부분이 생긴다면 레이블링이 일치하도록 labeling 지침을 수정해라  

**일치하지 않는 경우**
![image](https://user-images.githubusercontent.com/40943064/136821913-bb40cd8e-821e-45fb-873f-aa16f4c55d8f.png)  
**지침을 다시 준 경우**
![image](https://user-images.githubusercontent.com/40943064/136821887-89dae1b8-8392-44bf-8920-96e130d91853.png)  

![image](https://user-images.githubusercontent.com/40943064/136822437-9065e86c-fb94-4075-893d-bd4ae907223d.png)  




**3. Traning, error analysis & iterative improvement**  
모델 학습, 때로는 에러분석 단계에서 데이터 향상을 위해 이전 단계로 돌아가기도 한다.  
그리고 이러한 작업을 여러번 반복한 후에 다음단계를 진행한다.  
**4. Deplot, monitor and maintain system**  
생산단계에 모델을 deploy, 때로는 데이터에 기반하여 이전 단계들로 돌아가기도 한다.  
![image](https://user-images.githubusercontent.com/40943064/136818950-b76cf70c-dfc6-4d0c-a51a-4771ca236b91.png)  

