# 🗓️PracticeCal

A beautifully minimal music practice tracker focused on what matters most—making music.

## What it does

PracticeCal helps musicians track their daily practice sessions with radical simplicity. Click any day to log your practice time, see your weekly total, and focus on what matters most—making music.

### Core Features

- **Clean Calendar View** — See your entire week at a glance
- **One-Tap Logging** — Add practice sessions effortlessly
- **Weekly Totals** — Track your progress with elegant typography
- **Multi-Instrument** — Log different instruments and session notes
- **Auto-Time Tracking** — Practice duration calculated automatically from recording length

## Design Philosophy

- **Radical Simplification** — No visual clutter, just essential functionality
- **Content First** — Your practice data is the hero
- **Intuitive Interactions** — Everything works exactly as you'd expect
- **Thoughtful Design** — Clean typography, generous whitespace, purposeful interactions

## Planned Features

### 🎯 Practice Suggestions
Intelligent practice recommendations based on your history and goals.

### 🎙️ Audio Recording & Auto-Tracking
Record practice sessions directly in the app. PracticeCal automatically calculates your practice time based on the actual recording duration—no more manual timers or forgotten sessions. Just hit record, practice, and stop. Your session time is logged precisely.

**Auto-tracking features:**
- Seamless recording integration
- Automatic duration calculation
- Background recording detection
- Smart pause/resume handling

### 📺 YouTube Live Broadcasting
Stream your practice sessions live to YouTube with one-tap broadcasting.

## Tech Stack

- **Frontend**: React with clean, minimal CSS
- **Backend**: FastAPI with GraphQL
- **Data**: In-memory storage (perfect for personal use)

## Getting Started

```bash
# Install dependencies
uv sync

# Run the app
uv run fastapi dev app/main.py
```

Open [localhost:8000](http://localhost:8000) and start tracking your practice.

---

*"Simplicity is the ultimate sophistication."* — Leonardo da Vinci