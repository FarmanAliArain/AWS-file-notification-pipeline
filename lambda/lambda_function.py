import json
import os
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def log_json(level, message, **fields):
    entry = {"level": level, "message": message}
    entry.update(fields)
    print(json.dumps(entry))

def lambda_handler(event, context):
    for record in event['Records']:
        message_id = record.get('messageId', 'unknown')
        try:
            body = json.loads(record['body'])
            bucket, key = body['bucket'], body['key']

            log_json("INFO", "Processing started",
                      message_id=message_id,
                      request_id=context.aws_request_id,
                      bucket=bucket, key=key)

            meta = s3.head_object(Bucket=bucket, Key=key)

            sns_response = sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f"New File: {key}",
                Message=(
                    f"New file uploaded!\n\n"
                    f"File Name: {key}\nBucket: {bucket}\n"
                    f"Size: {meta['ContentLength']} bytes\n"
                    f"Content Type: {meta.get('ContentType','N/A')}\n"
                    f"Last Modified: {meta['LastModified']}\n"
                    f"ETag: {meta['ETag']}\n"
                    f"Storage Class: {meta.get('StorageClass','STANDARD')}"
                )
            )

            log_json("INFO", "File notification published",
                      message_id=message_id,
                      sns_message_id=sns_response['MessageId'],
                      file_name=key, key=key, bucket=bucket,
                      size_bytes=meta['ContentLength'],
                      content_type=meta.get('ContentType','N/A'),
                      last_modified=str(meta['LastModified']),
                      etag=meta['ETag'],
                      storage_class=meta.get('StorageClass','STANDARD'))

        except Exception as e:
            log_json("ERROR", "Processing failed", error=str(e))
            raise e

    return {"statusCode": 200, "body": json.dumps("Done")}

