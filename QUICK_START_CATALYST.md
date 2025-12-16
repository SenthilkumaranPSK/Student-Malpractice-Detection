# 🎯 Quick Start: Deploy ExamGuard to Zoho Catalyst

## ⚡ Fast Track Deployment (5 Minutes)

### **Step 1: Install Catalyst CLI**
```bash
npm install -g zcatalyst-cli
```

### **Step 2: Login**
```bash
catalyst login
```
(Browser will open for authentication)

### **Step 3: Navigate to Your Project**
```bash
cd "c:\Users\Senthilkumaran\OneDrive\Documents\My Codzz\Exam_Guard"
```

### **Step 4: Deploy!**
```bash
catalyst deploy
```

That's it! You'll get a live URL like:
```
https://examguard-xxxxx.catalyst.zoho.com
```

---

## 🔄 Update Your README Demo Button

After deployment, update the demo URL in `README.md`:

**Line 13:** Replace this:
```markdown
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-success?style=for-the-badge)](https://your-app-url.catalyst.zoho.com)
```

**With your actual URL:**
```markdown
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-success?style=for-the-badge)](https://examguard-xxxxx.catalyst.zoho.com)
```

Then commit and push:
```bash
git add README.md
git commit -m "Update demo URL"
git push origin main
```

---

## ✅ What You Now Have on GitHub:

1. ✅ **Live Demo Button** - Beautiful badge at top of README
2. ✅ **Deploy to Catalyst Button** - Links to deployment guide
3. ✅ **catalyst.json** - Catalyst configuration
4. ✅ **Procfile** - Deployment instructions
5. ✅ **ZOHO_CATALYST_DEPLOYMENT.md** - Complete guide
6. ✅ **Updated requirements.txt** - Includes gunicorn

---

## 🎨 Your GitHub README Now Shows:

```
🛡️ ExamGuard - AI-Powered Exam Proctoring System

[Badges: ExamGuard | Python | Flask | YOLOv8 | License]

Secure your online exams with cutting-edge AI technology

[🚀 Live Demo - Click Here] [Deploy to Zoho Catalyst]

Features • Demo • Installation • Usage • Documentation
```

---

## 📱 Alternative: Use Zoho Catalyst Console (No CLI)

1. Go to: https://console.catalyst.zoho.com/
2. Click **"Create Project"**
3. Select **"Import from GitHub"**
4. Choose: `SenthilkumaranPSK/AIML-Project`
5. Configure:
   - Branch: `main`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -b 0.0.0.0:$PORT main:app`
6. Click **"Deploy"**

---

## 🎉 You're Done!

Your ExamGuard is now:
- ✅ On GitHub with demo button
- ✅ Ready to deploy to Zoho Catalyst
- ✅ Professional and shareable
- ✅ Production-ready

**Next:** Deploy and update the demo URL! 🚀
