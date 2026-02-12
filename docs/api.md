# FlowLens API (MVP)

Base URL: http://localhost:8000

## 1) Start analysis

POST /analyze

Request (one of):
```json
{ "source": { "type": "path", "value": "/abs/path/to/repo" } }
{ "source": { "type": "git",  "value": "https://github.com/org/repo.git" } }
```
Response:
```json
202 Accepted
{ "repo_id": "<id>", "status": "QUEUED" }
```
## 2) Status

GET /repos/{repo_id}/status

Response:
```json
{ "repo_id": "<id>", "status": "QUEUED|RUNNING|READY|FAILED", "message": "" }
```
## 3) List endpoints

GET /repos/{repo_id}/endpoints

Response:
```json
{ "repo_id": "<id>", "count": 17, "endpoints": [
    { "method": "POST", "path": "/orders", "handler": "routes.orders:create_order", "file": "routes/orders.py", "line": 42 }
  ] }
```
## 4) Get flow for endpoint

GET /repos/{repo_id}/flow?method=POST&path=/orders&depth=8

Response:
```json
{ "repo_id": "<id>", "method": "POST", "path": "/orders",
    "confidence": 0.78,
    "unknown_edges": 1,
    "steps": [
      { "label": "routes/orders.py:create_order", "file": "routes/orders.py", "line": 42, "kind": "func" },
      { "label": "services/order_service.py:create_order", "file": "services/order_service.py", "line": 15, "kind": "func" },
      { "label": "db/session.py:commit", "file": "db/session.py", "line": 88, "kind": "db" }
    ],
    "gaps": [
      { "file": "services/order_service.py", "line": 22, "reason": "dynamic call via variable" }
    ],
    "mermaid": "flowchart TD\nA-->B\n..."
  }
```