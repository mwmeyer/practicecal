from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import List, Optional

import strawberry

from strawberry.fastapi import GraphQLRouter


# In-memory storage for todos (replace with database in production)
todos_storage = [
    {"id": 1, "task": "Buy milk"},
    {"id": 2, "task": "Read a book"}
]
next_todo_id = 3


@strawberry.type
class Todo:
    id: int
    task: str


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

    @strawberry.field
    def todos(self) -> List[Todo]:
        return [Todo(id=todo["id"], task=todo["task"]) for todo in todos_storage]

    @strawberry.field
    def todo(self, id: int) -> Optional[Todo]:
        todo_data = next((todo for todo in todos_storage if todo["id"] == id), None)
        return Todo(id=todo_data["id"], task=todo_data["task"]) if todo_data else None


@strawberry.type
class Mutation:
    @strawberry.field
    def add_todo(self, task: str) -> Todo:
        global next_todo_id
        new_todo = {"id": next_todo_id, "task": task}
        todos_storage.append(new_todo)
        todo = Todo(id=next_todo_id, task=task)
        next_todo_id += 1
        return todo

    @strawberry.field
    def delete_todo(self, id: int) -> bool:
        global todos_storage
        original_length = len(todos_storage)
        todos_storage = [todo for todo in todos_storage if todo["id"] != id]
        return len(todos_storage) < original_length


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(graphql_app, prefix="/graphql")

app.mount("/", StaticFiles(directory="app/ui", html=True), name="ui")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
