# ML Project - AWS ECR & EC2 Deployment Guide

This guide walks you through deploying your ML project Docker image to AWS ECR and running it on EC2.

## Prerequisites

Before you start, ensure you have:
1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Docker installed on your local machine
4. EC2 instance created and running (Ubuntu 22.04 or similar)
5. IAM user with ECR and EC2 permissions

## Step 1: AWS Setup

### 1.1 Configure AWS Credentials

```bash
aws configure
```

You'll be prompted for:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Default output format (json)

### 1.2 Create ECR Repository

```bash
# Set your repository name
export REPO_NAME="ml-project"
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create ECR repository
aws ecr create-repository \
  --repository-name $REPO_NAME \
  --region $AWS_REGION
```

## Step 2: Build and Push Docker Image to ECR

### 2.1 Build Docker Image Locally

```bash
# Navigate to project directory
cd C:\Users\atharvshivale\Desktop\MLProject

# Build the Docker image
docker build -t $REPO_NAME:latest .

# Tag the image for ECR
docker tag $REPO_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest
```

### 2.2 Authenticate Docker with ECR

```bash
# Get login token (valid for 12 hours)
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
```

### 2.3 Push Image to ECR

```bash
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest

# You should see output like:
# The push refers to repository [123456789.dkr.ecr.us-east-1.amazonaws.com/ml-project]
# ...
# latest: digest: sha256:... size: ...
```

## Step 3: Deploy to EC2

### 3.1 SSH into EC2 Instance

```bash
# Replace with your EC2 instance details
ssh -i "your-key-pair.pem" ec2-user@your-ec2-instance-ip
# or for Ubuntu
ssh -i "your-key-pair.pem" ubuntu@your-ec2-instance-ip
```

### 3.2 Install Docker on EC2 (if not already installed)

```bash
# For Amazon Linux 2
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# For Ubuntu
sudo apt-get update
sudo apt-get install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

### 3.3 Authenticate Docker with ECR on EC2

```bash
# Export environment variables
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID="123456789"  # Replace with your account ID
export REPO_NAME="ml-project"

# Get ECR login token
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
```

### 3.4 Pull and Run the Docker Image

```bash
# Pull the image from ECR
docker pull $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest

# Run the container
docker run -d \
  --name ml-app \
  -p 5000:5000 \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest

# Verify the container is running
docker ps

# View logs
docker logs ml-app
```

### 3.5 Configure Security Group (AWS Console or CLI)

Make sure your EC2 instance's Security Group allows inbound traffic on port 5000:

```bash
# Via AWS CLI
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --protocol tcp \
  --port 5000 \
  --cidr 0.0.0.0/0 \
  --region $AWS_REGION
```

### 3.6 Access Your Application

Visit your EC2 instance in a browser:
```
http://your-ec2-public-ip:5000
```

## Step 4: (Optional) Use Docker Compose for EC2

Create a `docker-compose.yml` on EC2:

```yaml
version: '3.8'
services:
  ml-app:
    image: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ml-project:latest
    ports:
      - "5000:5000"
    restart: always
    environment:
      - FLASK_ENV=production
```

Then run:
```bash
docker-compose up -d
```

## Step 5: (Optional) Use ECS for Container Orchestration

For production deployments, consider using AWS ECS:

1. Create an ECS cluster
2. Create a task definition pointing to your ECR image
3. Create a service to run the task
4. Load balance traffic if needed

This is more scalable and handles auto-scaling, rolling updates, etc.

## Troubleshooting

### Issue: Docker image not found after pull
- Verify the image exists: `aws ecr list-images --repository-name $REPO_NAME`
- Check image name and tag are correct
- Verify ECR authentication is still valid

### Issue: Container crashes immediately
- Check logs: `docker logs ml-app`
- Verify Flask app is binding to `0.0.0.0:5000`
- Check if required files (models, templates) are in the Docker image

### Issue: Cannot connect to application
- Check Security Group allows port 5000
- Verify container is running: `docker ps`
- Check Flask app is not binding only to localhost

### Issue: ECR authentication fails
- Re-authenticate: `aws ecr get-login-password...`
- Check AWS credentials: `aws sts get-caller-identity`
- Verify IAM user has ECR permissions

## Quick Reference Commands

```bash
# Environment setup
export REPO_NAME="ml-project"
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# Build and push (run locally)
docker build -t $REPO_NAME:latest .
docker tag $REPO_NAME:latest $ECR_REGISTRY/$REPO_NAME:latest
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
docker push $ECR_REGISTRY/$REPO_NAME:latest

# Deploy to EC2
ssh -i "key.pem" ubuntu@ec2-ip
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
docker pull $ECR_REGISTRY/$REPO_NAME:latest
docker run -d --name ml-app -p 5000:5000 $ECR_REGISTRY/$REPO_NAME:latest
```

## Next Steps

1. **Monitor**: Use CloudWatch to monitor container logs
2. **Auto-scaling**: Set up auto-scaling groups if needed
3. **CI/CD**: Automate deployment with CodePipeline
4. **Database**: Connect to RDS if your app needs persistent storage
5. **SSL/TLS**: Set up Application Load Balancer with HTTPS
