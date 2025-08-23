# 🚀 Deployment Guide for Specimen Tracker

This guide will help you deploy your Flask application to a live hosting service so it works online.

## 🔍 **Before You Deploy - Test Everything!**

First, run the deployment test suite to ensure your app is ready:

```bash
# Use the correct Python path
C:\Users\findl\AppData\Local\Programs\Python\Python313\python.exe test_deployment.py
```

**Only deploy if ALL tests pass!** ✅

## 📋 **What You Need for Deployment**

### **1. GitHub Repository** ✅
- Your code stored and version controlled
- **This does NOT make your app live online**

### **2. Hosting Service** ❌ (You need this!)
- A service that actually runs your Flask app
- Provides a live website URL
- Handles database and server infrastructure

## 🌐 **Recommended Hosting Services**

### **Option 1: Render (Recommended for beginners)**
- **Free tier available**
- **Easy deployment from GitHub**
- **Automatic HTTPS**
- **PostgreSQL database included**

### **Option 2: Railway**
- **Free tier available**
- **Very simple deployment**
- **Good for small projects**

### **Option 3: Heroku**
- **Free tier discontinued**
- **Professional service**
- **Excellent documentation**

## 🚀 **Step-by-Step Deployment to Render**

### **Step 1: Prepare Your Code**
1. **Test your app locally** (use `test_deployment.py`)
2. **Push to GitHub** (if not already done)
3. **Ensure all files are committed**

### **Step 2: Create Render Account**
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"

### **Step 3: Connect Your Repository**
1. **Connect GitHub** and select your `specimen_tracker` repo
2. **Name**: `specimen-tracker` (or your preferred name)
3. **Environment**: `Python 3`
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `gunicorn wsgi:app`

### **Step 4: Configure Environment Variables**
Add these in Render's dashboard:
```
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://... (Render will provide this)
FLASK_ENV=production
FLASK_DEBUG=False
```

### **Step 5: Deploy!**
1. Click "Create Web Service"
2. Wait for build to complete (5-10 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

## 🗄️ **Database Setup**

### **SQLite (Development)**
- ✅ Works locally
- ❌ **Won't work in production** (file system access issues)

### **PostgreSQL (Production)**
- ✅ **Required for production**
- ✅ Render provides this automatically
- ✅ Your app will use the `DATABASE_URL` environment variable

## 🔧 **Production Configuration Changes**

### **1. Update wsgi.py for Production**
```python
# Change this line:
app.run(debug=True, host='0.0.0.0', port=5000)

# To this:
app.run(debug=False, host='127.0.0.1', port=5000)
```

### **2. Environment Variables**
- **Never hardcode secrets** in your code
- Use environment variables for all sensitive data
- Set `FLASK_DEBUG=False` in production

## 🧪 **Testing Your Deployed App**

### **After Deployment, Test:**
1. ✅ **Homepage loads** at your live URL
2. ✅ **All routes work** (patients, samples, tests)
3. ✅ **Forms submit successfully**
4. ✅ **Database operations work**
5. ✅ **Static files load** (CSS, JS)

### **Common Issues & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| App won't start | Missing dependencies | Check `requirements.txt` |
| Database errors | Wrong DATABASE_URL | Verify environment variable |
| 500 errors | Debug mode issues | Set FLASK_DEBUG=False |
| Static files 404 | Path issues | Check file structure |

## 📊 **Monitoring Your Live App**

### **Render Dashboard Shows:**
- ✅ **Build status** and logs
- ✅ **Deployment history**
- ✅ **Environment variables**
- ✅ **Database status**
- ✅ **App performance**

### **Check Logs Regularly:**
- Look for error messages
- Monitor performance
- Check database connections

## 🔒 **Security Checklist**

Before going live, ensure:
- ✅ **SECRET_KEY** is set and secure
- ✅ **Debug mode is OFF**
- ✅ **Database credentials** are secure
- ✅ **HTTPS is enabled** (Render does this automatically)
- ✅ **No sensitive data** in code

## 🎯 **Your Deployment Checklist**

- [ ] **Run `test_deployment.py`** - All tests pass
- [ ] **Code pushed to GitHub** - All files committed
- [ ] **Choose hosting service** - Render recommended
- [ ] **Configure environment variables** - SECRET_KEY, DATABASE_URL
- [ ] **Deploy and test** - Verify all functionality works
- [ ] **Monitor performance** - Check logs and status

## 🆘 **Need Help?**

### **If deployment fails:**
1. Check the build logs in Render
2. Verify all environment variables are set
3. Ensure `requirements.txt` is complete
4. Test locally with `test_deployment.py`

### **If app doesn't work after deployment:**
1. Check the app logs in Render
2. Verify database connection
3. Test individual routes
4. Check environment variable configuration

## 🎉 **Success!**

Once deployed successfully, you'll have:
- 🌐 **Live website URL** (e.g., `https://specimen-tracker.onrender.com`)
- 🗄️ **Production database** with real data
- 🔒 **Secure HTTPS connection**
- 📱 **Accessible from anywhere** in the world

**Remember**: GitHub stores your code, but hosting services make it live online!
