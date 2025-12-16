# 🚀 Deploying ExamGuard to Zoho Catalyst

This guide will help you deploy your ExamGuard application to Zoho Catalyst.

---

## 📋 Prerequisites

1. **Zoho Catalyst Account**
   - Sign up at: https://catalyst.zoho.com/
   - Free tier available

2. **Catalyst CLI Installed**
   ```bash
   npm install -g zcatalyst-cli
   ```

3. **Git Repository**
   - Your code is already on GitHub ✅

---

## 🔧 Step-by-Step Deployment

### **Step 1: Login to Catalyst CLI**

```bash
catalyst login
```

This will open a browser window for authentication.

### **Step 2: Initialize Catalyst Project**

Navigate to your project directory:
```bash
cd "c:\Users\Senthilkumaran\OneDrive\Documents\My Codzz\Exam_Guard"
```

Initialize Catalyst:
```bash
catalyst init
```

Follow the prompts:
- **Project Name:** ExamGuard
- **Project Type:** Web Application
- **Runtime:** Python 3.9
- **Framework:** Flask

### **Step 3: Configure Project**

The `catalyst.json` file has already been created for you with:
- Project name: ExamGuard
- Runtime: Python 3.9
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn -b 0.0.0.0:$PORT main:app`

### **Step 4: Deploy to Catalyst**

```bash
catalyst deploy
```

This will:
1. ✅ Package your application
2. ✅ Upload to Zoho Catalyst
3. ✅ Install dependencies
4. ✅ Start the application
5. ✅ Provide you with a live URL

### **Step 5: Get Your Live URL**

After deployment, you'll receive a URL like:
```
https://examguard-<project-id>.catalyst.zoho.com
```

---

## ⚙️ Configuration Files Created

### **1. catalyst.json**
```json
{
  "defaults": {
    "project": {
      "name": "ExamGuard",
      "description": "AI-Powered Exam Proctoring System"
    }
  },
  "services": {
    "web": {
      "type": "python",
      "runtime": "python3.9",
      "build_command": "pip install -r requirements.txt",
      "start_command": "gunicorn -b 0.0.0.0:$PORT main:app"
    }
  }
}
```

### **2. Procfile**
```
web: gunicorn -b 0.0.0.0:$PORT --timeout 300 --workers 2 main:app
```

### **3. requirements.txt** (Updated)
Added `gunicorn==21.2.0` for production server

---

## 🎯 Alternative: Deploy via GitHub Integration

### **Option 1: Connect GitHub to Catalyst**

1. Go to Catalyst Console: https://console.catalyst.zoho.com/
2. Click **"Create Project"**
3. Select **"Import from GitHub"**
4. Choose your repository: `SenthilkumaranPSK/AIML-Project`
5. Configure:
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -b 0.0.0.0:$PORT main:app`
6. Click **"Deploy"**

### **Option 2: Automatic Deployments**

Enable auto-deploy on push:
1. In Catalyst Console → Your Project
2. Go to **Settings** → **Deployments**
3. Enable **"Auto Deploy on Git Push"**
4. Select branch: `main`

Now every push to GitHub automatically deploys! 🎉

---

## 🔍 Important Notes

### **Camera Access Limitation**

⚠️ **Important:** Web-based deployments have limitations with camera access due to browser security:

1. **HTTPS Required:** Camera only works on HTTPS (Catalyst provides this ✅)
2. **User Permission:** Users must grant camera permission
3. **Browser Compatibility:** Works best on Chrome/Firefox

### **Performance Considerations**

For production use, consider:

1. **Upgrade Catalyst Plan** for:
   - More CPU/Memory
   - Better performance for AI models
   - More concurrent users

2. **Optimize for Web:**
   - Reduce frame rate if needed
   - Implement frame skipping
   - Use lighter models if necessary

---

## 📊 Monitoring Your Deployment

### **View Logs:**
```bash
catalyst logs
```

### **Check Status:**
```bash
catalyst status
```

### **Update Deployment:**
```bash
catalyst deploy
```

---

## 🌐 Custom Domain (Optional)

1. Go to Catalyst Console
2. Navigate to **Domains**
3. Click **"Add Custom Domain"**
4. Follow DNS configuration steps
5. Example: `examguard.yourdomain.com`

---

## 💰 Pricing

**Catalyst Free Tier:**
- ✅ 1 Project
- ✅ 1 GB Storage
- ✅ 10 GB Bandwidth
- ✅ HTTPS included
- ✅ Custom domains

**Paid Plans:** Starting at $10/month for more resources

---

## 🆘 Troubleshooting

### **Issue: Deployment Fails**

**Solution:**
```bash
# Check logs
catalyst logs

# Redeploy
catalyst deploy --force
```

### **Issue: Camera Not Working**

**Solution:**
- Ensure HTTPS is enabled (Catalyst does this automatically)
- Check browser permissions
- Test on Chrome/Firefox

### **Issue: Slow Performance**

**Solution:**
- Upgrade Catalyst plan
- Optimize detection parameters in `models/detection_parameters.json`
- Reduce video frame rate

---

## 🎓 Resources

- **Catalyst Documentation:** https://docs.catalyst.zoho.com/
- **Catalyst CLI Guide:** https://docs.catalyst.zoho.com/cli/
- **Python on Catalyst:** https://docs.catalyst.zoho.com/python/
- **Support:** https://help.catalyst.zoho.com/

---

## ✅ Deployment Checklist

Before deploying, ensure:

- [x] `catalyst.json` created
- [x] `Procfile` created
- [x] `gunicorn` added to `requirements.txt`
- [x] Code pushed to GitHub
- [x] Catalyst CLI installed
- [ ] Logged into Catalyst
- [ ] Project initialized
- [ ] Deployed successfully
- [ ] Tested live URL

---

## 🎉 After Deployment

Once deployed, you'll have:

✅ **Live URL** for your ExamGuard app
✅ **HTTPS** enabled automatically
✅ **Auto-scaling** based on traffic
✅ **Monitoring** and logs
✅ **Easy updates** via CLI or GitHub

**Your ExamGuard is now live on the internet!** 🌍

---

## 📞 Need Help?

- **Zoho Catalyst Support:** https://help.catalyst.zoho.com/
- **Community Forum:** https://community.zoho.com/catalyst
- **Email:** support@zohocatalyst.com

---

**Happy Deploying! 🚀**
