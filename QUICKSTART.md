# 🚀 Quick Start Guide

## Option 1: Instant Use (HTML Only) ⚡

1. **Open** `aibe-smart-prep-enhanced.html` in your browser
2. **Click** AI Settings tab
3. **Get free API key** from https://console.groq.com/keys
4. **Paste** your key and click Save
5. **Start studying!** Auto-generation will handle the rest 🎓

## Option 2: Python Script (Batch Generation) 🐍

```bash
# Install requirements
pip install requests

# Get API key from https://console.groq.com/keys
export LLM_PROVIDER=groq
export LLM_API_KEY=gsk_your_key_here

# Create sample data
python flashcard_generator.py sample

# Generate 15+ cards per topic
python flashcard_generator.py
```

## Option 3: 100% Local with Ollama 🏠

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download a model
ollama pull llama3.1

# Run generator (no API key needed!)
export LLM_PROVIDER=ollama
python flashcard_generator.py

# Or use in HTML app:
# Provider: Ollama
# URL: http://localhost:11434
# Model: llama3.1
```

## 🎯 Key Features to Try

### Auto-Generation
- Just study normally
- When you reach the last 3 cards, more are generated automatically
- No manual clicking needed!

### Manual Generate
- Click "Generate 15 More" button anytime
- Get instant batch of cards
- Perfect for focused study sessions

### AI Chat
- Ask questions about any legal topic
- Get instant explanations with case laws
- Great for doubt clearing

## 🔧 Settings Explained

| Setting | What it does | Recommended |
|---------|--------------|-------------|
| **Auto-generate** | Generate when reaching last 3 cards | ✅ ON |
| **Min 15 cards** | Ensure 15 cards when starting topic | ✅ ON |
| **Cards per batch** | How many to generate at once | 15-20 |
| **Provider** | Which AI to use | Groq (free & fast) |

## 💡 Pro Tips

1. **Test your connection** first (Test Connection button)
2. **Enable auto-generation** for seamless experience
3. **Start with Groq** - it's fast and free
4. **Download the app** to use offline (with saved cards)
5. **Check progress bar** to know when generation happens

## ⚠️ Troubleshooting

### "API key not configured"
→ Go to AI Settings and save your key

### "Connection failed"
→ Click Test Connection to diagnose
→ Check your API key is correct
→ Verify you have API quota remaining

### Ollama not working?
→ Make sure it's running: `ollama serve`
→ Test: `curl http://localhost:11434/api/tags`

### Cards generating slowly?
→ Normal for free tiers
→ Try Groq (fastest free option)
→ Or use Ollama locally

## 📊 What to Expect

- **First card generation**: 10-30 seconds
- **Subsequent generations**: 5-15 seconds (Groq)
- **Ollama**: Depends on your hardware
- **Cards quality**: High - exam-focused questions

## 🎓 Study Flow

1. Select a topic
2. Study the curated cards first
3. Auto-generation kicks in automatically
4. Keep studying seamlessly!
5. Use AI Chat for doubts
6. Repeat with all topics

## 🆓 Free API Limits

| Provider | Free Tier |
|----------|-----------|
| **Groq** | 30 requests/min, 14,400/day |
| **OpenRouter** | Various free models |
| **Ollama** | Unlimited (local) |

For heavy use: Install Ollama locally!

## 📱 Need Help?

1. Check the main README.md for detailed docs
2. Review the troubleshooting section
3. Test your connection in AI Settings
4. Try different providers if one fails

---

**Ready?** Open the HTML file and start studying! 🚀

Good luck with AIBE! 🎯
