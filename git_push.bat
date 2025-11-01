@echo off
git add poc/07-langchain-agent/agent_bedrock.py
git commit -m "Security fix: Remove hardcoded AWS credentials"
git push origin main
