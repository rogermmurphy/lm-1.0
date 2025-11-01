# Running Worker as Production Service

## Yes - Worker Should Run as Service in Production!

**In production, the worker runs continuously as a background service**, just like a web server.

---

## Production Deployment Options

### Option 1: Docker Container (RECOMMENDED) ✅

**Add to docker-compose.yml**:
```yaml
presentation-worker:
  build: ./poc/08-async-jobs
  container_name: lm-worker
  restart: unless-stopped
  environment:
    - POSTGRES_HOST=postgres
    - REDIS_HOST=redis
    - PRESENTON_URL=http://presenton:80
  depends_on:
    - postgres
    - redis
    - presenton
  networks:
    - lm-network
```

**Benefits**:
- ✅ Auto-restarts if crashes
- ✅ Scales easily (run multiple workers)
- ✅ Monitored by Docker
- ✅ Same deployment as other services

---

### Option 2: Systemd Service (Linux)

**Create**: `/etc/systemd/system/lm-worker.service`
```ini
[Unit]
Description=LM Presentation Worker
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/app/poc/08-async-jobs
ExecStart=/usr/bin/python3 worker.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Commands**:
```bash
sudo systemctl enable lm-worker
sudo systemctl start lm-worker
sudo systemctl status lm-worker
```

---

### Option 3: Windows Service

**Using NSSM** (Non-Sucking Service Manager):
```powershell
# Download nssm.exe
# Then:
nssm install LMWorker "C:\Python\python.exe" "C:\path\to\worker.py"
nssm set LMWorker AppDirectory "C:\path\to\poc\08-async-jobs"
nssm start LMWorker
```

---

### Option 4: Supervisor (Linux/Mac)

**Config**: `/etc/supervisor/conf.d/lm-worker.conf`
```ini
[program:lm-worker]
command=python3 worker.py
directory=/app/poc/08-async-jobs
autostart=true
autorestart=true
user=www-data
stdout_logfile=/var/log/lm-worker.log
stderr_logfile=/var/log/lm-worker-error.log
```

---

## Scaling in Production

### Single Worker
- Handles jobs one at a time
- Good for POC and low traffic

### Multiple Workers
```yaml
# docker-compose.yml
presentation-worker-1:
  # ... config
presentation-worker-2:
  # ... config
presentation-worker-3:
  # ... config
```

Redis queue automatically distributes jobs across workers!

---

## Monitoring in Production

### Health Check Endpoint
Add to worker:
```python
# Expose health check on port
from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'running', 'queue_size': redis.llen('presentation_queue')}

# Run in separate thread
threading.Thread(target=lambda: app.run(port=8001)).start()
```

### Logging
```python
import logging
logging.basicConfig(
    filename='/var/log/lm-worker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Metrics
- Jobs processed per hour
- Average processing time
- Error rate
- Queue depth

---

## Current Setup (For POC)

**Running**: Worker process in terminal (as you just started)  
**Good for**: Testing and development  
**Not for**: Production (would stop when terminal closes)

**For production**: Use Docker container or systemd service

---

## Summary

**Yes** - worker runs as a service in production, exactly like:
- Web server (nginx, Express)
- Database (PostgreSQL)
- Cache (Redis)
- Any other backend service

**It's a critical part of your infrastructure** that processes long-running jobs.

---

**Recommendation**: Docker container (easiest to deploy and scale)
