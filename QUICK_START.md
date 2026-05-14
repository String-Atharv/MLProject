# ML Project AWS Deployment - Quick Start

Welcome! This document will get you up and running with deploying your ML project to AWS ECR and EC2 in the fastest way possible.

## 📋 What You Need

Before starting, make sure you have:
1. **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop)
2. **AWS CLI v2** - [Download](https://aws.amazon.com/cli/)
3. **AWS Account** with billing enabled
4. **EC2 Key Pair** (.pem file) saved on your computer
5. **Running EC2 Instance** (Ubuntu 22.04 recommended)

## 🚀 Quick Start (5 Steps)

### Step 1: Configure AWS (5 minutes)

```bash
# Configure AWS credentials
aws configure

# When prompted, enter:
# - AWS Access Key ID: [from IAM user]
# - AWS Secret Access Key: [from IAM user]
# - Default region: us-east-1
# - Default output format: json

# Verify it works
aws sts get-caller-identity
```

### Step 2: Get Your AWS Account ID (1 minute)

```bash
# This is important - save this number!
aws sts get-caller-identity --query Account --output text
# Output: 123456789 (save this)
```

### Step 3: Build & Push to ECR (10 minutes)

**Option A: Windows (Easiest)**
```bash
cd C:\Users\atharvshivale\Desktop\MLProject
deploy-to-ecr.bat ml-project us-east-1 latest
```

**Option B: Linux/Mac**
```bash
cd ~/MLProject
chmod +x deploy-to-ecr.sh
./deploy-to-ecr.sh ml-project us-east-1 latest
```

**Option C: Manual (if scripts don't work)**
```bash
# Set your account ID
$AWS_ACCOUNT_ID = "123456789"  # Replace with your actual ID
$AWS_REGION = "us-east-1"

# Build
docker build -t ml-project:latest .

# Tag
docker tag ml-project:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ml-project:latest

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Push
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ml-project:latest
```

### Step 4: Connect to EC2 & Deploy (10 minutes)

Open PowerShell or Terminal and connect to your EC2 instance:

```bash
# Replace with your EC2 details
ssh -i "your-key-pair.pem" ubuntu@your-ec2-public-ip

# Once connected, run the deployment script:
./deploy-to-ec2.sh 123456789 us-east-1 ml-project latest
# Replace 123456789 with your AWS Account ID
```

**Not on EC2 yet?** First copy the script there:
```bash
scp -i "your-key-pair.pem" deploy-to-ec2.sh ubuntu@your-ec2-public-ip:/home/ubuntu/
```

### Step 5: Test Your Application (2 minutes)

Open your browser and visit:
```
http://your-ec2-public-ip:5000
```

You should see your ML application!

## 📁 Documentation Files

Here's what each file is for:

| File | Purpose |
|------|---------|
| **DEPLOYMENT_GUIDE.md** | Comprehensive step-by-step guide (read this first if you're new) |
| **AWS_SETUP_GUIDE.md** | Detailed setup instructions for all prerequisites |
| **DEPLOYMENT_CHECKLIST.md** | Checklist to track your progress |
| **QUICK_REFERENCE.md** | Quick command reference for common tasks |
| **deploy-to-ecr.bat** | Automated Windows script to build and push to ECR |
| **deploy-to-ecr.sh** | Automated Linux/Mac script to build and push to ECR |
| **deploy-to-ec2.sh** | Automated Linux script to deploy on EC2 instance |
| **Dockerfile** | Container definition (already updated) |
| **Dockerfile.prod** | Production-ready Dockerfile with health checks |

## 🎯 Typical Workflow

```
1. Local Development
   └─ Test Docker image locally
   
2. Push to ECR
   └─ Run deploy-to-ecr.bat (or .sh)
   
3. Deploy to EC2
   └─ SSH to EC2 instance
   └─ Run deploy-to-ec2.sh
   
4. Test Application
   └─ Visit http://your-ec2-ip:5000
   
5. Monitor & Maintain
   └─ View logs: docker logs -f ml-app
   └─ Check health: docker ps
```

## ⚠️ Important Notes

### AWS Account ID
Your AWS Account ID is a 12-digit number. Find it in AWS Console or run:
```bash
aws sts get-caller-identity --query Account --output text
```

### EC2 Security Group
Make sure your EC2 Security Group allows:
- **SSH (22)**: For connecting to EC2
- **Port 5000**: For accessing the Flask app

### Cost Awareness
- EC2 t2.micro is free-tier eligible (1 year)
- ECR: $0.10 per GB stored, $0.09 per GB transferred
- Monitor your AWS costs regularly!

### Environment Variables
Replace these in commands with your actual values:
- `123456789` → Your AWS Account ID
- `us-east-1` → Your AWS region
- `your-ec2-public-ip` → Your EC2 instance public IP
- `your-key-pair.pem` → Your EC2 key pair file

## ✅ Verification Checklist

After deployment, verify:
- [ ] Docker image built successfully
- [ ] Image pushed to ECR
- [ ] Container running on EC2: `docker ps`
- [ ] Application accessible: http://your-ec2-ip:5000
- [ ] No errors in logs: `docker logs ml-app`

## 🆘 Troubleshooting

### Docker image fails to build
```bash
# Verify Docker is running
docker --version

# Check if all required files are present
ls -la requirements.txt
ls -la application.py
ls -la Dockerfile
```

### Cannot authenticate with ECR
```bash
# Re-authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Check AWS credentials
aws sts get-caller-identity
```

### Cannot SSH to EC2
```bash
# Verify key file has correct permissions
chmod 400 your-key-pair.pem

# Check security group allows SSH (port 22)
# Verify you're using the correct public IP
```

### Application not loading
```bash
# Check if container is running
docker ps

# View container logs
docker logs ml-app

# Test container connectivity
docker exec ml-app curl localhost:5000

# Check if Security Group allows port 5000
```

## 📚 Next Steps

1. **Read DEPLOYMENT_GUIDE.md** - Comprehensive step-by-step instructions
2. **Follow DEPLOYMENT_CHECKLIST.md** - Track your progress
3. **Reference QUICK_REFERENCE.md** - For common commands
4. **Use AWS_SETUP_GUIDE.md** - If you need detailed setup help

## 🎓 Learning Resources

- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/deployment/)

## 💡 Pro Tips

1. **Use IAM Roles on EC2** - Better than hardcoding credentials
2. **Set up Auto-Scaling** - Scale EC2 instances automatically
3. **Use Application Load Balancer** - Distribute traffic across instances
4. **Enable CloudWatch** - Monitor CPU, memory, logs
5. **Use RDS** - For persistent database if needed
6. **Set up CI/CD** - Automate deployment with CodePipeline

## 📞 Support

If you get stuck:
1. Check the QUICK_REFERENCE.md for command syntax
2. Review TROUBLESHOOTING section in DEPLOYMENT_GUIDE.md
3. Check AWS documentation links above
4. Verify all prerequisites are installed correctly

---

**Ready to deploy?** Start with Step 1 above!

For detailed information, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
