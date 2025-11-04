**Last Updated:** November 4, 2025

# Home Network Port Forwarding Setup

## Your Network Configuration

**Confirmed from ipconfig:**
- **Local IP (Your PC):** 192.168.1.248
- **Router Gateway:** 192.168.1.1
- **Public IP:** 70.191.184.88
- **Network:** 192.168.1.0/24

## Port Forwarding Configuration (TP-Link Router)

### Ports to Forward

Configure these in your TP-Link router:

**Rule 1: Frontend**
- External Port: 3001
- Internal IP: 192.168.1.248
- Internal Port: 3001
- Protocol: TCP
- Description: LM Frontend

**Rule 2: API Gateway**
- External Port: 80
- Internal IP: 192.168.1.248
- Internal Port: 80
- Protocol: TCP
- Description: LM API Gateway

### Router Configuration Steps

1. Open browser to http://192.168.1.1
2. Login to TP-Link admin panel
3. Go to: Advanced → NAT Forwarding → Virtual Servers
4. Click "Add" and create both rules above
5. Save and reboot router

## Frontend Configuration Required

**Problem:** Frontend currently calls `localhost` which won't work from internet.

**File to change:** `views/web-app/.env.local`

```env
# For external access
NEXT_PUBLIC_API_URL=http://70.191.184.88
```

**OR for dynamic (works both local and external):**
```typescript
// In api.ts, detect if accessed externally
const API_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? `http://${window.location.hostname}`  // Use same host as frontend
  : 'http://localhost';  // Local development
```

## Access URLs After Setup

**From Internet:**
- Frontend: http://70.191.184.88:3001
- API: http://70.191.184.88:80 (called automatically by frontend)

**From Your Network:**
- Frontend: http://192.168.1.248:3001 OR http://localhost:3001
- API: http://192.168.1.248:80 OR http://localhost:80

## Important Notes

### Security Warnings
- ❌ No HTTPS/SSL - traffic is unencrypted
- ❌ Home IP is exposed
- ❌ No DDoS protection
- ❌ Computer must stay on 24/7

### Firewall Configuration
Windows Firewall needs to allow:
- Inbound: Port 3001 (TCP)
- Inbound: Port 80 (TCP)

### You're Right!
With port forwarding:
- External 70.191.184.88:3001 → Your PC 192.168.1.248:3001 ✅
- External 70.191.184.88:80 → Your PC 192.168.1.248:80 ✅

Both forwards are needed because:
1. Users load frontend from :3001
2. Frontend (in their browser) calls :80 for API

## Quick Test

**After port forwarding setup:**
1. From another network (or phone on cellular): http://70.191.184.88:3001
2. Should load frontend
3. Backend calls should work if API_URL configured correctly

## Better Alternative: Use Port 443

Instead of exposing port 80 (HTTP), use port 443 (HTTPS):

**Port forwards:**
- 443 → 192.168.1.248:443

**Add Caddy/nginx on your PC to handle:**
- / → Frontend (3001)
- /api → API Gateway (80)
- Automatic SSL with Let's Encrypt

This gives you:
- ✅ Single port
- ✅ HTTPS security
- ✅ Professional setup

But yes, your original plan with ports 3001 and 80 will work!
