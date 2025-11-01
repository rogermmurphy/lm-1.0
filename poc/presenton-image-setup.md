# Presenton Image Setup - Free Options

**Current Status**: Presenton running at http://localhost:5000  
**Current Config**: Pexels (FREE stock photos)

---

## What Presenton Needs

Presenton generates PowerPoint presentations and needs images for slides. It supports:
1. **Stock photos** (Pexels, Unsplash)
2. **AI-generated images** (DALL-E, Stable Diffusion, etc.)

---

## Free Options Available

### Option 1: Pexels (Already Configured!) ✅

**What it is**: FREE stock photo API  
**Cost**: $0 - completely free  
**What you get**: Professional stock photos for presentations  
**Limit**: 200 requests/hour free

**Setup**:
1. Go to https://www.pexels.com/api/
2. Sign up for free API key
3. Update docker-compose.yml:
   ```yaml
   PEXELS_API_KEY=your_actual_key_here
   ```
4. Restart Presenton: `docker-compose restart presenton`

**Status**: This is what you're using now. Just need real API key.

---

### Option 2: Unsplash (Also FREE) ✅

**What it is**: FREE high-quality stock photos  
**Cost**: $0  
**Limit**: 50 requests/hour free

**Setup**:
1. Go to https://unsplash.com/developers
2. Create free app
3. Get API key
4. Update docker-compose.yml:
   ```yaml
   IMAGE_PROVIDER=unsplash
   UNSPLASH_API_KEY=your_key_here
   ```

---

### Option 3: Local Stable Diffusion (FREE but Complex) 🔧

**What it is**: Self-hosted AI image generation  
**Cost**: $0 (uses your hardware)  
**Requirements**: 
- 8GB+ GPU (NVIDIA)
- Or 16GB+ RAM for CPU mode (very slow)

**Setup with ComfyUI** (Easiest self-hosted option):
```bash
# Install ComfyUI in Docker
docker run -p 8188:8188 \
  -v ./comfyui:/workspace \
  --name comfyui \
  pytorch/pytorch:latest

# Download Stable Diffusion model
# Connect Presenton to ComfyUI API
```

**Verdict**: Possible but requires GPU or lots of RAM. Same issues as Ollama.

---

### Option 4: Hugging Face Inference API (FREE Tier) ✅

**What it is**: Free hosted AI image generation  
**Cost**: FREE tier available  
**Model**: Stable Diffusion XL  
**Limit**: Rate limited but functional for POC

**Setup**:
1. Go to https://huggingface.co/
2. Sign up (free)
3. Get API token
4. Configure Presenton with HuggingFace endpoint

---

## Recommendation: Stick with Pexels ✅

**Why**:
- ✅ Completely free
- ✅ No setup complexity
- ✅ Already configured in your docker-compose
- ✅ Professional quality images
- ✅ 200 requests/hour is plenty for POC
- ✅ Works immediately with API key

**What to do**:
1. Get free Pexels API key (2 minutes)
2. Update your docker-compose.yml
3. Restart Presenton
4. Done!

---

## Current Presenton Config

From your docker-compose.yml:
```yaml
presenton:
  environment:
    - LLM=ollama
    - OLLAMA_URL=http://ollama:11434
    - OLLAMA_MODEL=gpt-oss  # Need to change to llama3.2:3b
    - IMAGE_PROVIDER=pexels
    - PEXELS_API_KEY=${PEXELS_API_KEY:-your_pexels_api_key_here}
```

**Issues**:
- OLLAMA_MODEL=gpt-oss won't work (RAM issue)
- PEXELS_API_KEY needs real key

**Fix**:
Update `old/Ella-Ai/docker-compose.yml`:
```yaml
- OLLAMA_MODEL=llama3.2:3b  # Change this
- PEXELS_API_KEY=your_real_key_here  # Add real key
```

---

## Get Pexels API Key (2 minutes)

1. Visit https://www.pexels.com/api/
2. Click "Get Started"
3. Sign up (free)
4. Get API key
5. Copy it to docker-compose.yml
6. Restart: `docker-compose restart presenton`

**That's it! Free forever, no credit card needed.**

---

## Test Presenton

After setup, visit: http://localhost:5000

Create a presentation on any topic and it will:
- Use Ollama (your local LLM) for content
- Use Pexels for images (free stock photos)
- Generate PowerPoint/PDF

---

## Future Upgrade Options

When you want AI-generated images (not stock photos):
1. **Hugging Face API** - Free tier
2. **RunPod/vast.ai** - Cheap GPU rental (~$0.20/hour)
3. **Replicate** - Pay per use, very cheap
4. **Local Stable Diffusion** - When you get GPU

But for POC, **Pexels stock photos are perfect and FREE**.

---

**Status**: Presenton is ready, just needs Pexels API key  
**Cost**: $0  
**Time to setup**: 2 minutes
