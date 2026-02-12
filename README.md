# flowlens-fastapi-flow-analyzer
Static request-flow analyzer for FastAPI codebases with async processing and deterministic call graph extraction.
## Architecture (MVP)

flowchart LR
    CLI[CLI Interface]
    API[FastAPI Service]
    Redis[(Redis Queue)]
    Worker[Analysis Worker]
    SQLite[(SQLite Metadata DB)]
    Artifacts[(Graph Artifacts JSON)]

    CLI --> API
    API --> Redis
    Redis --> Worker
    Worker --> SQLite
    Worker --> Artifacts
    API --> SQLite

sequenceDiagram
    participant User
    participant CLI
    participant API
    participant Redis
    participant Worker
    participant DB

    User->>CLI: flowlens analyze repo
    CLI->>API: POST /analyze
    API->>Redis: enqueue job
    Worker->>Redis: fetch job
    Worker->>DB: save endpoints + graph
    CLI->>API: GET /status
    CLI->>API: GET /endpoints