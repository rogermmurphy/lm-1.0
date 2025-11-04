#!/usr/bin/env python3
"""Remove CORS from all microservices - nginx handles it"""
import os
import re

services = [
    'services/ai-study-tools/src/main.py',
    'services/social-collaboration/src/main.py',
    'services/gamification/src/main.py',
    'services/notifications/src/main.py',
    'services/study-analytics/src/main.py',
    'services/content-capture/src/main.py',
]

for service_path in services:
    if not os.path.exists(service_path):
        continue
    
    with open(service_path, 'r') as f:
        content = f.read()
    
    # Remove CORS middleware
    content = re.sub(
        r'from fastapi\.middleware\.cors import CORSMiddleware\n',
        '',
        content
    )
    
    content = re.sub(
        r'app\.add_middleware\(\s*CORSMiddleware,\s*allow_origins=.*?\)',
        '# CORS handled by nginx gateway',
        content,
        flags=re.DOTALL
    )
    
    # Remove OPTIONS handler
    content = re.sub(
        r'@app\.options\([^)]+\)\s*async def options_handler[^:]+:.*?(?=\n@|\nif __name__|$)',
        '# OPTIONS handled by nginx',
        content,
        flags=re.DOTALL
    )
    
    with open(service_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed: {service_path}")

print("Done! Rebuild affected containers.")
