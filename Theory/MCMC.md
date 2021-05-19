Markov Chain Monte Carlo
Markov Chain : 미래의 상태(미래 상태의 조건부 확률 분포)는 과거 상태와는 독립적으로 현재 상태에 의해서만 영향받는것을 의미한다.
Monte Carlo : 무수히 많은 횟수의 시행으로 통계적인 정보를 얻어내도록 하는 방법

MCMC를 이해하기 위해서는 Rejection sampling에 대한 이해가 선행되므로 이에 대한 이론을 간단하게 정리하고 코드를 정리한다.
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
