# 🗓️PracticeCal

A minimal music practice tracker!

## What it does

PracticeCal helps musicians track their daily practice sessions by recording them and providing support. Click any day to log your practice time, see your weekly total.

## Tech Stack

- **Frontend**: React with clean, minimal CSS
- **Backend**: FastAPI with GraphQL

## Getting Started

```bash
# Install dependencies
uv sync

# Run the app
uv run uvicorn app.main:app
```

Open [localhost:8000](http://localhost:8000) and start tracking your practice.

## Deployment / Demo

Available on fly.io at https://practicecal.fly.dev.

Deploy updates with the `flyctl deploy` command.