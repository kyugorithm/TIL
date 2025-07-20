## Abstract

### Proposal  
Propose a robot action generation method by modeling the visuomotor policy as a **conditional denoising diffusion probabilistic model (DDPM)**.

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
