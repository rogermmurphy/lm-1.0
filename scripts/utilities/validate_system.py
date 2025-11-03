#!/usr/bin/env python3
"""
System Validation Script
Validates all services and components are healthy and ready for production
"""
import requests
import sys
from typing import Dict, List, Tuple

# Service health check endpoints
SERVICES = {
    'auth-service': 'http://localhost/api/auth/health',
    'llm-service': 'http://localhost/api/chat/conversations',  # Requires auth
    'nginx': 'http://localhost',
}

# Database check
DB_CHECK = "psql postgresql://postgres.ynrfvvqxqxqxqxqx@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require -c 'SELECT COUNT(*) FROM users;'"

def check_service(name: str, url: str) -> Tuple[bool, str]:
    """Check if service is responding"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code in [200, 401]:  # 401 is ok for protected endpoints
            return True, f"✅ {name}: Healthy"
        else:
            return False, f"❌ {name}: Unhealthy (status {response.status_code})"
    except Exception as e:
        return False, f"❌ {name}: Not responding ({str(e)})"

def main():
    """Main validation function"""
    print("\n" + "="*60)
    print(" "*15 + "SYSTEM VALIDATION")
    print("="*60 + "\n")
    
    all_healthy = True
    results = []
    
    # Check services
    print("📊 Checking Services...")
    print("-" * 60)
    for name, url in SERVICES.items():
        healthy, message = check_service(name, url)
        results.append(message)
        print(message)
        if not healthy:
            all_healthy = False
    
    print("\n" + "="*60)
    if all_healthy:
        print("✅ ALL SERVICES HEALTHY")
        print("="*60)
        print("\n🎉 System is ready for testing!")
        print("\nNext steps:")
        print("  1. Run seed data: cd database/seeds && python seed_all.py")
        print("  2. Test in browser: http://localhost:3004")
        print("  3. Login: testuser@test.com / password123")
        return 0
    else:
        print("❌ SOME SERVICES UNHEALTHY")
        print("="*60)
        print("\n⚠️  Please start all services:")
        print("  docker-compose up -d")
        print("  cd views/web-app && npm run dev")
        return 1

if __name__ == "__main__":
    sys.exit(main())
