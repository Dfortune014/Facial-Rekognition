# AWS S3 Pre-signed URL Upload Service

This project demonstrates how to generate **pre-signed URLs** using **AWS Lambda** for uploading files to an **S3 bucket** via **API Gateway**.

## Features

- Generate pre-signed URLs for secure file uploads to S3.
- Use API Gateway to provide an endpoint that triggers a Lambda function.
- Fully serverless architecture using AWS services.

## Architecture Overview

1. **Client Request**: The client (React app or other) requests a pre-signed URL from API Gateway.
2. **Lambda Function**: The Lambda function generates the pre-signed URL using the S3 `generate_presigned_url()` method.
3. **File Upload**: The client uploads the file directly to S3 using the pre-signed URL.

## Setup

### AWS Services

- **S3**: Create a bucket (e.g., `visitor-pics-bucket`).
- **Lambda**: Create a function that generates a pre-signed URL.
- **API Gateway**: Set up an endpoint that triggers the Lambda function.

### Lambda Permissions

Ensure your Lambda function has the following permissions:

```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject", "s3:GetObject"],
  "Resource": "arn:aws:s3:::visitor-pics-bucket/*"
}
```

### React Frontend (Optional)

A simple React component for uploading files using the pre-signed URL:

```javascript
const UploadImage = () => {
  /* Code omitted for brevity */
};
```

## Usage

1. Client requests pre-signed URL from API Gateway.
2. File is uploaded directly to S3 using the pre-signed URL.

## Important

- Ensure CORS is enabled on API Gateway.
- Adjust URL expiration time as needed.

---
