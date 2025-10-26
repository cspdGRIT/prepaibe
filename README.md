# AIBE Smart Prep - Enhanced Flashcard System 🎓

An intelligent flashcard application with **automatic AI generation** that seamlessly provides unlimited questions for AIBE exam preparation.

## ✨ Key Features

### 🤖 Auto AI Generation
- **Automatic card generation** when you approach the end of available cards (last 3 cards)
- **Minimum 15 cards per topic** - automatically generates on topic start if needed
- **Configurable batch size** (5-30 cards per generation)
- **Seamless experience** - no manual clicking needed for more cards

### 🔧 Multiple LLM Providers
Choose from various AI providers:

1. **Groq (Recommended)** - Fast and free
   - Model: Llama 3.1 70B
   - Get key: https://console.groq.com/keys
   
2. **OpenRouter** - Access to multiple models
   - Free models: Llama 3.1 8B, Gemini 2.0 Flash, Mistral 7B
   - Get key: https://openrouter.ai/keys
   
3. **Ollama (Local)** - 100% free, runs on your machine
   - No API key needed
   - Install: https://ollama.ai
   - Models: llama3.1, mistral, etc.
   
4. **Custom OpenAI-Compatible** - Use any compatible API

### 📊 Smart Features
- **Progress tracking** with visual progress bar
- **Card source badges** - Know which cards are curated vs AI-generated
- **Persistent storage** - All AI-generated cards saved locally
- **AI Chat assistant** - Ask questions about any legal topic
- **Export/Download** - Save the app with all your data

## 🚀 Quick Start

### Option 1: HTML Only (Simple)

1. Open `aibe-smart-prep-enhanced.html` in your browser
2. Go to **AI Settings** tab
3. Select your LLM provider and enter API key
4. Configure auto-generation settings
5. Click **Save Settings**
6. Start studying! 🎓

### Option 2: Python Helper (For JSON Expansion)

Generate more cards directly into JSON files:

```bash
# Install dependencies
pip install requests

# Set up your API provider
export LLM_PROVIDER=groq  # or openrouter, ollama, openai
export LLM_API_KEY=your_key_here

# Create sample JSON
python flashcard_generator.py sample

# Expand flashcards to 15+ per topic
python flashcard_generator.py

# Output: flashcards_expanded.json
```

### For Ollama (Local, No API Key Needed)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.1

# Run the generator
export LLM_PROVIDER=ollama
python flashcard_generator.py
```

## ⚙️ Configuration Options

### AI Settings

| Setting | Description | Default |
|---------|-------------|---------|
| **LLM Provider** | AI service to use | Groq |
| **Cards per batch** | How many cards to generate at once | 15 |
| **Auto-generate** | Generate automatically when nearing end | ✅ Enabled |
| **Min cards per topic** | Ensure minimum cards on topic start | 15 |

### Auto-Generation Trigger

Cards are automatically generated when:
- You reach the **last 3 cards** of a topic
- You start a topic with **fewer than 15 cards** (if enabled)

## 📁 File Structure

```
aibe-smart-prep-enhanced.html  # Main application (standalone)
flashcard_generator.py         # Python helper for JSON expansion
flashcards_sample.json        # Sample data structure
flashcards_expanded.json      # Generated expanded cards
README.md                     # This file
```

## 🔨 Usage Examples

### Example 1: Using Groq (Free & Fast)

1. Get API key from https://console.groq.com/keys
2. In the HTML app:
   - AI Settings → Provider: Groq
   - Paste API key
   - Save Settings
3. Study any topic - auto-generation will kick in automatically!

### Example 2: Using OpenRouter (Multiple Free Models)

```javascript
// In AI Settings:
Provider: OpenRouter
API Key: sk-or-v1-...
Model: Llama 3.1 8B (Free)
```

### Example 3: Using Ollama (Fully Local)

```bash
# Terminal
ollama pull llama3.1
ollama serve

# In HTML app:
Provider: Ollama
Base URL: http://localhost:11434
Model: llama3.1
```

### Example 4: Python Script for Batch Generation

```python
from flashcard_generator import FlashcardGenerator

# Initialize
generator = FlashcardGenerator(
    provider='groq',
    api_key='your_groq_key'
)

# Generate cards
cards = generator.generate_flashcards(
    topic_title="Contract Law",
    topic_subtitle="Indian Contract Act, 1872",
    count=20
)

print(f"Generated {len(cards)} cards")
for card in cards:
    print(f"Q: {card['q']}")
    print(f"A: {card['a']}\n")
```

## 🎯 How Auto-Generation Works

1. **Topic Start**: 
   - Checks if topic has < 15 cards
   - Automatically generates to reach 15 (if enabled)

2. **During Study**:
   - Monitors your position in card deck
   - When you reach last 3 cards, triggers generation
   - Seamlessly adds new cards to the end

3. **Manual Generation**:
   - Click "Generate More" button anytime
   - Generates configured batch size (default 15)

## 🔐 Security & Privacy

- **API keys stored locally** in browser localStorage
- **All data stays in your browser** - nothing sent to external servers except LLM API calls
- **Ollama option** for 100% local, private usage
- **Downloadable** - save the entire app offline

## 📝 Adding Your Own Topics

Edit the `syllabusData` in the HTML file:

```javascript
const syllabusData = {
    topics: [
        {
            id: 1,
            title: "Your Topic",
            subtitle: "Description"
        }
    ]
};

const flashcardsData = {
    1: [
        { q: "Your question?", a: "Your answer" }
    ]
};
```

## 🎨 Customization

### Change Generation Prompt

Edit the prompt in the HTML file (line ~708):

```javascript
const prompt = `Generate ${batchSize} flashcards for ${topic.title}...
YOUR CUSTOM REQUIREMENTS HERE
`;
```

### Change Card Styling

Modify CSS variables:

```css
:root {
    --primary: #1e40af;      /* Main color */
    --primary-light: #3b82f6; /* Hover color */
    --secondary: #10b981;     /* Success color */
}
```

## 🐛 Troubleshooting

### Cards not generating?
- Check API key in Settings
- Click "Test Connection" to verify
- Check browser console for errors

### Ollama not working?
```bash
# Make sure it's running
ollama serve

# Test it
curl http://localhost:11434/api/tags
```

### API quota exceeded?
- Groq: 30 requests/minute free tier
- OpenRouter: Check your credit balance
- Ollama: Unlimited (local)

### JSON parsing errors?
- Some LLMs may return malformed JSON
- Try different model/provider
- Check temperature setting (lower = more consistent)

## 🎓 Best Practices

1. **Start with Groq** - fastest free option
2. **Enable auto-generation** - seamless experience
3. **Set 15-20 cards per batch** - good balance
4. **Use manual generate** for quick bursts
5. **Save regularly** - generated cards persist
6. **Test connection** before studying

## 🤝 Contributing

Want to add more features? Feel free to:
- Add more LLM providers
- Improve prompt engineering
- Add more AIBE topics
- Enhance UI/UX

## 📄 License

Free to use for educational purposes. Attribution appreciated!

## 🙋 FAQ

**Q: How many cards can I generate?**
A: Unlimited! As long as you have API quota.

**Q: Do I need internet?**
A: Only for AI generation. Ollama works fully offline.

**Q: Is my data saved?**
A: Yes, in browser localStorage. Use download feature for backup.

**Q: Can I use my own OpenAI key?**
A: Yes, select "Custom" provider and enter OpenAI endpoint.

**Q: Best free option?**
A: Groq for cloud, Ollama for local.

## 🚀 Future Enhancements

- [ ] Spaced repetition algorithm
- [ ] Performance analytics
- [ ] Multi-language support
- [ ] Voice mode
- [ ] Cloud sync
- [ ] Mobile app

---

Made with ❤️ for AIBE aspirants. Good luck with your exam! 🎯
