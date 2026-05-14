# AWS Deployment Setup Guide - ML Project

Complete step-by-step guide to deploy your ML project to AWS ECR and EC2.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [AWS Account Setup](#aws-account-setup)
4. [Build and Push to ECR](#build-and-push-to-ecr)
5. [EC2 Setup](#ec2-setup)
6. [Deploy to EC2](#deploy-to-ec2)
7. [Verification & Testing](#verification--testing)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Local Machine
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- [AWS CLI v2](https://aws.amazon.com/cli/) installed
- Git (optional)

### AWS Account
- Active AWS Account
- Access to IAM, ECR, and EC2 services
- Billing enabled

### EC2 Instance
- EC2 instance running (Ubuntu 22.04 recommended)
- Security Group configured to allow SSH (port 22) and HTTP (port 5000)
- Key pair (.pem file) for SSH access

## Local Setup

### 1. Verify Docker Installation
```bash
docker --version
# Should show: Docker version X.X.X
```

### 2. Test Flask Application Locally

```bash
# Navigate to project directory
cd C:\Users\atharvshivale\Desktop\MLProject

# Build Docker image
docker build -t ml-project:latest .

# Run container locally
docker run -p 5000:5000 ml-project:latest

# In another terminal, test the app
curl http://localhost:5000

# Stop container
docker stop <container-id>
```

## AWS Account Setup

### 1. Create IAM User (if needed)

Go to AWS Console → IAM → Users → Create user

**Attach policies:**
- `AmazonEC2ContainerRegistryPowerUser` - for ECR operations
- `AmazonEC2FullAccess` - for EC2 operations

### 2. Create Access Keys

For the IAM user:
1. Go to Security credentials tab
2. Create access key
3. Save the Access Key ID and Secret Access Key

### 3. Configure AWS CLI

On your local machine:

```bash
aws configure
```

When prompted, enter:
- AWS Access Key ID: [paste from step 2]
- AWS Secret Access Key: [paste from step 2]
- Default region: us-east-1 (or your preferred region)
- Default output format: json

Verify configuration:
```bash
aws sts get-caller-identity
```

## Build and Push to ECR

### Option 1: Using Automated Script (Recommended for Windows)

```batch
# Windows Command Prompt
cd C:\Users\atharvshivale\Desktop\MLProject
deploy-to-ecr.bat ml-project us-east-1 latest
```

### Option 2: Using Automated Script (Linux/Mac)

```bash
cd ~/MLProject
chmod +x deploy-to-ecr.sh
./deploy-to-ecr.sh ml-project us-east-1 latest
```

### Option 3: Manual Steps

```bash
# Set environment variables
$env:REPO_NAME = "ml-project"
$env:AWS_REGION = "us-east-1"
$env:AWS_ACCOUNT_ID = $(aws sts get-caller-identity --query Account --output text)
$env:ECR_REGISTRY = "$env:AWS_ACCOUNT_ID.dkr.ecr.$env:AWS_REGION.amazonaws.com"

# Create ECR repository
aws ecr create-repository `
  --repository-name $env:REPO_NAME `
  --region $env:AWS_REGION

# Build Docker image
docker build -t $env:REPO_NAME:latest .

# Tag for ECR
docker tag $env:REPO_NAME:latest $env:ECR_REGISTRY/$env:REPO_NAME:latest

# Authenticate with ECR
aws ecr get-login-password --region $env:AWS_REGION | docker login --username AWS --password-stdin $env:ECR_REGISTRY

# Push to ECR
docker push $env:ECR_REGISTRY/$env:REPO_NAME:latest
```

## EC2 Setup

### 1. Create EC2 Instance (AWS Console)

1. Go to EC2 Dashboard → Instances → Launch Instance
2. Choose Ubuntu 22.04 LTS AMI
3. Instance type: t2.micro (free tier) or t2.small for better performance
4. Configure Security Group:
   - SSH (22): Your IP or 0.0.0.0/0
   - HTTP (80): 0.0.0.0/0
   - Custom TCP (5000): 0.0.0.0/0
5. Create or select key pair
6. Launch instance

### 2. Note Instance Details
- Public IP/DNS: You'll use this to connect
- Key pair (.pem file): Store securely

### 3. Connect to EC2

```bash
# Set appropriate permissions on key file (Linux/Mac)
chmod 400 your-key-pair.pem

# SSH into instance (replace with your details)
ssh -i "your-key-pair.pem" ubuntu@your-ec2-public-ip

# For Amazon Linux
ssh -i "your-key-pair.pem" ec2-user@your-ec2-public-ip
```

## Deploy to EC2

### Option 1: Using Automated Script (Recommended)

On your EC2 instance:

```bash
# Download the deployment script
wget https://raw.githubusercontent.com/your-repo/deploy-to-ec2.sh
# Or copy the script from your local machine via SCP

chmod +x deploy-to-ec2.sh

# Run the deployment script
./deploy-to-ec2.sh 123456789 us-east-1 ml-project latest
```

Replace `123456789` with your AWS Account ID.

### Option 2: Manual Steps

```bash
# 1. Install Docker
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 2. Install AWS CLI
sudo apt-get install -y awscli

# 3. Configure AWS credentials (or use IAM role)
aws configure

# 4. Set environment variables
export AWS_ACCOUNT_ID="123456789"  # Replace
export AWS_REGION="us-east-1"
export REPO_NAME="ml-project"
export ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# 5. Authenticate with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# 6. Pull image from ECR
docker pull $ECR_REGISTRY/$REPO_NAME:latest

# 7. Run container
docker run -d \
  --name ml-app \
  -p 5000:5000 \
  --restart unless-stopped \
  $ECR_REGISTRY/$REPO_NAME:latest

# 8. Verify
docker ps
```

## Verification & Testing

### 1. Check Container Status

```bash
# On EC2
docker ps

# View logs
docker logs -f ml-app

# Get container IP
docker inspect ml-app | grep IPAddress
```

### 2. Test Application

In your browser:
```
http://your-ec2-public-ip:5000
```

Or from command line:
```bash
curl http://your-ec2-public-ip:5000
```

### 3. Access Prediction Endpoint

```bash
# GET prediction form
curl http://your-ec2-public-ip:5000/predictdata

# POST prediction (replace with actual values)
curl -X POST http://your-ec2-public-ip:5000/predictdata \
  -d "gender=male&race_ethnicity=group A&parental_level_of_education=bachelor%27s+degree&lunch=standard&test_preparation_course=completed&reading_score=80&writing_score=75"
```

## Production Recommendations

### 1. Use Application Load Balancer (ALB)
- Distributes traffic across multiple EC2 instances
- Handles SSL/TLS termination
- Better availability and scalability

### 2. Use Auto Scaling
- Automatically scales EC2 instances based on demand
- Ensures high availability

### 3. Use AWS Systems Manager
- Centralized management of EC2 instances
- View logs and system metrics
- Execute commands remotely

### 4. Enable CloudWatch Monitoring
- Monitor CPU, memory, disk usage
- Create alarms for issues
- View application logs

### 5. Use AWS Secrets Manager
- Store API keys, database credentials securely
- Rotate credentials automatically

### 6. Use RDS for Database
- Managed database service
- Automatic backups and patches
- High availability with Multi-AZ

## Troubleshooting

### Issue: Docker push fails with "Unauthorized"
```bash
# Re-authenticate with ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

### Issue: Cannot connect to application on EC2
1. Check Security Group allows port 5000
2. Verify container is running: `docker ps`
3. Check application logs: `docker logs ml-app`
4. Test from EC2: `curl localhost:5000`

### Issue: Container keeps restarting
```bash
# Check logs for errors
docker logs ml-app

# Run in foreground to debug
docker run -it $ECR_REGISTRY/$REPO_NAME:latest
```

### Issue: "No such file or directory" for model files
- Verify model files are copied in Dockerfile
- Check COPY commands in Dockerfile
- Rebuild image: `docker build --no-cache -t ml-project:latest .`

### Issue: AWS CLI not found on EC2
```bash
# Install AWS CLI
sudo apt-get install -y awscli

# Or for latest version
sudo apt-get install -y unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Issue: Permission denied when running docker commands
```bash
sudo usermod -aG docker $USER
# Then log out and log back in, or:
newgrp docker
```

## Quick Reference

```bash
# Get Account ID
aws sts get-caller-identity --query Account --output text

# List ECR repositories
aws ecr describe-repositories

# List images in repository
aws ecr list-images --repository-name ml-project

# Check EC2 instances
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress]'

# View container logs (last 100 lines)
docker logs --tail 100 ml-app

# Stop and remove container
docker stop ml-app
docker rm ml-app

# Remove image from EC2
docker rmi $ECR_REGISTRY/$REPO_NAME:latest
```

## Support Resources

- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
