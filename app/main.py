from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime, date, timedelta
import strawberry
from strawberry.fastapi import GraphQLRouter

# In-memory storage
sessions = []
next_id = 1

def get_week_start(date_str: str) -> str:
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    days_since_sunday = (target_date.weekday() + 1) % 7
    week_start = target_date - timedelta(days=days_since_sunday)
    return week_start.strftime("%Y-%m-%d")

@strawberry.type
class PracticeSession:
    id: int
    date: str
    duration_minutes: int

@strawberry.type
class DayPractice:
    date: str
    day_name: str
    sessions: List[PracticeSession]
    total_minutes: int

@strawberry.type
class WeeklyPractice:
    total_minutes: int

@strawberry.input
class CreatePracticeSessionInput:
    date: str
    duration_minutes: int

@strawberry.input
class UpdatePracticeSessionInput:
    id: int
    duration_minutes: int

@strawberry.type
class Query:
    @strawberry.field
    def current_week_start(self) -> str:
        today = date.today()
        days_since_sunday = (today.weekday() + 1) % 7
        week_start = today - timedelta(days=days_since_sunday)
        return week_start.strftime("%Y-%m-%d")

    @strawberry.field
    def practice_sessions_by_day(self, week_start: str) -> List[DayPractice]:
        week_start_date = datetime.strptime(week_start, "%Y-%m-%d").date()
        day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        daily_practice = []
        for i in range(7):
            current_date = week_start_date + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")

            day_sessions = []
            total_minutes = 0

            for session in sessions:
                if session["date"] == date_str:
                    day_sessions.append(PracticeSession(
                        id=session["id"],
                        date=session["date"],
                        duration_minutes=session["duration_minutes"]
                    ))
                    total_minutes += session["duration_minutes"]

            daily_practice.append(DayPractice(
                date=date_str,
                day_name=day_names[i],
                sessions=day_sessions,
                total_minutes=total_minutes
            ))

        return daily_practice

    @strawberry.field
    def practice_sessions_for_week(self, week_start: str) -> WeeklyPractice:
        week_start_date = datetime.strptime(week_start, "%Y-%m-%d").date()
        total_minutes = 0

        for i in range(7):
            current_date = week_start_date + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")

            for session in sessions:
                if session["date"] == date_str:
                    total_minutes += session["duration_minutes"]

        return WeeklyPractice(total_minutes=total_minutes)

@strawberry.type
class Mutation:
    @strawberry.field
    def create_practice_session(self, input: CreatePracticeSessionInput) -> PracticeSession:
        global next_id

        new_session = {
            "id": next_id,
            "date": input.date,
            "duration_minutes": input.duration_minutes
        }

        sessions.append(new_session)
        session_obj = PracticeSession(
            id=next_id,
            date=input.date,
            duration_minutes=input.duration_minutes
        )

        next_id += 1
        return session_obj

    @strawberry.field
    def update_practice_session(self, input: UpdatePracticeSessionInput) -> Optional[PracticeSession]:
        for session in sessions:
            if session["id"] == input.id:
                session["duration_minutes"] = input.duration_minutes
                return PracticeSession(
                    id=session["id"],
                    date=session["date"],
                    duration_minutes=session["duration_minutes"]
                )
        return None

    @strawberry.field
    def delete_practice_session(self, id: int) -> bool:
        global sessions
        original_length = len(sessions)
        sessions = [s for s in sessions if s["id"] != id]
        return len(sessions) < original_length

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
app.mount("/", StaticFiles(directory="app/ui", html=True), name="ui")
