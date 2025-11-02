"""
Direct Bedrock Test - Verify Claude Sonnet 4 works
"""
import boto3
import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

# Create client (uses AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from environment)
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Model ID - needs "us." prefix for cross-region inference
model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Simple test
conversation = [
    {
        "role": "user",
        "content": [{"text": "What is 2+2? Answer in one sentence."}],
    }
]

try:
    print(f"Testing model: {model_id}")
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )
    
    response_text = response["output"]["message"]["content"][0]["text"]
    print(f"SUCCESS: {response_text}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
