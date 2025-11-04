"""Fix all hardcoded service URLs to use gateway"""
import re

files_to_fix = [
    ('views/web-app/src/app/dashboard/groups/page.tsx', 'localhost:8010', 'localhost'),
    ('views/web-app/src/app/dashboard/flashcards/page.tsx', 'localhost:8009', 'localhost'),
    ('views/web-app/src/app/dashboard/assignments/page.tsx', 'localhost:8007', 'localhost'),
]

for filepath, old_url, new_url in files_to_fix:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count occurrences
    count = content.count(old_url)
    
    # Replace
    new_content = content.replace(old_url, new_url)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Fixed {count} occurrences in {filepath}")

print("\nAll hardcoded URLs fixed!")
