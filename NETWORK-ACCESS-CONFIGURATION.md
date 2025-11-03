# Network Access Configuration
## Allow Traffic from Multiple Sources

**Date:** November 3, 2025  
**Status:** Configured for Home Network + Public Access

---

## Changes Made

I've updated the application to allow traffic from multiple sources:

### ✅ Configured Sources

The application now accepts traffic from:
- ✅ localhost (127.0.0.1)
- ✅ localhost:3000
- ✅ Your local network (192.168.x.x)
- ✅ Your public IP (70.191.184.88)
- ✅ Any other device on your home network

### Files Modified

1. **views/web-app/next.config.js**
   - Added CORS headers to allow all origins
   - Enabled access from any network interface

2. **views/web-app/package.json**
   - Changed dev script to bind to 0.0.0.0 (all interfaces)
   - Now: `next dev -H 0.0.0.0`

3. **services/api-gateway/nginx.conf**
   - Updated CORS headers to allow all origins
   - Added support for credentials and additional headers

---

## How to Use

### Start the Application

```bash
# In views/web-app directory, restart the dev server:
npm run dev
```

The application will now be accessible from:
- ✅ http://localhost:3000 (same computer)
- ✅ http://127.0.0.1:3000 (same computer)
- ✅ http://192.168.0.1:3000 (router IP, if applicable)
- ✅ http://192.168.0.X:3000 (other devices on network - replace X with your computer's local IP)
- ✅ http://70.191.184.88:3000 (your public IP, if port forwarding is set up)

### Find Your Local IP

To find your computer's local IP address:

```bash
# Windows
ipconfig

# Look for "IPv4 Address" under your active network adapter
# Example: 192.168.0.105
```

Then access from another device: http://192.168.0.105:3000

---

## Network Access Scenarios

### Scenario 1: Same Computer
```
URL: http://localhost:3000
Status: ✅ Always works
```

### Scenario 2: Other Device on Home Network (Phone/Tablet)
```
URL: http://192.168.0.X:3000 (X = your computer's IP)
Status: ✅ Works if:
  - Both devices on same WiFi
  - Windows Firewall allows port 3000
```

### Scenario 3: Outside Your Home Network (Internet)
```
URL: http://70.191.184.88:3000
Status: ⚠️ Works if:
  - Router port forwarding configured (3000 → your computer)
  - Windows Firewall allows port 3000
  - ISP doesn't block incoming port 3000
```

---

## Firewall Configuration

### Windows Firewall Rule

If you want access from your home network or internet:

```powershell
# Run PowerShell as Administrator

# Allow port 3000 inbound
New-NetFirewallRule -DisplayName "Next.js Dev Server" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow

# Verify rule was created
Get-NetFirewallRule -DisplayName "Next.js Dev Server"
```

### Router Port Forwarding (For Internet Access)

If you want access from outside your home network:

1. Log into your router (usually http://192.168.0.1 or http://192.168.1.1)
2. Find "Port Forwarding" or "Virtual Server" settings
3. Add new rule:
   - External Port: 3000
   - Internal IP: Your computer's IP (find with `ipconfig`)
   - Internal Port: 3000
   - Protocol: TCP
4. Save and test from phone (using mobile data, not WiFi)

---

## CORS Configuration Details

### Next.js Headers (next.config.js)

```javascript
async headers() {
  return [
    {
      source: '/:path*',
      headers: [
        { key: 'Access-Control-Allow-Origin', value: '*' },
        { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
        { key: 'Access-Control-Allow-Headers', value: 'X-Requested-With,Content-Type,Authorization' },
        { key: 'Access-Control-Allow-Credentials', value: 'true' },
      ],
    },
  ]
}
```

### Nginx Gateway (nginx.conf)

```nginx
# CORS headers for all responses - Allow all origins
add_header 'Access-Control-Allow-Origin' '*' always;
add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS, PATCH' always;
add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, X-Requested-With, Accept, Origin' always;
add_header 'Access-Control-Allow-Credentials' 'true' always;
add_header 'Access-Control-Max-Age' '3600' always;
```

---

## Testing Access

### From Same Computer

```bash
curl http://localhost:3000
curl http://127.0.0.1:3000
```

### From Another Device on Network

```bash
# Replace 192.168.0.X with your computer's local IP
curl http://192.168.0.X:3000
```

### From Browser on Phone (Same WiFi)

```
http://192.168.0.X:3000
```

Where X = your computer's IP address from `ipconfig`

---

## Troubleshooting

### Can't Access from Other Devices

**Check Windows Firewall:**
```powershell
Get-NetFirewallRule -DisplayName "Next.js Dev Server"
```

**Temporarily disable firewall to test:**
```powershell
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
# Test access
# Re-enable after testing:
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

### Can't Access from Internet

1. Verify port forwarding in router
2. Check your public IP: https://whatismyipaddress.com
3. Test from phone using mobile data (not WiFi)
4. Check if ISP blocks port 3000 (some do)

### Docker Services Not Responding

The backend services (auth, database, etc.) are separate from the Next.js frontend. If login fails:

```bash
# Start backend services
docker-compose up -d postgres redis auth-service nginx
```

---

## Security Warning

⚠️ **Development Configuration**

These settings allow access from ANY origin (`*`). This is fine for:
- Local development
- Home network access
- Testing

For production deployment:
- Replace `'*'` with specific allowed origins
- Use HTTPS instead of HTTP
- Implement proper authentication
- Use environment-specific configs

---

## Production Configuration

For production, replace `'*'` with specific origins:

```javascript
// next.config.js - Production
{ key: 'Access-Control-Allow-Origin', value: 'https://yourdomain.com' }
```

```nginx
# nginx.conf - Production  
add_header 'Access-Control-Allow-Origin' 'https://yourdomain.com' always;
```

---

## Summary

✅ **What You Can Do Now:**
- Access from localhost
- Access from 192.168.0.x addresses on your home network
- Access from your public IP (if port forwarding configured)
- Share link with family/friends on same WiFi

🔧 **Next Steps:**
1. Restart Next.js dev server: `npm run dev` (in views/web-app)
2. Find your local IP: `ipconfig`
3. Test from phone on same WiFi: http://YOUR_LOCAL_IP:3000
4. Configure router port forwarding for internet access (optional)

The application now supports multi-source network access for development and home use.
