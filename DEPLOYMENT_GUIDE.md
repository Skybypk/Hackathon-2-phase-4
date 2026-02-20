# Deployment Guide - Fly.io + Vercel

This guide will help you deploy the Todo Chatbot app to Fly.io (backend) and Vercel (frontend).

## Prerequisites

1. **GitHub Account** - Your code is already at: https://github.com/Skybypk/Hackathon-2-phase-4
2. **Fly.io Account** - Sign up at https://fly.io/app/sign-up
3. **Vercel Account** - Sign up at https://vercel.com/signup

---

## Step 1: Install Fly.io CLI

### Windows (PowerShell - Run as Administrator)
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Or using npm (any OS)
```bash
npm install -g @flydotio/flyctl
```

### Verify Installation
```bash
fly version
```

---

## Step 2: Login to Fly.io

```bash
fly auth login
```

This will open a browser window. Log in to your Fly.io account.

---

## Step 3: Deploy Backend to Fly.io

### Navigate to backend folder
```bash
cd D:\Quarter-4\Projects\Q4-Hackathon-02\h-2-phase-4\backend
```

### Launch the app on Fly.io
```bash
fly launch --name todo-chatbot-backend --region sin --copy-config
```

**Note:** 
- `--region sin` deploys to Singapore (closest to most users)
- Available regions: `sin` (Singapore), `lhr` (London), `iad` (US East), `lax` (US West), etc.
- Choose a region closest to your users

### Create persistent volume for database
```bash
fly volumes create todos_data --region sin --size 1
```

### Deploy the app
```bash
fly deploy
```

### Open the app
```bash
fly open
```

### Get your backend URL
```bash
fly apps info
```

Your backend URL will be: `https://todo-chatbot-backend.fly.dev`

---

## Step 4: Deploy Frontend to Vercel

### Option A: Deploy via Vercel CLI

#### Install Vercel CLI
```bash
npm install -g vercel
```

#### Navigate to frontend folder
```bash
cd D:\Quarter-4\Projects\Q4-Hackathon-02\h-2-phase-4\frontend
```

#### Login to Vercel
```bash
vercel login
```

#### Deploy
```bash
vercel
```

#### Set environment variable
```bash
vercel env add BACKEND_URL https://todo-chatbot-backend.fly.dev
```

#### Deploy to production
```bash
vercel --prod
```

### Option B: Deploy via Vercel Website

1. Go to https://vercel.com/new
2. Import your GitHub repository: `Skybypk/Hackathon-2-phase-4`
3. Set **Root Directory** to `frontend`
4. Add Environment Variable:
   - Name: `BACKEND_URL`
   - Value: `https://todo-chatbot-backend.fly.dev`
5. Click **Deploy**

---

## Step 5: Update Frontend Backend URL

After deploying the backend, update the frontend configuration:

### In Vercel Dashboard:
1. Go to your project settings
2. Navigate to **Environment Variables**
3. Add/Edit `BACKEND_URL` with your Fly.io backend URL
4. Redeploy the project

---

## Troubleshooting

### Fly.io Deployment Failed

**Error: App name not available**
```bash
# Choose a different name
fly launch --name todo-chatbot-backend-unique --region sin --copy-config
```

**Error: No region specified**
```bash
# Specify region explicitly
fly launch --region sin
```

**Error: Volume already exists**
```bash
# Skip volume creation if it already exists
fly deploy
```

### Backend Not Responding

```bash
# Check app status
fly status

# View logs
fly logs

# Restart the app
fly restart
```

### Frontend Can't Connect to Backend

1. Ensure `BACKEND_URL` environment variable is set in Vercel
2. Check CORS settings in backend (should allow all origins currently)
3. Verify backend is running: `fly open`

---

## Useful Commands

### Fly.io
```bash
fly status          # Check app status
fly logs            # View logs
fly restart         # Restart app
fly open            # Open app in browser
fly apps info       # Get app info including URL
fly volumes list    # List volumes
```

### Vercel
```bash
vercel ls           # List deployments
vercel logs         # View logs
vercel --prod       # Deploy to production
```

---

## Your Deployed URLs

After deployment, you'll have:

- **Backend API**: `https://todo-chatbot-backend.fly.dev`
- **Frontend**: `https://your-app.vercel.app`

---

## Quick Deploy Script

Save this as `deploy.bat` for easy deployment:

```batch
@echo off
echo Deploying Backend to Fly.io...
cd backend
fly deploy
echo.
echo Backend deployed! Get URL with: fly apps info
echo.
echo Deploying Frontend to Vercel...
cd ..\frontend
vercel --prod
echo.
echo Deployment complete!
pause
```

---

## Support

- Fly.io Docs: https://fly.io/docs/
- Vercel Docs: https://vercel.com/docs/
- FastAPI Docs: https://fastapi.tiangolo.com/
- Next.js Docs: https://nextjs.org/docs/
