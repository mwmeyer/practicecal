# PracticeCal Application Architecture

## Overview

PracticeCal is a web-based practice tracking application that allows users to log practice sessions, record audio/video media, and visualize their progress in a weekly calendar format. The application uses a modern full-stack architecture with a Python/FastAPI backend and React frontend.

## System Architecture

The application follows a clean separation between frontend and backend:

- **Frontend**: React single-page application served as static files
- **Backend**: FastAPI application with GraphQL API
- **Storage**: In-memory data structures (sessions lost on restart)
- **Media**: Base64-encoded audio/video stored with session data

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic API documentation
- **Strawberry GraphQL**: Type-safe GraphQL implementation for Python
- **In-memory storage**: Simple Python data structures for rapid prototyping

### Frontend
- **React 18**: Component-based UI library loaded via CDN
- **Vanilla JavaScript**: No build process, browser-compiled with Babel
- **Custom GraphQL client**: Lightweight implementation for API communication
- **Web APIs**: MediaRecorder and getUserMedia for media capture

## Core Functionality

### Practice Session Management
- Create, read, update, and delete practice sessions
- Sessions include date, duration, and optional media recordings
- Data organized by week with Sunday as week start

### Media Recording
- Browser-based audio/video recording using Web APIs
- Media stored as Base64 strings within session data
- Playback capabilities with download options

### Calendar Interface
- Weekly calendar view showing practice sessions
- Navigation between weeks
- Daily and weekly practice time aggregation
- Mobile-responsive design

## Key Architectural Decisions

### GraphQL API
Chose GraphQL over REST for flexible data fetching and type safety. The schema provides queries for retrieving practice data and mutations for session management.

### In-Memory Storage
Used for simplicity and rapid development. All data is stored in Python lists and dictionaries, making the application stateless but non-persistent.

### Single-File Frontend
The entire React application is contained in one HTML file with embedded JavaScript, eliminating build processes and simplifying deployment.

### Base64 Media Storage
Audio and video recordings are encoded as Base64 strings and stored directly with session data, avoiding file system complexity.

## Production Considerations

### Current Limitations
- **Data Persistence**: All data is lost when the application restarts
- **Scalability**: In-memory storage limits the number of sessions
- **Security**: No authentication or user isolation
- **Media Storage**: Base64 encoding increases payload size significantly

### Recommended Improvements
- Add persistent database (PostgreSQL or SQLite)
- Implement file-based media storage with cloud backup
- Add user authentication and session management
- Implement proper error handling and logging
- Add environment-based configuration

## Development Setup

The application runs as a single FastAPI process that serves both the API and static frontend files. No separate frontend build process is required - changes to HTML/CSS/JS are immediately reflected.

## Deployment

Currently designed for single-instance deployment where FastAPI serves both the GraphQL API at `/graphql` and the React frontend at the root path. Static files are served directly from the `app/ui` directory.

For production deployment, consider:
- Separating API and frontend serving
- Adding reverse proxy (nginx)
- Implementing proper HTTPS termination
- Adding health checks and monitoring