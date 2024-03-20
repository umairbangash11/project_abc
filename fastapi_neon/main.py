from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated, List
#from fastapi_neon import DATABASE_URL 
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends, HTTPException, Query
# from models import TodoCreate, TodoRead, TodoUpdate, Todo, TodoBase
from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

class TodoBase(SQLModel):
    content: str = Field(index=True)

class Todo(TodoBase, table=True):
     id:int | None = Field(default=None, primary_key=True)

class TodoCreate(TodoBase):
     pass

class TodoRead(TodoBase):
    id: int

class TodoUpdate(SQLModel):
     content:str | None = None
     id: int | None = None

# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://localost:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

def get_session():
    with Session(engine) as session:
        yield session


@app.post("/todos/", response_model=TodoRead)
def create_todo(todo: TodoCreate, session: Annotated[Session, Depends(get_session)]):
        db_todo = Todo.model_validate(todo)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

@app.get("/todos/", response_model=List[TodoRead])
async def read_todos(session: Annotated = Depends(get_session), offset: int = 0, limit: int = Query(default=10, le=10)):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos

@app.get("/todos/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
        todo = session.get(Todo, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, todo: TodoUpdate, session: Annotated[Session, Depends(get_session)]):
        db_todo = session.get(Todo, todo_id)
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo_data = todo.model_dump(exclude_unset=True)
        db_todo.sqlmodel_update(todo_data)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int, session: Annotated = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    await session.commit()
    return {"message": "Todo deleted successfully"}