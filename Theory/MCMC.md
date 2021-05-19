#### MCMC(Markov Chain Monte Carlo)
Markov Chain : 미래의 상태(미래 상태의 조건부 확률 분포)는 과거 상태와는 독립적으로 현재 상태에 의해서만 영향받는것을 의미한다.
Monte Carlo : 무수히 많은 횟수의 시행으로 통계적인 정보를 얻어내도록 하는 방법

MCMC를 이해하기 위해서는 Rejection sampling에 대한 이해가 선행되므로 이에 대한 이론을 간단하게 정리하고 코드를 정리한다.  

#### What is rejection sampling?
Sampling 방법론의 일종으로 확률분포의 확률밀도함수PDF의 형태는 알고있으나 해당 분포로부터 샘플을 추출하지 못하는 경우 사용하는 알고리즘이다.  
제목을 통해 알 수 있듯, 추출 된 샘플중 어떤것은 accept하고 어떤것은 reject하여 정의한 확률분포로부터 샘플을 추출할 수 있도록 한다.  

Rejection sampling을 수행하는 방법은 내가 쉽게 샘플링할 수 있는 확률분포를 이용하여 샘플을 얻고 이 샘플을 특정 조건을 만족하도록 하여 원하는 확률분포를 따르도록 하는 것이다.  
쉽게 샘플링할 수 있는 분포를 제안분포(propose distribution)라고 하는데, 이는 내가 사용하는 PDF에 가까운형태를 사용하는것이 좋다고한다. (샘플링의 정확성을 위해서인것 같다)  
나는 uniform distribution을 사용하였다. 내가 적용하고싶은 pdf를 target distribution이라고 하는데, propose distribution을 target distribution의 최대값에 맞추기 위해 rescaling을 수행한다.(이것도 꼭 크기를 맞출 필요는 없으나 target pdf를 최대한 효율적으로 덮기 위한것 같다.)  
어쨋든, 다음으로는 두개의 distribution이 가지는 x의 공간에서 propose pdf를 이용하여 샘플을 추출한다. 그리고 해당 x의 위치에서 (0, Mxpropose)사이의 값을 uniform sampling하여 target pdf값보다 큰지 작은지에 따라 rejection 할지 accept할지를 결정한다. 이과정을 무수히 반복하면 내가 원하는 분포에 대한 샘플을 획득할 수 있게 된다.
python 코드는 아래와 같다. 

```python
import numpy as np
from sympy import symbols, exp
import matplotlib.pyplot as plt

# Sample Number
N = 10000

x = symbols('x')

x_rand           = np.array(np.random.uniform(low = -7, high = 17, size=N)).reshape(N,1)
u_rand           = np.array(np.random.uniform(low =  0, high =  1, size=N)).reshape(N,1)

f_target         = 0.3*exp(-0.2*x**2) + 0.7*exp(-0.2*(x-10)**2)
f_propose        = 1/24
f_target_max     = f_target.subs(x, 10)
M                = f_target_max / f_propose

target_boundary  = np.array([f_target.subs(x, xnow) for xnow in x_rand]).reshape(N,1)
propose_boundary = 24*np.ones((N,1))
ratio            = target_boundary/(M/propose_boundary)

idx_accept       = np.where(u_rand < ratio)[0]
idx_reject       = np.where(u_rand >= ratio)[0]

#%%
plt.subplot(2,1,1)
plt.plot(x_rand[idx_accept], u_rand[idx_accept],'.')
plt.plot(x_rand[idx_reject], u_rand[idx_reject],'.')
plt.grid()
plt.xlabel('x')

plt.subplot(2,1,2)
plt.hist(x_rand[idx_accept],bins=100)
plt.grid()
```
<img src='https://github.com/kyugorithm/TIL/blob/main/sources/resource_rejectionsampling.png'>
