@echo off
echo Starting Cloudflare Tunnel for Little Monster GPA...
echo.
echo This will provide a secure HTTPS URL for remote access.
echo Keep this window open while using the app remotely.
echo.
echo The tunnel will expose localhost:3000 to the internet.
echo You will receive a temporary trycloudflare.com URL.
echo.
..\remote-server\cloudflared.exe tunnel --url http://localhost:80
