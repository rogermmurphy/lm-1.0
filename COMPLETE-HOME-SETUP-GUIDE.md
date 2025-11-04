# Complete Home Network Internet Access Setup

## Your Network (Confirmed)
- **Your PC IP:** 192.168.1.248
- **Router:** 192.168.1.1 (TP-Link)
- **Public IP:** 70.191.184.88

## Step-by-Step Setup

### Step 1: Configure TP-Link Router Port Forwarding

**Access router:**
```
1. Open browser → http://192.168.1.1
2. Login with your TP-Link credentials
3. Go to: Advanced → NAT Forwarding → Virtual Servers
```

**Add two port forwarding rules:**

**Rule 1: Frontend**
```
Service Name: LM-Frontend
External Port: 3001
Internal IP: 192.168.1.248
Internal Port: 3001
Protocol: TCP
Status: Enabled
```

**Rule 2: API Gateway**
```
Service Name: LM-API-Gateway
External Port: 80
Internal IP: 192.168.1.248
Internal Port: 80
Protocol: TCP
Status: Enabled
```

**Save and Apply**

### Step 2: Configure Windows Firewall

**Allow inbound connections for both ports:**

**Option A: GUI Method**
```
1. Open: Control Panel → Windows Defender Firewall → Advanced Settings
2. Click "Inbound Rules" → "New Rule"
3. Rule Type: Port
4. Protocol: TCP, Specific local ports: 3001
5. Action: Allow the connection
6. Profile: All (Domain, Private, Public)
7. Name: Little Monster Frontend

Repeat for port 80:
8. Same steps but use port 80
9. Name: Little Monster API Gateway
```

**Option B: Command Line (Run as Administrator)**
```cmd
netsh advfirewall firewall add rule name="LM Frontend" dir=in action=allow protocol=TCP localport=3001

netsh advfirewall firewall add rule name="LM API Gateway" dir=in action=allow protocol=TCP localport=80
```

### Step 3: Frontend Already Configured ✅

I've already updated `views/web-app/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://70.191.184.88
```

This tells the frontend to call your public IP for API requests.

### Step 4: Restart Frontend

**To apply the new .env.local:**
```bash
# Stop the current npm process (Ctrl+C in terminal)
# Then restart:
cd views\web-app
npm run dev
```

### Step 5: Test Access

**From another network (phone on cellular, friend's house, etc.):**

1. Visit: http://70.191.184.88:3001
2. Should see Little Monster login page
3. Try logging in - API calls should work!

**From your local network:**

Still works at: http://localhost:3001 or http://192.168.1.248:3001

## Traffic Flow After Setup

```
Internet User
    ↓
70.191.184.88:3001 (Your Public IP)
    ↓
TP-Link Router (Port Forward)
    ↓
192.168.1.248:3001 (Your PC - Frontend)
    |
    | Frontend loads, then calls:
    | http://70.191.184.88:80/api/...
    ↓
70.191.184.88:80
    ↓
TP-Link Router (Port Forward)
    ↓
192.168.1.248:80 (Your PC - API Gateway)
    ↓
Nginx routes to backend services (internal Docker network)
```

## Summary - What You Need

✅ **TP-Link Port Forwards:** 3001 and 80 → 192.168.1.248
✅ **Windows Firewall:** Allow 3001 and 80 inbound
✅ **Frontend Config:** Uses 70.191.184.88 (done!)
✅ **Keep PC On:** Must run 24/7 for access

## Troubleshooting

**If it doesn't work:**

1. **Check router:** Verify port forwards are active
2. **Check firewall:** Run `netsh advfirewall firewall show rule name="LM Frontend"`
3. **Check services:** Run `docker ps` - all should be running
4. **Check frontend:** Make sure it's running with new .env.local
5. **Test locally first:** http://192.168.1.248:3001 from another device on your network

## Security Notes

⚠️ **This exposes your home network to the internet**
- No HTTPS encryption (traffic visible)
- Your public IP is known
- Consider DDoS risks
- Computer must stay on always

**For production, I still recommend cloud deployment, but this will work for testing/personal use!**
