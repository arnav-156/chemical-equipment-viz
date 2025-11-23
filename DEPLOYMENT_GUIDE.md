# 🚀 Free Deployment Guide

## 🎯 Recommended: Deploy to Vercel (Easiest & Free)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```
- Opens browser
- Sign in with GitHub (recommended)

### Step 3: Deploy Frontend
```bash
cd chemical-equipment-viz/web-frontend
vercel
```

**Follow prompts:**
- Set up and deploy? **Y**
- Which scope? **Your account**
- Link to existing project? **N**
- Project name? **chemical-equipment-viz** (or your choice)
- Directory? **./web-frontend**
- Override settings? **N**

**Done!** You'll get a URL like: `https://chemical-equipment-viz.vercel.app`

### Step 4: Deploy Backend (Render.com)

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. **New → Web Service**
4. **Connect your repo:** `arnav-156/chemical-equipment-viz`
5. **Configure:**
   ```
   Name: chemical-equipment-viz-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn chemical_equipment_viz.wsgi:application
   ```
6. **Add Environment Variables:**
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=.render.com
   ```
7. **Click "Create Web Service"**

**Done!** You'll get: `https://chemical-equipment-viz-api.onrender.com`

### Step 5: Connect Frontend to Backend

Update your frontend API URL:

**In `web-frontend/src/services/api.js`:**
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://chemical-equipment-viz-api.onrender.com';
```

**Redeploy frontend:**
```bash
cd web-frontend
vercel --prod
```

---

## 🎯 Alternative: Netlify (Frontend Only)

### Quick Deploy
```bash
cd chemical-equipment-viz/web-frontend
npm run build
```

**Drag and drop `build` folder to:** https://app.netlify.com/drop

**Or use CLI:**
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

---

## 🎯 Alternative: GitHub Pages (Frontend Only)

### Step 1: Add to package.json
```json
{
  "homepage": "https://arnav-156.github.io/chemical-equipment-viz"
}
```

### Step 2: Install gh-pages
```bash
cd web-frontend
npm install --save-dev gh-pages
```

### Step 3: Add deploy scripts
```json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

### Step 4: Deploy
```bash
npm run deploy
```

**Live at:** `https://arnav-156.github.io/chemical-equipment-viz`

---

## 🎯 Full Stack: Railway.app

### Step 1: Sign up
- Go to: https://railway.app
- Sign in with GitHub

### Step 2: New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose: `arnav-156/chemical-equipment-viz`

### Step 3: Configure
**Frontend:**
```
Root Directory: web-frontend
Build Command: npm install && npm run build
Start Command: npx serve -s build
```

**Backend:**
```
Root Directory: .
Build Command: pip install -r requirements.txt
Start Command: gunicorn chemical_equipment_viz.wsgi:application
```

### Step 4: Add Database
- Click "New" → "Database" → "PostgreSQL"
- Automatically connects to Django

**Done!** Both deployed with one click!

---

## 📊 Comparison

| Platform | Frontend | Backend | Database | Free Tier | Best For |
|----------|----------|---------|----------|-----------|----------|
| **Vercel** | ✅ | ⚠️ Limited | ❌ | Unlimited | Frontend |
| **Netlify** | ✅ | ❌ | ❌ | 100GB/mo | Frontend |
| **Render** | ✅ | ✅ | ✅ | 750hrs/mo | Full Stack |
| **Railway** | ✅ | ✅ | ✅ | $5 credit | Full Stack |
| **GitHub Pages** | ✅ | ❌ | ❌ | Unlimited | Static |

---

## 🎯 My Recommendation

### For Demo/Portfolio:
**Vercel (Frontend) + Render (Backend)**
- Easiest setup
- Best performance
- Free forever
- Professional URLs

### For Production:
**Railway**
- Everything in one place
- Database included
- Easy scaling
- $5/month free tier

---

## 🚀 Quick Start (Vercel + Render)

### 1. Deploy Frontend (2 minutes)
```bash
npm install -g vercel
cd chemical-equipment-viz/web-frontend
vercel --prod
```

### 2. Deploy Backend (5 minutes)
1. Go to https://render.com
2. New Web Service
3. Connect GitHub repo
4. Deploy!

### 3. Update API URL (1 minute)
```javascript
// In api.js
const API_BASE_URL = 'https://your-backend.onrender.com';
```

### 4. Redeploy Frontend (1 minute)
```bash
vercel --prod
```

**Total time: ~10 minutes** ⏱️

---

## 🎉 After Deployment

### Your Live URLs:
- **Frontend:** `https://chemical-equipment-viz.vercel.app`
- **Backend:** `https://chemical-equipment-viz-api.onrender.com`
- **PWA Install:** Works automatically on HTTPS!

### Test PWA:
1. Visit your Vercel URL
2. Look for install button
3. Install as app
4. Test offline mode

### Share:
- Add to resume/portfolio
- Share on LinkedIn
- Demo in interviews

---

## 🐛 Troubleshooting

### Frontend won't build
```bash
cd web-frontend
npm install
npm run build
# Check for errors
```

### Backend won't start
```bash
# Check requirements.txt
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### CORS errors
**In Django settings.py:**
```python
CORS_ALLOWED_ORIGINS = [
    "https://chemical-equipment-viz.vercel.app",
]
```

### Database errors
**Use Render PostgreSQL:**
- Automatically configured
- Free tier included
- No setup needed

---

## 💡 Pro Tips

### 1. Environment Variables
**Never commit:**
- API keys
- Secret keys
- Database passwords

**Use platform environment variables instead**

### 2. Custom Domain (Optional)
**Vercel:**
- Settings → Domains
- Add custom domain
- Free SSL included

### 3. Automatic Deployments
**Both Vercel and Render:**
- Auto-deploy on git push
- Preview deployments for PRs
- Rollback with one click

### 4. Monitoring
**Free tools:**
- Vercel Analytics
- Render Metrics
- Google Analytics

---

## 🎯 Next Steps

1. **Deploy frontend to Vercel** (easiest)
2. **Deploy backend to Render** (free tier)
3. **Test PWA installation** (works on HTTPS)
4. **Share your live URL!** 🎉

---

**Need help? Let me know which platform you want to use!** 🚀
