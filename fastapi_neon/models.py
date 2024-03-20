from sqlmodel import SQLModel, Field




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