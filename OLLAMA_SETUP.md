# Ollama Setup Guide - FREE Local AI

Ollama allows you to run powerful AI models locally on your Mac for **100% FREE** - no API keys, no usage limits, complete privacy!

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Ollama

**On macOS:**
```bash
# Download and install from website
# Visit: https://ollama.ai/download

# Or use Homebrew
brew install ollama
```

**On Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**On Windows:**
Download from: https://ollama.ai/download

### Step 2: Start Ollama Server

```bash
ollama serve
```

This starts the Ollama server on `http://localhost:11434`

### Step 3: Pull a Model

In a new terminal:

```bash
# Recommended: Llama 3 (best quality)
ollama pull llama3

# Or try other models:
ollama pull mistral      # Faster, still good quality
ollama pull llama2       # Older but reliable
ollama pull codellama    # Better for technical docs
```

**Model Download Sizes:**
- Llama 3: ~4.7 GB
- Mistral: ~4.1 GB  
- Llama 2: ~3.8 GB

### Step 4: Test Ollama

```bash
# Test if it's working
ollama run llama3 "Hello, how are you?"
```

If you get a response, you're ready! ✅

## 📱 Using Ollama in the Web App

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **In the web app:**
   - Check "✨ Use AI-Powered Task Generation"
   - Select "🆓 Ollama (FREE - Local)"
   - Choose your model (Llama 3 recommended)
   - Upload your PDF and process!

## 🎯 Model Recommendations

### For PDF to Jira Tasks:

| Model | Speed | Quality | Size | Best For |
|-------|-------|---------|------|----------|
| **Llama 3** | Medium | ⭐⭐⭐⭐⭐ | 4.7 GB | Best overall quality |
| **Mistral** | Fast | ⭐⭐⭐⭐ | 4.1 GB | Good balance of speed/quality |
| Llama 2 | Medium | ⭐⭐⭐ | 3.8 GB | Reliable, older model |
| Code Llama | Slow | ⭐⭐⭐⭐ | 3.8 GB | Technical documentation |

**Recommendation:** Start with **Llama 3** for best results!

## 🔧 Advanced Configuration

### Run Ollama on Different Port

```bash
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

### List Downloaded Models

```bash
ollama list
```

### Remove a Model

```bash
ollama rm llama3
```

### Update a Model

```bash
ollama pull llama3
```

## 💡 Tips & Tricks

### 1. Keep Ollama Running in Background

**macOS/Linux:**
```bash
# Add to ~/.zshrc or ~/.bashrc
alias ollama-start='nohup ollama serve > /dev/null 2>&1 &'
```

Then just run: `ollama-start`

### 2. Check if Ollama is Running

```bash
curl http://localhost:11434/api/tags
```

If you get a JSON response, it's running!

### 3. Performance Tips

- **First run is slower** - models load into memory
- **Subsequent runs are fast** - models stay cached
- **Close other apps** - AI needs RAM (8GB+ recommended)
- **Use SSD** - models load faster from SSD

## 🆚 Ollama vs OpenAI Comparison

| Feature | Ollama | OpenAI |
|---------|--------|--------|
| Cost | **FREE** ✅ | ~$0.01-0.05 per PDF ❌ |
| Privacy | **Runs locally** ✅ | Sent to cloud ❌ |
| Speed | Slower (30-60s) | Faster (5-10s) ✅ |
| Quality | Very Good ⭐⭐⭐⭐ | Excellent ⭐⭐⭐⭐⭐ |
| Internet | **Works offline** ✅ | Requires internet ❌ |
| Setup | Download models (~5GB) | Just API key ✅ |

## 🐛 Troubleshooting

### "Ollama is not running"
```bash
# Start Ollama
ollama serve
```

### "Model not found"
```bash
# Pull the model first
ollama pull llama3
```

### Slow Performance
- Close other applications
- Ensure you have 8GB+ RAM
- Try a smaller model (mistral instead of llama3)

### Port Already in Use
```bash
# Use a different port
OLLAMA_HOST=localhost:11435 ollama serve
```

Then update the app to use port 11435.

### Out of Memory
- Close browser tabs and other apps
- Use a smaller model
- Add more RAM to your system

## 🎓 Learn More

- **Official Docs:** https://ollama.ai/
- **Model Library:** https://ollama.ai/library
- **GitHub:** https://github.com/ollama/ollama

## ✨ Example Workflow

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Pull model (one-time)
ollama pull llama3

# Terminal 3: Start your web app
python app.py

# Browser: Open http://localhost:5000
# ✅ Check "Use AI"
# ✅ Select "Ollama"
# ✅ Choose "Llama 3"
# ✅ Upload PDF
# 🎉 Get intelligent tasks!
```

## 🎉 Success!

You now have **FREE, local AI** for PDF processing! 

**Benefits:**
- ✅ No API costs
- ✅ Complete privacy
- ✅ Works offline
- ✅ Unlimited usage
- ✅ No rate limits

Enjoy your PDF to Jira automation! 🚀
