# AIBE Smart Prep - JSON-Based System 📚

Complete flashcard system with **external JSON files**, **web scraping**, and **auto-generation**.

## 🎯 What's New

### ✅ External JSON Files
- **Modular data structure** - Each topic in separate JSON file
- **Easy to edit** - Update flashcards without touching HTML
- **Easy to expand** - Add new cards via scripts
- **Version control friendly** - Track changes to individual topics

### ✅ Web Scraper
- **Scrapes legal content** from Indian Kanoon, Wikipedia, etc.
- **Generates flashcards** from scraped content using LLM
- **Incremental updates** - Add cards to existing topics
- **Maintains quality** - Filters duplicates automatically

### ✅ Current Content
- **Contract Law**: 18 comprehensive flashcards
- **Constitutional Law**: 18 comprehensive flashcards  
- **Criminal Law**: 18 comprehensive flashcards
- **Professional Ethics**: 16 comprehensive flashcards

More topics can be generated using the scraper script!

## 📁 File Structure

```
aibe-smart-prep-json-loader.html    # Updated HTML (loads from JSON)
data/
  ├── topics_index.json             # Master index of all topics
  ├── contract_law.json              # Contract Law flashcards (18 cards)
  ├── constitutional_law.json        # Constitutional Law flashcards (18 cards)
  ├── criminal_law.json              # Criminal Law flashcards (18 cards)
  ├── professional_ethics.json       # Professional Ethics (16 cards)
  └── [more topics...]
json_scraper_generator.py            # Web scraper & JSON generator
flashcard_generator.py               # Original LLM-only generator
```

## 🚀 Quick Start

### Option 1: Use Pre-Made JSON Files

1. **Open** `aibe-smart-prep-json-loader.html` in browser
2. Flashcards load automatically from `data/` folder
3. **Configure AI** for generating more cards
4. Start studying! 🎓

### Option 2: Generate More Content

```bash
# Install dependencies
pip install requests beautifulsoup4 lxml --break-system-packages

# Set API key
export LLM_PROVIDER=groq
export LLM_API_KEY=your_groq_key_here

# Run the scraper/generator
python json_scraper_generator.py
```

## 📖 JSON Format

### topics_index.json
```json
{
  "topics": [
    {
      "id": 1,
      "title": "Contract Law",
      "subtitle": "Indian Contract Act, 1872",
      "file": "contract_law.json",
      "card_count": 18
    }
  ],
  "version": "1.0",
  "last_updated": "2025-10-26"
}
```

### individual topic file (e.g., contract_law.json)
```json
{
  "topic_id": 1,
  "topic_title": "Contract Law",
  "topic_subtitle": "Indian Contract Act, 1872",
  "flashcards": [
    {
      "q": "What is a contract under Section 2(h)?",
      "a": "An agreement enforceable by law..."
    }
  ]
}
```

## 🔧 Using the Scraper Script

### Workflow 1: Scrape & Generate
Scrape legal content from websites and generate flashcards:

```bash
python json_scraper_generator.py
# Select: 1. Scrape and generate for specific topic

# Example inputs:
Topic name: Torts
Search queries: law of torts india, vicarious liability, negligence tort
Output filename: torts.json
```

### Workflow 2: Expand All Topics
Ensure all topics have at least 15 cards:

```bash
python json_scraper_generator.py
# Select: 2. Expand all topics to 15+ cards
```

### Workflow 3: Create New Topic
Create a completely new topic from scratch:

```bash
python json_scraper_generator.py
# Select: 3. Create new topic from scratch

# Example:
Topic ID: 11
Topic title: Negotiable Instruments Act
Topic subtitle: NI Act, 1881
Filename: negotiable_instruments.json
```

### Workflow 4: Add More Cards
Add cards to existing topic using LLM only:

```bash
python json_scraper_generator.py
# Select: 4. Add cards to existing topic

# Example:
Existing topic file: contract_law.json
Number of cards to add: 10
```

## 🌐 Web Scraping Sources

The scraper can pull content from:

1. **Indian Kanoon** - Case laws, judgments, bare acts
2. **Wikipedia** - Legal concepts, overviews
3. **Bare Acts** - Direct statutory content

Content is then processed by LLM to generate exam-focused flashcards.

## 🎓 How It Works

```
1. Scraper fetches legal content from websites
                  ↓
2. Content is cleaned and combined
                  ↓
3. LLM processes content and generates flashcards
                  ↓
4. Flashcards are added to JSON file (duplicates filtered)
                  ↓
5. HTML app loads updated JSON automatically
                  ↓
6. You study with expanded content! 🚀
```

## 📊 Content Quality

### Current Flashcards Include:
- **Section numbers** (e.g., Section 300 IPC)
- **Case laws** (e.g., Kesavananda Bharati)
- **Legal principles** (e.g., Basic Structure Doctrine)
- **Definitions** (e.g., What is mens rea?)
- **Comparisons** (e.g., Murder vs Culpable Homicide)
- **Practical examples** and applications

All cards are:
- ✅ AIBE-exam focused
- ✅ Concise (2-4 sentence answers)
- ✅ Accurate legal information
- ✅ Progressive difficulty

## 🔄 Incremental Updates

### Adding Cards to Existing Topic

```python
from json_scraper_generator import JSONManager, FlashcardGenerator

# Initialize
json_mgr = JSONManager('data')
generator = FlashcardGenerator(provider='groq', api_key='your_key')

# Generate new cards
new_cards = generator.generate_topic_cards(
    "Contract Law",
    "Indian Contract Act, 1872",
    count=10
)

# Add to existing file (duplicates filtered automatically)
json_mgr.add_cards_to_topic('contract_law.json', new_cards)
```

### Scraping and Adding

```python
from json_scraper_generator import (
    LegalContentScraper, 
    FlashcardGenerator,
    JSONManager
)

# Scrape content
scraper = LegalContentScraper()
content = scraper.scrape_indiankanoon("doctrine of frustration")

# Generate flashcards from content
generator = FlashcardGenerator(provider='groq', api_key='your_key')
cards = generator.generate_from_content(
    content['content'], 
    "Contract Law",
    count=5
)

# Add to JSON
json_mgr = JSONManager('data')
json_mgr.add_cards_to_topic('contract_law.json', cards)
```

## 📝 Editing JSON Manually

You can also edit JSON files directly:

```bash
# Open in text editor
nano data/contract_law.json

# Add new flashcard
{
  "q": "Your new question?",
  "a": "Your detailed answer..."
}

# Save and refresh browser - changes load automatically!
```

## 🎯 Best Practices

### For Scraping:
1. **Be specific** with search queries
2. **Multiple sources** give better coverage
3. **Rate limit** - use delays between requests
4. **Review content** - check generated cards for accuracy

### For JSON Management:
1. **Backup files** before major changes
2. **Use descriptive filenames** (e.g., `criminal_procedure_code.json`)
3. **Keep format consistent** - follow existing structure
4. **Update topics_index.json** when adding new topics

### For Quality:
1. **Verify legal accuracy** - double-check section numbers
2. **Keep answers concise** - 2-4 sentences ideal
3. **Include context** - mention relevant acts/cases
4. **Progressive difficulty** - mix easy and hard questions

## 🆕 Adding New Topics

### Step 1: Create JSON File

```json
{
  "topic_id": 11,
  "topic_title": "Your Topic",
  "topic_subtitle": "Related Act/Area",
  "flashcards": []
}
```

### Step 2: Generate Content

```bash
python json_scraper_generator.py
# Select workflow 3 or 4
```

### Step 3: Update Index

Edit `data/topics_index.json`:

```json
{
  "id": 11,
  "title": "Your Topic",
  "subtitle": "Related Act/Area",
  "file": "your_topic.json",
  "card_count": 15
}
```

### Step 4: Refresh Browser

The HTML app will automatically load the new topic!

## 🐛 Troubleshooting

### Cards not loading?
```bash
# Check file paths
ls -la data/

# Verify JSON syntax
python -m json.tool data/contract_law.json

# Check browser console (F12)
# Should show: "✅ Loaded X cards for topic Y"
```

### Scraper not working?
```bash
# Test API connection
curl https://indiankanoon.org

# Check API key
echo $LLM_API_KEY

# Try simpler query first
python json_scraper_generator.py
# Use workflow 4 (LLM only, no scraping)
```

### Duplicate questions?
The script automatically filters duplicates, but if you manually edit:

```python
# Run deduplication
json_mgr = JSONManager('data')
data = json_mgr.load_topic('contract_law.json')

# Remove duplicates manually
questions_seen = set()
unique_cards = []
for card in data['flashcards']:
    if card['q'] not in questions_seen:
        unique_cards.append(card)
        questions_seen.add(card['q'])

data['flashcards'] = unique_cards
json_mgr.save_topic('contract_law.json', data)
```

## 📈 Scaling Up

### Generate 50+ Cards Per Topic

```bash
# Method 1: Multiple batches
for i in {1..5}; do
  python json_scraper_generator.py
  # Select workflow 4, add 10 cards each time
done

# Method 2: Scraping + Generation
python json_scraper_generator.py
# Select workflow 1
# Use multiple search queries
```

### Bulk Process All Topics

```bash
# Create script to loop through all topics
for topic in topics_list:
    ensure_minimum_cards(topic, min_count=20)
```

### Scheduled Updates

```bash
# Cron job to add cards daily
0 2 * * * cd /path/to/project && python json_scraper_generator.py <<< "2\n20"
```

## 🎓 Study Workflow

1. **Start with JSON-loaded cards** (already 15+ per topic)
2. **AI auto-generates more** as you study
3. **Use scraper** to add specialized content
4. **Manual edits** for specific needs
5. **Never run out** of practice material!

## 📚 Content Roadmap

### Phase 1: Core Subjects ✅
- Contract Law (18 cards)
- Constitutional Law (18 cards)
- Criminal Law (18 cards)
- Professional Ethics (16 cards)

### Phase 2: Extended Subjects (Coming Soon)
- Torts (scrape + generate)
- Property Law (scrape + generate)
- Family Law (scrape + generate)
- Company Law (scrape + generate)
- Civil Procedure Code (scrape + generate)
- Evidence Act (scrape + generate)

### Phase 3: Specialized Topics
- Arbitration & Conciliation
- Intellectual Property
- Cyber Law
- Labour Law
- Environmental Law
- Tax Law

## 🤝 Contributing Content

Want to add content? Two ways:

### 1. Submit JSON Files
Create JSON files following the format and submit via PR

### 2. Share Search Queries
Provide good search queries for topics:
```
Topic: Evidence Act
Queries:
- "hearsay evidence section 60"
- "dying declaration admissibility"
- "burden of proof criminal cases"
```

## 🔐 Data Privacy

- **All data local** - JSON files on your machine
- **No tracking** - scraper doesn't send data anywhere except LLM API
- **API calls** - only to generate flashcards, no user data shared
- **Open source** - inspect code to verify

## ⚡ Performance

- **Fast loading** - JSON parsing is instant
- **Lazy loading** - Topics load on demand
- **Cached** - AI-generated cards persist locally
- **Scalable** - Handles 100+ cards per topic easily

## 📱 Offline Usage

```bash
# 1. Generate all content first
python json_scraper_generator.py  # Workflow 2

# 2. Save HTML + data folder
# 3. Use offline - AI features require API key
# 4. Or use Ollama for fully offline experience
```

---

## 🎯 Summary

**You asked for:**
- At least 15 flashcards per topic ✅
- External JSON files ✅
- Web scraper to collect content ✅
- Incremental data increase ✅
- Same webpage functionality ✅

**You got:**
- 15-18 cards per topic (already made) ✨
- Modular JSON architecture ✨
- Powerful web scraper + LLM generator ✨
- Multiple workflows for expansion ✨
- Enhanced HTML with JSON loading ✨
- 4 comprehensive workflows ✨

**Ready to ace AIBE!** 🚀

For questions, check the main README.md or inspect the Python scripts.

Good luck! 🎓📚
