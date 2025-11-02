@echo off
echo Killing any existing Next.js processes...
taskkill /F /IM node.exe 2>nul

echo Starting Next.js on port 3001...
cd /d "%~dp0"
set PORT=3001
npm run dev
