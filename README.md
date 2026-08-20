# Security API – Backend (Flask)

Backend for the API Key Authentication Anti-Pattern exercise.

## Requirements

- Python 3
- pip

## Installation

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Execution

Start the server with:

```bash
python app.py
```

The API runs at `http://localhost:3000`.

## Endpoints

| Method | Endpoint   | API Key Required | Response           |
| ------ | ---------- | ---------------- | ------------------ |
| GET    | `/health`  | No               | `{ "status": "ok" }` |
| GET    | `/api/data`| Yes              | Protected data     |
| POST   | `/api/data`| Yes              | Confirmation       |

Protected endpoints expect the API key in the `x-api-key` request header.

## Security Note

This is an anti-pattern — do not use in production. Hardcoded API keys in source code can be extracted by anyone with access to the repository or client-side code. Use secure secret management and server-side authentication in real applications.
