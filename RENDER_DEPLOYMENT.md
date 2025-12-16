# 🚀 Deploying Student Malpractice Detection to Render.com

This project uses **YOLOv8** and **MediaPipe** (heavy AI libraries). 
**Vercel Free Tier CANNOT host this** because it exceeds the 250MB size limit.

✅ **Best Free Solution:** [Render.com](https://render.com) (Native Python support, no size limits).

---

## ⚡ 3-Minute Deployment Steps

### **1. Push to GitHub**
Ensure your code is pushed to: 
`https://github.com/SenthilkumaranPSK/Student-Malpractice-Detection`

### **2. Create Service on Render**
1. **[Click Here to Deploy](https://render.com/deploy?repo=https://github.com/SenthilkumaranPSK/Student-Malpractice-Detection)**  
   *(Or go to Dashboard → New → Web Service → Connect GitHub repo)*

2. **Configure Settings:**
   - **Name:** `student-malpractice-detection`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app`
   
3. **Environment Variables:**
   You don't need any for the basic demo!

### **3. Wait & Launch**
- Click **"Create Web Service"**.
- Render will install pure Python, OpenCV, and AI models.
- Wait ~5 minutes.
- **Your URL will be:** `https://student-malpractice-detection.onrender.com`

---

## ⚠️ Notes
- **Cold Boot:** On free tier, the first request after inactivity might take 50 seconds.
- **Camera:** Users must allow camera access in the browser.
