# Quick Usage Examples 🚀

## Example 1: Using Pre-Made Content (Instant Start)

```bash
# Just open the HTML file - that's it!
open aibe-smart-prep-json-loader.html

# Already includes:
# - 18 Contract Law cards
# - 18 Constitutional Law cards
# - 18 Criminal Law cards
# - 16 Professional Ethics cards
# All from external JSON files!
```

## Example 2: Generate Torts Topic from Scratch

```bash
# Setup
export LLM_PROVIDER=groq
export LLM_API_KEY=gsk_your_key_here

# Run script
python json_scraper_generator.py

# Select: 3 (Create new topic)
# Inputs:
#   Topic ID: 4
#   Topic title: Torts
#   Topic subtitle: Law of Torts
#   Filename: torts.json

# Result: data/torts.json with 15 flashcards created!
```

## Example 3: Scrape and Generate Evidence Act Content

```bash
python json_scraper_generator.py

# Select: 1 (Scrape and generate)
# Inputs:
#   Topic name: Evidence Act
#   Search queries: indian evidence act sections, hearsay evidence, burden of proof, dying declaration
#   Output filename: evidence_act.json

# The script will:
# 1. Search Indian Kanoon for each query
# 2. Scrape Wikipedia articles
# 3. Combine all content
# 4. Generate 15 flashcards using LLM
# 5. Save to data/evidence_act.json
```

## Example 4: Expand Existing Topic (Contract Law)

```bash
python json_scraper_generator.py

# Select: 4 (Add cards to existing topic)
# Inputs:
#   Existing topic file: contract_law.json
#   Number of cards to add: 10

# Result: 10 new unique cards added to contract_law.json
# (duplicates automatically filtered)
```

## Example 5: Ensure All Topics Have 20+ Cards

```bash
python json_scraper_generator.py

# Select: 2 (Expand all topics)
# Input:
#   Minimum cards per topic: 20

# The script will:
# 1. Check each topic in topics_index.json
# 2. Generate cards for topics below 20
# 3. Update all JSON files
# Result: Every topic has at least 20 cards!
```

## Example 6: Scrape Specific Case Law

```bash
python json_scraper_generator.py

# Select: 1 (Scrape and generate)
# Inputs:
#   Topic name: Kesavananda Bharati Case
#   Search queries: kesavananda bharati basic structure, judicial review amendment
#   Output filename: constitutional_law.json  # adds to existing

# Result: New cards about this specific case added!
```

## Example 7: Create Multiple Topics Batch

```bash
#!/bin/bash
# save as: batch_create.sh

export LLM_PROVIDER=groq
export LLM_API_KEY=your_key

topics=(
  "5,Property Law,Transfer of Property Act,property_law.json"
  "6,Family Law,Hindu Marriage Act,family_law.json"
  "7,Company Law,Companies Act 2013,company_law.json"
  "9,Civil Procedure Code,CPC 1908,cpc.json"
  "10,Indian Penal Code,IPC 1860,ipc.json"
)

for topic in "${topics[@]}"; do
  IFS=',' read -r id title subtitle file <<< "$topic"
  echo "Creating: $title"
  python3 -c "
from json_scraper_generator import workflow_create_new_topic
workflow_create_new_topic($id, '$title', '$subtitle', '$file')
"
  sleep 5
done

echo "✅ All topics created!"
```

## Example 8: Update Index After Adding Topics

```python
# update_index.py
import json
from pathlib import Path

# Read existing index
with open('data/topics_index.json', 'r') as f:
    index = json.load(f)

# Add new topic
index['topics'].append({
    "id": 11,
    "title": "Negotiable Instruments Act",
    "subtitle": "NI Act, 1881",
    "file": "ni_act.json",
    "card_count": 15
})

index['last_updated'] = "2025-10-26"

# Save
with open('data/topics_index.json', 'w') as f:
    json.dump(index, f, indent=2)

print("✅ Index updated!")
```

## Example 9: Quality Check All JSON Files

```bash
#!/bin/bash
# check_quality.sh

echo "Checking all JSON files..."

for file in data/*.json; do
  echo "Checking: $file"
  
  # Validate JSON syntax
  python -m json.tool "$file" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    # Count cards
    cards=$(python -c "import json; f=open('$file'); d=json.load(f); print(len(d.get('flashcards', [])))")
    echo "  ✅ Valid JSON, $cards cards"
  else
    echo "  ❌ Invalid JSON!"
  fi
done
```

## Example 10: Create Custom Workflow Script

```python
# my_custom_workflow.py
from json_scraper_generator import (
    LegalContentScraper,
    FlashcardGenerator,
    JSONManager
)
import os

# Setup
generator = FlashcardGenerator(
    provider='groq',
    api_key=os.environ.get('LLM_API_KEY')
)
scraper = LegalContentScraper()
json_mgr = JSONManager('data')

# My workflow: Scrape, generate, and add 20 cards
topics_to_expand = [
    ('contract_law.json', 'offer and acceptance', 'consideration', 'breach of contract'),
    ('criminal_law.json', 'section 302 IPC', 'mens rea', 'criminal procedure'),
]

for filename, *queries in topics_to_expand:
    print(f"\n📚 Expanding: {filename}")
    
    # Scrape content
    all_content = []
    for query in queries:
        results = scraper.scrape_indiankanoon(query, max_results=2)
        all_content.extend(results)
    
    # Generate cards
    combined = "\n\n".join([r['content'] for r in all_content if r.get('content')])
    if combined:
        cards = generator.generate_from_content(combined, filename.split('.')[0], count=20)
        
        # Add to file
        json_mgr.add_cards_to_topic(filename, cards)
        print(f"✅ Added {len(cards)} cards!")

print("\n🎉 Custom workflow complete!")
```

## Example 11: Monitor Card Count

```bash
# count_cards.sh
echo "📊 Card Count Report"
echo "===================="

total=0
for file in data/*_law.json data/*_ethics.json; do
  if [ -f "$file" ]; then
    count=$(python -c "import json; f=open('$file'); d=json.load(f); print(len(d.get('flashcards', [])))")
    title=$(python -c "import json; f=open('$file'); d=json.load(f); print(d.get('topic_title', 'Unknown'))")
    echo "$title: $count cards"
    total=$((total + count))
  fi
done

echo "===================="
echo "Total: $total cards"
```

## Example 12: Ollama (Fully Offline)

```bash
# Step 1: Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Step 2: Pull model
ollama pull llama3.1

# Step 3: Start server
ollama serve

# Step 4: Use with script (in another terminal)
export LLM_PROVIDER=ollama
python json_scraper_generator.py

# Select any workflow - fully offline!
```

## Example 13: Hybrid Approach (Mix Scraping + LLM)

```python
# hybrid_generation.py
from json_scraper_generator import *
import os

generator = FlashcardGenerator(provider='groq', api_key=os.environ['LLM_API_KEY'])
scraper = LegalContentScraper()
json_mgr = JSONManager('data')

topic_file = 'constitutional_law.json'

# Part 1: Scrape 5 cards
print("📥 Scraping content...")
results = scraper.scrape_indiankanoon("fundamental rights article 14", max_results=3)
content = "\n\n".join([r['content'] for r in results if r.get('content')])
scraped_cards = generator.generate_from_content(content, "Constitutional Law", count=5)

# Part 2: Generate 10 cards from LLM knowledge
print("🤖 Generating from LLM...")
llm_cards = generator.generate_topic_cards("Constitutional Law", "Indian Constitution", count=10)

# Part 3: Combine and add
all_cards = scraped_cards + llm_cards
json_mgr.add_cards_to_topic(topic_file, all_cards)

print(f"✅ Added {len(all_cards)} cards total!")
print(f"  - {len(scraped_cards)} from scraping")
print(f"  - {len(llm_cards)} from LLM")
```

## Example 14: Verify No Duplicates

```python
# check_duplicates.py
import json
from pathlib import Path

for json_file in Path('data').glob('*.json'):
    if json_file.name == 'topics_index.json':
        continue
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    questions = [card['q'] for card in data.get('flashcards', [])]
    unique_questions = set(questions)
    
    if len(questions) != len(unique_questions):
        print(f"⚠️  {json_file.name}: {len(questions) - len(unique_questions)} duplicates found!")
    else:
        print(f"✅ {json_file.name}: No duplicates ({len(questions)} cards)")
```

## Example 15: Export All Cards to CSV

```python
# export_to_csv.py
import json
import csv
from pathlib import Path

all_cards = []

for json_file in Path('data').glob('*.json'):
    if json_file.name == 'topics_index.json':
        continue
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    topic = data.get('topic_title', 'Unknown')
    for card in data.get('flashcards', []):
        all_cards.append({
            'Topic': topic,
            'Question': card['q'],
            'Answer': card['a']
        })

# Write to CSV
with open('all_flashcards.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Topic', 'Question', 'Answer'])
    writer.writeheader()
    writer.writerows(all_cards)

print(f"✅ Exported {len(all_cards)} cards to all_flashcards.csv")
```

---

## 🎯 Quick Reference

**Instant start:** Just open `aibe-smart-prep-json-loader.html`

**Add 10 cards:** `python json_scraper_generator.py` → Select 4

**New topic:** `python json_scraper_generator.py` → Select 3

**Scrape content:** `python json_scraper_generator.py` → Select 1

**Expand all:** `python json_scraper_generator.py` → Select 2

**Check files:** `ls -la data/ && python -m json.tool data/*.json`

---

Pick any example, modify to your needs, and go! 🚀
