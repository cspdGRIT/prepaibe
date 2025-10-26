"""
AIBE Flashcard Generator - Python Helper Script
Generates flashcards using various LLM providers and expands JSON data
"""

import json
import os
from typing import List, Dict
import requests

class FlashcardGenerator:
    def __init__(self, provider='groq', api_key=None, config=None):
        """
        Initialize the flashcard generator
        
        Args:
            provider: 'groq', 'openrouter', 'ollama', or 'openai'
            api_key: API key for the provider
            config: Additional configuration dict
        """
        self.provider = provider
        self.api_key = api_key
        self.config = config or {}
        
    def generate_flashcards(self, topic_title, topic_subtitle, count=15, existing_questions=None):
        """
        Generate flashcards for a specific topic
        
        Args:
            topic_title: Main topic title
            topic_subtitle: Topic subtitle/description
            count: Number of cards to generate
            existing_questions: List of existing questions to avoid duplication
            
        Returns:
            List of flashcard dicts with 'q' and 'a' keys
        """
        existing_q_text = ""
        if existing_questions:
            existing_q_text = "\n\nExisting questions to avoid duplicating:\n" + "\n".join([f"- {q}" for q in existing_questions[:10]])
        
        prompt = f"""Generate {count} high-quality AIBE exam flashcards for the topic: "{topic_title}" ({topic_subtitle}).

Requirements:
- Each card should have a clear Question (q) and detailed Answer (a)
- Focus on exam-relevant concepts, sections, case laws, and principles
- Answers should be comprehensive but concise (2-4 sentences)
- Cover different subtopics within {topic_title}
- Include section numbers, legal principles, and practical examples
- Make questions progressively challenging
- Avoid duplicating existing questions{existing_q_text}

Format response as a JSON array:
[
  {{"q": "Question 1?", "a": "Answer 1"}},
  {{"q": "Question 2?", "a": "Answer 2"}}
]

Return ONLY the JSON array, no additional text or markdown formatting."""

        response = self._call_llm(prompt)
        return self._parse_flashcards(response)
    
    def _call_llm(self, prompt):
        """Call the configured LLM provider"""
        
        system_prompt = "You are an expert in Indian law preparing AIBE exam questions. Generate high-quality flashcards in valid JSON format only."
        
        if self.provider == 'groq':
            return self._call_groq(prompt, system_prompt)
        elif self.provider == 'openrouter':
            return self._call_openrouter(prompt, system_prompt)
        elif self.provider == 'ollama':
            return self._call_ollama(prompt, system_prompt)
        elif self.provider == 'openai':
            return self._call_openai(prompt, system_prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _call_groq(self, prompt, system_prompt):
        """Call Groq API"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.get('model', 'llama-3.1-70b-versatile'),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 4000
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def _call_openrouter(self, prompt, system_prompt):
        """Call OpenRouter API"""
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://aibe-prep.local",
            "X-Title": "AIBE Prep"
        }
        data = {
            "model": self.config.get('model', 'meta-llama/llama-3.1-8b-instruct:free'),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def _call_ollama(self, prompt, system_prompt):
        """Call Ollama local API"""
        url = f"{self.config.get('base_url', 'http://localhost:11434')}/api/chat"
        data = {
            "model": self.config.get('model', 'llama3.1'),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['message']['content']
    
    def _call_openai(self, prompt, system_prompt):
        """Call OpenAI-compatible API"""
        url = f"{self.config.get('base_url', 'https://api.openai.com/v1')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.get('model', 'gpt-3.5-turbo'),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def _parse_flashcards(self, response):
        """Parse LLM response to extract flashcards"""
        content = response.strip()
        
        # Remove markdown code blocks
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        
        # Try to find JSON array
        import re
        json_match = re.search(r'\[[\s\S]*\]', content)
        if json_match:
            content = json_match.group(0)
        
        try:
            cards = json.loads(content)
            if not isinstance(cards, list):
                raise ValueError("Response is not a list")
            return cards
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Response: {content[:200]}")
            return []


def expand_json_flashcards(input_file, output_file, generator, target_per_topic=15):
    """
    Expand existing JSON flashcards to meet minimum count
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSON file
        generator: FlashcardGenerator instance
        target_per_topic: Minimum cards per topic
    """
    
    # Load existing data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    topics = data.get('topics', [])
    flashcards = data.get('flashcards', {})
    
    print(f"Loaded {len(topics)} topics")
    
    # Process each topic
    for topic in topics:
        topic_id = str(topic['id'])
        existing_cards = flashcards.get(topic_id, [])
        existing_count = len(existing_cards)
        
        print(f"\nTopic {topic_id}: {topic['title']}")
        print(f"  Existing cards: {existing_count}")
        
        if existing_count < target_per_topic:
            needed = target_per_topic - existing_count
            print(f"  Generating {needed} more cards...")
            
            existing_questions = [card['q'] for card in existing_cards]
            
            try:
                new_cards = generator.generate_flashcards(
                    topic['title'],
                    topic['subtitle'],
                    count=needed,
                    existing_questions=existing_questions
                )
                
                flashcards[topic_id] = existing_cards + new_cards
                print(f"  ✅ Generated {len(new_cards)} cards")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
        else:
            print(f"  ✅ Already has enough cards")
    
    # Save expanded data
    expanded_data = {
        'topics': topics,
        'flashcards': flashcards
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(expanded_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved expanded flashcards to {output_file}")


def create_sample_json():
    """Create a sample JSON structure for flashcards"""
    data = {
        "topics": [
            {"id": 1, "title": "Contract Law", "subtitle": "Indian Contract Act, 1872"},
            {"id": 2, "title": "Constitutional Law", "subtitle": "Indian Constitution"},
            {"id": 3, "title": "Criminal Law", "subtitle": "IPC, CrPC, Evidence Act"},
            {"id": 4, "title": "Torts", "subtitle": "Law of Torts"},
            {"id": 5, "title": "Property Law", "subtitle": "Transfer of Property Act"}
        ],
        "flashcards": {
            "1": [
                {"q": "What is a contract under Section 2(h)?", "a": "An agreement enforceable by law."},
                {"q": "What are essential elements of a valid contract?", "a": "Offer, acceptance, consideration, capacity, free consent, lawful object."}
            ],
            "2": [
                {"q": "What is the Preamble?", "a": "Declares India as Sovereign, Socialist, Secular, Democratic Republic."}
            ],
            "3": [
                {"q": "What is mens rea?", "a": "Guilty mind - the mental element of a crime."}
            ],
            "4": [
                {"q": "What is a tort?", "a": "A civil wrong causing harm to another person."}
            ],
            "5": [
                {"q": "What is Transfer of Property Act about?", "a": "Regulates transfer of property between living persons."}
            ]
        }
    }
    
    with open('flashcards_sample.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ Created flashcards_sample.json")


# Example usage
if __name__ == "__main__":
    import sys
    
    print("AIBE Flashcard Generator")
    print("=" * 50)
    
    # Configuration
    PROVIDER = os.environ.get('LLM_PROVIDER', 'groq')
    API_KEY = os.environ.get('LLM_API_KEY', '')
    
    if len(sys.argv) > 1 and sys.argv[1] == 'sample':
        create_sample_json()
        sys.exit(0)
    
    if not API_KEY:
        print("\n⚠️  No API key found!")
        print("\nSet environment variables:")
        print("  export LLM_PROVIDER=groq  # or openrouter, ollama, openai")
        print("  export LLM_API_KEY=your_key_here")
        print("\nFor Ollama (local): export LLM_PROVIDER=ollama")
        print("\nOr create sample JSON: python script.py sample")
        sys.exit(1)
    
    # Configure generator
    config = {}
    if PROVIDER == 'ollama':
        config = {
            'base_url': 'http://localhost:11434',
            'model': 'llama3.1'
        }
        API_KEY = None  # Ollama doesn't need API key
    elif PROVIDER == 'openrouter':
        config = {'model': 'meta-llama/llama-3.1-8b-instruct:free'}
    elif PROVIDER == 'groq':
        config = {'model': 'llama-3.1-70b-versatile'}
    
    generator = FlashcardGenerator(
        provider=PROVIDER,
        api_key=API_KEY,
        config=config
    )
    
    # Check for input file
    input_file = 'flashcards_sample.json'
    output_file = 'flashcards_expanded.json'
    
    if not os.path.exists(input_file):
        print(f"\n⚠️  Input file '{input_file}' not found!")
        print("Creating sample file first...")
        create_sample_json()
    
    print(f"\n📚 Expanding flashcards from {input_file}")
    print(f"   Target: 15 cards per topic")
    print(f"   Provider: {PROVIDER}\n")
    
    try:
        expand_json_flashcards(input_file, output_file, generator, target_per_topic=15)
        print("\n" + "=" * 50)
        print("✅ Done! Use the expanded JSON in your HTML app.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
