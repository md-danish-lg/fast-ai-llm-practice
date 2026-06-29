# 🤖 Python AI Service

A lightweight FastAPI microservice that wraps LLM API calls behind clean REST endpoints. Built to be called from a Java/Spring Boot backend as part of a polyglot microservice architecture.

## Tech Stack

- **Python 3** + **FastAPI** — REST API framework
- **Pydantic** — request/response validation
- **Groq API** — LLM inference (llama-3.3-70b-versatile)
- **python-dotenv** — environment variable management
- **uvicorn** — ASGI server

## Architecture

This service sits alongside a Java/Spring Boot backend, handling all AI/LLM work in Python where the AI ecosystem is strongest.

```
Spring Boot Backend → POST /summarize → FastAPI AI Service → Groq LLM API
                    → POST /translate →
                    → POST /echo     →
```

## Endpoints

| Method | Endpoint | Request Body | Description |
|--------|----------|-------------|-------------|
| `GET` | `/` | — | Health check |
| `POST` | `/echo` | `{"text": "..."}` | Echo text back |
| `POST` | `/summarize` | `{"text": "..."}` | LLM-generated summary |
| `POST` | `/translate` | `{"text": "...", "language": "spanish"}` | Translate text to target language |

All endpoints validate input with Pydantic — empty strings return `422 Unprocessable Entity`. LLM errors return `500` with a descriptive message.

## Getting Started

### Prerequisites
- Python 3.10+
- A Groq API key (free at console.groq.com)

### Setup
```bash
pip install fastapi uvicorn groq python-dotenv
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

### Run
```bash
uvicorn main:app --reload
```

Service available at `http://localhost:8000`

## Example Requests

**Summarize text**
```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI is a modern Python web framework for building APIs with automatic validation and documentation."}'
```

**Translate text**
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?", "language": "spanish"}'
```

## What I Learned

- Building REST APIs with FastAPI and Pydantic validation
- Integrating LLM APIs (Groq) into a backend service
- Managing secrets with python-dotenv
- Designing a service meant to be called by another backend — polyglot microservice pattern
- Structuring Python projects for backend use, not just scripting