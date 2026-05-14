# Quick Reference - AWS ECR & EC2 Commands

## One-Time Setup Commands

### AWS Account Setup
```bash
# Configure AWS CLI
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1), Output format (json)

# Verify configuration
aws sts get-caller-identity

# Get your AWS Account ID (save this!)
aws sts get-caller-identity --query Account --output text
```

### Create ECR Repository
```bash
aws ecr create-repository --repository-name ml-project --region us-east-1
```

## Local Machine - Build & Push to ECR

### Windows PowerShell
```powershell
# Set variables
$REPO_NAME = "ml-project"
$AWS_REGION = "us-east-1"
$AWS_ACCOUNT_ID = "123456789"  # Replace with your account ID
$ECR_REGISTRY = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# Build image
docker build -t $REPO_NAME:latest .

# Tag for ECR
docker tag $REPO_NAME:latest $ECR_REGISTRY/$REPO_NAME:latest

# Authenticate with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Push to ECR
docker push $ECR_REGISTRY/$REPO_NAME:latest
```

### Linux/Mac Bash
```bash
# Set variables
export REPO_NAME="ml-project"
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID="123456789"  # Replace with your account ID
export ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# Build image
docker build -t $REPO_NAME:latest .

# Tag for ECR
docker tag $REPO_NAME:latest $ECR_REGISTRY/$REPO_NAME:latest

# Authenticate with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Push to ECR
docker push $ECR_REGISTRY/$REPO_NAME:latest
```

## EC2 Instance - Deploy Application

### SSH Connection
```bash
# Connect to EC2 (replace with your details)
ssh -i "your-key-pair.pem" ubuntu@your-ec2-public-ip

# For Amazon Linux
ssh -i "your-key-pair.pem" ec2-user@your-ec2-public-ip

# Or run the deployment script
./deploy-to-ec2.sh 123456789 us-east-1 ml-project latest
```

### Manual Deployment on EC2
```bash
# Set variables (on EC2 instance)
export AWS_ACCOUNT_ID="123456789"
export AWS_REGION="us-east-1"
export REPO_NAME="ml-project"
export ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
export IMAGE_NAME="$ECR_REGISTRY/$REPO_NAME:latest"

# Authenticate with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Pull image
docker pull $IMAGE_NAME

# Run container
docker run -d \
  --name ml-app \
  -p 5000:5000 \
  --restart unless-stopped \
  $IMAGE_NAME

# Verify
docker ps
```

## Container Management Commands

### View Container Status
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Get detailed container info
docker inspect ml-app

# View container logs
docker logs ml-app

# View last 100 lines of logs
docker logs --tail 100 ml-app

# Follow logs in real-time
docker logs -f ml-app

# View container resource usage
docker stats ml-app
```

### Container Control
```bash
# Stop container
docker stop ml-app

# Start container
docker start ml-app

# Restart container
docker restart ml-app

# Remove container
docker rm ml-app

# Kill container (force stop)
docker kill ml-app
```

### Image Management
```bash
# List images
docker images

# Remove image
docker rmi $ECR_REGISTRY/$REPO_NAME:latest

# Remove unused images and containers
docker system prune

# Remove all dangling images
docker image prune
```

## ECR Management Commands

### ECR Repository Operations
```bash
# List all ECR repositories
aws ecr describe-repositories

# List images in repository
aws ecr list-images --repository-name ml-project

# Get repository details
aws ecr describe-repositories --repository-names ml-project

# Delete repository
aws ecr delete-repository --repository-name ml-project --force

# Get authorization token
aws ecr get-authorization-token --region us-east-1
```

### Push New Version
```bash
# Build new version
docker build -t $REPO_NAME:v2.0 .

# Tag for ECR
docker tag $REPO_NAME:v2.0 $ECR_REGISTRY/$REPO_NAME:v2.0

# Push new version
docker push $ECR_REGISTRY/$REPO_NAME:v2.0

# On EC2: Pull and run new version
docker pull $ECR_REGISTRY/$REPO_NAME:v2.0
docker stop ml-app
docker rm ml-app
docker run -d --name ml-app -p 5000:5000 $ECR_REGISTRY/$REPO_NAME:v2.0
```

## EC2 Management Commands

### SSH Operations
```bash
# List EC2 instances
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress,PrivateIpAddress]'

# Get instance public IP
aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --query 'Reservations[0].Instances[0].PublicIpAddress'

# Copy file to EC2 (from local machine)
scp -i "key.pem" deploy-to-ec2.sh ubuntu@your-ec2-ip:/home/ubuntu/

# Copy file from EC2 (to local machine)
scp -i "key.pem" ubuntu@your-ec2-ip:/home/ubuntu/logs.txt ./
```

### EC2 Instance Control
```bash
# Stop instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Reboot instance
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# Terminate instance (delete)
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

### Security Group Management
```bash
# List security groups
aws ec2 describe-security-groups --query 'SecurityGroups[].[GroupId,GroupName,IpPermissions]'

# Allow port 5000 inbound from anywhere
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --protocol tcp \
  --port 5000 \
  --cidr 0.0.0.0/0

# Revoke port 5000 inbound
aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --protocol tcp \
  --port 5000 \
  --cidr 0.0.0.0/0
```

## Testing & Verification

### Local Testing
```bash
# Build locally
docker build -t ml-project:latest .

# Run locally
docker run -p 5000:5000 ml-project:latest

# Test in another terminal
curl http://localhost:5000

# Test prediction endpoint
curl -X POST http://localhost:5000/predictdata \
  -d "gender=male&race_ethnicity=group+A&parental_level_of_education=bachelor%27s+degree&lunch=standard&test_preparation_course=completed&reading_score=80&writing_score=75"
```

### Remote Testing (from local machine)
```bash
# Test application is running
curl http://your-ec2-public-ip:5000

# Test prediction endpoint
curl http://your-ec2-public-ip:5000/predictdata

# Check if port 5000 is open
netstat -an | grep 5000  # Linux/Mac
netstat -an | findstr 5000  # Windows
```

### On EC2 Instance
```bash
# Test locally on EC2
curl localhost:5000

# Check port is listening
netstat -tlnp | grep 5000

# Check docker network
docker network ls

# Check DNS resolution
nslookup google.com
```

## Troubleshooting Commands

### Docker Issues
```bash
# Check Docker daemon status
sudo systemctl status docker

# Start Docker
sudo systemctl start docker

# View Docker system info
docker system info

# Check Docker logs
sudo journalctl -u docker -n 50

# Clean up Docker
docker system prune -a
```

### Network Issues
```bash
# Check network connectivity
ping google.com

# Check DNS
nslookup 8.8.8.8

# Check open ports
sudo netstat -tlnp

# Check firewall rules
sudo ufw status
```

### AWS Credentials Issues
```bash
# Check configured credentials
aws sts get-caller-identity

# Check credentials file location
cat ~/.aws/credentials

# Check configuration
cat ~/.aws/config

# Reconfigure
aws configure --profile default
```

### Container Issues
```bash
# Check container environment variables
docker exec ml-app env

# Check container networking
docker exec ml-app ifconfig

# Check container file system
docker exec ml-app ls -la /app

# Execute command in running container
docker exec ml-app python --version

# Run shell in container
docker exec -it ml-app /bin/bash
```

## Performance & Monitoring

### Docker Stats
```bash
# Real-time container stats
docker stats

# Specific container stats
docker stats ml-app

# Get container resource limits
docker inspect ml-app | grep -i memory
```

### CloudWatch (AWS Console)
```bash
# View CloudWatch metrics
aws cloudwatch list-metrics --namespace AWS/EC2

# Get metric statistics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 300 \
  --statistics Average
```

## Common Issues & Solutions

### "Cannot connect to Docker daemon"
```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
```

### "Unauthorized" when pushing to ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

### Container keeps crashing
```bash
docker logs ml-app  # Check error messages
docker run -it $IMAGE_NAME  # Run interactively
```

### Cannot SSH to EC2
```bash
# Check key permissions
chmod 400 your-key-pair.pem

# Try verbose SSH
ssh -vvv -i "key.pem" ubuntu@ec2-ip
```

## Useful Links

- Save your AWS Account ID: `___________________`
- Save your EC2 public IP: `___________________`
- Save your ECR repository URL: `___________________`
- Save your EC2 instance ID: `___________________`
- Key pair file location: `___________________`
