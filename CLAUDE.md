/i# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Quick start (recommended)
./run.sh

# Manual start
cd backend && uv run uvicorn app:app --reload --port 8000
```

### Environment Setup
```bash
# Install dependencies
uv sync

# Create .env file with Anthropic API key (required)
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

The application runs on `http://localhost:8000` with API docs at `/docs`.

## Architecture Overview

This is a RAG (Retrieval-Augmented Generation) system for querying course materials using semantic search and AI responses.

### Core Flow
1. **Document Processing Pipeline**: Course documents in `/docs/*.txt` are chunked (~500 chars), embedded using sentence-transformers, and stored in ChromaDB at startup
2. **Query Processing**: User queries → Vector similarity search → Context retrieval → Claude AI generation → Response with sources
3. **Session Management**: Conversation history is maintained per session for context-aware responses

### Key Components

**RAGSystem** (`backend/rag_system.py`): Main orchestrator coordinating all subsystems
- Initializes and manages DocumentProcessor, VectorStore, AIGenerator, SessionManager, and ToolManager
- Handles document ingestion and query processing

**VectorStore** (`backend/vector_store.py`): ChromaDB wrapper for semantic search
- Stores document embeddings and metadata
- Performs similarity search with configurable result limits

**AIGenerator** (`backend/ai_generator.py`): Claude API integration
- Generates contextual responses using retrieved chunks and conversation history

**SearchTools** (`backend/search_tools.py`): Extensible tool system
- CourseSearchTool provides structured course information extraction

**FastAPI Application** (`backend/app.py`): HTTP API layer
- `/query` endpoint for RAG queries
- `/stats` endpoint for course statistics
- Serves frontend static files with special handling for root path

### Data Models
- **Course**: Contains title, description, and lessons
- **Lesson**: Individual lesson with title and content
- **CourseChunk**: Text chunk with metadata for vector storage

## Important Configuration

The system expects:
- Course documents in `/docs/course*.txt` format
- Anthropic API key in `.env` file
- Python 3.13+ with uv package manager
- ChromaDB persistent storage in `backend/chroma_db/`

Frontend is served from `/frontend/` directory with automatic fallback to index.html for development.
- always run uv to run the server. do not use pip directly. make sure to use uv to manage all dependencies