Feature	Stanford Online Products (SOP)	iNaturalist (iNat)	CUB-200-2011 (Caltech-UCSD Birds-200-2011)
Introduced by	Song et al. in "Deep Metric Learning via Lifted Structured Feature Embedding"	Horn et al. in "The iNaturalist Species Classification and Detection Dataset"	Wah et al. in "The Caltech-UCSD Birds-200-2011 Dataset"
Content	120,053 product images	675,170 training and validation images from natural fine-grained categories	11,788 bird images
Classes/Subcategories	22,634 classes	5,089 fine-grained categories	200 subcategories
Training Split	11,318 classes (59,551 images)	--	5,994 images
Testing Split	11,316 classes (60,502 images)	--	5,794 images
Super-categories	--	13 super-categories including Plantae (Plant), Insecta (Insect), Aves (Bird), Mammalia (Mammal), etc.	--
Imbalance	--	Highly imbalanced: Largest (Plantae) with 196,613 images from 2,101 categories; Smallest (Protozoa) with 381 images from 4 categories	--
Annotations	Basic class labels	Basic class labels with super-category information	Detailed annotations: 1 subcategory label, 15 part locations, 312 binary attributes, 1 bounding box
Textual Information	--	--	10 single-sentence descriptions per image collected via Amazon Mechanical Turk (AMT), required to be at least 10 words long, no subcategory or action information
Primary Research Focus	Deep metric learning	Fine-grained categorization with emphasis on handling imbalanced data	Fine-grained visual categorization with extensive annotations and textual descriptions
Size	120,053 images	675,170 images	11,788 images
