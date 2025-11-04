# Little Monster GPA - Deployment & Operations Guide
## Alpha 1.0 - Production Operations Manual

**Version:** 1.0.0-alpha  
**Date:** November 4, 2025  
**Status:** Operational  
**Parent Document:** TECHNICAL-ARCHITECTURE.md

---

## Table of Contents
1. [Deployment Procedures](#deployment-procedures)
2. [Operations Runbook](#operations-runbook)
3. [Monitoring & Alerting](#monitoring--alerting)
4. [Backup & Recovery](#backup--recovery)
5. [Troubleshooting Guide](#troubleshooting-guide)
6. [Performance Tuning](#performance-tuning)

---

## Deployment Procedures

### Local Development Deployment

```bash
# ============================================================================
# Local Development Deployment (Docker Compose)
# ============================================================================

# Step 1: Clone repository
git clone https://github.com/your-org/lm-1.0.git
cd lm-1.0

# Step 2: Create environment file
cp .env.example .env
# Edit .env with your configuration

# Step 3: Generate secrets
python scripts/utilities/generate-secrets.py > .env.secrets
cat .env.secrets >> .env

# Step 4: Initialize database
docker-compose up -d postgres
timeout 10  # Wait for PostgreSQL to start
python database/scripts/deploy-schema.py

# Step 5: Start infrastructure services
docker-compose up -d redis chromadb ollama

# Step 6: Start application services
docker-compose up -d
# This starts all services defined in docker-compose.yml

# Step 7: Verify all services
curl http://localhost/health
curl http://localhost:8001/health  # Auth
curl http://localhost:8005/health  # LLM
# ... check other services

# Step 8: Start frontend (separate terminal)
cd views/web-app
npm install
npm run dev

# Access:
# - Web App: http://localhost:3000
# - API Gateway: http://localhost:80
# - Adminer: http://localhost:8080
```

### Important Deployment Notes

**⚠️ Web-App Requires Image Rebuild:**
- The web-app service has NO volume mount in docker-compose.yml
- Code changes require rebuilding the Docker image:
  ```bash
  docker-compose build web-app
  docker-compose up -d web-app
  ```
- For development, use `npm run dev` locally instead

**Recent Fixes:**
- Groups page TypeError has been fixed (November 2025)
- All critical MVP features are operational

---

## Operations Runbook

### Service Lifecycle Management

```bash
# ============================================================================
# Service Management Commands
# ============================================================================

# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d auth-service

# Stop all services
docker-compose down

# Stop specific service  
docker-compose stop auth-service

# Restart service (with rebuild)
docker-compose up -d --build auth-service

# View logs
docker-compose logs -f auth-service

# View logs for all services
docker-compose logs -f

# Scale service
docker-compose up -d --scale llm-service=3

# Check service status
docker-compose ps

# Execute command in container
docker-compose exec auth-service /bin/bash

# View resource usage
docker stats
```

### Health Check Procedures

```bash
# ============================================================================
# Health Check Commands
# ============================================================================

# Check all services via gateway
curl http://localhost/health

# Check individual services
curl http://localhost:8001/health  # Auth
curl http://localhost:8002/health  # STT
curl http://localhost:8003/health  # TTS
curl http://localhost:8004/health  # Recording
curl http://localhost:8005/health  # LLM
curl http://localhost:8006/health  # Class Management
curl http://localhost:8008/health  # Content Capture
curl http://localhost:8009/health  # AI Study Tools
curl http://localhost:8010/health  # Social
curl http://localhost:8011/health  # Gamification
curl http://localhost:8012/health  # Analytics
curl http://localhost:8013/health  # Notifications

# Check infrastructure
docker exec lm-postgres pg_isready
docker exec lm-redis redis-cli ping
curl http://localhost:8000/api/v1/heartbeat  # ChromaDB
curl http://localhost:11434/api/tags  # Ollama

# Expected response format:
# {
#   "status": "healthy",
#   "service": "service-name",
#   "version": "1.0.0",
#   "dependencies": {
#     "database": "connected",
#     "redis": "connected"
#   }
# }
```

### Database Operations

```bash
# ============================================================================
# Database Operations
# ============================================================================

# Connect to database
docker exec -it lm-postgres psql -U postgres -d littlemonster

# Run schema migrations
python database/scripts/deploy-schema.py

# Backup database
docker exec lm-postgres pg_dump -U postgres littlemonster > backup_$(date +%Y%m%d).sql

# Restore database
docker exec -i lm-postgres psql -U postgres littlemonster < backup_20251104.sql

# Verify tables
python database/scripts/verify_tables.py

# Seed database with test data
python database/seeds/seed_all.py

# Check database size
docker exec lm-postgres psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('littlemonster'));"

# Check connection count
docker exec lm-postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity WHERE datname='littlemonster';"
```

---

## Monitoring & Alerting

### Key Performance Indicators

```
Service Health Metrics:

┌─────────────────────────────────────────────────────┐
│  CRITICAL METRICS (Alert Immediately)               │
├─────────────────────────────────────────────────────┤
│  • Service availability < 99.5%                     │
│  • Response time P95 > 1000ms                       │
│  • Error rate > 1%                                  │
│  • Database connection pool > 90%                   │
│  • Redis memory > 90%                               │
│  • Disk usage > 85%                                 │
│  • CPU usage > 80% (sustained 5min)                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  WARNING METRICS (Investigate Soon)                 │
├─────────────────────────────────────────────────────┤
│  • Response time P95 > 500ms                        │
│  • Error rate > 0.5%                                │
│  • Queue depth > 100                                │
│  • Failed job rate > 5%                             │
│  • Memory usage > 75%                               │
└─────────────────────────────────────────────────────┘
```

### Monitoring Commands

```bash
# View real-time container stats
docker stats

# View service logs
docker-compose logs --tail=100 -f auth-service

# View error logs only
docker-compose logs auth-service 2>&1 | findstr ERROR

# Check database connections
docker exec lm-postgres psql -U postgres -c "SELECT pid, usename, application_name, state, query_start FROM pg_stat_activity WHERE datname = 'littlemonster' ORDER BY query_start DESC LIMIT 20;"

# Check Redis memory usage
docker exec lm-redis redis-cli INFO memory

# Check Redis key count
docker exec lm-redis redis-cli DBSIZE
```

---

## Backup & Recovery

### Backup Strategy

```
Backup Schedule:

┌────────────────────────────────────────────────────┐
│              BACKUP TIERS                          │
├────────────────────────────────────────────────────┤
│                                                    │
│  Tier 1: Continuous (WAL Archiving)              │
│  └─ PostgreSQL Write-Ahead Logs                   │
│  └─ Frequency: Continuous                          │
│  └─ Retention: 7 days                             │
│  └─ Recovery: Point-in-time                        │
│                                                    │
│  Tier 2: Hourly Snapshots                         │
│  └─ Redis RDB snapshots                           │
│  └─ Frequency: Every hour                          │
│  └─ Retention: 24 hours                           │
│  └─ Recovery: Last known good state               │
│                                                    │
│  Tier 3: Daily Full Backups                       │
│  └─ PostgreSQL pg_dump                            │
│  └─ Vector database exports                        │
│  └─ Frequency: Daily at 2 AM UTC                  │
│  └─ Retention: 30 days                            │
│  └─ Recovery: Full restore                         │
│                                                    │
│  Tier 4: Weekly Archives                          │
│  └─ Complete system backup                         │
│  └─ Frequency: Sunday at 3 AM UTC                 │
│  └─ Retention: 90 days                            │
│  └─ Recovery: Disaster recovery                    │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Backup Commands

```bash
# Full PostgreSQL backup
docker exec lm-postgres pg_dump -U postgres -Fc littlemonster > backups/lm_full_$(date +%Y%m%d_%H%M%S).dump

# Backup with compression
docker exec lm-postgres pg_dump -U postgres littlemonster | gzip > backups/lm_$(date +%Y%m%d).sql.gz

# Export Redis data
docker exec lm-redis redis-cli --rdb backups/redis_dump.rdb

# Automated backup script
# Save as /usr/local/bin/backup-lm.sh
```

### Recovery Procedures

```bash
# 1. Full Database Restore
docker exec lm-postgres psql -U postgres -c "DROP DATABASE IF EXISTS littlemonster;"
docker exec lm-postgres psql -U postgres -c "CREATE DATABASE littlemonster;"
docker exec -i lm-postgres pg_restore -U postgres -d littlemonster < backups/lm_full_20251104.dump

# 2. Redis Restore
docker exec lm-redis redis-cli SHUTDOWN SAVE
docker cp backups/redis_dump.rdb lm-redis:/data/dump.rdb
docker-compose restart redis

# 3. Verify Recovery
python scripts/utilities/validate_system.py

# 4. Restart services
docker-compose up -d
```

---

## Troubleshooting Guide

### Common Issues

```
┌─────────────────────────────────────────────────────────────┐
│                  TROUBLESHOOTING MATRIX                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Issue: Service won't start                                 │
│  ├─ Check: Docker logs (docker logs lm-service)            │
│  ├─ Check: Port conflicts (netstat -ano | findstr PORT)    │
│  ├─ Check: Environment variables (.env file)               │
│  └─ Solution: Fix config, restart service                   │
│                                                              │
│  Issue: High CPU usage                                      │
│  ├─ Check: Container stats (docker stats)                  │
│  ├─ Check: Slow queries (pg_stat_statements)               │
│  └─ Solution: Optimize queries, scale horizontally          │
│                                                              │
│  Issue: Database connection errors                          │
│  ├─ Check: Max connections (SHOW max_connections;)         │
│  ├─ Check: Connection pool settings                         │
│  └─ Solution: Increase max_connections                      │
│                                                              │
│  Issue: 502 Bad Gateway                                     │
│  ├─ Check: Target service health                           │
│  ├─ Check: Nginx upstream config                           │
│  └─ Solution: Restart service, check logs                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Debug Mode

```bash
# Set LOG_LEVEL=DEBUG in .env
echo "LOG_LEVEL=DEBUG" >> .env

# Restart services
docker-compose restart

# View verbose logs
docker-compose logs -f --tail=1000

# Test specific endpoint
curl -v -H "Authorization: Bearer $TOKEN" http://localhost/api/auth/me
```

---

## Performance Tuning

### Database Performance

```sql
-- Identify slow queries
SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Check indexes
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public';
```

### Caching Strategy

```
Cache Hierarchy:

Layer 1: Browser Cache (static assets, 1 hour - 1 day)
Layer 2: Redis Cache (sessions, API responses, 1-24 hours)
Layer 3: Database (source of truth, permanent)
```

---

## Scaling Procedures

### Horizontal Scaling

```bash
# Scale specific service
docker-compose up -d --scale llm-service=3

# Production scaling (AWS ECS)
aws ecs update-service \
  --cluster lm-production \
  --service lm-llm \
  --desired-count 5
```

---

## Disaster Recovery

### Recovery Time Objectives

```
┌──────────────────┬─────────┬─────────┬──────────────┐
│ Severity         │   RTO   │   RPO   │   Priority   │
├──────────────────┼─────────┼─────────┼──────────────┤
│ Critical         │  5 min  │  5 min  │      1       │
│ (Auth down)      │         │         │              │
├──────────────────┼─────────┼─────────┼──────────────┤
│ High             │ 15 min  │ 15 min  │      2       │
│ (Core services)  │         │         │              │
├──────────────────┼─────────┼─────────┼──────────────┤
│ Medium           │  1 hour │ 30 min  │      3       │
│ (Optional feat)  │         │         │              │
└──────────────────┴─────────┴─────────┴──────────────┘

RTO = Recovery Time Objective (max downtime)
RPO = Recovery Point Objective (max data loss)
```

---

## Reference

For complete operational procedures, monitoring specifications, and detailed troubleshooting guides, see the archived alpha-0.9 documentation at docs/historical/alpha-0.9-archived/DEPLOYMENT-OPERATIONS.md.
