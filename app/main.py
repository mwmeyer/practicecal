from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import items, users

import strawberry

from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)


app = FastAPI()


app.include_router(users.router)
app.include_router(items.router)

app.include_router(graphql_app, prefix="/graphql")

app.mount("/", StaticFiles(directory="app/ui", html=True), name="ui")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
