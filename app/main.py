from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime

import strawberry

from strawberry.fastapi import GraphQLRouter


# In-memory storage (replace with database in production)
boards_storage = [
    {"id": 1, "name": "My First Board"},
    {"id": 2, "name": "Personal Tasks"}
]

lists_storage = [
    {"id": 1, "name": "To Do", "board_id": 1, "position": 0},
    {"id": 2, "name": "In Progress", "board_id": 1, "position": 1},
    {"id": 3, "name": "Done", "board_id": 1, "position": 2},
    {"id": 4, "name": "Backlog", "board_id": 2, "position": 0},
    {"id": 5, "name": "Current", "board_id": 2, "position": 1}
]

cards_storage = [
    {"id": 1, "title": "Buy milk", "description": "Get organic milk from the store", "list_id": 1, "position": 0, "due_date": None},
    {"id": 2, "title": "Read a book", "description": "Finish reading 'Clean Code'", "list_id": 1, "position": 1, "due_date": "2024-01-15"},
    {"id": 3, "title": "Write documentation", "description": "Complete API documentation", "list_id": 2, "position": 0, "due_date": None},
    {"id": 4, "title": "Exercise", "description": "30 minutes workout", "list_id": 5, "position": 0, "due_date": None}
]

next_board_id = 3
next_list_id = 6
next_card_id = 5


@strawberry.type
class Card:
    id: int
    title: str
    description: Optional[str]
    list_id: int
    position: int
    due_date: Optional[str]


@strawberry.type
class BoardList:
    id: int
    name: str
    board_id: int
    position: int
    cards: List[Card]


@strawberry.type
class Board:
    id: int
    name: str
    lists: List[BoardList]


@strawberry.input
class CreateBoardInput:
    name: str


@strawberry.input
class CreateListInput:
    name: str
    board_id: int = strawberry.field(name="boardId")


@strawberry.input
class CreateCardInput:
    title: str
    description: Optional[str] = None
    list_id: int = strawberry.field(name="listId")
    due_date: Optional[str] = strawberry.field(name="dueDate", default=None)


@strawberry.input
class MoveCardInput:
    card_id: int = strawberry.field(name="cardId")
    target_list_id: int = strawberry.field(name="targetListId")
    position: int


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello Trello-like Board!"

    @strawberry.field
    def boards(self) -> List[Board]:
        result = []
        for board_data in boards_storage:
            # Get lists for this board
            board_lists = []
            for list_data in sorted([l for l in lists_storage if l["board_id"] == board_data["id"]], key=lambda x: x["position"]):
                # Get cards for this list
                list_cards = []
                for card_data in sorted([c for c in cards_storage if c["list_id"] == list_data["id"]], key=lambda x: x["position"]):
                    list_cards.append(Card(
                        id=card_data["id"],
                        title=card_data["title"],
                        description=card_data["description"],
                        list_id=card_data["list_id"],
                        position=card_data["position"],
                        due_date=card_data["due_date"]
                    ))

                board_lists.append(BoardList(
                    id=list_data["id"],
                    name=list_data["name"],
                    board_id=list_data["board_id"],
                    position=list_data["position"],
                    cards=list_cards
                ))

            result.append(Board(
                id=board_data["id"],
                name=board_data["name"],
                lists=board_lists
            ))
        return result

    @strawberry.field
    def board(self, id: int) -> Optional[Board]:
        board_data = next((board for board in boards_storage if board["id"] == id), None)
        if not board_data:
            return None

        # Get lists for this board
        board_lists = []
        for list_data in sorted([l for l in lists_storage if l["board_id"] == board_data["id"]], key=lambda x: x["position"]):
            # Get cards for this list
            list_cards = []
            for card_data in sorted([c for c in cards_storage if c["list_id"] == list_data["id"]], key=lambda x: x["position"]):
                list_cards.append(Card(
                    id=card_data["id"],
                    title=card_data["title"],
                    description=card_data["description"],
                    list_id=card_data["list_id"],
                    position=card_data["position"],
                    due_date=card_data["due_date"]
                ))

            board_lists.append(BoardList(
                id=list_data["id"],
                name=list_data["name"],
                board_id=list_data["board_id"],
                position=list_data["position"],
                cards=list_cards
            ))

        return Board(
            id=board_data["id"],
            name=board_data["name"],
            lists=board_lists
        )


@strawberry.type
class Mutation:
    @strawberry.field
    def create_board(self, input: CreateBoardInput) -> Board:
        global next_board_id
        new_board = {"id": next_board_id, "name": input.name}
        boards_storage.append(new_board)

        board = Board(id=next_board_id, name=input.name, lists=[])
        next_board_id += 1
        return board

    @strawberry.field
    def create_list(self, input: CreateListInput) -> BoardList:
        global next_list_id
        # Find the next position for this board
        board_lists = [l for l in lists_storage if l["board_id"] == input.board_id]
        next_position = len(board_lists)

        new_list = {
            "id": next_list_id,
            "name": input.name,
            "board_id": input.board_id,
            "position": next_position
        }
        lists_storage.append(new_list)

        board_list = BoardList(
            id=next_list_id,
            name=input.name,
            board_id=input.board_id,
            position=next_position,
            cards=[]
        )
        next_list_id += 1
        return board_list

    @strawberry.field
    def create_card(self, input: CreateCardInput) -> Card:
        global next_card_id
        # Find the next position for this list
        list_cards = [c for c in cards_storage if c["list_id"] == input.list_id]
        next_position = len(list_cards)

        new_card = {
            "id": next_card_id,
            "title": input.title,
            "description": input.description,
            "list_id": input.list_id,
            "position": next_position,
            "due_date": input.due_date
        }
        cards_storage.append(new_card)

        card = Card(
            id=next_card_id,
            title=input.title,
            description=input.description,
            list_id=input.list_id,
            position=next_position,
            due_date=input.due_date
        )
        next_card_id += 1
        return card

    @strawberry.field
    def move_card(self, input: MoveCardInput) -> bool:
        # Find the card
        card = next((c for c in cards_storage if c["id"] == input.card_id), None)
        if not card:
            return False

        old_list_id = card["list_id"]

        # Update card's list and position
        card["list_id"] = input.target_list_id
        card["position"] = input.position

        # Reorder positions in the old list
        old_list_cards = [c for c in cards_storage if c["list_id"] == old_list_id and c["id"] != input.card_id]
        for i, c in enumerate(sorted(old_list_cards, key=lambda x: x["position"])):
            c["position"] = i

        # Reorder positions in the new list
        new_list_cards = [c for c in cards_storage if c["list_id"] == input.target_list_id]
        new_list_cards.sort(key=lambda x: x["position"])

        # Insert the moved card at the specified position
        for i, c in enumerate(new_list_cards):
            if c["id"] == input.card_id:
                continue
            if i >= input.position:
                c["position"] = i + 1

        return True

    @strawberry.field
    def delete_card(self, id: int) -> bool:
        global cards_storage
        card = next((c for c in cards_storage if c["id"] == id), None)
        if not card:
            return False

        list_id = card["list_id"]
        original_length = len(cards_storage)
        cards_storage = [c for c in cards_storage if c["id"] != id]

        # Reorder remaining cards in the list
        list_cards = [c for c in cards_storage if c["list_id"] == list_id]
        for i, c in enumerate(sorted(list_cards, key=lambda x: x["position"])):
            c["position"] = i

        return len(cards_storage) < original_length

    @strawberry.field
    def delete_list(self, id: int) -> bool:
        global lists_storage, cards_storage
        list_data = next((l for l in lists_storage if l["id"] == id), None)
        if not list_data:
            return False

        board_id = list_data["board_id"]

        # Delete all cards in this list
        cards_storage = [c for c in cards_storage if c["list_id"] != id]

        # Delete the list
        original_length = len(lists_storage)
        lists_storage = [l for l in lists_storage if l["id"] != id]

        # Reorder remaining lists in the board
        board_lists = [l for l in lists_storage if l["board_id"] == board_id]
        for i, l in enumerate(sorted(board_lists, key=lambda x: x["position"])):
            l["position"] = i

        return len(lists_storage) < original_length

    @strawberry.field
    def delete_board(self, id: int) -> bool:
        global boards_storage, lists_storage, cards_storage
        board = next((b for b in boards_storage if b["id"] == id), None)
        if not board:
            return False

        # Get all list IDs for this board
        board_list_ids = [l["id"] for l in lists_storage if l["board_id"] == id]

        # Delete all cards in all lists of this board
        cards_storage = [c for c in cards_storage if c["list_id"] not in board_list_ids]

        # Delete all lists in this board
        lists_storage = [l for l in lists_storage if l["board_id"] != id]

        # Delete the board
        original_length = len(boards_storage)
        boards_storage = [b for b in boards_storage if b["id"] != id]

        return len(boards_storage) < original_length


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(graphql_app, prefix="/graphql")

app.mount("/", StaticFiles(directory="app/ui", html=True), name="ui")


@app.get("/")
async def root():
    return {"message": "Welcome to your Trello-like Board App!"}
