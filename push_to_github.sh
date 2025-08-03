#!/bin/bash

# Script to push the autonomous assistant to GitHub
echo "🚀 Pushing Autonomous Personal Assistant to GitHub..."

# Initialize git repository
echo "📁 Initializing git repository..."
git init

# Configure git user
echo "👤 Configuring git user..."
git config user.email "adhithanraja6@gmail.com"
git config user.name "adhimiw"

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Initial commit: Autonomous Personal Assistant with DSPy, Gemini, and Perplexity integration

Features:
- 🧠 Gemini API integration for reasoning and generation
- 🔍 Perplexity API integration for real-time search
- 🎯 DSPy framework for advanced AI programming
- 🔧 API Manager with intelligent routing and fallbacks
- 🔐 Secure configuration and credential management
- 📊 Comprehensive logging and monitoring
- 🏗️ Extensible architecture ready for MCP tools
- 🤖 Autonomous operation capabilities
- 📚 Complete documentation and setup guides

Ready for integration with Gmail, Drive, Notion, GitHub, Slack and more!"

# Add remote origin
echo "🔗 Adding remote origin..."
git remote add origin https://github.com/adhimiw/agent8.git

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

# Push to GitHub
echo "⬆️ Pushing to GitHub..."
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo "🌐 Repository URL: https://github.com/adhimiw/agent8"
echo ""
echo "📋 Next steps:"
echo "1. Clone the repository on other machines"
echo "2. Copy your .env.local file for API keys"
echo "3. Run: pip install -r requirements.txt"
echo "4. Run: python scripts/test_apis.py"
echo "5. Run: python src/main.py"
