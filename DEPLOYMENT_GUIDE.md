# 🚀 Deploy ExamGuard to Zoho Catalyst - Step by Step

## ✅ **Easy Method: Use Catalyst Console** (No CLI needed!)

### **Step 1: Login to Catalyst Console**

1. Open your browser and go to: **https://console.catalyst.zoho.com/**
2. Login with your Zoho account: `senthilvandhanaa@gmail.com`
3. You'll see the Catalyst Dashboard

---

### **Step 2: Create New Project**

1. Click the **"+ Create Project"** button (top right or center)
2. You'll see two options:
   - **Create from scratch**
   - **Import from Git** ← Choose this one!

---

### **Step 3: Import from GitHub**

1. Click **"Import from Git"**
2. Select **"GitHub"** as the source
3. You may need to authorize Catalyst to access your GitHub
4. Once authorized, you'll see your repositories

---

### **Step 4: Configure Your Project**

**Select Repository:**
- Repository: `SenthilkumaranPSK/AIML-Project`
- Branch: `main`

**Project Settings:**
- Project Name: `ExamGuard`
- Description: `AI-Powered Exam Proctoring System`

**Build Configuration:**
- Runtime: `Python 3.9`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn -b 0.0.0.0:$PORT main:app`

---

### **Step 5: Deploy!**

1. Click **"Deploy"** button
2. Wait for deployment (2-5 minutes)
3. You'll see:
   - ✅ Installing dependencies
   - ✅ Building application
   - ✅ Starting server
   - ✅ Deployment successful!

---

### **Step 6: Get Your Live URL**

After deployment, you'll get a URL like:
```
https://examguard-60037000000123456.catalyst.zoho.com
```

**Copy this URL!** You'll need it for the demo button.

---

## 🔄 **Update Demo Button on GitHub**

### **Step 1: Edit README.md**

Open `README.md` and find line 13:
```markdown
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-success?style=for-the-badge)](https://your-app-url.catalyst.zoho.com)
```

Replace with your actual URL:
```markdown
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-success?style=for-the-badge)](https://examguard-60037000000123456.catalyst.zoho.com)
```

### **Step 2: Commit and Push**

```bash
git add README.md
git commit -m "Update live demo URL"
git push origin main
```

---

## ⚠️ **Important Notes**

### **Camera Access:**
- The app needs camera permission
- Users must click "Allow" when prompted
- Works best on Chrome/Firefox
- Must be HTTPS (Catalyst provides this automatically ✅)

### **Performance:**
- Free tier has limited resources
- May be slower than local
- Consider upgrading for production use

---

## 🎯 **Alternative: Deploy Using Render.com** (Easier!)

If Catalyst is complicated, try Render.com instead:

### **Step 1: Go to Render.com**
1. Visit: https://render.com/
2. Sign up with GitHub

### **Step 2: Create Web Service**
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub: `SenthilkumaranPSK/AIML-Project`
3. Configure:
   - Name: `examguard`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -b 0.0.0.0:$PORT main:app`
4. Click **"Create Web Service"**

### **Step 3: Get URL**
You'll get: `https://examguard.onrender.com`

**Render.com is FREE and easier!** ✨

---

## 🆘 **Troubleshooting**

### **Issue: "Cannot understand what targets"**
**Solution:** Use the web console instead of CLI (easier!)

### **Issue: Deployment fails**
**Possible causes:**
1. Large dependencies (YOLOv8 is big)
2. Memory limits on free tier
3. Build timeout

**Solutions:**
- Try Render.com instead (more generous free tier)
- Or use Heroku
- Or deploy locally and use ngrok for demo

---

## 🌐 **Quick Demo with ngrok** (Instant!)

If you just need a quick demo URL:

### **Step 1: Install ngrok**
Download from: https://ngrok.com/download

### **Step 2: Run your app locally**
```bash
python main.py
```

### **Step 3: Expose with ngrok**
```bash
ngrok http 5000
```

You'll get a URL like: `https://abc123.ngrok.io`

**Use this for demo!** (Temporary, but instant)

---

## 📊 **Deployment Options Comparison**

| Platform | Difficulty | Free Tier | Speed | Best For |
|----------|-----------|-----------|-------|----------|
| **Zoho Catalyst** | Medium | Limited | Medium | Zoho ecosystem |
| **Render.com** | Easy | Good | Fast | Quick deployment |
| **Heroku** | Easy | Good | Fast | Popular choice |
| **ngrok** | Very Easy | Good | Instant | Quick demos |

---

## 🎯 **My Recommendation:**

**For Quick Demo:** Use **ngrok** (instant!)
**For Production:** Use **Render.com** (easiest)
**For Zoho Integration:** Use **Catalyst Console** (web interface)

---

## 📞 **Need Help?**

I recommend trying **Render.com** - it's the easiest and most reliable for Python apps!

1. Go to https://render.com/
2. Sign up with GitHub
3. Click "New Web Service"
4. Select your repo
5. Deploy!

**It's that simple!** 🚀
