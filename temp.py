{
  "Comment": "PRISM Workflow for Video Metadata Processing",
  "StartAt": "InitProcessing",
  "States": {
    "InitProcessing": {
      "Type": "Pass",
      "Next": "ParallelProcessing"
    },
    "ParallelProcessing": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "TextAnalysis",
          "States": {
            "TextAnalysis": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Parameters": {
                "FunctionName": "TextAnalysisFunction",
                "Payload": {
                  "input.$": "$"
                }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "ImageAnalysis",
          "States": {
            "ImageAnalysis": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Parameters": {
                "FunctionName": "ImageAnalysisFunction",
                "Payload": {
                  "input.$": "$"
                }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "ShotSceneDetection",
          "States": {
            "ShotSceneDetection": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Parameters": {
                "FunctionName": "ShotSceneDetectionFunction",
                "Payload": {
                  "input.$": "$"
                }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "AudioAnalysisTranscription",
          "States": {
            "AudioAnalysisTranscription": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "Parameters": {
                "FunctionName": "AudioAnalysisFunction",
                "Payload": {
                  "input.$": "$"
                }
              },
              "End": true
            }
          }
        }
      ],
      "Next": "CheckSDandAACompletion"
    },
    "CheckSDandAACompletion": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.ShotSceneDetection.Status",
          "StringEquals": "COMPLETED",
          "And": [
            {
              "Variable": "$.AudioAnalysisTranscription.Status",
              "StringEquals": "COMPLETED"
            }
          ],
          "Next": "MultimodalVectorEmbedding"
        }
      ],
      "Default": "WaitForSDandAA"
    },
    "WaitForSDandAA": {
      "Type": "Wait",
      "Seconds": 10,
      "Next": "CheckSDandAACompletion"
    },
    "MultimodalVectorEmbedding": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "MultimodalVectorEmbeddingFunction",
        "Payload": {
          "input.$": "$"
        }
      },
      "Next": "CombineResults"
    },
    "CombineResults": {
      "Type": "Pass",
      "Result": {
        "ProcessingComplete": true
      },
      "End": true
    }
  }
}
