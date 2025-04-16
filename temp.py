


PRISM System Architecture and Processing Flow
Overview
The PRISM system is an advanced video processing pipeline that utilizes AWS services to analyze and extract meaningful data from video content. The system performs multiple analyses in parallel, including text extraction, image classification, shot/scene detection, and audio transcription. This document outlines the end-to-end flow of the PRISM system, detailing each module's functionality and dependencies.
Trigger Mechanism
When a video is uploaded to a designated S3 bucket, the system initiates the following sequence:

Amazon EventBridge detects the upload event
EventBridge triggers an AWS Lambda function
The Lambda function invokes AWS Step Functions
Step Functions orchestrates the entire workflow of video processing

Video Pre-Processing
The initial stage prepares the video for parallel analysis:

Extracts media information from the video (resolution, codec, duration, etc.)
Separates audio stream from the video
Creates a subsampled version of the video for more efficient processing
This stage typically requires 2-3 minutes to complete

Parallel Processing Modules
Once pre-processing is complete, four analysis modules run concurrently as a batch:
Text Analysis

Performs Optical Character Recognition (OCR) on video frames
Extracts all text visible in the images
Pairs extracted text with corresponding timecodes
Stores results as metadata in the target bucket
Does not store the actual images, only the extracted information

Image Analysis

Applies classification algorithms to video frames
Uses sliding windows of 640x640 or 512x512 pixels to analyze sections of each frame
Detects specific elements such as rising sun flags, pixel errors, and other classifiable objects
Pairs classification results with timecodes
Stores only metadata in the target bucket
No images are stored since they can be referenced from the original video using index, X, and Y offsets

Shot/Scene Detection

Identifies and marks boundaries between different shots and scenes in the video
Creates semantic segmentation of the video content
Indexes each segment with corresponding timecodes
Provides critical information for subsequent processes like vector embedding
Enables more meaningful analysis by processing content within its semantic context
Stores segmentation data in the target bucket

Audio Analysis

Utilizes transcription models (such as Whisper) to convert speech to text
Detects audio quality issues and errors through specialized algorithms
Pairs transcriptions and error detection results with timecodes
Stores audio analysis results in the target bucket

Vector Embedding
After the parallel processing modules complete their work:

Begins the vector embedding process
Depends on completed shot/scene detection and audio analysis results
Creates embeddings based on semantic segments identified in previous stages
Stores vector information in the target bucket

Storage System
All processed data is stored in:

A bucket managed by the ML data management system called "Alios"
Under a specific path named "PRISM"
Organized in a way that facilitates subsequent operations

Downstream Applications
Once preprocessing and vector embedding are complete, the system can trigger various applications based on needs or JSON input parameters:

Content QC (Quality Control)
VLM (Vision Language Model) processing
Localization
Poster generation
Other potential applications

Flexibility
The PRISM system is designed with modularity in mind:

The workflow can be modified to add or remove processing steps as needed
New modules can be integrated into the existing architecture
The system can be tailored to specific use cases while maintaining the overall processing flow

Performance Considerations

Initial pre-processing takes approximately 2-3 minutes
Parallel processing optimizes the overall execution time
Dependencies between modules are carefully managed to ensure efficient processing





--------
[Full English Translation of Your Description]

Let me explain the overall flow of the PRISM system. First, when a video is uploaded to the bucket, an event is triggered through Amazon EventBridge. This triggers a Lambda function. The Lambda collects the event and invokes an AWS Step Function, which starts the processing pipeline.

The first phase is video pre-processing, where the system extracts media metadata, audio, and a sparsely sampled version of the video.
	•	The audio is used either for transcription or audio error analysis.
	•	The sampled video is analyzed using ML models for various image-based tasks.

This phase takes about 2 to 3 minutes and then transitions into a parallel batch processing stage that includes four modules:
	1.	Text Analysis (OCR)
	•	For each image, OCR is performed to extract text.
	•	The text and corresponding timecodes are saved as metadata in the target bucket for future content QC or video QC tasks.
	2.	Image Analysis (Classification)
	•	Each image is scanned with sliding windows (e.g., 640x640 or 512x512) to check for content such as the “rising sun flag” or pixel errors.
	•	The classification results are stored along with timecodes, without saving the actual image since the original frame can be reconstructed from the source video and XY offset.
	3.	Shot/Scene Detection
	•	This module detects semantic segments in the video.
	•	These are useful for vector embedding, content summarization, and poster generation.
	•	The results are stored in the bucket with segment indices.
	4.	Audio Analysis
	•	Whisper or similar transcription models are used to convert spoken language into text.
	•	Audio errors are detected with specialized algorithms, and both the transcription and error logs are saved.

Once these parallel processes are complete, the vector embedding phase begins.
	•	This depends on both shot/scene detection and transcription results.
	•	Vectors are extracted and stored in a target bucket managed by Arios, an internal ML data management system, under the /prism path.

Finally, depending on configurations or JSON input, downstream jobs like Content QC, VLM, Localization, or Poster Generation are triggered.
This is the overall pipeline flow of PRISM. New modules may be added or removed depending on future needs.
