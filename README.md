


# MindMate: An AI Companion for Emotional Wellness 

# Mental Wellness Chatbot 🌿💙

A production-ready, AI-powered mental wellness chatbot that provides empathetic emotional support with real-time sentiment analysis and safety guardrails. Designed for reliability, simplicity, and deployment.

**Project Status:** ✅ Fully Functional | Ready for GitHub & Local Deployment

---

## 🎯 Project Overview

This chatbot is built to:
- ✅ Perform **real-time sentiment/emotion analysis** on user messages
- ✅ Generate **empathetic, emotionally-aware responses** using LLM
- ✅ Provide **non-clinical mental wellness support** (stress, anxiety, burnout, etc.)
- ✅ Detect **high-risk language** (suicide, self-harm indicators)
- ✅ Redirect to **professional help resources** when needed
- ✅ Run **reliably with minimal dependencies**
- ✅ Deploy easily to **production environments**

### Key Features

| Feature | Details |
|---------|---------|
| **Sentiment Analysis** | Real-time detection using DistilBERT (fast, lightweight) |
| **Risk Detection** | Hybrid approach (keyword + semantic) for crisis situations |
| **Response Generation** | LLM-powered empathetic responses with fallback mode |
| **Conversation Context** | Maintains history for continuity (max 20 messages) |
| **Safety First** | Crisis responses + professional resource links |
| **Web Interface** | Clean, modern, responsive chat UI |
| **Logging** | Comprehensive error handling & debugging |
| **No Medical Claims** | Clear disclaimers throughout |

---

## 🏗️ System Architecture

```
Frontend (HTML/CSS/JS)  ←→  Backend (FastAPI)  ←→  LLM Provider
     ↓                              ↓                    ↓
  Chat UI          Sentiment        Risk      Response  (Ollama or
                   Analysis         Detection Generation  HF API)
```

### Backend Modules

| Module | Purpose |
|--------|---------|
| `main.py` | FastAPI app, routes, request handling |
| `nlp_pipeline.py` | Sentiment analysis using DistilBERT |
| `response_generator.py` | Response generation (HF API or Ollama) |
| `safety_handler.py` | Risk detection, crisis responses |

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.8+, FastAPI |
| **NLP** | HuggingFace Transformers (DistilBERT) |
| **LLM** | HuggingFace API or Ollama (optional) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Deployment** | Docker (optional), GitHub, Heroku, etc. |

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for model downloads)

### Installation

#### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/mental-wellness-chatbot.git
cd mental-wellness-chatbot
```

#### Step 2: Create virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Set up environment variables
```bash
# Copy the example file
cp .env.example .env

# Option A: Use HuggingFace API (Recommended for quick start)
# 1. Get free API key from https://huggingface.co/settings/tokens
# 2. Edit .env and add your key:
#    LLM_PROVIDER=huggingface-api
#    HF_API_KEY=hf_your_key_here

# Option B: Use Ollama (Local, no API key needed)
# 1. Install Ollama from https://ollama.ai
# 2. Run: ollama run mistral (or another model)
# 3. Edit .env:
#    LLM_PROVIDER=ollama
#    OLLAMA_URL=http://localhost:11434
```

#### Step 5: Run the backend
```bash
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     NLP pipeline initialized successfully
```

#### Step 6: Open frontend in browser
```bash
# Option 1: Open directly
open index.html  # macOS
# or
start index.html  # Windows
# or
firefox index.html  # Linux

# Option 2: Use Python's simple server (recommended for CORS)
python -m http.server 3000
# Then visit: http://localhost:3000
```

✅ **Done!** Start chatting with the bot.

---

## 📖 Configuration Guide

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# ===== Choose ONE LLM Provider =====

# Option 1: HuggingFace API
LLM_PROVIDER=huggingface-api
HF_API_KEY=hf_your_free_api_key  # Get from https://huggingface.co/settings/tokens

# Option 2: Ollama (Local, Free)
# LLM_PROVIDER=ollama
# OLLAMA_URL=http://localhost:11434
# OLLAMA_MODEL=mistral
```

### LLM Provider Setup

#### Option A: HuggingFace API (Easiest, No Setup)
1. Visit https://huggingface.co/settings/tokens
2. Create a free account
3. Generate an API token
4. Add to `.env`: `HF_API_KEY=hf_xxxx`
5. Run the bot - it works immediately

**Pros:**
- Zero setup
- Uses latest models
- Works from anywhere

**Cons:**
- Rate limited on free tier
- Requires internet
- Slight latency

#### Option B: Ollama (Best for Privacy & Speed)
1. Download Ollama from https://ollama.ai
2. Install and run: `ollama serve`
3. In another terminal: `ollama run mistral`
4. Set in `.env`:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=mistral
   ```
5. Run the bot

**Pros:**
- No API key needed
- Complete privacy
- Faster (local processing)
- No rate limits

**Cons:**
- Requires 4GB+ RAM
- Initial setup & model download
- Models vary in quality

#### Option C: Fallback Mode (No LLM)
If neither is configured, the bot uses template-based responses automatically. This still works well but lacks personalization.

---

## 📚 API Documentation

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-14T11:13:00",
  "nlp_model": "distilbert-base-uncased-finetuned-sst-2-english",
  "llm_provider": "huggingface-api"
}
```

### Chat Endpoint (Main)
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "message": "I've been feeling really stressed lately",
  "conversation_history": []
}
```

Response:
```json
{
  "user_message": "I've been feeling really stressed lately",
  "sentiment": {
    "label": "NEGATIVE",
    "score": 0.95
  },
  "is_high_risk": false,
  "risk_level": "low",
  "bot_response": "I hear you. Stress can be really overwhelming... [empathetic response]",
  "conversation_summary": "User expressing difficult emotions - heightened empathy mode"
}
```

### Sentiment Analysis Only
```bash
POST http://localhost:8000/analyze-sentiment
Content-Type: application/json

{"message": "I'm feeling great!"}
```

### Risk Assessment Only
```bash
POST http://localhost:8000/assess-risk
Content-Type: application/json

{"message": "I'm having suicidal thoughts"}
```

---

## 🔒 Safety & Guardrails

### Risk Detection Levels

| Level | Indicators | Response |
|-------|-----------|----------|
| **High** | "suicide", "self-harm", "kill myself" | Immediate crisis response + hotline numbers |
| **Medium** | "depressed", "panic", "can't cope" | Supportive response + resource suggestions |
| **Low** | Regular emotional language | Normal supportive response |

### Crisis Response

When high-risk language is detected, the bot:
1. ⚠️ Immediately alerts with warning banner
2. 📞 Provides emergency hotline numbers
3. 🔗 Links to professional resources
4. ✋ Refuses to engage normally (doesn't trivialize)

**Resources Provided:**
- 🆘 National Suicide Prevention Lifeline: 988
- 💬 Crisis Text Line: Text HOME to 741741
- 🌍 International resources
- 🏥 Emergency services guidance

### Non-Clinical Disclaimer

Displayed prominently:
> "This chatbot provides non-clinical mental wellness support. It is not a substitute for professional medical advice, therapy, or emergency services."

---

## 🧪 Testing

### Test Cases

#### Test 1: Basic Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I manage anxiety?"}'
```

#### Test 2: Sentiment Detection
```bash
curl -X POST http://localhost:8000/analyze-sentiment \
  -H "Content-Type: application/json" \
  -d '{"message": "I am so happy today!"}'
```

#### Test 3: Risk Detection
```bash
curl -X POST http://localhost:8000/assess-risk \
  -H "Content-Type: application/json" \
  -d '{"message": "I am having thoughts of suicide"}'
```

### Manual Testing in UI
1. Open `index.html` in browser
2. Try different emotional prompts
3. Watch sentiment change in real-time
4. Test with concerning language
5. Check crisis response triggers

---

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t mental-wellness-chatbot .
```

### Run Docker Container
```bash
docker run -p 8000:8000 \
  -e LLM_PROVIDER=huggingface-api \
  -e HF_API_KEY=your_api_key \
  mental-wellness-chatbot
```

---

## 🌐 Deployment Options

### 1. **Heroku** (Free tier)
```bash
heroku create your-app-name
heroku config:set LLM_PROVIDER=huggingface-api
heroku config:set HF_API_KEY=your_key
git push heroku main
```

### 2. **AWS Lambda + API Gateway**
- Serverless deployment
- Pay-per-use pricing
- See `serverless.yml` for config

### 3. **Vercel/Netlify** (Frontend only)
- Host `index.html` as static site
- Point to backend API URL
- See `vercel.json` config

### 4. **DigitalOcean / VPS**
- Affordable ($5-10/month)
- Full control
- Easy Docker deployment

### 5. **GitHub Pages** (Frontend only)
- Host frontend statically
- Point to deployed backend API
- Free hosting

---

## 📝 Project Structure

```
mental-wellness-chatbot/
├── main.py                 # FastAPI backend
├── nlp_pipeline.py         # Sentiment analysis
├── response_generator.py   # LLM integration
├── safety_handler.py       # Risk detection
├── index.html              # Frontend UI
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker config (optional)
├── README.md               # This file
└── docs/
    ├── ARCHITECTURE.md     # Technical details
    ├── API.md              # API reference
    └── DEPLOYMENT.md       # Deployment guide
```

---

## 🔧 Troubleshooting

### Issue: "Connection refused" on localhost:8000

**Solution:**
```bash
# Make sure backend is running
python main.py

# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port if needed
# Change port in main.py and frontend API_BASE_URL
```

### Issue: CORS errors in browser

**Solution:**
- CORS is enabled by default for development
- In production, update in `main.py`:
  ```python
  allow_origins=["https://yourdomain.com"]  # Specify exact origins
  ```

### Issue: HuggingFace API timeout

**Solution:**
- Free tier is rate-limited
- Wait a few seconds between messages
- Consider upgrading to paid tier or using Ollama

### Issue: NLP model download hangs

**Solution:**
```bash
# The first run downloads ~400MB of models
# This is normal and one-time only
# You can pre-download models:
python
>>> from transformers import pipeline
>>> pipeline("sentiment-analysis")  # Downloads automatically
```

### Issue: "CUDA out of memory" (GPU)

**Solution:**
- Force CPU usage in `.env`:
  ```env
  NLP_DEVICE=-1
  ```

### Issue: Port already in use

**Solution:**
```bash
# Use different port
python -m uvicorn main:app --port 8001
```

---

## 🚦 Performance & Limits

| Metric | Value | Notes |
|--------|-------|-------|
| **Sentiment Analysis** | ~50-100ms | Local, very fast |
| **Response Generation** | 2-5 seconds | Depends on LLM provider |
| **Max Message Length** | 5000 chars | Validation in place |
| **Conversation History** | 20 messages | Auto-trimmed |
| **Concurrent Users** | ~100 (free tier) | Scale with better infra |
| **Memory Usage** | ~2GB | NLP model + FastAPI |

---

## 📖 How It Works: Technical Deep Dive

### Request Flow

```
User Message
    ↓
[1] Validate Input (length, emptiness)
    ↓
[2] Sentiment Analysis (DistilBERT)
    ↓ (Processes in ~100ms)
    ↓
[3] Risk Assessment (Keyword + Semantic)
    ↓
[4] HIGH RISK? → Return Crisis Response
    ↓ NO
[5] Generate Context (Recent history)
    ↓
[6] LLM Response Generation (HF API or Ollama)
    ↓ (2-5 seconds)
    ↓
[7] Format Response with Sentiment
    ↓
Return to Frontend
```

### Sentiment Analysis

- **Model:** DistilBERT (67M parameters)
- **Fine-tuned on:** SST-2 (Stanford Sentiment Treebank)
- **Output:** POSITIVE (0.0-1.0) or NEGATIVE
- **Confidence:** 0.0 (uncertain) to 1.0 (confident)

### Response Generation

**System Prompt Template:**
```
You are a compassionate mental wellness support chatbot.
- Always be warm and non-judgmental
- Validate feelings, suggest healthy coping
- NEVER give medical advice
- Keep responses to 2-4 sentences
- Ask thoughtful follow-ups
```

**Adjusted by:** User sentiment + conversation context

### Risk Detection

- **High-Risk Keywords:** suicide, self-harm, abuse indicators
- **Medium-Risk:** depressed, panic, overwhelming
- **Hybrid Approach:** Keyword matching + semantic reasoning
- **False Positive Prevention:** Word boundary matching

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Multi-language support
- [ ] Better emotion classification (6-emotion model)
- [ ] User session persistence (database)
- [ ] Mobile app (React Native)
- [ ] Voice input/output
- [ ] Integration with professional resources API
- [ ] Admin dashboard for monitoring

**To contribute:**
1. Fork the repo
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📄 License

MIT License - Free for personal and commercial use.

---

## ⚠️ Important Disclaimer

### This Is NOT a Substitute for Professional Help

**Critical:** This chatbot provides **emotional support only**. It is:
- ❌ NOT a substitute for therapy or counseling
- ❌ NOT capable of diagnosis
- ❌ NOT a medical professional
- ❌ NOT trained in crisis intervention

**If you're in crisis:**
1. 🆘 Call emergency services (911 in US)
2. 📞 National Suicide Prevention: 988
3. 💬 Crisis Text Line: Text HOME to 741741
4. 🏥 Go to nearest emergency room

**Always prioritize professional mental health care.**

---

## 📞 Support & Issues

- **GitHub Issues:** Report bugs or request features
- **Documentation:** See `/docs` folder for detailed guides
- **Email:** your-email@example.com

---

## 🎓 Learning Resources

- [HuggingFace Transformers Guide](https://huggingface.co/transformers)
- [FastAPI Tutorial](https://fastapi.tiangolo.com)
- [DistilBERT Paper](https://arxiv.org/abs/1910.01108)
- [Mental Health Resources](https://www.samhsa.gov/helpline)

---

## 🙏 Acknowledgments

- HuggingFace for transformers library
- FastAPI for web framework
- DistilBERT authors for efficient NLP
- All mental health professionals

---

**Made with 💙 for mental wellness.** Start supporting today.

* [Groq](https://groq.com) for the LLaMA model access
* [Medical News Today](https://www.medicalnewstoday.com) for mental health resources
* [Wikipedia](https://www.wikipedia.org) for factual information


