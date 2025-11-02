"""
Locust Performance Test
Load testing for Little Monster services
Target: 1000+ concurrent users, <500ms response time
"""
from locust import HttpUser, task, between
import random


class LittleMonsterUser(HttpUser):
    """Simulated user for load testing"""
    
    wait_time = between(1, 3)
    host = "http://localhost"
    
    def on_start(self):
        """Login before starting tasks"""
        # Register
        self.client.post("/api/auth/register", json={
            "email": f"user{random.randint(1000,9999)}@example.com",
            "password": "TestPass123!",
            "username": f"user{random.randint(1000,9999)}"
        })
        
        # Login
        response = self.client.post("/api/auth/login", json={
            "email": self.email,
            "password": "TestPass123!"
        })
        
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
    
    @task(3)
    def chat_with_ai(self):
        """Test AI chat endpoint (most common operation)"""
        self.client.post("/api/chat/message", 
            json={"message": "What is photosynthesis?", "use_rag": False},
            headers={"Authorization": f"Bearer {self.access_token}"})
    
    @task(1)
    def get_conversations(self):
        """Test conversation list"""
        self.client.get("/api/chat/conversations",
            headers={"Authorization": f"Bearer {self.access_token}"})
    
    @task(1)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/health")


# Run with: locust -f tests/performance/locustfile.py
# Open browser: http://localhost:8089
# Set users: 1000, spawn rate: 100
# Target: All requests <500ms p95
