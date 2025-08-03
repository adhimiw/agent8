# 🚀 Quick Start Guide

Get your Autonomous Personal Assistant up and running in minutes!

## 📋 Prerequisites

- Python 3.11 or higher
- Git (for cloning repositories)
- Internet connection (for API calls)

## ⚡ Quick Setup

### 1. Install Dependencies

```bash
cd autonomous_assistant
pip install -r requirements.txt
```

### 2. Configure API Keys

Your API keys are already configured in the `.env` file:
- ✅ **Gemini API**: `AIzaSyAzayQbTLvUw-IKtLlnJ14kNuVY3gxAaqI`
- ✅ **Perplexity API**: `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`

### 3. Test API Connections

```bash
python scripts/test_apis.py
```

This will verify that both APIs are working correctly.

### 4. Run the Assistant

```bash
python src/main.py
```

## 🎯 What You Can Do Now

### Basic Commands
- **Chat with the Assistant**: Type any question or request
- **Get Help**: Type `help` for available commands
- **Exit**: Type `exit`, `quit`, or `bye` to stop

### Example Interactions

```
Assistant> What is artificial intelligence?
```
*Uses Gemini API for reasoning and explanation*

```
Assistant> What are the latest AI news today?
```
*Uses Perplexity API for real-time search and current information*

```
Assistant> Explain quantum computing and find recent developments
```
*Uses both APIs in hybrid mode for comprehensive response*

## 🔧 Configuration Options

### Environment Variables
Edit `.env` file to customize:

```bash
# Autonomous behavior
AUTONOMOUS_MODE=true
PROACTIVE_MONITORING=true
TRIGGER_CHECK_INTERVAL=60

# Feature flags
ENABLE_EMAIL_PROCESSING=true
ENABLE_CALENDAR_INTEGRATION=true
ENABLE_GITHUB_MONITORING=true
```

### API Settings
```bash
# Gemini configuration
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=8192

# Perplexity configuration
PERPLEXITY_MODEL=sonar-pro
PERPLEXITY_TEMPERATURE=0.3
PERPLEXITY_MAX_TOKENS=4096
```

## 🧪 Testing & Validation

### Run API Tests
```bash
python scripts/test_apis.py
```

### Check Configuration
```bash
python scripts/setup.py
```

### View Logs
```bash
tail -f logs/assistant.log
```

## 🎨 Advanced Features

### DSPy Integration
The assistant uses DSPy for advanced AI programming:
- Declarative AI module composition
- Automatic prompt optimization
- Multi-step reasoning workflows

### MCP Tool Integration
Ready for integration with:
- Gmail (email processing)
- Google Drive (file management)
- Notion (knowledge management)
- GitHub (code monitoring)
- Slack (team communication)

### Autonomous Operations
When enabled, the assistant can:
- Monitor triggers automatically
- Take proactive actions
- Learn from user patterns
- Provide intelligent suggestions

## 🔍 Troubleshooting

### Common Issues

**API Key Errors**
```bash
# Check if keys are set correctly
grep -E "(GEMINI|PERPLEXITY)_API_KEY" .env
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Permission Errors**
```bash
# Make scripts executable
chmod +x scripts/*.py
```

### Getting Help

1. **Check Logs**: `tail -f logs/assistant.log`
2. **Run Tests**: `python scripts/test_apis.py`
3. **Reconfigure**: `python scripts/setup.py`

## 🚀 Next Steps

1. **Explore Features**: Try different types of queries
2. **Configure Integrations**: Add your productivity tool credentials
3. **Enable Autonomous Mode**: Let the assistant work proactively
4. **Customize Workflows**: Modify the orchestration logic
5. **Add MCP Tools**: Integrate with your favorite applications

## 📚 Documentation

- **Full Documentation**: See `README.md`
- **API Reference**: Check `src/apis/` for implementation details
- **Configuration Guide**: Review `config/settings.py`
- **Architecture Overview**: Examine `src/core/orchestrator.py`

## 🎉 You're Ready!

Your autonomous personal assistant is now configured and ready to help you with:
- ✅ Intelligent reasoning (Gemini)
- ✅ Real-time search (Perplexity)
- ✅ Hybrid AI responses
- ✅ Extensible architecture
- ✅ Autonomous capabilities

Start exploring and let your AI assistant enhance your productivity!
