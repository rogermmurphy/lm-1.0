# AWS Bedrock LLM Switch Guide

## Overview

The LLM Agent service now supports **two LLM providers**:

| Provider | Speed | Cost | Use Case |
|----------|-------|------|----------|
| **Ollama** (llama3.2:3b) | 3-5 minutes per response | Free (local) | Production (when hardware upgraded) |
| **AWS Bedrock** (Claude 3 Sonnet) | <10 seconds per response | Pay-per-use | Fast testing & development |

## Why This Was Added

**Problem**: Ollama responses take 3-5 minutes, making zero-tolerance test-fix-test cycles impractical.

**Solution**: Add AWS Bedrock as a fast testing alternative without removing Ollama functionality.

## Architecture

```
┌─────────────────────────────────────────────────┐
│            LLM Service (Unified)                │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  if provider == "bedrock":              │   │
│  │      bedrock_service.generate()         │   │
│  │  else:                                  │   │
│  │      ollama_service.generate()          │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
         │                        │
         │                        │
    ┌────▼────┐            ┌─────▼──────┐
    │ Bedrock │            │   Ollama   │
    │ Claude  │            │ llama3.2:3b│
    │ <10s    │            │  3-5 min   │
    └─────────┘            └────────────┘
```

## How to Switch Providers

### Method 1: Environment Variable (Recommended)

Edit `services/llm-agent/.env`:

```bash
# For fast testing (Bedrock)
LLM_PROVIDER=bedrock

# For production (Ollama)
LLM_PROVIDER=ollama
```

Then restart the LLM service:

```bash
docker-compose restart llm-agent
```

### Method 2: Docker Compose Override

Edit `docker-compose.yml` and add environment variable to llm-agent service:

```yaml
llm-agent:
  environment:
    - LLM_PROVIDER=bedrock  # or ollama
```

## Using Bedrock (Cloud)

### Step 1: Get AWS Credentials

You need AWS credentials with Bedrock access:

1. Log into AWS Console
2. Go to IAM → Users → Create Access Key
3. Ensure user has `bedrock:InvokeModel` permission
4. Copy Access Key ID and Secret Access Key

### Step 2: Configure Credentials

Edit `services/llm-agent/.env`:

```bash
# LLM Provider Selection
LLM_PROVIDER=bedrock

# AWS Bedrock Configuration
BEDROCK_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Step 3: Install Dependencies

```bash
cd services/llm-agent
pip install -r requirements.txt  # Includes boto3
```

### Step 4: Restart Service

```bash
docker-compose restart llm-agent
```

### Step 5: Verify

Check logs for:
```
[LLM] Using AWS Bedrock (anthropic.claude-3-sonnet-20240229-v1:0)
```

## Using Ollama (Local)

### Step 1: Configure

Edit `services/llm-agent/.env`:

```bash
# LLM Provider Selection
LLM_PROVIDER=ollama

# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

### Step 2: Ensure Ollama is Running

```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Should return list of models including llama3.2:3b
```

### Step 3: Restart Service

```bash
docker-compose restart llm-agent
```

### Step 4: Verify

Check logs for:
```
[LLM] Using Ollama (llama3.2:3b)
```

## Testing the Switch

### Test with Bedrock

1. Set `LLM_PROVIDER=bedrock` in `.env`
2. Add AWS credentials
3. Restart: `docker-compose restart llm-agent`
4. Send chat message via UI
5. Response should arrive in <10 seconds

### Test with Ollama

1. Set `LLM_PROVIDER=ollama` in `.env`
2. Restart: `docker-compose restart llm-agent`
3. Send chat message via UI
4. Response will take 3-5 minutes (expected)

## Code Changes Summary

### Files Modified

1. **`src/config.py`**: Added `LLM_PROVIDER`, `BEDROCK_MODEL` config
2. **`src/services/bedrock_service.py`**: New - Bedrock integration
3. **`src/services/llm_service.py`**: Updated to support both providers
4. **`requirements.txt`**: Added `boto3>=1.28.0`
5. **`.env`**: Added provider selection and Bedrock credentials

### Key Implementation

```python
class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        
        if self.provider == "bedrock":
            self.bedrock_service = BedrockService()
            print(f"[LLM] Using AWS Bedrock")
        else:
            self.ollama_url = f"{settings.OLLAMA_URL}/api/generate"
            print(f"[LLM] Using Ollama")
    
    def generate(self, prompt, temperature=0.7, max_tokens=None):
        if self.provider == "bedrock":
            return self.bedrock_service.generate(prompt, temperature, max_tokens)
        else:
            # Ollama logic
            ...
```

## Benefits

✅ **Fast Testing**: Bedrock responses in <10 seconds vs 3-5 minutes  
✅ **Ollama Preserved**: All Ollama code intact for production  
✅ **Simple Switch**: One environment variable  
✅ **Same API**: UI sees no difference  
✅ **Proven Code**: Bedrock integration from validated POC 07  

## Cost Considerations

### Bedrock Costs

- **Model**: Claude 3 Sonnet
- **Pricing**: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- **Typical Chat**: ~500 tokens = $0.01 per chat
- **100 test chats**: ~$1.00

### Ollama Costs

- **Free** (runs locally)
- **But slow**: 3-5 minutes per response

## Troubleshooting

### "Bedrock generation failed"

**Cause**: Invalid AWS credentials or missing Bedrock access

**Fix**:
1. Verify AWS credentials in `.env`
2. Check IAM permissions include `bedrock:InvokeModel`
3. Ensure Bedrock is enabled in your AWS region

### "Connection refused to Ollama"

**Cause**: Ollama service not running

**Fix**:
```bash
# Start Ollama
docker-compose up -d ollama

# Or on host
ollama serve
```

### Service starts but no provider message

**Cause**: Invalid `LLM_PROVIDER` value

**Fix**: Ensure `LLM_PROVIDER` is exactly `"ollama"` or `"bedrock"` (lowercase)

## Next Steps

1. **For Testing**: Switch to Bedrock for fast zero-tolerance testing
2. **After Testing**: Switch back to Ollama for production
3. **Future**: Upgrade hardware to speed up Ollama responses

## Reference: POC 07

Original Bedrock implementation: `poc/07-langchain-agent/agent_bedrock.py`

Test results showing <5 second responses: `poc/07-langchain-agent/BEDROCK-TEST-RESULT.md`
