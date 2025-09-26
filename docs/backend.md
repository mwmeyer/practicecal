# GraphQL Schema and Data Model Documentation

## Overview

PracticeCal uses GraphQL as its primary API interface, providing a type-safe and flexible way to query and mutate practice session data. The schema is built using Strawberry GraphQL and focuses on practice session management with week-based organization.

## Core Data Types

### PracticeSession

The primary entity representing a single practice session.

```graphql
type PracticeSession {
  id: Int!
  date: String!
  duration_minutes: Int!
  media_data: String
  mime_type: String
}
```

**Fields:**
- `id`: Unique identifier for the session (auto-generated)
- `date`: ISO date string in YYYY-MM-DD format
- `duration_minutes`: Duration of the practice session in minutes
- `media_data`: Base64-encoded audio/video recording (optional)
- `mime_type`: MIME type of the media data (e.g., "audio/webm", "video/mp4")

**Example:**
```json
{
  "id": 1,
  "date": "2024-01-15",
  "duration_minutes": 45,
  "media_data": "data:audio/webm;base64,UklGRnoG...",
  "mime_type": "audio/webm"
}
```

### DayPractice

Aggregated view of all practice sessions for a specific day.

```graphql
type DayPractice {
  date: String!
  day_name: String!
  sessions: [PracticeSession!]!
  total_minutes: Int!
}
```

**Fields:**
- `date`: ISO date string in YYYY-MM-DD format
- `day_name`: Human-readable day name (e.g., "Monday", "Tuesday")
- `sessions`: List of all practice sessions for this day
- `total_minutes`: Sum of duration_minutes for all sessions on this day

**Example:**
```json
{
  "date": "2024-01-15",
  "day_name": "Monday",
  "sessions": [
    {
      "id": 1,
      "date": "2024-01-15",
      "duration_minutes": 30,
      "media_data": null,
      "mime_type": null
    },
    {
      "id": 2,
      "date": "2024-01-15",
      "duration_minutes": 45,
      "media_data": "data:audio/webm;base64,UklGRnoG...",
      "mime_type": "audio/webm"
    }
  ],
  "total_minutes": 75
}
```

### WeeklyPractice

Aggregated view of total practice time for an entire week.

```graphql
type WeeklyPractice {
  total_minutes: Int!
}
```

**Fields:**
- `total_minutes`: Sum of all practice session durations for the week

**Example:**
```json
{
  "total_minutes": 420
}
```

## Input Types

### CreatePracticeSessionInput

Input type for creating new practice sessions.

```graphql
input CreatePracticeSessionInput {
  date: String!
  duration_minutes: Int!
  media_data: String
  mime_type: String
}
```

**Fields:**
- `date`: ISO date string (required)
- `duration_minutes`: Session duration in minutes (required)
- `media_data`: Base64-encoded media (optional)
- `mime_type`: MIME type for media (optional)

**Usage Example:**
```graphql
mutation {
  create_practice_session(input: {
    date: "2024-01-15"
    duration_minutes: 45
    media_data: "data:audio/webm;base64,UklGRnoG..."
    mime_type: "audio/webm"
  }) {
    id
    date
    duration_minutes
  }
}
```

### UpdatePracticeSessionInput

Input type for updating existing practice sessions.

```graphql
input UpdatePracticeSessionInput {
  id: Int!
  duration_minutes: Int!
  media_data: String
  mime_type: String
}
```

**Fields:**
- `id`: ID of the session to update (required)
- `duration_minutes`: New duration in minutes (required)
- `media_data`: New media data or null to remove (optional)
- `mime_type`: New MIME type or null to remove (optional)

**Usage Example:**
```graphql
mutation {
  update_practice_session(input: {
    id: 1
    duration_minutes: 60
    media_data: null
    mime_type: null
  }) {
    id
    duration_minutes
    media_data
  }
}
```

## Query Operations

### current_week_start

Returns the start date (Sunday) of the current week.

```graphql
type Query {
  current_week_start: String!
}
```

**Returns:** ISO date string representing the Sunday of the current week.

**Example Query:**
```graphql
query {
  current_week_start
}
```

**Example Response:**
```json
{
  "data": {
    "current_week_start": "2024-01-14"
  }
}
```

### practice_sessions_by_day

Returns a complete week view with practice sessions organized by day.

```graphql
type Query {
  practice_sessions_by_day(week_start: String!): [DayPractice!]!
}
```

**Parameters:**
- `week_start`: ISO date string for the Sunday of the desired week

**Returns:** Array of 7 DayPractice objects (Sunday through Saturday)

**Example Query:**
```graphql
query {
  practice_sessions_by_day(week_start: "2024-01-14") {
    date
    day_name
    total_minutes
    sessions {
      id
      duration_minutes
      media_data
    }
  }
}
```

**Example Response:**
```json
{
  "data": {
    "practice_sessions_by_day": [
      {
        "date": "2024-01-14",
        "day_name": "Sunday",
        "total_minutes": 0,
        "sessions": []
      },
      {
        "date": "2024-01-15",
        "day_name": "Monday",
        "total_minutes": 45,
        "sessions": [
          {
            "id": 1,
            "duration_minutes": 45,
            "media_data": "data:audio/webm;base64,..."
          }
        ]
      }
      // ... remaining days
    ]
  }
}
```

### practice_sessions_for_week

Returns aggregated practice time for an entire week.

```graphql
type Query {
  practice_sessions_for_week(week_start: String!): WeeklyPractice!
}
```

**Parameters:**
- `week_start`: ISO date string for the Sunday of the desired week

**Returns:** WeeklyPractice object with total minutes

**Example Query:**
```graphql
query {
  practice_sessions_for_week(week_start: "2024-01-14") {
    total_minutes
  }
}
```

**Example Response:**
```json
{
  "data": {
    "practice_sessions_for_week": {
      "total_minutes": 315
    }
  }
}
```

## Mutation Operations

### create_practice_session

Creates a new practice session.

```graphql
type Mutation {
  create_practice_session(input: CreatePracticeSessionInput!): PracticeSession!
}
```

**Parameters:**
- `input`: CreatePracticeSessionInput object with session details

**Returns:** The newly created PracticeSession

**Example:**
```graphql
mutation {
  create_practice_session(input: {
    date: "2024-01-15"
    duration_minutes: 30
  }) {
    id
    date
    duration_minutes
  }
}
```

### update_practice_session

Updates an existing practice session.

```graphql
type Mutation {
  update_practice_session(input: UpdatePracticeSessionInput!): PracticeSession
}
```

**Parameters:**
- `input`: UpdatePracticeSessionInput object with updated session details

**Returns:** The updated PracticeSession or null if not found

**Example:**
```graphql
mutation {
  update_practice_session(input: {
    id: 1
    duration_minutes: 60
  }) {
    id
    duration_minutes
  }
}
```

### delete_practice_session

Deletes a practice session by ID.

```graphql
type Mutation {
  delete_practice_session(id: Int!): Boolean!
}
```

**Parameters:**
- `id`: ID of the session to delete

**Returns:** Boolean indicating success (true) or failure (false)

**Example:**
```graphql
mutation {
  delete_practice_session(id: 1)
}
```

## Data Storage Implementation

### In-Memory Structure

Practice sessions are stored in a global Python list:

```python
sessions = []  # List of dictionaries
next_id = 1    # Auto-incrementing ID counter
```

Each session is stored as a dictionary:
```python
{
    "id": int,
    "date": str,              # "YYYY-MM-DD"
    "duration_minutes": int,
    "media_data": str,        # Base64 string or None
    "mime_type": str          # MIME type or None
}
```

### Week Calculation Logic

The application uses Sunday as the start of the week:

```python
def get_week_start(date_str: str) -> str:
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    days_since_sunday = (target_date.weekday() + 1) % 7
    week_start = target_date - timedelta(days=days_since_sunday)
    return week_start.strftime("%Y-%m-%d")
```

## Media Data Handling

### Format
Media data is stored as Base64-encoded strings with data URI format:
```
data:{mime_type};base64,{base64_data}
```

### Supported MIME Types
- `audio/webm`
- `audio/mp4`
- `video/webm`
- `video/mp4`

### Size Limitations
Base64 encoding increases data size by ~33%. Large media files can significantly impact:
- Memory usage (in-memory storage)
- Network transfer times
- JSON payload sizes

## API Endpoints

### GraphQL Endpoint
- **URL**: `/graphql`
- **Method**: POST
- **Content-Type**: application/json
- **Body**: GraphQL query/mutation

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**: `{"msg": "Hello World"}`

## Error Handling

### GraphQL Errors
- Invalid queries return GraphQL error responses
- Type validation is handled automatically by Strawberry
- Missing required fields result in validation errors

### Application Errors
- Session not found returns `null` for update operations
- Invalid date formats may cause runtime errors
- Media data validation is minimal (accepts any string)

## Performance Considerations

### Query Performance
- All operations are O(n) where n is the number of sessions
- Week queries iterate through all sessions to filter by date
- No indexing or optimization for large datasets

### Memory Usage
- All session data held in memory
- Base64 media encoding increases memory footprint
- No garbage collection of old sessions
