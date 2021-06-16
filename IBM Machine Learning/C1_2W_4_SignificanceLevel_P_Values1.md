**학습목표**
- 가설검정 : significance level & p-values (가설검정의 빈도주의적 접근방식)
- 검정력과 샘플 사이즈 고려

앞서 소개한 귀무가설 분포를 알고 있다. 동전확률은50/50이라거나 마케팅 무효성에 대한 분포등이 있다.  
기각영역을 얻기 위해서 검정통계를 계산한다. 데이터를 테스트하기 전에 우리는 귀무가설을 기각할 기준을 선택할 것이다.  
이를 위해서 significance level(a)를 정의해야하는데 a는 귀무가설을 기각하는 확률 threshold이다.  
이 significance level은 1종오류나 2종오류를 어느 스준으로 피하고싶은지에 매우 관련될 것이다.  
alpha값이 낮은 수준은 귀무가설에 대한 데이터의 확률이 매우 낮은 경우에도 귀무가설을 기각하려는 것이다.  
따라서 우리는 검정통계를 계산하기 이전에 알파값을 선택하야 하며 그렇지 않으면 귀무가설을 수용/기각 하는데  
사용되는 P값을 의도적으로 수정하는 P-hacking 행위로 비난받을것이다.  
당신이 확실하게 귀무가설을 기각하고자 한다면, 즉 실수로 귀무가설을 기각하는 1종 오류를 피하고 싶다면 매우 낮은  
알파값을 사용하면 된다.  
예를들어 만약 약물이 위험한 부작용이 있고 귀무가설은 약물이 질병에서 회복하는데 도움이 되지 않는다는 것이다.  
반대로 대립가설은 약물이 도움이 될것이라고 주장하는 것이다. 당신은 귀무가설을 기각할 수 있도록  
매우 확실하고자 한다.  
다른한편, 광고 글꼴 크기를 늘릴지말지 결정하고 그것이 효과가 있을지를 보는것처럼 엄격하지 않을 수 있다.  
귀무가설은 여전히 효과가 없고 2종 오류인 귀무가설을 기각하는것이 그렇게 위험하지는 않다.  
그리고 당신이 만일 약물효과 테스트와같은 문제에서 매우 안전한 결과를 얻고자 한다면  
p값으로 0.1, 0.05, 0.01혹은 0.001과 같은 통상적인 값을 사용한다는것을 주목할 가치가 있다.  
**p-value** : 결과의 귀무가설 분포에서 실제로 관측된 것보다 더 극단적일 확률  
(귀무 가설이 기각되는 작은 유의수준)  
**confidence interval** : 우리가 귀무가설을 수용하기 위한 통계값이고 기본적으로  
이 기각 영역의 P-값의 반대쪽이다.  
![image](https://user-images.githubusercontent.com/40943064/120486544-1f528080-c3f0-11eb-8208-0ceb9d015bb5.png)  
이제 이해를 돕기 위해 그림에서 p값과 때때로 정규분포의 형태를 취하는 귀무분포에 대한 관계로 유의수준을 본다.  
그래서 우리가 p값이 0.05라면 광고의 효과가 무효하다는 가설만 기각할 것이다.  
표본 데이터에서 취득한 값이 평균 값에서 표준편차를 크게 벋어나는 경우 효과가 없음을 나타낸다.  
본 그래프 위 수평선을보면 95%가 어떤 방향에서나 두 표준편차 사이에 속한다는것을 알 수 있다.  

다시 말해서, P를 0.05로 설정하면, 이 데이터가 두 표준 편차의 오른쪽이나 왼쪽으로 떨어져야 한다. 따라서 마케팅 캠페인을 다시 생각해보면, 이것이 가능성이 있습니다. 이제 우리가 어떤 캠페인을 운영하지 않았다고 가정해 보겠습니다. 이것은 우리가 얻은 표본 데이터를 랜덤하게 얻은 과거 데이터로 볼 때, 광고를 실행하지 않은 경우일 것입니다. 그래서 이런 일이 5%씩 일어납니다. 그래서 우연한 기회에 그런 일이 일어날 수도 있지만, 5%밖에 일어나지 않았습니다. 만약 우리가 5%만큼 극단적인 것을 보게 된다면, 우리가 실제로 캠페인을 운영했을 때, 우리는 그 캠페인이 아무런 효과가 없다는 무효를 거부합니다.  

![image](https://user-images.githubusercontent.com/40943064/120489924-f7185100-c3f2-11eb-9faa-206f8267add6.png)  

자, 앞서 논의했던 동전 던지기 예에 대해 생각해 봅시다. 그래서 우리가 세 개의 머리를 10개의 롤에 10개의 플립으로 뒤집는다고 가정해봅시다.  
우리는 3개의 헤드가 더 적은 만큼 가치를 극단적으로 얻을 가능성이 여기서 강조된다는 것을 알 수 있습니다.
우리는 제로 헤드, 1 헤드, 2 헤드, 3 헤드의 확률을 합산할 수 있습니다. 그리고 만약 우리가 공정한 동전을 가지고 있다면, 우리는 3개 혹은 그 이하를 얻을 17%의 확률로 얻을 수 있을 것입니다.
따라서, 동전의 가치라는 귀무 가설에서는, 이 극단적인 현상이 실제로 17% 정도 발생할 수 있습니다. 그리고 우리는 귀무 가설을 기각하지 않을 것입니다.
그래서 이 동전 던지기 예에서, 우리의 무효 가설은, 우리는 공정한 동전을 가지고 있다는 것이었습니다. 헤드의 확률은 0.5와 같으며, 우리의 대안은 동전이 불공정하고 헤드의 확률은 0.5보다 작다는 것이다.
그렇다면 만약 우리가 열 번의 뒤집기에서 세 개의 머리를 관찰한다면 어떻게 이 귀무 가설을 실험할 수 있을까요?
그래서 먼저 귀무 가설을 검정하기 위해, 우리는 귀무 가설을 알고 있습니다. Null 분포는 플립이 10개인 이항 분포로 분포하며, 각 분포가 착륙 헤드의 50% 확률이다.
P-값 컷오프를 선택합니다. 우리는 5%가 극단값이든 아니든 간에 우리의 단점이 될 것이라고 말한다.
우리는 이항으로부터 3개의 헤드의 누적 분포 함수를 계산하며, 랜딩 헤드의 확률은 10과 5050이다. 이것이 의미하는 것은, 앞서 본 곡선에 대한 면적의 누적 합계가 3개 이하가 되어야 한다는 것입니다. 또한 앞서 살펴본 도표와 일치합니다. 3개의 헤드에 대한 확률을 더하고, 점점 더 짧습니다.
누적 분포 함수는 17.1%로 컷오프(0.5)를 초과합니다. 그래서 우리는 동전의 귀무 가설을 거부하지 않기로 결정했다.
이제 여기서 마치겠습니다. P-값을 사용할 때 기억해야 할 몇 가지 중요한 의미를 짚어보겠습니다.


****
****