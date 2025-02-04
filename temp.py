{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::123456789012:role/SageMaker-ExecutionRole"
            },
            "Action": "lambda:InvokeFunction",
            "Resource": "arn:aws:lambda:region:123456789012:function:YourFunctionName"
        }
    ]
}
