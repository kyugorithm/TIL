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

Security-Related Questions & Answers:

	1.	Work Devices & Network Access
	•	Device provision or network access methods remain undecided.
	•	Coupang Play prefers minimal friction: likely no physical device provisioning, assuming AWS cloud-based development only.
	2.	Network & Internal Tool Access
	•	If internal systems or network access (VPN/internal tools) are needed, AWS Proserve must use either client-provided devices or blank loaner devices due to security constraints.
	3.	AWS Account Structure
	•	Separate environments exist for Development, Staging, and Production.
	•	AWS Proserve will primarily access the Development environment. Deployment to Production accounts will be managed by Coupang Play.
	4.	GenAI & AWS Bedrock Use
	•	Use of AWS Bedrock remains open; further internal discussions are planned to finalize the decision.

Long-term Project Vision:

	•	Coupang Play aims for complete automation (end-to-end video processing pipeline).
	•	This preprocessing pipeline (PRISM) integrates with COSMOS (existing video streaming service).
	•	Future projects include further automation and ML-based functionalities, integrated within this platform.

Next Steps:

	1.	AWS Proserve Action Items:
	•	Finalize the draft SOW (Statement of Work) and send it to Coupang Play.
	•	Provide a summary of previous projects (device/network setup) via email for Coupang Play’s internal review.
	2.	Coupang Play Action Items:
	•	Review the SOW draft promptly upon receipt. Provide comments and approval.
	•	Facilitate internal communication between stakeholders (Segon, James, John F.) to expedite purchasing approval.
	•	Clarify internal policies regarding AWS Proserve’s network access and device usage.
	3.	Collaborative Next Steps:
	•	Schedule a follow-up meeting (set up by Coupang Play) to provide AWS Proserve a comprehensive overview (high-level architecture & strategy) of PRISM, COSMOS, and other relevant infrastructure.
	•	Confirm internal use of AWS Bedrock and GenAI services based on forthcoming discussions.

This structured summary clearly defines responsibilities and the immediate next steps needed to efficiently progress with the project.
