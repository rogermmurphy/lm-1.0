#!/usr/bin/env python3
"""
Create Phase 6 service directory structure
"""
import os

# Define the directory structure
directories = [
    "services/study-analytics",
    "services/study-analytics/src",
    "services/study-analytics/src/routes",
    "services/study-analytics/src/services",
]

# Create directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created: {directory}")

# Create __init__.py files
init_files = [
    "services/study-analytics/src/__init__.py",
    "services/study-analytics/src/routes/__init__.py",
    "services/study-analytics/src/services/__init__.py",
]

for init_file in init_files:
    with open(init_file, 'w') as f:
        f.write('"""Package initialization"""\n')
    print(f"Created: {init_file}")

print("\nPhase 6 directory structure created successfully!")
