# 🤖 Autonomous Personal Assistant

A sophisticated AI-powered personal assistant that integrates MCP tools, DSPy reasoning, Gemini API, and Perplexity API for autonomous task handling and proactive operations.

## 🎯 **Project Overview**

This autonomous personal assistant acts as a digital extension of yourself, capable of:
- **Autonomous Task Execution**: Independently handles complex multi-step workflows
- **Proactive Operations**: Monitors triggers and takes initiative without explicit commands
- **Multi-API Intelligence**: Combines Gemini's reasoning with Perplexity's real-time search
- **MCP Tool Integration**: Seamlessly connects to Gmail, Drive, Notion, GitHub, Slack, and more
- **Learning & Adaptation**: Builds memory and learns from user preferences and patterns

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Web UI    │  │ Voice/Chat  │  │   Mobile App        │ │
│  │ (Streamlit) │  │ Interface   │  │   (Optional)        │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   CORE ORCHESTRATION LAYER                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              DSPy Reasoning Engine                      │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │ │
│  │  │ Intent      │ │ Planning    │ │ Execution       │  │ │
│  │  │ Recognition │ │ Module      │ │ Controller      │  │ │
│  │  └─────────────┘ └─────────────┘ └─────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    API INTEGRATION LAYER                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Gemini    │  │ Perplexity  │  │    MCP Client       │ │
│  │   API       │  │    API      │  │    Manager          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      MCP TOOLS LAYER                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ │
│  │ Gmail   │ │ Drive   │ │ Notion  │ │ GitHub  │ │ Slack │ │
│  │ Server  │ │ Server  │ │ Server  │ │ Server  │ │Server │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └───────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ │
│  │ Discord │ │ Zapier  │ │ Calendar│ │ Memory  │ │ File  │ │
│  │ Server  │ │ Server  │ │ Server  │ │ Server  │ │Server │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └───────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   MEMORY & STORAGE LAYER                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Vector    │  │   Redis     │  │   PostgreSQL        │ │
│  │ Database    │  │   Cache     │  │   Metadata          │ │
│  │ (Chroma)    │  │             │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 **Key Features**

### **Autonomous Capabilities**
- **Morning Briefings**: Automatically generates daily summaries from emails, calendar, and news
- **Email Intelligence**: Processes, categorizes, and responds to emails autonomously
- **Meeting Preparation**: Proactively prepares materials and agendas for upcoming meetings
- **Code Review Assistance**: Monitors GitHub for PRs and provides intelligent feedback
- **Task Orchestration**: Coordinates complex workflows across multiple platforms

### **Proactive Operations**
- **Trigger Monitoring**: Continuously monitors for important events and changes
- **Pattern Learning**: Adapts behavior based on user preferences and historical patterns
- **Predictive Actions**: Anticipates needs and takes preemptive actions
- **Context Awareness**: Maintains long-term memory and contextual understanding

## 🛠️ **Technology Stack**

- **Core Engine**: Python 3.11+ with asyncio for concurrent operations
- **AI Orchestration**: DSPy framework for declarative AI programming
- **Language Models**: Gemini API (reasoning) + Perplexity API (search/research)
- **Tool Integration**: Model Context Protocol (MCP) for standardized tool access
- **Memory System**: ChromaDB (vector storage) + Redis (caching) + PostgreSQL (metadata)
- **Web Interface**: Streamlit for rapid prototyping and user interaction
- **Security**: Environment-based configuration with encrypted credential storage

## 📁 **Project Structure**

```
autonomous_assistant/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
├── config/                            # Configuration files
├── src/                               # Source code
│   ├── core/                          # Core orchestration layer
│   ├── agents/                        # DSPy-based AI agents
│   ├── apis/                          # API integration layer
│   ├── mcp/                           # MCP client and server management
│   ├── memory/                        # Memory and context management
│   ├── workflows/                     # Autonomous workflow definitions
│   ├── security/                      # Security and encryption utilities
│   └── ui/                            # User interface components
├── tests/                             # Test suite
├── docs/                              # Additional documentation
├── scripts/                           # Utility scripts
└── data/                              # Data storage and logs
```

## 🔧 **Quick Start**

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd autonomous_assistant
   pip install -r requirements.txt
   ```

2. **Configure APIs**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Initialize Services**
   ```bash
   python scripts/setup.py
   ```

4. **Run Assistant**
   ```bash
   python src/main.py
   ```

## 🎯 **Use Cases**

- **"Summarize all new emails and update my Notion tracker"**
- **"If any email contains CV, forward to HR Slack and tag #screen"**
- **"Monitor GitHub issues tagged urgent, and ping me on Discord"**
- **"Every morning, give me a briefing from calendar, emails, Perplexity top 3 news"**
- **"Automatically schedule follow-ups for unanswered important emails"**
- **"Prepare meeting materials based on calendar events and participant history"**

## 🔐 **Security & Privacy**

- **API Key Management**: Secure storage using environment variables and encryption
- **Data Privacy**: Local processing with optional cloud integration
- **Access Control**: Granular permissions for different tool integrations
- **Audit Logging**: Comprehensive logging of all autonomous actions
- **User Consent**: Explicit approval required for sensitive operations

## 📈 **Development Roadmap**

### **Phase 1: Foundation** (Weeks 1-2)
- Core DSPy orchestration layer
- Basic MCP client manager
- Gemini and Perplexity API integration
- Vector database setup

### **Phase 2: Core Integration** (Weeks 3-4)
- Gmail, Drive, Calendar MCP integration
- Memory and context management
- Basic autonomous triggers
- Simple workflow execution

### **Phase 3: Advanced Features** (Weeks 5-6)
- Notion, GitHub, Slack integration
- Learning and preference system
- Advanced autonomous decision making
- Web UI development

### **Phase 4: Production Ready** (Weeks 7-8)
- Complex workflow automation
- Security hardening
- Performance optimization
- Comprehensive testing

## 🤝 **Contributing**

This project follows modern Python development practices with comprehensive testing, documentation, and security considerations. Contributions are welcome!

## 📄 **License**

MIT License - see LICENSE file for details.
