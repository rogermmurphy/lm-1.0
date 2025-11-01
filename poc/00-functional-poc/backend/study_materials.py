"""
Study Materials Generator - Create flashcards, quizzes, and study guides
"""

import requests
import json
from typing import List, Dict
import re

class StudyMaterialsGenerator:
    def __init__(self, 
                 ollama_host="localhost",
                 ollama_port=11434,
                 model="llama3.2:3b"):
        """Initialize study materials generator"""
        self.ollama_url = f"http://{ollama_host}:{ollama_port}/api/generate"
        self.model = model
        print(f"[OK] Study Materials Generator initialized")
        print(f"  - Ollama: {ollama_host}:{ollama_port}")
        print(f"  - Model: {model}")
    
    def ask_ollama(self, prompt: str) -> str:
        """Send prompt to Ollama"""
        try:
            response = requests.post(self.ollama_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }, timeout=300)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            print(f"[ERROR] Error calling Ollama: {e}")
            return f"Error: {str(e)}"
    
    def generate_flashcards(self, topic: str, context: str = None, count: int = 10) -> List[Dict]:
        """Generate flashcards on a topic"""
        print(f"\nGenerating {count} flashcards on: {topic}")
        
        if context:
            prompt = f"""Based on the following educational content, create {count} flashcards for studying {topic}.

Content:
{context}

Create {count} flashcards in this EXACT format:

Q: [Question text]
A: [Answer text]

Q: [Question text]
A: [Answer text]

Make the questions test understanding, not just memorization. Include key facts, definitions, and concepts."""
        else:
            prompt = f"""Create {count} educational flashcards about {topic} for high school students.

Use this EXACT format:

Q: [Question text]
A: [Answer text]

Q: [Question text]
A: [Answer text]

Cover key concepts, definitions, and important facts. Make questions clear and answers concise."""
        
        response = self.ask_ollama(prompt)
        flashcards = self.parse_flashcards(response)
        
        print(f"[OK] Generated {len(flashcards)} flashcards")
        return flashcards
    
    def parse_flashcards(self, text: str) -> List[Dict]:
        """Parse flashcard text into structured data"""
        flashcards = []
        lines = text.split('\n')
        current_card = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                if current_card and 'question' in current_card and 'answer' in current_card:
                    flashcards.append(current_card)
                current_card = {'question': line[2:].strip()}
            elif line.startswith('A:') and 'question' in current_card:
                current_card['answer'] = line[2:].strip()
        
        # Add last card
        if current_card and 'question' in current_card and 'answer' in current_card:
            flashcards.append(current_card)
        
        return flashcards
    
    def generate_quiz(self, topic: str, context: str = None, count: int = 5, difficulty: str = "medium") -> List[Dict]:
        """Generate multiple choice quiz questions"""
        print(f"\nGenerating {count} quiz questions on: {topic} ({difficulty} difficulty)")
        
        if context:
            prompt = f"""Based on the following educational content, create {count} multiple-choice quiz questions about {topic}.

Content:
{context}

Create {count} questions in this EXACT format:

Q: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
ANSWER: [Correct letter]
EXPLANATION: [Why this is correct]

Q: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
ANSWER: [Correct letter]
EXPLANATION: [Why this is correct]

Make questions {difficulty} difficulty and test understanding, not just memorization."""
        else:
            prompt = f"""Create {count} multiple-choice quiz questions about {topic} for high school students.
Difficulty level: {difficulty}

Use this EXACT format:

Q: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
ANSWER: [Correct letter]
EXPLANATION: [Why this is correct]

Q: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
ANSWER: [Correct letter]
EXPLANATION: [Why this is correct]

Make questions test understanding and include plausible distractors."""
        
        response = self.ask_ollama(prompt)
        quiz = self.parse_quiz(response)
        
        print(f"[OK] Generated {len(quiz)} quiz questions")
        return quiz
    
    def parse_quiz(self, text: str) -> List[Dict]:
        """Parse quiz text into structured data"""
        questions = []
        lines = text.split('\n')
        current_q = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                if current_q and 'question' in current_q:
                    questions.append(current_q)
                current_q = {
                    'question': line[2:].strip(),
                    'options': {}
                }
            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                if 'options' in current_q:
                    letter = line[0]
                    text = line[2:].strip()
                    current_q['options'][letter] = text
            elif line.startswith('ANSWER:'):
                current_q['correct_answer'] = line[7:].strip()
            elif line.startswith('EXPLANATION:'):
                current_q['explanation'] = line[12:].strip()
        
        # Add last question
        if current_q and 'question' in current_q:
            questions.append(current_q)
        
        return questions
    
    def generate_study_guide(self, topic: str, context: str = None) -> Dict:
        """Generate a comprehensive study guide"""
        print(f"\nGenerating study guide for: {topic}")
        
        if context:
            prompt = f"""Create a comprehensive study guide based on this content about {topic}.

Content:
{context}

Study Guide Format:
1. OVERVIEW: Brief introduction
2. KEY CONCEPTS: Main ideas and definitions
3. IMPORTANT FACTS: Critical information to remember
4. STUDY TIPS: How to approach learning this material
5. PRACTICE QUESTIONS: 3 questions to test understanding

Make it clear, organized, and helpful for students."""
        else:
            prompt = f"""Create a comprehensive study guide about {topic} for high school students.

Include:
1. OVERVIEW: Brief introduction to the topic
2. KEY CONCEPTS: Main ideas and definitions
3. IMPORTANT FACTS: Critical information to remember
4. COMMON MISCONCEPTIONS: What students often get wrong
5. STUDY TIPS: How to master this material
6. PRACTICE QUESTIONS: 3 questions to test understanding

Make it clear, organized, and educational."""
        
        response = self.ask_ollama(prompt)
        
        return {
            "topic": topic,
            "content": response.strip()
        }

def main():
    """Test the study materials generator"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python study_materials.py <type> <topic>")
        print("Types: flashcards, quiz, guide")
        print('Example: python study_materials.py flashcards "photosynthesis"')
        sys.exit(1)
    
    material_type = sys.argv[1]
    topic = " ".join(sys.argv[2:])
    
    generator = StudyMaterialsGenerator()
    
    if material_type == "flashcards":
        flashcards = generator.generate_flashcards(topic, count=10)
        print(f"\n{'='*60}")
        print(f"FLASHCARDS: {topic}")
        print(f"{'='*60}\n")
        for i, card in enumerate(flashcards, 1):
            print(f"Card {i}:")
            print(f"Q: {card['question']}")
            print(f"A: {card['answer']}")
            print()
    
    elif material_type == "quiz":
        questions = generator.generate_quiz(topic, count=5)
        print(f"\n{'='*60}")
        print(f"QUIZ: {topic}")
        print(f"{'='*60}\n")
        for i, q in enumerate(questions, 1):
            print(f"Question {i}: {q['question']}")
            for letter, option in q.get('options', {}).items():
                print(f"  {letter}) {option}")
            print(f"  Answer: {q.get('correct_answer', 'N/A')}")
            print(f"  Explanation: {q.get('explanation', 'N/A')}")
            print()
    
    elif material_type == "guide":
        guide = generator.generate_study_guide(topic)
        print(f"\n{'='*60}")
        print(f"STUDY GUIDE: {guide['topic']}")
        print(f"{'='*60}\n")
        print(guide['content'])
    
    else:
        print(f"Unknown type: {material_type}")
        print("Use: flashcards, quiz, or guide")

if __name__ == "__main__":
    main()
