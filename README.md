# AWS-file-notification-pipeline
Serverless event-driven file notification pipeline using AWS CLI --S3,SQS,Lambda,SNS
# AWS Event-Driven File Notification Pipeline

A fully serverless pipeline built using **AWS CLI only** — no console clicks except confirming the SNS email subscription.

## Architecture

S3 Upload → SQS → Lambda → S3 (get metadata) → SNS → Email

See `diagram/architecture-diagram.png` for the visual flow.

## How It Works

1. A file is uploaded to an S3 bucket.
2. A JSON message (bucket + key) is sent to an SQS queue.
3. An SQS-triggered Lambda function reads the message, fetches the file's metadata from S3 (size, content type, last modified, ETag, storage class).
4. Lambda publishes a formatted notification to an SNS topic.
5. SNS emails the subscriber with the file details.

## IAM Approach

The Lambda execution role follows least privilege — every permission is scoped to a specific resource ARN, no wildcards. See `iam-policies/`.

## Folder Structure

- `lambda/` — Lambda function source code
- `iam-policies/` — Trust policy and least-privilege permission policy
- `commands.md` — Every AWS CLI command used to build this, in order
- `screenshots/` — Proof of each stage working (S3, SQS, email, CloudWatch)
- `diagram/` — Architecture diagram

## What I Learned

[Fill this in with your own specific experience — e.g. IAM propagation delays, structured JSON logging in Lambda, debugging CloudWatch log groups]
