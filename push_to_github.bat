@echo off
echo ========================================
echo GitHub Push Script
echo ========================================
echo.
echo This script will push your code to GitHub
echo Repository: https://github.com/arnav-156/chemical-equipment-viz
echo.

REM Check if remote exists
git remote -v | findstr "origin" >nul
if %errorlevel% neq 0 (
    echo Adding GitHub remote...
    git remote add origin https://github.com/arnav-156/chemical-equipment-viz.git
    echo Remote added!
) else (
    echo Remote already exists.
)

echo.
echo Current branch:
git branch

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
echo.
echo NOTE: If the repository doesn't exist yet, you need to:
echo 1. Go to https://github.com/new
echo 2. Create repository named: chemical-equipment-viz
echo 3. DO NOT initialize with README
echo 4. Then run this script again
echo.

pause

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Code pushed to GitHub
    echo ========================================
    echo.
    echo View your repository at:
    echo https://github.com/arnav-156/chemical-equipment-viz
    echo.
) else (
    echo.
    echo ========================================
    echo PUSH FAILED
    echo ========================================
    echo.
    echo Common issues:
    echo 1. Repository doesn't exist - Create it at https://github.com/new
    echo 2. Authentication failed - You may need a Personal Access Token
    echo 3. Network issues - Check your internet connection
    echo.
    echo See PUSH_TO_GITHUB.md for detailed instructions
    echo.
)

pause
