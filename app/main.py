from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime, date, timedelta
import strawberry
from strawberry.fastapi import GraphQLRouter


# In-memory storage for practice sessions
practice_sessions_storage = [
    {
        "id": 1,
        "instrument": "Guitar",
        "date": "2024-01-15",
        "duration_minutes": 30,
        "notes": "Worked on scales and chord progressions",
        "week_start": "2024-01-14"  # Sunday of that week
    },
    {
        "id": 2,
        "instrument": "Piano",
        "date": "2024-01-16",
        "duration_minutes": 45,
        "notes": "Bach Invention No. 1 - slow practice",
        "week_start": "2024-01-14"
    },
    {
        "id": 3,
        "instrument": "Guitar",
        "date": "2024-01-17",
        "duration_minutes": 25,
        "notes": "Song practice - Hotel California intro",
        "week_start": "2024-01-14"
    }
]

next_session_id = 4


def get_week_start(date_str: str) -> str:
    """Get the Sunday date for the week containing the given date"""
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    days_since_sunday = target_date.weekday() + 1  # Monday is 0, so Sunday is -1, but we want Sunday as 0
    if days_since_sunday == 7:  # Sunday
        days_since_sunday = 0
    week_start = target_date - timedelta(days=days_since_sunday)
    return week_start.strftime("%Y-%m-%d")


@strawberry.type
class PracticeSession:
    id: int
    instrument: str
    date: str  # YYYY-MM-DD format
    duration_minutes: int
    notes: Optional[str]
    week_start: str


@strawberry.type
class WeeklyPractice:
    week_start: str  # Sunday date in YYYY-MM-DD format
    instrument: str
    sessions: List[PracticeSession]
    total_minutes: int


@strawberry.type
class DayPractice:
    date: str
    day_name: str  # Sunday, Monday, etc.
    sessions: List[PracticeSession]
    total_minutes: int


@strawberry.input
class CreatePracticeSessionInput:
    instrument: str
    date: str
    duration_minutes: int
    notes: Optional[str] = None


@strawberry.input
class UpdatePracticeSessionInput:
    id: int
    instrument: Optional[str] = None
    date: Optional[str] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Welcome to PracticeProgress - Your Music Learning Tracker!"

    @strawberry.field
    def practice_sessions_for_week(self, week_start: str, instrument: Optional[str] = None) -> WeeklyPractice:
        """Get all practice sessions for a specific week and instrument"""
        sessions = []
        total_minutes = 0

        for session_data in practice_sessions_storage:
            session_matches = session_data["week_start"] == week_start
            if instrument:
                session_matches = session_matches and session_data["instrument"].lower() == instrument.lower()

            if session_matches:
                session = PracticeSession(
                    id=session_data["id"],
                    instrument=session_data["instrument"],
                    date=session_data["date"],
                    duration_minutes=session_data["duration_minutes"],
                    notes=session_data["notes"],
                    week_start=session_data["week_start"]
                )
                sessions.append(session)
                total_minutes += session_data["duration_minutes"]

        return WeeklyPractice(
            week_start=week_start,
            instrument=instrument or "All Instruments",
            sessions=sessions,
            total_minutes=total_minutes
        )

    @strawberry.field
    def practice_sessions_by_day(self, week_start: str, instrument: Optional[str] = None) -> List[DayPractice]:
        """Get practice sessions organized by day for a specific week"""
        week_start_date = datetime.strptime(week_start, "%Y-%m-%d").date()
        day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        daily_practice = []

        for i in range(7):  # 7 days in a week
            current_date = week_start_date + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")
            day_name = day_names[i]

            # Find sessions for this day
            day_sessions = []
            total_minutes = 0

            for session_data in practice_sessions_storage:
                session_matches = session_data["date"] == date_str
                if instrument:
                    session_matches = session_matches and session_data["instrument"].lower() == instrument.lower()

                if session_matches:
                    session = PracticeSession(
                        id=session_data["id"],
                        instrument=session_data["instrument"],
                        date=session_data["date"],
                        duration_minutes=session_data["duration_minutes"],
                        notes=session_data["notes"],
                        week_start=session_data["week_start"]
                    )
                    day_sessions.append(session)
                    total_minutes += session_data["duration_minutes"]

            daily_practice.append(DayPractice(
                date=date_str,
                day_name=day_name,
                sessions=day_sessions,
                total_minutes=total_minutes
            ))

        return daily_practice

    @strawberry.field
    def available_instruments(self) -> List[str]:
        """Get list of instruments that have been used in practice sessions"""
        instruments = set()
        for session in practice_sessions_storage:
            instruments.add(session["instrument"])
        return sorted(list(instruments))

    @strawberry.field
    def current_week_start(self) -> str:
        """Get the Sunday date for the current week"""
        today = date.today()
        days_since_sunday = (today.weekday() + 1) % 7  # Convert to Sunday=0 system
        week_start = today - timedelta(days=days_since_sunday)
        return week_start.strftime("%Y-%m-%d")


@strawberry.type
class Mutation:
    @strawberry.field
    def create_practice_session(self, input: CreatePracticeSessionInput) -> PracticeSession:
        global next_session_id

        week_start = get_week_start(input.date)

        new_session = {
            "id": next_session_id,
            "instrument": input.instrument,
            "date": input.date,
            "duration_minutes": input.duration_minutes,
            "notes": input.notes,
            "week_start": week_start
        }

        practice_sessions_storage.append(new_session)

        session = PracticeSession(
            id=next_session_id,
            instrument=input.instrument,
            date=input.date,
            duration_minutes=input.duration_minutes,
            notes=input.notes,
            week_start=week_start
        )

        next_session_id += 1
        return session

    @strawberry.field
    def update_practice_session(self, input: UpdatePracticeSessionInput) -> Optional[PracticeSession]:
        session_data = next((s for s in practice_sessions_storage if s["id"] == input.id), None)
        if not session_data:
            return None

        # Update fields if provided
        if input.instrument is not None:
            session_data["instrument"] = input.instrument
        if input.date is not None:
            session_data["date"] = input.date
            session_data["week_start"] = get_week_start(input.date)
        if input.duration_minutes is not None:
            session_data["duration_minutes"] = input.duration_minutes
        if input.notes is not None:
            session_data["notes"] = input.notes

        return PracticeSession(
            id=session_data["id"],
            instrument=session_data["instrument"],
            date=session_data["date"],
            duration_minutes=session_data["duration_minutes"],
            notes=session_data["notes"],
            week_start=session_data["week_start"]
        )

    @strawberry.field
    def delete_practice_session(self, id: int) -> bool:
        global practice_sessions_storage
        session = next((s for s in practice_sessions_storage if s["id"] == id), None)
        if not session:
            return False

        original_length = len(practice_sessions_storage)
        practice_sessions_storage = [s for s in practice_sessions_storage if s["id"] != id]

        return len(practice_sessions_storage) < original_length


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(graphql_app, prefix="/graphql")

app.mount("/", StaticFiles(directory="app/ui", html=True), name="ui")


@app.get("/")
async def root():
    return {"message": "Welcome to PracticeProgress - Your Music Learning Tracker!"}
