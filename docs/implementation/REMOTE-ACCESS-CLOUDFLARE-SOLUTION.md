# Remote Access via Cloudflare Tunnel - Complete Guide

**Date:** November 5, 2025
**Status:** REQUIRED FOR REMOTE ACCESS
**Priority:** HIGH
**Mode:** ZERO TOLERANCE + YOLO MODE

---

## PROBLEM STATEMENT

**Issue:** Application accessible on localhost:3000 but NOT from external IP (70.191.169.227:3000)

**Root Cause:** Frontend (port 3000) and backend (port 80) on different ports. Remote access shows `baseURL: 'http://localhost'` which resolves to user's machine, not server.

**Attempts That Failed:**
1. ❌ Next.js rewrites - Caused 500 errors in dev mode
2. ❌ Empty baseURL - API calls went to wrong port (3000 instead of 80)
3. ❌ Multiple config changes - Made things worse

---

## THE SOLUTION: Cloudflare Tunnel

**Why Cloudflare Tunnel:**
- Bypasses port forwarding issues
- Exposes localhost to internet securely  
- No firewall/router configuration needed
- Works with any port
- Free tier available

---

## STEP-BY-STEP IMPLEMENTATION

### Phase 1: Install Cloudflared

**Windows:**
```powershell
# Download from Cloudflare
# https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
# Or use package manager
winget install --id Cloudflare.cloudflared
```

**Verify Installation:**
```bash
cloudflared --version
```

### Phase 2: Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This opens browser for authentication. Follow prompts to authorize.

### Phase 3: Create Tunnel

```bash
cloudflared tunnel create lm-app
```

**Expected Output:**
- Tunnel ID (save this)
- Credentials file location (e.g., `~/.cloudflared/<tunnel-id>.json`)

### Phase 4: Configure Tunnel

Create config file: `C:\Users\roger\.cloudflared\config.yml`

```yaml
tunnel: <tunnel-id-from-step-3>
credentials-file: C:\Users\roger\.cloudflared\<tunnel-id>.json

ingress:
  - hostname: lm-app.yourdomain.com
    service: http://localhost:3000
  - service: http_status:404
```

**Or Quick Test (No DNS):**
```bash
cloudflared tunnel --url http://localhost:3000
```

### Phase 5: Start Tunnel

**With Config:**
```bash
cloudflared tunnel run lm-app
```

**Quick Test:**
```bash
cloudflared tunnel --url http://localhost:3000
```

**Expected Output:**
```
Your quick Tunnel has been created! Visit it at:
https://random-name.trycloudflare.com
```

### Phase 6: Update Frontend Config (If Needed)

If Cloudflare URL is permanent, update:

**File: `views/web-app/.env.local`**
```env
NEXT_PUBLIC_API_URL=http://localhost
# OR for Cloudflare-specific routing
NEXT_PUBLIC_CLOUDFLARE_URL=https://your-tunnel.trycloudflare.com
```

---

## TESTING PROCEDURE (Zero Tolerance)

### Test 1: Verify Tunnel Active
```bash
cloudflared tunnel info lm-app
```

### Test 2: Access via Cloudflare URL
1. Navigate to Cloudflare URL (e.g., https://random-name.trycloudflare.com)
2. Should see login page
3. Check DevTools console for errors

### Test 3: Login Functionality
1. Enter credentials: testuser@example.com / TestPass123!
2. Click Login
3. Should redirect to dashboard
4. Check console: Should show `baseURL: 'http://localhost'`
5. Verify NO 500 errors

### Test 4: Navigate to Classes
1. Click Classes in sidebar
2. Should load classes list
3. Check console for errors

### Test 5: Navigate to Class Detail
1. Click on a class
2. Should load class detail page
3. Verify all data displays
4. Check console for errors

### Test 6: Verify Zero Errors
- ✅ Only acceptable error: favicon 404
- ❌ NO API 404 errors
- ❌ NO 500 errors
- ❌ NO JavaScript errors

---

## SUCCESS CRITERIA

Task is COMPLETE when:
- [ ] Cloudflare tunnel running
- [ ] Application accessible via Cloudflare URL
- [ ] Login works
- [ ] Classes page works
- [ ] Class detail page works
- [ ] Console shows ZERO errors (except favicon)
- [ ] Tested via Playwright automation
- [ ] Results documented in DEVELOPER-HANDOVER.md

---

## ALTERNATIVE: Nginx Reverse Proxy (If Cloudflare Fails)

### Option B: Configure Nginx to Serve Frontend

**File: `services/api-gateway/nginx.conf`**

Add location block for frontend:
```nginx
location / {
    proxy_pass http://web-app:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
```

Then access via: `http://70.191.169.227` (port 80, not 3000)

---

## TROUBLESHOOTING

### Issue: Tunnel Won't Start
**Solution:** Check if port 3000 is accessible
```bash
curl http://localhost:3000
```

### Issue: 500 Errors via Cloudflare
**Solution:** Check web-app container logs
```bash
docker logs lm-web-app --tail 50
```

### Issue: API Calls Fail
**Solution:** Verify nginx gateway accessible from web-app
```bash
docker exec lm-web-app curl http://nginx/api/classes
```

---

## COMMANDS REFERENCE

```bash
# Check if cloudflared installed
cloudflared --version

# Create tunnel
cloudflared tunnel create lm-app

# Quick test (temporary URL)
cloudflared tunnel --url http://localhost:3000

# Run configured tunnel
cloudflared tunnel run lm-app

# List tunnels
cloudflared tunnel list

# Delete tunnel (if needed)
cloudflared tunnel delete lm-app

# Check Docker status
docker ps | grep lm-web-app
docker logs lm-web-app --tail 20
```

---

## FILES TO REVIEW

1. `.clinerules/zero-tolerance-yolo-debugging.md` - Methodology
2. `docs/implementation/DEVELOPER-HANDOVER.md` - Previous attempts
3. `docker-compose.yml` - Container configuration
4. `views/web-app/.env.local` - Current config (working for localhost)
5. `views/web-app/next.config.js` - Clean config
6. `services/api-gateway/nginx.conf` - Gateway routing

---

## NEXT DEVELOPER: Your Mission

1. Read this entire document
2. Install cloudflared
3. Create and configure tunnel
4. Start tunnel
5. Test via Cloudflare URL
6. Fix any issues found
7. Continue until ZERO errors
8. Update DEVELOPER-HANDOVER.md with results

**Remember:** ZERO TOLERANCE = no errors. YOLO = don't stop until complete.

Good luck. 🦖
