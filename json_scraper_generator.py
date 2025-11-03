"""
AIBE Flashcard Web Scraper and JSON Generator
Scrapes legal content from websites and generates flashcards using LLM
"""

import json
import os
import re
import time
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    os.system("pip install requests beautifulsoup4 lxml --break-system-packages")
    import requests
    from bs4 import BeautifulSoup


class LegalContentScraper:
    """Scrapes legal content from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_indiankanoon(self, query: str, max_results: int = 5) -> List[Dict]:
        """Scrape content from Indian Kanoon"""
        results = []
        try:
            url = f"https://indiankanoon.org/search/?formInput={query.replace(' ', '%20')}"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for result in soup.find_all('div', class_='result')[:max_results]:
                title_elem = result.find('a', class_='cite')
                if title_elem:
                    title = title_elem.text.strip()
                    link = 'https://indiankanoon.org' + title_elem['href']
                    
                    # Get content from result page
                    content = self._extract_text(result)
                    
                    results.append({
                        'title': title,
                        'url': link,
                        'content': content,
                        'source': 'Indian Kanoon'
                    })
                    
            print(f"✅ Scraped {len(results)} results from Indian Kanoon")
        except Exception as e:
            print(f"❌ Error scraping Indian Kanoon: {e}")
        
        return results
    
    def scrape_wikipedia_legal(self, topic: str) -> Dict:
        """Scrape legal topic from Wikipedia"""
        try:
            # Try to find relevant Wikipedia article
            search_terms = [
                topic,
                f"{topic} India",
                f"Indian {topic}",
                f"{topic} Act"
            ]
            
            for term in search_terms:
                url = f"https://en.wikipedia.org/wiki/{term.replace(' ', '_')}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    content_div = soup.find('div', {'id': 'mw-content-text'})
                    
                    if content_div:
                        # Extract paragraphs
                        paragraphs = []
                        for p in content_div.find_all('p', limit=10):
                            text = p.text.strip()
                            if len(text) > 50:  # Skip short paragraphs
                                paragraphs.append(text)
                        
                        if paragraphs:
                            print(f"✅ Found Wikipedia article: {term}")
                            return {
                                'title': term,
                                'url': url,
                                'content': '\n\n'.join(paragraphs),
                                'source': 'Wikipedia'
                            }
            
            print(f"⚠️  No Wikipedia article found for: {topic}")
            return {}
            
        except Exception as e:
            print(f"❌ Error scraping Wikipedia: {e}")
            return {}
    
    def scrape_bare_acts(self, act_name: str) -> Dict:
        """Scrape bare act content from legal databases"""
        results = {'sections': [], 'source': 'Bare Acts'}
        
        try:
            # Try IndianKanoon for bare acts
            url = f"https://indiankanoon.org/search/?formInput={act_name.replace(' ', '%20')}%20bare%20act"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract first result
            first_result = soup.find('div', class_='result')
            if first_result:
                link_elem = first_result.find('a', class_='cite')
                if link_elem:
                    act_url = 'https://indiankanoon.org' + link_elem['href']
                    act_response = self.session.get(act_url, timeout=10)
                    act_soup = BeautifulSoup(act_response.content, 'html.parser')
                    
                    # Extract sections
                    content_div = act_soup.find('div', class_='judgments')
                    if content_div:
                        text = self._extract_text(content_div)
                        results['content'] = text
                        results['url'] = act_url
                        
            print(f"✅ Scraped bare act content for: {act_name}")
            
        except Exception as e:
            print(f"❌ Error scraping bare acts: {e}")
        
        return results
    
    def _extract_text(self, element) -> str:
        """Extract clean text from BeautifulSoup element"""
        # Remove script and style elements
        for script in element(['script', 'style']):
            script.decompose()
        
        text = element.get_text(separator='\n')
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text


class FlashcardGenerator:
    """Generate flashcards from content using LLM"""
    
    def __init__(self, provider='groq', api_key=None, config=None):
        self.provider = provider
        self.api_key = api_key
        self.config = config or {}
    
    def generate_from_content(self, content: str, topic: str, count: int = 15) -> List[Dict]:
        """Generate flashcards from scraped content"""
        
        # Truncate content if too long
        max_content_length = 8000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        
        prompt = f"""Based on the following content about {topic}, generate {count} high-quality AIBE exam flashcards.

CONTENT:
{content}

REQUIREMENTS:
- Extract key legal concepts, definitions, sections, and principles
- Each card should have a clear Question (q) and detailed Answer (a)
- Focus on exam-relevant information
- Answers should be 2-4 sentences
- Include section numbers and case laws where mentioned
- Cover different aspects of the topic

Format response as JSON array:
[
  {{"q": "Question 1?", "a": "Answer 1"}},
  {{"q": "Question 2?", "a": "Answer 2"}}
]

Return ONLY the JSON array, no additional text."""

        try:
            response = self._call_llm(prompt)
            cards = self._parse_flashcards(response)
            print(f"✅ Generated {len(cards)} flashcards from content")
            return cards
        except Exception as e:
            print(f"❌ Error generating flashcards: {e}")
            return []
    
    def generate_topic_cards(self, topic_title: str, topic_subtitle: str, count: int = 15) -> List[Dict]:
        """Generate flashcards for a topic using LLM knowledge"""
        
        prompt = f"""Generate {count} high-quality AIBE exam flashcards for: "{topic_title}" ({topic_subtitle}).

REQUIREMENTS:
- Cover key concepts, sections, case laws, and principles
- Each card: clear Question (q) and detailed Answer (a)
- Answers: 2-4 sentences, exam-focused
- Include relevant section numbers
- Progressive difficulty
- Different subtopics

Format: JSON array only
[
  {{"q": "Question?", "a": "Answer"}},
  ...
]"""

        try:
            response = self._call_llm(prompt)
            cards = self._parse_flashcards(response)
            return cards
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def _call_llm(self, prompt: str) -> str:
        """Call configured LLM"""
        system_prompt = "You are an expert in Indian law preparing AIBE exam questions. Generate high-quality flashcards in valid JSON format only."
        
        if self.provider == 'groq':
            return self._call_groq(prompt, system_prompt)
        elif self.provider == 'openrouter':
            return self._call_openrouter(prompt, system_prompt)
        elif self.provider == 'ollama':
            return self._call_ollama(prompt, system_prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _call_groq(self, prompt: str, system_prompt: str) -> str:
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
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def _call_openrouter(self, prompt: str, system_prompt: str) -> str:
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
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def _call_ollama(self, prompt: str, system_prompt: str) -> str:
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
        
        response = requests.post(url, json=data, timeout=120)
        response.raise_for_status()
        return response.json()['message']['content']
    
    def _parse_flashcards(self, response: str) -> List[Dict]:
        """Parse LLM response to extract flashcards"""
        content = response.strip()
        
        # Remove markdown
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        
        # Find JSON array
        json_match = re.search(r'\[[\s\S]*\]', content)
        if json_match:
            content = json_match.group(0)
        
        try:
            cards = json.loads(content)
            if not isinstance(cards, list):
                raise ValueError("Not a list")
            return [card for card in cards if 'q' in card and 'a' in card]
        except Exception as e:
            print(f"Parse error: {e}")
            return []


class JSONManager:
    """Manage JSON flashcard files"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def load_topic(self, filename: str) -> Dict:
        """Load topic JSON file"""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_topic(self, filename: str, data: Dict):
        """Save topic JSON file"""
        filepath = self.data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved: {filepath}")
    
    def add_cards_to_topic(self, filename: str, new_cards: List[Dict]):
        """Add cards to existing topic file"""
        data = self.load_topic(filename)
        
        if not data:
            print(f"⚠️  Topic file not found: {filename}")
            return
        
        existing_cards = data.get('flashcards', [])
        existing_questions = {card['q'] for card in existing_cards}
        
        # Filter duplicates
        unique_cards = [card for card in new_cards if card['q'] not in existing_questions]
        
        data['flashcards'] = existing_cards + unique_cards
        self.save_topic(filename, data)
        
        print(f"✅ Added {len(unique_cards)} unique cards (filtered {len(new_cards) - len(unique_cards)} duplicates)")
    
    def ensure_minimum_cards(self, filename: str, min_count: int = 15, generator: FlashcardGenerator = None):
        """Ensure topic has minimum number of cards"""
        data = self.load_topic(filename)
        
        if not data:
            print(f"⚠️  Topic file not found: {filename}")
            return
        
        current_count = len(data.get('flashcards', []))
        
        if current_count >= min_count:
            print(f"✅ {data['topic_title']}: Already has {current_count} cards")
            return
        
        needed = min_count - current_count
        print(f"📝 {data['topic_title']}: Need {needed} more cards...")
        
        if generator:
            new_cards = generator.generate_topic_cards(
                data['topic_title'],
                data['topic_subtitle'],
                count=needed
            )
            
            if new_cards:
                self.add_cards_to_topic(filename, new_cards)


# ========== MAIN WORKFLOWS ==========

def workflow_scrape_and_generate(topic: str, search_queries: List[str], output_file: str):
    """Complete workflow: scrape content and generate flashcards"""
    
    print(f"\n{'='*60}")
    print(f"WORKFLOW: Scrape and Generate for {topic}")
    print(f"{'='*60}\n")
    
    # Initialize
    scraper = LegalContentScraper()
    generator = FlashcardGenerator(
        provider=os.environ.get('LLM_PROVIDER', 'groq'),
        api_key=os.environ.get('LLM_API_KEY'),
        config={}
    )
    json_mgr = JSONManager('data')
    
    all_content = []
    
    # Scrape from multiple sources
    for query in search_queries:
        print(f"\n🔍 Searching: {query}")
        
        # Indian Kanoon
        results = scraper.scrape_indiankanoon(query, max_results=3)
        all_content.extend(results)
        time.sleep(2)  # Rate limiting
        
        # Wikipedia
        wiki_result = scraper.scrape_wikipedia_legal(query)
        if wiki_result:
            all_content.append(wiki_result)
        time.sleep(2)
    
    # Combine content
    combined_content = "\n\n---\n\n".join([item['content'] for item in all_content if item.get('content')])
    
    if not combined_content:
        print("❌ No content scraped!")
        return
    
    print(f"\n✅ Scraped {len(all_content)} sources, {len(combined_content)} characters total")
    
    # Generate flashcards
    print(f"\n🤖 Generating flashcards using {generator.provider}...")
    flashcards = generator.generate_from_content(combined_content, topic, count=15)
    
    if flashcards:
        # Add to JSON
        json_mgr.add_cards_to_topic(output_file, flashcards)
        print(f"\n✅ Successfully added flashcards to {output_file}")
    else:
        print("\n❌ No flashcards generated!")


def workflow_expand_all_topics(min_cards: int = 15):
    """Expand all topics to minimum card count"""
    
    print(f"\n{'='*60}")
    print(f"WORKFLOW: Expand All Topics to {min_cards} cards")
    print(f"{'='*60}\n")
    
    generator = FlashcardGenerator(
        provider=os.environ.get('LLM_PROVIDER', 'groq'),
        api_key=os.environ.get('LLM_API_KEY'),
        config={}
    )
    json_mgr = JSONManager('data')
    
    # Load topics index
    try:
        with open('data/topics_index.json', 'r') as f:
            index = json.load(f)
    except FileNotFoundError:
        print("❌ topics_index.json not found!")
        return
    
    for topic_info in index['topics']:
        filename = topic_info['file']
        print(f"\n📚 Processing: {topic_info['title']}")
        
        json_mgr.ensure_minimum_cards(filename, min_cards, generator)
        time.sleep(3)  # Rate limiting


def workflow_create_new_topic(topic_id: int, title: str, subtitle: str, filename: str):
    """Create new topic JSON file with cards"""
    
    print(f"\n{'='*60}")
    print(f"WORKFLOW: Create New Topic - {title}")
    print(f"{'='*60}\n")
    
    generator = FlashcardGenerator(
        provider=os.environ.get('LLM_PROVIDER', 'groq'),
        api_key=os.environ.get('LLM_API_KEY'),
        config={}
    )
    json_mgr = JSONManager('data')
    
    # Generate initial cards
    print("🤖 Generating 15 initial flashcards...")
    cards = generator.generate_topic_cards(title, subtitle, count=15)
    
    if not cards:
        print("❌ Failed to generate cards!")
        return
    
    # Create new JSON file
    data = {
        "topic_id": topic_id,
        "topic_title": title,
        "topic_subtitle": subtitle,
        "flashcards": cards
    }
    
    json_mgr.save_topic(filename, data)
    print(f"\n✅ Created new topic with {len(cards)} cards!")


# ========== CLI INTERFACE ==========

if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("AIBE Flashcard Web Scraper & JSON Generator")
    print("="*60)
    
    # Check configuration
    provider = os.environ.get('LLM_PROVIDER', 'groq')
    api_key = os.environ.get('LLM_API_KEY', '')
    
    if not api_key and provider != 'ollama':
        print("\n⚠️  Configuration Required!")
        print("\nSet environment variables:")
        print("  export LLM_PROVIDER=groq")
        print("  export LLM_API_KEY=your_key_here")
        print("\nOr for Ollama: export LLM_PROVIDER=ollama")
        sys.exit(1)
    
    print(f"\n✅ Configuration: {provider}")
    
    # Menu
    print("\nSelect workflow:")
    print("1. Scrape and generate for specific topic")
    print("2. Expand all topics to 15+ cards")
    print("3. Create new topic from scratch")
    print("4. Add cards to existing topic (LLM only)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        topic = input("Topic name: ")
        queries = input("Search queries (comma-separated): ").split(',')
        output = input("Output filename (e.g., torts.json): ")
        workflow_scrape_and_generate(topic, [q.strip() for q in queries], output)
    
    elif choice == '2':
        min_cards = int(input("Minimum cards per topic (default 15): ") or "15")
        workflow_expand_all_topics(min_cards)
    
    elif choice == '3':
        topic_id = int(input("Topic ID: "))
        title = input("Topic title: ")
        subtitle = input("Topic subtitle: ")
        filename = input("Filename (e.g., new_topic.json): ")
        workflow_create_new_topic(topic_id, title, subtitle, filename)
    
    elif choice == '4':
        filename = input("Existing topic file: ")
        count = int(input("Number of cards to add: "))
        
        generator = FlashcardGenerator(provider=provider, api_key=api_key)
        json_mgr = JSONManager('data')
        
        data = json_mgr.load_topic(filename)
        if data:
            print(f"\n🤖 Generating {count} new cards...")
            new_cards = generator.generate_topic_cards(
                data['topic_title'],
                data['topic_subtitle'],
                count=count
            )
            if new_cards:
                json_mgr.add_cards_to_topic(filename, new_cards)
    
    else:
        print("Invalid choice!")
    
    print("\n" + "="*60)
    print("✅ Done!")
    print("="*60)
