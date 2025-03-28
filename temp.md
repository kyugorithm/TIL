1. Key Q&A Summary

(1) Region Considerations

	•	Question: “Do we need to use only the Seoul (ap-northeast-2) Region? Can we consider other Regions for better cost optimization? What are the pros and cons?”
	•	Presenter (Kevin) Response
	•	Currently, the default plan is to use the Seoul Region.
	•	Other Regions could be considered for cost optimization, but data transfer costs, latency, and internal security policies must be taken into account.
	•	Additional Follow-Up Needed
	•	Investigate actual cost/latency differences if other Regions are used.
	•	Clarify any security/regulatory implications for transferring data outside Seoul Region, in line with Coupang Play’s internal policies.

(2) Payment Integration

	•	Question: “We handle iOS/Android in-app purchases and subscription flows. Does AWS offer any specific payment service for this?”
	•	AWS Response
	•	There is no dedicated AWS in-app payment service; typically, Apple/Google payment systems are used.
	•	ProServe can share best practices or reference architectures if relevant.
	•	Presenter (Coupang) Follow-Up
	•	Determine whether the payment component is directly tied to the ML pipeline, or if it is a separate project requiring its own scope.

(3) ML Pipeline Integration with External Systems

	•	Question: “If the results (e.g., poster generation, QC) are simply stored in S3, can we enable other teams or systems (e.g., CMS, recommendation engines) to easily access these results or re-trigger pipelines via events/triggers?”
	•	AWS Response
	•	There are multiple integration options (EventBridge, Lambda, etc.). ProServe can incorporate these features into the overall architecture.
	•	Presenter (Kevin) Follow-Up
	•	Specify the exact API or data format required by internal CMS or other systems.
	•	Consider whether results should move from S3 into a database (DynamoDB, RDS) or be served via an API, and outline the approach.

(4) Cost & Performance Optimization

	•	Question: “How can we optimize both cost and performance in an ML pipeline using GPU instances?”
	•	Presenter (Kevin) Explanation
	•	Currently using G4dn or similar GPU instances but is also evaluating other options (SageMaker, Spot Instances, etc.).
	•	Additional Follow-Up Needed
	•	Provide metrics on daily/monthly processing volume, GPU usage, processing times, etc.
	•	AWS can then assess potential cost savings, for example by using Spot, Reserved Instances, or a different Region.

(5) Timeline and Next Steps

	•	Question: “When can collaboration with ProServe start in practical terms, and how does the process work until the Statement of Work (SOW) is finalized?”
	•	AWS Response
	•	The typical flow is: additional Q&A → define detailed scope → draft SOW → internal reviews → contract signing.
	•	The timeline can be expedited if Coupang Play is ready to move quickly.
	•	Presenter (Coupang) Request
	•	Wishes to proceed as soon as possible; they would like to receive a list of questions and provide answers promptly so that follow-up meetings can be scheduled right away.
