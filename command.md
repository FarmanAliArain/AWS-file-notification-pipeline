# AWS CLI Commands — File Notification Pipeline

## 1. S3 Bucket
aws s3api create-bucket --bucket <BUCKET_NAME> --region <REGION>
aws s3 cp sample.txt s3://<BUCKET_NAME>/sample.txt

## 2. SQS Queue
aws sqs create-queue --queue-name file-notification-queue --region <REGION>
aws sqs send-message --queue-url <QUEUE_URL> --message-body '{"bucket": "<BUCKET_NAME>", "key": "sample.txt"}'

## 3. SNS Topic
aws sns create-topic --name file-notification-topic --region <REGION>
aws sns subscribe --topic-arn <TOPIC_ARN> --protocol email --notification-endpoint <EMAIL>

## 4. IAM Role
aws iam create-role --role-name lambda-file-notification-role --assume-role-policy-document file://trust-policy.json
aws iam put-role-policy --role-name lambda-file-notification-role --policy-name least-privilege-policy --policy-document file://permission-policy.json

## 5. Lambda Function
aws lambda create-function --function-name file-notification-lambda --runtime python3.12 --role <ROLE_ARN> --handler lambda_function.lambda_handler --zip-file fileb://function.zip --timeout 30 --region <REGION>
aws lambda update-function-configuration --function-name file-notification-lambda --environment "Variables={SNS_TOPIC_ARN=<TOPIC_ARN>}"

## 6. Connect SQS to Lambda
aws lambda create-event-source-mapping --function-name file-notification-lambda --event-source-arn <QUEUE_ARN> --batch-size 1

## 7. Test
aws sqs send-message --queue-url <QUEUE_URL> --message-body '{"bucket": "<BUCKET_NAME>", "key": "sample.txt"}'
aws logs tail /aws/lambda/file-notification-lambda --since 10m
