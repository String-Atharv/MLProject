# ECR & EC2 Deployment Checklist

Use this checklist to track your progress through the deployment process.

## Phase 1: Prerequisites & Setup

### Local Environment
- [ ] Docker Desktop installed and running
- [ ] AWS CLI v2 installed
- [ ] Git installed (optional)
- [ ] Docker test successful (`docker --version`)
- [ ] AWS CLI configured (`aws configure`)

### AWS Account
- [ ] AWS Account created and active
- [ ] IAM user created with appropriate permissions
- [ ] Access Keys generated (save securely!)
- [ ] AWS CLI credentials configured locally
- [ ] AWS credentials verified (`aws sts get-caller-identity`)

### EC2 Instance
- [ ] EC2 instance created and running
- [ ] Security Group configured:
  - [ ] SSH (22) access enabled for your IP
  - [ ] HTTP (80) open for web traffic
  - [ ] TCP (5000) open for Flask app
- [ ] Key pair (.pem file) saved securely
- [ ] Note public IP address: `___________________`

## Phase 2: Local Testing

### Docker Build Test
- [ ] Navigate to project directory
- [ ] Run `docker build -t ml-project:latest .` successfully
- [ ] Run `docker run -p 5000:5000 ml-project:latest`
- [ ] Test locally: http://localhost:5000
- [ ] Verify app loads without errors
- [ ] Stop container (`docker stop <id>`)

### Docker Image Verification
- [ ] Image appears in `docker images` output
- [ ] Image size is reasonable (not bloated)
- [ ] All required files are in image

## Phase 3: ECR Setup

### Create ECR Repository
- [ ] Logged in to AWS Console
- [ ] Navigated to ECR service
- [ ] Created repository named: `ml-project`
- [ ] Region: `___________________`
- [ ] Account ID: `___________________`

### Alternative: Create via AWS CLI
```bash
aws ecr create-repository --repository-name ml-project --region us-east-1
```
- [ ] Repository created successfully

## Phase 4: Build and Push to ECR

### Using Windows Script (Recommended)
```batch
deploy-to-ecr.bat ml-project us-east-1 latest
```

### Manual Steps (if not using script)
- [ ] Set environment variables:
  - REPO_NAME = ml-project
  - AWS_REGION = us-east-1
  - AWS_ACCOUNT_ID = `___________________`
  - ECR_REGISTRY = $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

- [ ] Build image: `docker build -t ml-project:latest .`
- [ ] Tag for ECR: `docker tag ml-project:latest $ECR_REGISTRY/ml-project:latest`
- [ ] Get ECR login token: `aws ecr get-login-password --region us-east-1`
- [ ] Authenticate docker: (pipe login command)
- [ ] Push to ECR: `docker push $ECR_REGISTRY/ml-project:latest`
- [ ] Verify in ECR console (image appears in repository)

### Verification
- [ ] Image pushed to ECR successfully
- [ ] Image visible in ECR console
- [ ] Image tagged as 'latest'
- [ ] Image size matches expected size

## Phase 5: EC2 Preparation

### Connect to EC2
- [ ] Open terminal/PowerShell
- [ ] Navigate to directory with key pair (.pem file)
- [ ] Connect via SSH:
  ```bash
  ssh -i "your-key-pair.pem" ubuntu@your-ec2-public-ip
  ```
- [ ] Successfully logged into EC2 instance

### Verify EC2 Environment
- [ ] Check OS: `cat /etc/os-release` or `lsb_release -a`
- [ ] Check network: `curl ifconfig.me` (should return public IP)
- [ ] Check available storage: `df -h`

## Phase 6: Deploy to EC2

### Using Automated Script (Recommended)
- [ ] Copy deploy-to-ec2.sh to EC2 instance (via SCP or manually)
- [ ] Make executable: `chmod +x deploy-to-ec2.sh`
- [ ] Run script: `./deploy-to-ec2.sh 123456789 us-east-1 ml-project latest`
  - Replace 123456789 with your AWS Account ID
- [ ] Script completed successfully
- [ ] Container is running

### Manual Steps (if not using script)
- [ ] Install Docker: `sudo apt-get update && sudo apt-get install -y docker.io`
- [ ] Start Docker: `sudo systemctl start docker && sudo systemctl enable docker`
- [ ] Add user to docker group: `sudo usermod -aG docker $USER`
- [ ] Exit and re-login to EC2
- [ ] Install AWS CLI: `sudo apt-get install -y awscli`
- [ ] Configure AWS credentials: `aws configure`
- [ ] Authenticate with ECR: (run login command)
- [ ] Pull image: `docker pull $ECR_REGISTRY/ml-project:latest`
- [ ] Run container: `docker run -d --name ml-app -p 5000:5000 $ECR_REGISTRY/ml-project:latest`

### Verification
- [ ] Check container running: `docker ps`
- [ ] Container name is 'ml-app'
- [ ] Port mapping shows 5000:5000
- [ ] Container status is 'Up'
- [ ] No errors in `docker logs ml-app`

## Phase 7: Application Testing

### Browser Testing
- [ ] Access application: http://<EC2-PUBLIC-IP>:5000
- [ ] Homepage loads successfully
- [ ] Navigation works
- [ ] No SSL/security warnings

### API Testing
- [ ] Test prediction endpoint: http://<EC2-PUBLIC-IP>:5000/predictdata
- [ ] Form appears correctly
- [ ] Submit prediction (test with sample values)
- [ ] Prediction result displays

### Container Health
- [ ] View logs: `docker logs ml-app`
- [ ] Check resource usage: `docker stats ml-app`
- [ ] Verify no errors in logs
- [ ] Application is responsive

## Phase 8: Production Hardening

### Security
- [ ] Review Security Group rules (restrict as needed)
- [ ] Update inbound rules to specific IPs if possible
- [ ] Remove unnecessary Security Group rules
- [ ] Consider adding HTTPS (use ALB or Nginx reverse proxy)

### Monitoring
- [ ] Enable CloudWatch monitoring for EC2 instance
- [ ] Create CloudWatch alarms for CPU/Memory
- [ ] Enable detailed monitoring
- [ ] Test alarm notifications

### Updates & Maintenance
- [ ] Set up auto-updates for EC2 instance
- [ ] Document model file locations
- [ ] Set up backup strategy
- [ ] Document troubleshooting procedures

## Phase 9: Documentation

### Project Documentation
- [ ] Update README.md with AWS deployment info
- [ ] Document environment variables needed
- [ ] Create runbook for common tasks
- [ ] Document how to update the application

### Important Information to Save
- [ ] EC2 Instance ID: `___________________`
- [ ] EC2 Public IP: `___________________`
- [ ] ECR Repository URI: `___________________`
- [ ] AWS Region: `___________________`
- [ ] Key pair file location: `___________________`

## Phase 10: Future Improvements

### Consider Implementing
- [ ] Auto Scaling Group for multiple EC2 instances
- [ ] Application Load Balancer for traffic distribution
- [ ] RDS for persistent database (if needed)
- [ ] S3 for model storage and versioning
- [ ] CloudFormation for Infrastructure as Code
- [ ] CodePipeline for CI/CD automation
- [ ] CloudWatch Logs for centralized logging

## Quick Troubleshooting Reference

### Container won't start
```bash
docker logs ml-app              # Check error messages
docker run -it $IMAGE_NAME      # Run interactively to debug
```

### Cannot connect to application
```bash
# From EC2:
curl localhost:5000             # Test locally
docker ps                       # Verify container is running
sudo iptables -L                # Check firewall rules
```

### AWS CLI not working
```bash
aws sts get-caller-identity     # Verify credentials
aws ec2 describe-instances      # Test AWS access
```

### Docker push fails
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY
docker push $IMAGE_NAME          # Try push again
```

## Support & Resources

- **AWS Documentation**: https://docs.aws.amazon.com/
- **Docker Documentation**: https://docs.docker.com/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **AWS Support**: https://aws.amazon.com/support/

---

**Last Updated**: 2026-05-13
**Project**: ML Project - Student Performance Prediction
**Deployment Type**: Docker on ECR and EC2
