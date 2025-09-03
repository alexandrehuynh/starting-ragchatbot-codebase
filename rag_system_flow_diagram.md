# RAG System Information Flow Diagram

## Request/Response Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Frontend<br/>(HTML/JS)
    participant FastAPI as FastAPI Backend<br/>(app.py)
    participant RAG as RAG System<br/>(rag_system.py)
    participant VectorStore as Vector Store<br/>(ChromaDB)
    participant SearchTools as Search Tools<br/>(search_tools.py)
    participant AI as AI Generator<br/>(Claude API)
    participant Session as Session Manager

    User->>Frontend: Enter query in chat interface
    Frontend->>FastAPI: POST /query<br/>{query, session_id}
    
    FastAPI->>RAG: process_query(query, session_id)
    
    RAG->>Session: get_context(session_id)
    Note over Session: Retrieve conversation history
    
    RAG->>VectorStore: search(query, n_results=5)
    Note over VectorStore: 1. Generate embeddings<br/>2. Similarity search<br/>3. Return top chunks
    
    RAG->>SearchTools: search_courses(query)
    Note over SearchTools: Extract course-specific<br/>information if needed
    
    RAG->>AI: generate_response()<br/>[query + context + search results]
    Note over AI: Claude processes:<br/>- User query<br/>- Retrieved chunks<br/>- Conversation history
    
    AI-->>RAG: AI-generated response
    
    RAG->>Session: add_messages()<br/>[user query, AI response]
    Note over Session: Update conversation history
    
    RAG-->>FastAPI: {response, sources, session_id}
    
    FastAPI-->>Frontend: JSON Response
    Frontend-->>User: Display response in chat UI
```

## Data Processing Pipeline (Startup)

```mermaid
flowchart TD
    Start([Application Startup])
    Start --> LoadDocs[Load Course Documents<br/>docs/*.txt]
    
    LoadDocs --> Process[Document Processor]
    Process --> Chunk[Split into Chunks<br/>~500 chars each]
    
    Chunk --> Embed[Generate Embeddings<br/>sentence-transformers]
    
    Embed --> Store[Store in ChromaDB]
    Store --> Ready([System Ready])
    
    style Start fill:#e1f5e1
    style Ready fill:#e1f5e1
    style Process fill:#fff3cd
    style Store fill:#d4edda
```

## Component Interaction Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Web Interface<br/>index.html + script.js]
    end
    
    subgraph "API Layer"
        API[FastAPI Server<br/>:8000]
    end
    
    subgraph "Processing Layer"
        RAGSys[RAG System]
        SessionMgr[Session Manager]
        DocProc[Document Processor]
        SearchTool[Search Tools]
    end
    
    subgraph "Storage Layer"
        Chroma[ChromaDB<br/>Vector Store]
        Docs[Course Documents]
    end
    
    subgraph "AI Layer"
        Claude[Claude AI<br/>Anthropic API]
    end
    
    UI <-->|HTTP/JSON| API
    API --> RAGSys
    RAGSys --> SessionMgr
    RAGSys --> SearchTool
    RAGSys --> Chroma
    RAGSys --> Claude
    DocProc --> Docs
    DocProc --> Chroma
    
    style UI fill:#e3f2fd
    style API fill:#fff3e0
    style RAGSys fill:#f3e5f5
    style Chroma fill:#e8f5e9
    style Claude fill:#fce4ec
```

## Key Data Structures

```
Request Flow:
├── User Query (string)
├── Session ID (string)
└── Processing:
    ├── Embeddings Generation
    ├── Vector Search (top 5 chunks)
    ├── Context Building:
    │   ├── Retrieved chunks
    │   ├── Conversation history  
    │   └── Search tool results
    └── AI Response Generation

Response Flow:
├── AI Response (string)
├── Sources (list of chunks)
├── Session ID (string)
└── Metadata (timestamps, course info)
```