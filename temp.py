import boto3
import json

# Lambda 클라이언트 생성
lambda_client = boto3.client('lambda')

# Lambda 함수 호출할 데이터 준비
payload = {
   "key1": "value1",
   "key2": "value2"
}

try:
   # Lambda 함수 호출 - ARN 사용 및 동기식
   response = lambda_client.invoke(
       FunctionName='arn:aws:lambda:region:account-id:function:function-name',  # 실제 Lambda ARN으로 교체
       InvocationType='RequestResponse',  # 동기식 호출
       Payload=json.dumps(payload)
   )
   
   # 응답 처리
   response_payload = json.loads(response['Payload'].read().decode('utf-8'))
   print("Lambda 함수 응답:", response_payload)
   
except Exception as e:
   print("Error:", str(e))
