## Abstract

### Proposal  
Propose a robot action generation method by modeling the visuomotor policy as a **conditional DDPM**.

### Performance  
Achieves an **average 46.9% improvement** over prior state-of-the-art methods across **15 tasks** spanning **4 robot manipulation benchmarks**.

### Techniques  
- Learns the **score function gradient** of the action distribution using a conditional DDPM.  
- Performs iterative optimization during inference via **Langevin dynamics steps**.

### Strengths  
- Effectively handles **multi-modal action distributions**.  
- Scales well to **high-dimensional action spaces**.  
- Demonstrates **high training stability**.

### Contributions  
- Integrates **Receding Horizon Control (RHC)**.  
- Enables **visual-conditioned generation** from raw observations.  
- Introduces a **Time-series Diffusion Transformer** architecture.

### Goal  
Motivate diffusion-based policy learning as a **new standard** for robot control.



## 4. Intriguing Properties of Diffusion Policy

### 4.1 Modeling Multi-Modal Action Distributions
- Diffusion Policy naturally models **multi-modal action distributions**, a challenge for conventional behavior cloning.
- Reasons:
  - **Gaussian-based stochastic initialization** provides diverse starting points for different action modes.
  - **Stochastic Langevin Dynamics optimization** enables convergence to different modes via iterative sampling.
- Example: In a pushing task, it learns both "left" and "right" paths and commits to one per rollout.

### 4.2 Synergy with Position Control
- Unlike prior works preferring **velocity control**, Diffusion Policy performs better with **position control**.
- Reasons:
  - Position control presents **stronger multimodality**, which Diffusion Policy can leverage.
  - Position control reduces **compounding error**, improving sequence prediction stability.

### 4.3 Benefits of Action-Sequence Prediction
- Diffusion Policy predicts **entire action sequences**, avoiding pitfalls of step-wise prediction:
  - Ensures **temporal consistency**, preventing jittery or mode-switching actions.
  - Handles **idle actions** robustly, avoiding overfitting to pauses during demonstrations.

### 4.4 Training Stability
- Unlike Energy-Based Models (EBMs) like IBC, which suffer from unstable training due to negative sampling,
  Diffusion Policy:
  - Models the **score function directly**, bypassing normalization constant estimation.
  - Achieves **stable training** and evaluation, with smoother convergence.

### 4.5 Connections to Control Theory
- In simple linear control settings (e.g., LQR), Diffusion Policy converges to the **optimal linear policy**.
- For **nonlinear or multimodal tasks**, Diffusion Policy extends beyond classical control methods,
  leveraging its generative capacity for complex action distributions.
