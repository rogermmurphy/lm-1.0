# LM-1.0 - Learning Management AI Platform

AI-powered learning management system with RAG (Retrieval Augmented Generation), speech-to-text transcription, and automated presentation generation.

## Overview

This repository contains proof-of-concept implementations for an AI-driven educational platform that includes:

- **RAG Chatbot** - Question answering with ChromaDB
- **Speech-to-Text** - Lecture transcription using Whisper AI
- **Presentation Generation** - Automated slide creation
- **Async Job Processing** - Background workers for long-running tasks
- **LangChain Agents** - Agentic AI with tool use

## Project Structure

```
lm-1.0/
├── poc/                           # Proof of Concept implementations
│   ├── 00-functional-poc/         # Basic RAG chatbot
│   ├── 01-llm-ollama/            # Ollama LLM integration
│   ├── 07-langchain-agent/       # LangChain agents
│   ├── 07-mcp-agent/             # Model Context Protocol
│   ├── 08-async-jobs/            # Async job processing
│   └── 09-speech-to-text/        # Whisper transcription ✨ NEW
└── old/                          # Legacy code
```

## Featured: Speech-to-Text POC (09)

**Status**: ✅ Complete and Tested

Fully functional speech-to-text transcription system using OpenAI's Whisper model:

- **Async Processing** - Queue jobs, process in background
- **Local & Free** - Runs locally with Whisper
- **Multi-language** - Supports 99+ languages
- **RAG Integration** - Auto-loads transcripts to ChromaDB
- **Production Ready** - Complete with tests and documentation

### Quick Start (Speech-to-Text)

```bash
# 1. Install dependencies
cd poc/09-speech-to-text
pip install -r requirements.txt

# 2. Setup database
psql -U postgres -d lm_dev -f schema.sql

# 3. Create sample audio and test
python create_real_speech.py
python test_real_speech.py
```

See [poc/09-speech-to-text/START-HERE.md](poc/09-speech-to-text/START-HERE.md) for detailed instructions.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- FFmpeg (for audio processing)
- Ollama (optional, for local LLMs)

## Technology Stack

- **AI/ML**: OpenAI Whisper, Ollama, LangChain, ChromaDB
- **Backend**: Python, FastAPI (planned)
- **Database**: PostgreSQL, Redis
- **Queue**: Redis
- **Vector DB**: ChromaDB

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/lm-1.0.git
   cd lm-1.0
   ```

2. **Set up infrastructure**
   - Install PostgreSQL
   - Install Redis
   - Install FFmpeg

3. **Choose a POC to explore**
   - Each POC has its own README and START-HERE guide
   - See individual directories for detailed setup

## Documentation

- [Quick Start Guide](poc/QUICK-START.md)
- [Getting Started](poc/GETTING-STARTED.md)
- [Infrastructure Assessment](poc/INFRASTRUCTURE-ASSESSMENT.md)
- [Final Status](poc/FINAL-STATUS.md)

## Recent Updates

### November 2025
- ✅ **Speech-to-Text POC** - Complete Whisper integration
- ✅ Real speech transcription tested
- ✅ Database integration
- ✅ ChromaDB auto-loading
- ✅ Async job processing

## License

[Specify your license here]

## Contributing

Contributions welcome! Please read our contributing guidelines first.

## Contact

[Your contact information]

---

**Status**: Active Development
**Latest Version**: POC Phase
**Last Updated**: November 2025
