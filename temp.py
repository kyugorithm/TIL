import boto3
import json

def invoke_media_convert_lambda(source_s3_key):
    # Lambda 클라이언트 생성
    lambda_client = boto3.client('lambda')
    
    # Lambda 함수에 전달할 payload
    payload = {
        "sourceS3Key": source_s3_key
    }
    
    try:
        # Lambda 함수 호출
        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:region:streaming-account:function:your-function-name',  # Lambda ARN을 실제 값으로 변경하세요
            InvocationType='RequestResponse',  # 동기 호출
            Payload=json.dumps(payload)
        )
        
        # 응답 처리
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        
        # Lambda 함수가 에러를 반환했는지 확인
        if 'FunctionError' in response:
            print(f"Lambda function error: {response_payload}")
            return None
            
        return response_payload
        
    except Exception as e:
        print(f"Error invoking Lambda function: {str(e)}")
        return None

# 사용 예시
if __name__ == "__main__":
    source_key = "s3://ingestion-out-bucket/your/path/here"
    result = invoke_media_convert_lambda(source_key)
    print(f"Lambda execution result: {result}")
