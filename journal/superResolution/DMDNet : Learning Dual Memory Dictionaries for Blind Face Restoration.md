## Abstract
### Complexity and Importance of Blind Face Restoration:
BFR is a challenging task due to unknown variables and complex degradation factors. Nevertheless, it has significant value across various practical applications.

### Limitations of Existing Methodologies:

#### Generic Restoration:  
While it relies on a general facial structure, it struggles to adapt to real-world degraded conditions. This is mainly due to the limitations of CNN-based mappings, which also miss out on capturing identity-specific details.

#### Specific Restoration:  
This aims to restore identity-specific features using a reference image of the same identity. However, the requirement for an appropriate reference image significantly restricts the applicable use-cases.

#### Innovative Approach of DMDNet:  
Dual Dictionaries: DMDNet explicitly separates generic facial features and identity-specific features, storing them in separate dictionaries. The generic dictionary learns from high-quality images of various identities, whereas the specific dictionary stores features unique to each individual identity.

#### Dictionary Transform Module:  
Whether or not a degraded input image has a specific reference, this module extracts relevant features from both dictionaries and fuses them into the input features. This enhances the flexibility and effectiveness of the restoration process.

#### Multi-Scale Dictionaries:  
These are utilized to consider features at various resolutions, enabling restoration at multiple levels of detail, from fine to coarse.

#### Additional Technical Features:  
End-to-End Optimization: The entire framework of DMDNet is optimized in an end-to-end manner, making it easily adaptable to a variety of application scenarios.

#### CelebRef-HQ Dataset:  
A new high-quality dataset has been constructed to foster research in specific face restoration at higher resolutions.

#### Performance and Validation:  
DMDNet outperforms state-of-the-art technologies in both quantitative and qualitative metrics. Importantly, it excels in restoring low-quality images in real-world scenarios.
By addressing these various facets, DMDNet presents an innovative approach capable of effectively tackling the challenges of blind face restoration.
