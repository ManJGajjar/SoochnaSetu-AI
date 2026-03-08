# 🚀 Deploy to AWS S3 + CloudFront - Complete Guide

## Why S3 + CloudFront?

✅ **Cheapest**: ~$1-3/month (cheapest AWS option)
✅ **Fast**: Global CDN with CloudFront
✅ **Scalable**: Handles millions of users
✅ **Reliable**: 99.99% uptime SLA

**Cost**: ~$1-3/month for small traffic

---

## 📋 Prerequisites

1. AWS Account (create at https://aws.amazon.com)
2. AWS CLI installed
3. Your Next.js project

---

## 🎯 Step-by-Step Deployment

### Step 1: Configure Next.js for Static Export

1. **Update `next.config.js`**

Open `soochna-setu-final/frontend/next.config.js` and replace with:

```javascript
/** @type {import('next').Config} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}

module.exports = nextConfig
```

2. **Update `package.json` (add export script)**

Add this to scripts section:

```json
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint",
  "export": "next build"
}
```

---

### Step 2: Build Static Files

```cmd
cd soochna-setu-final\frontend
npm install
npm run build
```

This creates an `out` folder with static files.

**Verify**: Check that `out` folder exists with HTML files.

---

### Step 3: Install AWS CLI (if not installed)

**Download and install:**
- Windows: https://awscli.amazonaws.com/AWSCLIV2.msi
- Run the installer

**Verify installation:**
```cmd
aws --version
```

Should show: `aws-cli/2.x.x`

---

### Step 4: Configure AWS CLI

```cmd
aws configure
```

Enter:
- **AWS Access Key ID**: (from AWS Console → IAM → Users → Security credentials)
- **AWS Secret Access Key**: (from same place)
- **Default region**: `us-east-1` (or your preferred region)
- **Default output format**: `json`

**To get Access Keys:**
1. Go to AWS Console: https://console.aws.amazon.com/
2. Click your name (top right) → Security credentials
3. Scroll to "Access keys"
4. Click "Create access key"
5. Download and save the keys

---

### Step 5: Create S3 Bucket

**Option A: Using AWS CLI**

```cmd
aws s3 mb s3://soochna-setu-ai --region us-east-1
```

**Option B: Using AWS Console**

1. Go to S3 Console: https://s3.console.aws.amazon.com/
2. Click "Create bucket"
3. Bucket name: `soochna-setu-ai` (must be globally unique)
4. Region: `us-east-1`
5. Uncheck "Block all public access"
6. Check "I acknowledge..."
7. Click "Create bucket"

---

### Step 6: Enable Static Website Hosting

**Using AWS Console:**

1. Click on your bucket name
2. Go to "Properties" tab
3. Scroll to "Static website hosting"
4. Click "Edit"
5. Enable "Static website hosting"
6. Index document: `index.html`
7. Error document: `404.html`
8. Click "Save changes"

**Note the endpoint URL** (e.g., `http://soochna-setu-ai.s3-website-us-east-1.amazonaws.com`)

---

### Step 7: Set Bucket Policy (Make Public)

1. Go to "Permissions" tab
2. Scroll to "Bucket policy"
3. Click "Edit"
4. Paste this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::soochna-setu-ai/*"
    }
  ]
}
```

**Replace `soochna-setu-ai` with your bucket name**

5. Click "Save changes"

---

### Step 8: Upload Files to S3

**Using AWS CLI:**

```cmd
cd soochna-setu-final\frontend
aws s3 sync out/ s3://soochna-setu-ai --delete
```

**Using AWS Console:**

1. Go to your bucket
2. Click "Upload"
3. Drag and drop all files from `out` folder
4. Click "Upload"

**Verify**: Your site should now be accessible at the S3 website endpoint!

---

### Step 9: Create CloudFront Distribution (CDN)

**Why CloudFront?**
- Makes your site fast globally
- Provides HTTPS/SSL
- Caches content
- Custom domain support

**Steps:**

1. Go to CloudFront Console: https://console.aws.amazon.com/cloudfront/
2. Click "Create distribution"
3. **Origin settings:**
   - Origin domain: Select your S3 bucket
   - Origin path: (leave empty)
   - Name: (auto-filled)
   - Origin access: "Public"

4. **Default cache behavior:**
   - Viewer protocol policy: "Redirect HTTP to HTTPS"
   - Allowed HTTP methods: "GET, HEAD, OPTIONS"
   - Cache policy: "CachingOptimized"

5. **Settings:**
   - Price class: "Use all edge locations" (or choose based on your region)
   - Alternate domain name (CNAME): (leave empty for now, add custom domain later)
   - SSL certificate: "Default CloudFront certificate"
   - Default root object: `index.html`

6. Click "Create distribution"

**Wait 5-15 minutes** for deployment to complete.

---

### Step 10: Configure Error Pages (Important for Next.js)

1. In CloudFront, click on your distribution
2. Go to "Error pages" tab
3. Click "Create custom error response"
4. **For 403 errors:**
   - HTTP error code: `403`
   - Customize error response: Yes
   - Response page path: `/404.html`
   - HTTP response code: `404`
   - Click "Create"

5. **For 404 errors:**
   - HTTP error code: `404`
   - Customize error response: Yes
   - Response page path: `/404.html`
   - HTTP response code: `404`
   - Click "Create"

---

### Step 11: Test Your Website

**Your site is now live!**

CloudFront URL: `https://d1234abcdef.cloudfront.net`

Test:
- Homepage loads
- All pages work
- Images load
- Links work
- Mobile responsive

---

## 🔄 Update Your Website (Deploy Changes)

Whenever you make changes:

```cmd
# 1. Build new version
cd soochna-setu-final\frontend
npm run build

# 2. Upload to S3
aws s3 sync out/ s3://soochna-setu-ai --delete

# 3. Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

**To get Distribution ID:**
- Go to CloudFront Console
- Copy the ID from your distribution (e.g., `E1234ABCDEF`)

---

## 🌐 Add Custom Domain (Optional)

### Step 1: Get SSL Certificate

1. Go to AWS Certificate Manager: https://console.aws.amazon.com/acm/
2. **Important**: Switch region to `us-east-1` (required for CloudFront)
3. Click "Request certificate"
4. Certificate type: "Public certificate"
5. Domain name: `soochna-setu.com` and `www.soochna-setu.com`
6. Validation method: "DNS validation"
7. Click "Request"
8. Follow DNS validation steps (add CNAME records to your domain)
9. Wait for "Issued" status

### Step 2: Update CloudFront

1. Go to your CloudFront distribution
2. Click "Edit"
3. Alternate domain names (CNAMEs): Add `soochna-setu.com` and `www.soochna-setu.com`
4. SSL certificate: Select your ACM certificate
5. Click "Save changes"

### Step 3: Update DNS

Add these records to your domain DNS:

```
Type: CNAME
Name: www
Value: d1234abcdef.cloudfront.net

Type: A (Alias)
Name: @
Value: d1234abcdef.cloudfront.net
```

**Wait 10-60 minutes** for DNS propagation.

---

## 💰 Cost Breakdown

### S3 Costs:
- Storage: $0.023 per GB/month
- Requests: $0.0004 per 1,000 GET requests
- Data transfer: First 1GB free, then $0.09/GB

### CloudFront Costs:
- Data transfer: $0.085 per GB (first 10TB)
- Requests: $0.0075 per 10,000 HTTPS requests
- Free tier: 1TB data transfer + 10M requests/month (first year)

### Example Costs:

**Small traffic (10K visitors, 50GB/month):**
- S3: $0.50
- CloudFront: $1.50
- **Total: ~$2/month**

**Medium traffic (100K visitors, 500GB/month):**
- S3: $2
- CloudFront: $10
- **Total: ~$12/month**

---

## 🔧 Troubleshooting

### Issue: 403 Forbidden Error

**Solution:**
1. Check bucket policy is set correctly
2. Verify files are uploaded
3. Check CloudFront error pages configuration

### Issue: 404 on Page Refresh

**Solution:**
- Configure CloudFront error pages (Step 10)
- Make sure error pages redirect to `/404.html`

### Issue: Changes Not Showing

**Solution:**
```cmd
# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

### Issue: Slow Upload

**Solution:**
```cmd
# Use multipart upload for large files
aws s3 sync out/ s3://your-bucket --delete --size-only
```

---

## 📊 Monitoring

### View S3 Metrics:
1. Go to S3 Console
2. Click your bucket
3. Go to "Metrics" tab
4. View requests, data transfer, errors

### View CloudFront Metrics:
1. Go to CloudFront Console
2. Click your distribution
3. Go to "Monitoring" tab
4. View requests, data transfer, error rates

---

## 🔒 Security Best Practices

1. **Enable S3 Versioning:**
```cmd
aws s3api put-bucket-versioning --bucket soochna-setu-ai --versioning-configuration Status=Enabled
```

2. **Enable CloudFront Logging:**
- In CloudFront settings
- Enable "Standard logging"
- Choose S3 bucket for logs

3. **Add Security Headers:**
- Use Lambda@Edge to add security headers
- Or use CloudFront Functions

4. **Enable AWS WAF (Optional):**
- Protects against DDoS
- Costs extra (~$5/month)

---

## 📝 Quick Commands Reference

```cmd
# Build project
cd soochna-setu-final\frontend
npm run build

# Upload to S3
aws s3 sync out/ s3://soochna-setu-ai --delete

# Invalidate cache
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"

# Check bucket contents
aws s3 ls s3://soochna-setu-ai

# Delete bucket (if needed)
aws s3 rb s3://soochna-setu-ai --force
```

---

## ✅ Deployment Checklist

- [ ] Next.js configured for static export
- [ ] Project builds successfully
- [ ] S3 bucket created
- [ ] Static website hosting enabled
- [ ] Bucket policy set (public access)
- [ ] Files uploaded to S3
- [ ] CloudFront distribution created
- [ ] Error pages configured
- [ ] Website accessible via CloudFront URL
- [ ] All pages working
- [ ] Mobile responsive
- [ ] HTTPS enabled

---

## 🎓 For Hackathon Presentation

**Show judges:**

1. **Live URL**: Your CloudFront URL
2. **AWS Console**: Show S3 bucket and CloudFront
3. **Cost**: Mention it's only $1-3/month
4. **Performance**: Show CloudFront global distribution
5. **Scalability**: Explain it can handle millions of users

**Impressive points:**
- ✅ Deployed on AWS (professional)
- ✅ Global CDN (fast worldwide)
- ✅ HTTPS/SSL (secure)
- ✅ Cost-effective ($1-3/month)
- ✅ Scalable (handles any traffic)

---

## 🆘 Need Help?

**AWS Documentation:**
- S3: https://docs.aws.amazon.com/s3/
- CloudFront: https://docs.aws.amazon.com/cloudfront/

**Common Issues:**
- Bucket name taken → Use different name
- Access denied → Check bucket policy
- 404 errors → Configure error pages
- Slow updates → Invalidate cache

---

## 🎉 You're Done!

Your Soochna Setu AI is now:
- ✅ Live on AWS S3
- ✅ Globally distributed (CloudFront)
- ✅ Secure (HTTPS)
- ✅ Fast (CDN caching)
- ✅ Cheap ($1-3/month)
- ✅ Scalable (handles millions)

**Share your CloudFront URL with judges and users!**

---

**Deployment Time: ~30-45 minutes**
**Cost: $1-3/month**
**Difficulty: Medium ⭐⭐☆☆☆**

**Good luck with your hackathon! 🚀**
