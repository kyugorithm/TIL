Here’s a structured summary in English of the discussed questions and answers, along with clear next steps:

Summary of Discussion:

Scope-Related Questions & Answers:

	1.	Video Data Pipeline Start Point
	•	Initially, the video ingestion trigger was S3 bucket-based.
	•	Now changed to periodic batch processing. Video transcoding and delivery are already automated by Coupang.
	2.	Legacy System Dependencies
	•	Minimal dependencies exist. Current “Poster Generation” service integration is limited to input/output alignment only.
	3.	Architecture Flexibility
	•	AWS Proserve is free to redesign the architecture, as long as I/O formats are maintained.
	4.	Model Development Status
	•	Two existing services: Poster Generation (currently deployed) and Content QC (planned for near future).
	•	VLM, LLM, Localization models are planned but currently undeveloped.
	5.	Deployment Expectations
	•	Priority is establishing robust preprocessing infrastructure. Deploying final task-specific ML models (VLM, Localization) within the current 6-month timeline is ideal but not mandatory.
	6.	Inference Optimization Priority
	•	Current priority is infrastructure development and preprocessing pipeline, rather than model serving optimization.
	7.	Poster Generation Data Pipeline
	•	Existing Poster Generation model currently faces inefficiencies in backend/frontend data handling.
	•	Improving data delivery methods is desirable but lower in priority compared to infrastructure setup.
	8.	Project Deliverables & Goals
	•	Main goal: Build a general-purpose, reusable data preprocessing pipeline.
	•	Pipeline includes ML Ops setup with CI/CD automated deployment on AWS.
	9.	Timeline
	•	No fixed internal deadline from Coupang Play; however, starting ASAP is desired. The timeline can be determined collaboratively.
