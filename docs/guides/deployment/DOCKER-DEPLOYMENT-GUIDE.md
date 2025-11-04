**Last Updated:** November 4, 2025

# Docker Deployment Guide for Internet Access

## Overview

This guide explains how to:
1. Containerize the web app (frontend) with Docker
2. Deploy the entire stack to free hosting platforms
3. Make your application accessible from the internet

## Quick Answer: Localhost:3000

Yes! Once you run `npm run dev` in the `views/web-app` directory:
- Frontend will be at `http://localhost:3000`
- It connects to backend API at `http://localhost:80` (API Gateway)
- Everything should work locally

## Complete Docker Solution

### 1. Create Web App Dockerfile

I'll create `views/web-app/Dockerfile` to containerize the frontend.

### 2. Update docker-compose.yml

Add web app service to run alongside backend services.

### 3. Free Hosting Platform Options

#### Option A: Render.com (Recommended - Free Tier)
- **Pros:**
  - True free tier (no credit card required)
  - Supports Docker & docker-compose
  - PostgreSQL, Redis included
  - Auto-deploy from GitHub
  - SSL certificates included
  - Custom domains supported
- **Cons:**
  - Services spin down after 15 minutes of inactivity (30 second cold start)
  - 750 hours/month free tier limit

#### Option B: Railway.app (Great for Docker)
- **Pros:**
  - $5 free credit monthly (no credit card for first month)
  - Excellent Docker support
  - Fast deployments
  - Great developer experience
- **Cons:**
  - Requires credit card after trial
  - Limited free tier

#### Option C: Fly.io (Docker-Native)
- **Pros:**
  - Free tier: 3 shared-cpu-1x 256MB VMs
  - Native Docker support
  - Global deployment
  - Good for microservices
- **Cons:**
  - Requires credit card
  - Complex pricing model

#### Option D: Heroku (Classic but Paid)
- **Pros:**
  - Well documented
  - Easy deployment
- **Cons:**
  - No longer offers free tier (minimum $5/month)

### 4. Recommended Approach: Render.com

## Deployment Architecture

### Current Local Setup
```
Your Computer:
├── Backend Services (Docker) - Port 80 (API Gateway)
│   ├── Authentication - Port 8001
│   ├── LLM Agent - Port 8005
│   ├── Speech-to-Text - Port 8002
│   └── ... (other services)
├── Web App (npm run dev) - Port 3000
└── Database/Redis (Docker)
```

### Cloud Deployment on Render.com
```
Internet Users
    ↓
https://your-app.onrender.com (Render CDN + SSL)
    ↓
Web App Container (Port 3000)
    ↓
API Gateway Container (Port 80)
    ↓
Microservices Containers
    ↓
PostgreSQL + Redis (Render Managed Services)
```

## Step-by-Step Deployment to Render.com

### Prerequisites
1. GitHub account
2. Push your code to GitHub repository
3. Render.com account (free - no credit card)

### Step 1: Prepare Repository
```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Configure Render

Create `render.yaml` in project root for Infrastructure as Code deployment.

### Step 3: Environment Variables

Create `.env.production` files for each service with production settings.

### Step 4: Deploy

1. Go to Render.com dashboard
2. Click "New +" → "Blueprint"
3. Connect GitHub repository
4. Render will auto-detect `render.yaml`
5. Deploy!

## Simplified Alternative: Single Container Deployment

For easier deployment, we can combine frontend and backend into a single deployment unit.

### Architecture
```
Single Container:
├── Nginx (Reverse Proxy)
│   ├── / → Next.js Frontend
│   └── /api → Backend Services
└── Backend Services (FastAPI/Uvicorn)
```

## Environment Variables for Production

### Frontend (.env.production)
```env
NEXT_PUBLIC_API_URL=https://your-api.onrender.com
NODE_ENV=production
```

### Backend Services
```env
DATABASE_URL=postgresql://user:pass@postgres:5432/db
REDIS_URL=redis://redis:6379
JWT_SECRET_KEY=your-production-secret
OLLAMA_URL=http://ollama:11434
```

## Cost Considerations

### Render.com Free Tier Breakdown
- Web Services: 750 hours/month (enough for 1 always-on service)
- PostgreSQL: 90-day free trial, then $7/month
- Redis: Add-on required (minimal cost)

### Optimization Tips
1. Use Render's PostgreSQL free trial
2. Use Redis Cloud free tier (separate)
3. Single web service that runs frontend + API gateway
4. Backend microservices can be separate services that spin down

### Monthly Cost Estimate (After Free Tier)
- Minimal: $0-$7/month (if you stay within limits)
- Comfortable: $15-25/month (all services always-on)
- Compare to AWS: Would be $50-100/month minimum

## Important Notes

### Docker Compose Limitations
Most free platforms don't support full `docker-compose.yml` deployment. Options:
1. Convert to individual services (Render Blueprint)
2. Use Docker Swarm/Kubernetes (more complex)
3. Deploy to a VPS with docker-compose support

### Ollama in Production
Running Ollama (local LLM) in cloud is challenging:
- Requires GPU for good performance
- Large memory requirements (4GB+ for small models)
- **Recommendation:** Switch to AWS Bedrock (Claude) for production
  - Already configured in your codebase
  - Pay per use
  - Much more cost effective than running GPU servers

## Next Steps

1. **Immediate:** I'll create the necessary files for Docker deployment
2. **Short-term:** Test locally with full Docker stack
3. **Production:** Deploy to Render.com or Railway

Would you like me to:
1. Create the Dockerfile for web app?
2. Update docker-compose.yml to include web app?
3. Create render.yaml for easy deployment?
4. All of the above?
