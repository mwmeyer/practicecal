# Frontend UI Documentation

## Overview

Single-page React application with calendar interface for practice tracking. Built without build tools - uses React via CDN with in-browser Babel compilation.

## Key Components

### App
- Main container with week navigation
- Manages current week state and modal visibility
- Fetches practice data via custom GraphQL client

### Modal
- Handles session creation/editing
- Audio/video recording interface
- Automatic duration calculation

### Calendar
- Weekly grid (Sunday-Saturday)
- Click day to add session
- Click session to view/edit

## Duration Calculation

**Duration is automatically calculated from recording time:**

```javascript
const finalDuration = Math.max(1, Math.ceil(recordingTime / 60));
```

- Records actual practice time in seconds
- Converts to minutes (rounds up)
- Minimum 1 minute duration
- No manual time entry

Examples:
- 30 seconds → 1 minute
- 90 seconds → 2 minutes

## Recording System

### Features
- Audio-only or video+audio recording
- Browser MediaRecorder API
- Base64 storage in GraphQL
- Real-time recording timer

### Workflow
1. Click empty day → opens modal
2. Toggle video on/off
3. Click "Start Recording"
4. Practice while timer runs
5. Click "Stop Recording"
6. Duration auto-calculated and saved

### Media Storage
- Recordings stored as Base64 strings
- Sent to backend via GraphQL mutations
- Playback with built-in browser controls

## Visual Features

### Calendar States
- **Today**: Yellow highlight
- **Has Practice**: Blue background
- **Sessions**: Show duration + media icon (🎙️/📹)

### Time Formatting
- Under 1 hour: "45m"
- Over 1 hour: "1h 30m"
- Weekly totals prominently displayed

## Technical Details

- Custom GraphQL client (no Apollo)
- React hooks for state management
- Responsive CSS without frameworks
- Mobile-friendly design
- Automatic data refresh after mutations

## Browser Requirements

- MediaRecorder API support
- getUserMedia for camera/mic access
- Modern browsers (Chrome 47+, Firefox 29+, Safari 14+)