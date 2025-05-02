1. Background

In this evaluation, we aim to determine whether open-source large language models (LLMs) are practically usable for our specific task, as an alternative to commercial offerings such as ChatGPT. This involves assessing the capability of a selected open-source LLM to perform translation and subsequent refinement tasks on Subscription content.

The primary goals of the test are:
	•	To validate whether open-source LLMs (e.g., a 12B parameter model) can produce acceptable translation results on real-world subscription data.
	•	To design and implement a complete inference pipeline that supports batch processing and model serving in a production-like environment.
	•	To evaluate the performance gap between the open-source LLM and a commercial-grade model (ChatGPT-4.0) by comparing outputs on a fixed sample set.

This effort is foundational for reducing dependency on commercial APIs, lowering inference cost, and establishing internal infrastructure capable of supporting domain-specific fine-tuned LLMs.


2. Experiment Details

2.1 Task Definition

The target task is translation followed by linguistic and contextual refinement. The input is a Subscription content item (e.g., marketing or product descriptions), and the output is a high-quality, fluent translation suitable for end-user consumption.

Two major sub-tasks are performed:
	•	Translation: Convert original text into English using an open-source LLM.
	•	Refinement: Improve the translated result to enhance clarity, tone, and domain alignment.

2.2 Model Setup

	•	Open-Source Model: A 12B parameter model (e.g., Mistral or DeepSeek) is selected for baseline translation and refinement. The model is quantized and deployed via a custom inference pipeline.
	•	Reference Model: ChatGPT-4.0 is used as the performance upper-bound for comparison.
	•	Evaluation Data: A curated set of Subscription samples from actual production data is used to ensure realistic coverage.

2.3 Serving Pipeline

We implemented a modular serving pipeline with the following features:
	•	Batch Processing: Supports high-throughput inference on multiple subscription items.
	•	Prompt Templates: Optimized prompts for translation and refinement are used to ensure consistency.
	•	Latency and Throughput Monitoring: Basic profiling included to ensure feasibility under real-world constraints.

2.4 Evaluation

	•	Comparison Metrics: Manual qualitative comparison of translations will be performed between:
	•	Output from the open-source 12B model (baseline)
	•	Output after refinement using the same model
	•	Output from ChatGPT-4.0
	•	Criteria: Accuracy, fluency, tone appropriateness, and alignment with target use-case.
