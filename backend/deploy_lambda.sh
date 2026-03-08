#!/bin/bash
# ============================================================
# Soochna Setu AI - AWS Lambda Deployment Script
# ============================================================
# Prerequisites:
#   - AWS CLI configured with credentials
#   - Docker installed and running
#   - An ECR repository created
#
# Usage: bash deploy_lambda.sh
# ============================================================

set -e

# ── Configuration ──
AWS_REGION="${AWS_REGION:-ap-south-1}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO_NAME="soochna-setu-ai"
LAMBDA_FUNCTION_NAME="soochna-setu-ai-backend"
IMAGE_TAG="latest"
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"

echo "=== Soochna Setu AI - Lambda Deployment ==="
echo "Region: ${AWS_REGION}"
echo "Account: ${AWS_ACCOUNT_ID}"
echo "ECR Repo: ${ECR_REPO_NAME}"

# ── Step 1: Create ECR Repository (if not exists) ──
echo ">> Creating ECR repository..."
aws ecr describe-repositories --repository-names ${ECR_REPO_NAME} --region ${AWS_REGION} 2>/dev/null || \
  aws ecr create-repository --repository-name ${ECR_REPO_NAME} --region ${AWS_REGION}

# ── Step 2: Login to ECR ──
echo ">> Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URI}

# ── Step 3: Build Docker Image ──
echo ">> Building Docker image..."
docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} .

# ── Step 4: Tag and Push Image ──
echo ">> Pushing image to ECR..."
docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
docker push ${ECR_URI}:${IMAGE_TAG}

# ── Step 5: Create or Update Lambda Function ──
echo ">> Deploying Lambda function..."

FUNCTION_EXISTS=$(aws lambda get-function --function-name ${LAMBDA_FUNCTION_NAME} --region ${AWS_REGION} 2>/dev/null || echo "NOT_FOUND")

if [ "$FUNCTION_EXISTS" = "NOT_FOUND" ]; then
  echo ">> Creating new Lambda function..."

  # Create IAM role for Lambda (if not exists)
  ROLE_NAME="soochna-setu-lambda-role"
  ROLE_ARN=$(aws iam get-role --role-name ${ROLE_NAME} --query 'Role.Arn' --output text 2>/dev/null || echo "NOT_FOUND")

  if [ "$ROLE_ARN" = "NOT_FOUND" ]; then
    echo ">> Creating IAM role..."
    TRUST_POLICY='{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "lambda.amazonaws.com"},
        "Action": "sts:AssumeRole"
      }]
    }'
    aws iam create-role \
      --role-name ${ROLE_NAME} \
      --assume-role-policy-document "${TRUST_POLICY}" \
      --region ${AWS_REGION}

    # Attach policies
    aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
    aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/AmazonTextractFullAccess
    aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
    aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/AmazonPollyFullAccess
    aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/AmazonTranscribeFullAccess

    ROLE_ARN=$(aws iam get-role --role-name ${ROLE_NAME} --query 'Role.Arn' --output text)
    echo ">> Waiting for role propagation..."
    sleep 10
  fi

  aws lambda create-function \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --package-type Image \
    --code ImageUri=${ECR_URI}:${IMAGE_TAG} \
    --role ${ROLE_ARN} \
    --timeout 60 \
    --memory-size 512 \
    --environment "Variables={LLM_PROVIDER=bedrock,USE_TEXTRACT=true,USE_BEDROCK_EMBEDDINGS=true,AWS_REGION_NAME=${AWS_REGION}}" \
    --region ${AWS_REGION}
else
  echo ">> Updating existing Lambda function..."
  aws lambda update-function-code \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --image-uri ${ECR_URI}:${IMAGE_TAG} \
    --region ${AWS_REGION}
fi

# ── Step 6: Create API Gateway (Function URL) ──
echo ">> Creating Lambda Function URL..."
aws lambda add-permission \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --action lambda:InvokeFunctionUrl \
  --principal "*" \
  --function-url-auth-type NONE \
  --statement-id FunctionURLAllow \
  --region ${AWS_REGION} 2>/dev/null || true

FUNCTION_URL=$(aws lambda create-function-url-config \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --auth-type NONE \
  --cors '{"AllowOrigins":["*"],"AllowMethods":["*"],"AllowHeaders":["*"]}' \
  --region ${AWS_REGION} \
  --query 'FunctionUrl' --output text 2>/dev/null || \
aws lambda get-function-url-config \
  --function-name ${LAMBDA_FUNCTION_NAME} \
  --region ${AWS_REGION} \
  --query 'FunctionUrl' --output text)

echo ""
echo "=============================================="
echo "  Soochna Setu AI - Deployed Successfully!"
echo "=============================================="
echo "  Backend URL: ${FUNCTION_URL}"
echo ""
echo "  Set this in your frontend .env.local:"
echo "  NEXT_PUBLIC_API_URL=${FUNCTION_URL}"
echo "=============================================="
