@echo off
echo ============================================
echo  Todo Chatbot Deployment Script
echo  Backend: Fly.io | Frontend: Vercel
echo ============================================
echo.

:: Check if Fly.io CLI is installed
fly version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Fly.io CLI is not installed!
    echo.
    echo Install it using one of these commands:
    echo   PowerShell: iwr https://fly.io/install.ps1 -useb | iex
    echo   npm: npm install -g @flydotio/flyctl
    echo.
    pause
    exit /b 1
)

:: Check if Vercel CLI is installed
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Vercel CLI is not installed!
    echo Install it using: npm install -g vercel
    echo.
)

echo Step 1: Deploy Backend to Fly.io
echo ============================================
echo.
cd backend

:: Check if already logged in
fly auth whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Not logged in to Fly.io. Opening browser...
    fly auth login
)

:: Launch app if not already created
if not exist fly.toml (
    echo [INFO] Creating Fly.io app...
    fly launch --name todo-chatbot-backend --region sin --copy-config
) else (
    echo [INFO] Fly.io config found. Deploying...
)

:: Create volume if not exists
echo [INFO] Creating persistent volume...
fly volumes create todos_data --region sin --size 1 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Volume may already exist. Continuing...
)

:: Deploy
echo [INFO] Deploying backend...
fly deploy

:: Get app URL
echo.
echo [SUCCESS] Backend deployed!
fly apps info | findstr "Hostname"
echo.
echo Copy the above URL for the next step!
echo.
pause

:: Return to root
cd ..

echo.
echo Step 2: Deploy Frontend to Vercel
echo ============================================
echo.
cd frontend

:: Check if Vercel CLI is available
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Vercel CLI not installed!
    echo Please install it: npm install -g vercel
    echo.
    echo Alternatively, deploy manually at: https://vercel.com/new
    echo.
    pause
    exit /b 1
)

:: Login to Vercel
echo [INFO] Logging in to Vercel...
vercel login

:: Deploy
echo [INFO] Deploying frontend...
set /p BACKEND_URL="Enter your Fly.io backend URL (e.g., https://todo-chatbot-backend.fly.dev): "
vercel --env BACKEND_URL=%BACKEND_URL% --prod

echo.
echo [SUCCESS] Frontend deployed!
echo.
echo ============================================
echo  Deployment Complete!
echo ============================================
echo.
echo Backend: Check Fly.io dashboard
echo Frontend: Check Vercel dashboard
echo.
pause
