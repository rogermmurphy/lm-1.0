"""
E2E Tests for AI Study Tools Service
Following zero-tolerance testing principles
"""
import requests
import json

BASE_URL = "http://localhost:8009"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ai-study-tools"
    print("[OK] Health check passed")

def test_create_flashcard_deck():
    """Test creating a flashcard deck"""
    payload = {
        "user_id": 1,
        "title": "Test Deck",
        "description": "Test flashcard deck"
    }
    response = requests.post(f"{BASE_URL}/api/flashcards/decks", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Deck"
    assert data["card_count"] == 0
    print(f"[OK] Created flashcard deck: ID {data['id']}")
    return data["id"]

def test_create_flashcard(deck_id):
    """Test creating a single flashcard"""
    payload = {
        "deck_id": deck_id,
        "front_text": "What is Python?",
        "back_text": "A high-level programming language"
    }
    response = requests.post(f"{BASE_URL}/api/flashcards/cards", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["front_text"] == "What is Python?"
    print(f"[OK] Created flashcard: ID {data['id']}")
    return data["id"]

def test_get_deck(deck_id):
    """Test retrieving a deck with cards"""
    response = requests.get(f"{BASE_URL}/api/flashcards/decks/{deck_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == deck_id
    assert data["card_count"] >= 1
    assert len(data["cards"]) >= 1
    print(f"[OK] Retrieved deck with {data['card_count']} cards")

def test_review_flashcard(card_id):
    """Test reviewing a flashcard (spaced repetition)"""
    payload = {
        "card_id": card_id,
        "user_id": 1,
        "quality": 4
    }
    response = requests.post(f"{BASE_URL}/api/flashcards/reviews", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "next_review_date" in data
    assert data["interval_days"] > 0
    print(f"[OK] Recorded review: Next review in {data['interval_days']} days")

def test_list_user_decks():
    """Test listing all decks for a user"""
    response = requests.get(f"{BASE_URL}/api/flashcards/decks/user/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    print(f"[OK] Listed {len(data)} decks for user")

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*60)
    print("AI STUDY TOOLS SERVICE - E2E TESTS")
    print("="*60 + "\n")
    
    try:
        # Test 1: Health check
        test_health()
        
        # Test 2: Create deck
        deck_id = test_create_flashcard_deck()
        
        # Test 3: Create card
        card_id = test_create_flashcard(deck_id)
        
        # Test 4: Get deck
        test_get_deck(deck_id)
        
        # Test 5: Review card
        test_review_flashcard(card_id)
        
        # Test 6: List decks
        test_list_user_decks()
        
        print("\n" + "="*60)
        print("[SUCCESS] ALL TESTS PASSED (6/6)")
        print("="*60 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n[FAIL] CONNECTION ERROR: Service not running on port 8009")
        return False
    except Exception as e:
        print(f"\n[FAIL] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
