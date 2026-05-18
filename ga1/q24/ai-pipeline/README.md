# AI-Powered Data Pipeline

A FastAPI-based pipeline that fetches user data, enriches it with AI analysis, stores results, and sends notifications.

## 🚀 Endpoint URL

```
POST http://localhost:8000/pipeline
```

## 📋 Setup

### 1. Install Dependencies
```bash
cd ai-pipeline
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file:
```
AIPIPE_TOKEN=your_token_here
AIPIPE_BASE_URL=https://aipipe.org/openai/v1
PORT=8000
```

### 3. Run Server
```bash
python main.py
```

Server starts at `http://localhost:8000`

## 📡 API Usage

### Request
```bash
curl -X POST http://localhost:8000/pipeline \
  -H "Content-Type: application/json" \
  -d '{"email": "your-student-id", "source": "JSONPlaceholder Users"}'
```

### Response
```json
{
  "items": [
    {
      "original": {"name": "...", "email": "...", "company": "..."},
      "analysis": "AI-generated 2-sentence summary",
      "sentiment": "enthusiastic/critical/objective",
      "stored": true,
      "timestamp": "2026-02-09T10:30:00Z"
    }
  ],
  "notificationSent": true,
  "processedAt": "2026-02-09T10:30:05Z",
  "errors": []
}
```

## 🧪 Testing
```bash
python test_pipeline.py
```

## 📦 Pipeline Components

| Component | Description |
|-----------|-------------|
| **API Fetch** | Fetches first 3 users from JSONPlaceholder |
| **AI Analysis** | GPT-4o-mini generates summary & sentiment |
| **Storage** | Saves to `results.json` |
| **Notification** | Console log to specified email |
| **Error Handling** | Retry with exponential backoff |
