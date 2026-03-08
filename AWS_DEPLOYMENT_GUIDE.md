# 🚀 AWS Deployment Guide - Soochna Setu AI

## Overview

This guide covers multiple AWS deployment options for your Next.js frontend and FastAPI backend.

---

## 📋 Prerequisites

1. **AWS Account** - Sign up at https://aws.amazon.com
2. **AWS CLI** - Install from https://aws.amazon.com/cli/
3. **Node.js & npm** - Already installed
4. **Python 3.8+** - Already installed
5. **Git** - For version control

---

## 🎯 Deployment Options

### Option 1: AWS Amplify (Easiest - Recommended for Frontend)

**Best for:** Quick deployment, automatic CI/CD, serverless

#### Steps:

1. **Prepare Your Code**
```cmd
cd soochna-setu-final\frontend
npm run build
```

2. **Push to GitHub**
```cmd
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/soochna-setu.git
git push -u origin main
```

3. **Deploy via AWS Amplify Console**
- Go to AWS Amplify Console: https://console.aws.amazon.com/amplify/
- Click "New app" → "Host web app"
- Connect your GitHub repository
- Select branch: `main`
- Build settings (auto-detected for Next.js):
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/.next
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
```
- Click "Save and deploy"

**Cost:** ~$0.01 per build minute, ~$0.15/GB served

---

### Option 2: AWS S3 + CloudFront (Static Export)

**Best for:** Low cost, high performance, static sites

#### Steps:

1. **Export Next.js as Static**

Update `next.config.js`:
```javascript
/** @type {import('next').Config} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
```

2. **Build Static Files**
```cmd
cd soochna-setu-final\frontend
npm run build
```

3. **Create S3 Bucket**
```cmd
aws s3 mb s3://soochna-setu-ai --region us-east-1
```

4. **Configure Bucket for Static Hosting**
```cmd
aws s3 website s3://soochna-setu-ai --index-document index.html --error-document 404.html
```

5. **Upload Files**
```cmd
aws s3 sync out/ s3://soochna-setu-ai --acl public-read
```

6. **Create CloudFront Distribution**
- Go to CloudFront Console
- Create distribution
- Origin: Your S3 bucket
- Enable HTTPS
- Set default root object: `index.html`

**Cost:** ~$0.023/GB + $0.01/10,000 requests

---

### Option 3: AWS EC2 (Full Control)

**Best for:** Custom configurations, both frontend and backend

#### Frontend Deployment:

1. **Launch EC2 Instance**
- Go to EC2 Console
- Launch Instance
- Choose: Ubuntu Server 22.04 LTS
- Instance type: t2.micro (free tier)
- Configure security group:
  - SSH (22) - Your IP
  - HTTP (80) - 0.0.0.0/0
  - HTTPS (443) - 0.0.0.0/0

2. **Connect to Instance**
```cmd
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Nginx
sudo apt install -y nginx

# Install PM2
sudo npm install -g pm2
```

4. **Upload Your Code**
```cmd
# On your local machine
scp -i your-key.pem -r soochna-setu-final ubuntu@your-ec2-ip:~/
```

5. **Build and Run**
```bash
# On EC2
cd ~/soochna-setu-final/frontend
npm install
npm run build
pm2 start npm --name "soochna-setu" -- start
pm2 save
pm2 startup
```

6. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/soochna-setu
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/soochna-setu /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Backend Deployment (FastAPI):

1. **Install Python Dependencies**
```bash
cd ~/soochna-setu-final/backend
sudo apt install -y python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Run with PM2**
```bash
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name "soochna-setu-api"
pm2 save
```

3. **Update Nginx for API**
```nginx
location /api {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

**Cost:** ~$8.50/month (t2.micro)

---

### Option 4: AWS Elastic Beanstalk

**Best for:** Managed deployment, auto-scaling

#### Frontend:

1. **Install EB CLI**
```cmd
pip install awsebcli
```

2. **Initialize**
```cmd
cd soochna-setu-final\frontend
eb init -p node.js soochna-setu-frontend --region us-east-1
```

3. **Create Environment**
```cmd
eb create soochna-setu-prod
```

4. **Deploy**
```cmd
eb deploy
```

#### Backend:

1. **Initialize**
```cmd
cd soochna-setu-final\backend
eb init -p python-3.9 soochna-setu-backend --region us-east-1
```

2. **Create Procfile**
```
web: uvicorn main:app --host 0.0.0.0 --port 8000
```

3. **Deploy**
```cmd
eb create soochna-setu-api
eb deploy
```

**Cost:** ~$25/month (t2.small)

---

### Option 5: AWS Lambda + API Gateway (Serverless)

**Best for:** Pay-per-use, auto-scaling, cost-effective

#### Using Vercel (Easiest for Next.js):

1. **Install Vercel CLI**
```cmd
npm i -g vercel
```

2. **Deploy**
```cmd
cd soochna-setu-final\frontend
vercel
```

3. **Production Deploy**
```cmd
vercel --prod
```

#### Backend with AWS Lambda:

1. **Install Serverless Framework**
```cmd
npm install -g serverless
```

2. **Create serverless.yml**
```yaml
service: soochna-setu-api

provider:
  name: aws
  runtime: python3.9
  region: us-east-1

functions:
  api:
    handler: main.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

3. **Update main.py**
```python
from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()

# Your routes here

handler = Mangum(app)
```

4. **Deploy**
```cmd
serverless deploy
```

**Cost:** Free tier: 1M requests/month, then $0.20/1M requests

---

## 🔒 Security Best Practices

1. **Environment Variables**
```bash
# Never commit secrets
# Use AWS Secrets Manager or Parameter Store
aws secretsmanager create-secret --name soochna-setu/api-key --secret-string "your-secret"
```

2. **HTTPS/SSL**
```bash
# Use AWS Certificate Manager (free)
# Or Let's Encrypt with Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

3. **Security Groups**
- Restrict SSH to your IP only
- Use VPC for backend
- Enable AWS WAF for DDoS protection

4. **IAM Roles**
- Use least privilege principle
- Create separate roles for frontend/backend
- Enable MFA for AWS console

---

## 📊 Monitoring & Logging

1. **CloudWatch**
```bash
# Enable CloudWatch logs
aws logs create-log-group --log-group-name /aws/soochna-setu
```

2. **Application Monitoring**
```bash
# Install CloudWatch agent on EC2
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb
```

3. **Set Up Alarms**
- CPU > 80%
- Memory > 80%
- HTTP 5xx errors
- Response time > 2s

---

## 💰 Cost Estimation

### Small Scale (< 10K users/month):
- **Amplify**: ~$5-10/month
- **S3 + CloudFront**: ~$1-5/month
- **EC2 t2.micro**: ~$8.50/month (free tier eligible)
- **Lambda**: ~$0-5/month (free tier)

### Medium Scale (10K-100K users/month):
- **EC2 t2.small**: ~$25/month
- **Elastic Beanstalk**: ~$30-50/month
- **Lambda + API Gateway**: ~$10-30/month

### Large Scale (100K+ users/month):
- **EC2 Auto Scaling**: ~$100-500/month
- **ECS/EKS**: ~$200-1000/month
- **Lambda**: ~$50-200/month

---

## 🚀 Recommended Setup for Hackathon

**Frontend:** AWS Amplify (easiest, automatic CI/CD)
**Backend:** AWS Lambda + API Gateway (serverless, cost-effective)
**Database:** AWS DynamoDB (if needed)
**Storage:** S3 (for documents)

### Quick Deploy Commands:

```cmd
# Frontend
cd soochna-setu-final\frontend
npm install -g @aws-amplify/cli
amplify init
amplify add hosting
amplify publish

# Backend
cd ..\backend
pip install mangum
serverless deploy
```

---

## 📝 Post-Deployment Checklist

- [ ] Test all pages load correctly
- [ ] Verify API endpoints work
- [ ] Check mobile responsiveness
- [ ] Test on different browsers
- [ ] Set up custom domain
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up monitoring/alerts
- [ ] Create backup strategy
- [ ] Document API endpoints
- [ ] Add rate limiting
- [ ] Enable caching (CloudFront)

---

## 🆘 Troubleshooting

### Issue: Build fails on Amplify
**Solution:** Check Node version in build settings, ensure all dependencies in package.json

### Issue: 502 Bad Gateway
**Solution:** Check backend is running, verify security group rules, check logs

### Issue: Slow loading
**Solution:** Enable CloudFront caching, optimize images, use CDN

### Issue: High costs
**Solution:** Enable auto-scaling down, use reserved instances, optimize Lambda memory

---

## 📚 Additional Resources

- AWS Free Tier: https://aws.amazon.com/free/
- Next.js Deployment: https://nextjs.org/docs/deployment
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- AWS Documentation: https://docs.aws.amazon.com/

---

## 🎓 For Hackathon Demo

**Quickest Option:**
1. Deploy frontend to Vercel (free): `vercel --prod`
2. Deploy backend to Render (free): https://render.com
3. Get live URLs in 5 minutes!

**Alternative:**
1. Use AWS Amplify for frontend (free tier)
2. Use AWS Lambda for backend (free tier)
3. Professional AWS setup for judges!

---

**Need help?** Contact AWS Support or check AWS documentation.

**Good luck with your hackathon! 🚀**
