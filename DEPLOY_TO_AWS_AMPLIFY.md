# 🚀 Deploy to AWS Amplify - Step by Step Guide

## Why AWS Amplify?

✅ **Lowest Cost**: Free tier includes 1000 build minutes/month + 15GB served/month
✅ **Easiest**: No server management, automatic deployments
✅ **Efficient**: Built-in CDN, auto-scaling, HTTPS included
✅ **Fast**: Deploy in 10 minutes

**Cost**: $0 for first month (free tier), then ~$5-10/month for small traffic

---

## 📋 Prerequisites

1. AWS Account (create at https://aws.amazon.com if you don't have one)
2. GitHub account
3. Your project code

---

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Project

1. **Update next.config.js** (if not already done)

Create/update `soochna-setu-final/frontend/next.config.js`:

```javascript
/** @type {import('next').Config} */
const nextConfig = {
  // Add any custom config here
}

module.exports = nextConfig
```

2. **Test Build Locally**

```cmd
cd soochna-setu-final\frontend
npm install
npm run build
```

If build succeeds, you're ready!

---

### Step 2: Push to GitHub

1. **Initialize Git** (if not done)

```cmd
cd C:\PROJECTS\AI BHARAT 2\soochna-setu-final
git init
```

2. **Create .gitignore**

```cmd
echo node_modules/ > .gitignore
echo .next/ >> .gitignore
echo .env.local >> .gitignore
echo dist/ >> .gitignore
echo __pycache__/ >> .gitignore
```

3. **Commit Your Code**

```cmd
git add .
git commit -m "Initial commit - Soochna Setu AI"
```

4. **Create GitHub Repository**

- Go to https://github.com/new
- Repository name: `soochna-setu-ai`
- Make it Public (for free hosting)
- Don't initialize with README
- Click "Create repository"

5. **Push to GitHub**

```cmd
git remote add origin https://github.com/YOUR_USERNAME/soochna-setu-ai.git
git branch -M main
git push -u origin main
```

---

### Step 3: Deploy on AWS Amplify Console

1. **Go to AWS Amplify Console**

Open: https://console.aws.amazon.com/amplify/

2. **Click "New app" → "Host web app"**

3. **Connect GitHub**

- Select "GitHub"
- Click "Continue"
- Authorize AWS Amplify to access your GitHub
- Select your repository: `soochna-setu-ai`
- Select branch: `main`
- Click "Next"

4. **Configure Build Settings**

Amplify will auto-detect Next.js. Update the build settings:

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

**App name**: `soochna-setu-ai`

Click "Next"

5. **Review and Deploy**

- Review all settings
- Click "Save and deploy"

6. **Wait for Deployment** (5-10 minutes)

You'll see:
- ✅ Provision
- ✅ Build
- ✅ Deploy
- ✅ Verify

---

### Step 4: Access Your Live Website

Once deployed, you'll get a URL like:
```
https://main.d1234abcd.amplifyapp.com
```

**Your website is now LIVE! 🎉**

---

## 🌐 Add Custom Domain (Optional)

1. **In Amplify Console**, go to "Domain management"
2. Click "Add domain"
3. Enter your domain (e.g., `soochna-setu.com`)
4. Follow DNS configuration steps
5. Wait for SSL certificate (automatic, free)

---

## 🔄 Automatic Deployments

Every time you push to GitHub:

```cmd
git add .
git commit -m "Update feature"
git push
```

AWS Amplify will automatically:
1. Detect the change
2. Build your app
3. Deploy the new version
4. Update your live site

**No manual deployment needed!**

---

## 💰 Cost Breakdown

### Free Tier (First 12 months):
- ✅ 1,000 build minutes/month
- ✅ 15 GB served/month
- ✅ 5 GB storage

### After Free Tier:
- Build: $0.01 per build minute
- Hosting: $0.15 per GB served
- Storage: $0.023 per GB/month

**Example Cost for Small Traffic:**
- 10 builds/month (5 min each) = 50 min = $0.50
- 10 GB served = $1.50
- **Total: ~$2/month**

**For Hackathon Demo:**
- Completely FREE (within free tier limits)

---

## 📊 Monitor Your App

1. **Go to Amplify Console**
2. Select your app
3. View:
   - Build history
   - Traffic metrics
   - Error logs
   - Performance

---

## 🔧 Environment Variables (If Needed)

1. In Amplify Console, go to "Environment variables"
2. Add variables:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-api-url.com`
3. Redeploy

---

## 🐛 Troubleshooting

### Build Fails?

**Check build logs in Amplify Console**

Common fixes:

1. **Node version issue**
   - Add to build settings:
   ```yaml
   preBuild:
     commands:
       - nvm use 18
       - cd frontend
       - npm ci
   ```

2. **Module not found**
   ```cmd
   # Locally
   cd frontend
   npm install
   git add package-lock.json
   git commit -m "Update dependencies"
   git push
   ```

3. **Build timeout**
   - Increase timeout in Amplify settings
   - Or optimize your build

### Site not loading?

1. Check build completed successfully
2. Clear browser cache
3. Check Amplify URL is correct
4. Wait 2-3 minutes for CDN propagation

---

## 🚀 Deploy Backend (Optional)

For your FastAPI backend, use **AWS Lambda** (also free tier):

### Quick Backend Deploy:

1. **Install Serverless Framework**
```cmd
npm install -g serverless
```

2. **In backend folder, create serverless.yml**
```yaml
service: soochna-setu-api

provider:
  name: aws
  runtime: python3.9
  region: us-east-1

functions:
  api:
    handler: wsgi_handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
```

3. **Create wsgi_handler.py**
```python
from mangum import Mangum
from main import app

handler = Mangum(app)
```

4. **Install dependencies**
```cmd
pip install mangum
```

5. **Deploy**
```cmd
serverless deploy
```

You'll get an API URL like:
```
https://abc123.execute-api.us-east-1.amazonaws.com/dev
```

---

## ✅ Final Checklist

- [ ] Code pushed to GitHub
- [ ] AWS Amplify connected to GitHub
- [ ] Build completed successfully
- [ ] Website accessible via Amplify URL
- [ ] All pages working correctly
- [ ] Mobile responsive
- [ ] HTTPS enabled (automatic)

---

## 🎓 For Hackathon Presentation

**Show judges:**

1. **Live URL**: Your Amplify URL
2. **AWS Console**: Show Amplify dashboard
3. **Auto-deployment**: Push a change, show it auto-deploys
4. **Metrics**: Show traffic/performance metrics
5. **Cost**: Mention it's on AWS free tier

**Impressive points:**
- ✅ Deployed on AWS (professional)
- ✅ Auto-scaling (handles any traffic)
- ✅ HTTPS/SSL (secure)
- ✅ CDN (fast globally)
- ✅ CI/CD (automatic deployments)

---

## 📞 Need Help?

**AWS Support:**
- Free tier support: https://console.aws.amazon.com/support/
- Amplify docs: https://docs.amplify.aws/

**Common Issues:**
- Build fails → Check Node version
- 404 errors → Check build artifacts path
- Slow loading → Enable caching in Amplify settings

---

## 🎉 You're Done!

Your Soochna Setu AI is now:
- ✅ Live on AWS
- ✅ Automatically deploying
- ✅ Globally distributed (CDN)
- ✅ Secure (HTTPS)
- ✅ Scalable (auto-scaling)
- ✅ Cost-effective (free tier)

**Share your live URL with judges and users!**

---

## 📝 Quick Commands Reference

```cmd
# Local development
cd soochna-setu-final\frontend
npm run dev

# Build locally
npm run build

# Push updates
git add .
git commit -m "Your message"
git push

# That's it! Amplify auto-deploys
```

---

**Deployment Time: ~10 minutes**
**Cost: $0 (free tier) to $5/month**
**Difficulty: Easy ⭐⭐☆☆☆**

**Good luck with your hackathon! 🚀**
