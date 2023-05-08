from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List


class Todo(BaseModel):
    name: str
    description: str
    status: str


class UpdateTodo(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


app = FastAPI(title="TodoList API")

# temporary storage
storage = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


# GET
@app.get("/get-all-tasks/", response_model=List[Todo])
async def get_all_tasks():
    return storage


@app.get("/get-by-id/{id}")
async def get_task(id: int):
    # avoiding error
    try:
        return storage[id]
    except LookupError:
        raise HTTPException(status_code=404, detail="id not found")


@app.get("/get-by-name")
async def get_task(name: str):
    for i in storage:
        if i.name == name:
            return i
    return {"Data": "Not found"}


# POST
@app.post("/create-todo/")
async def create_todo(todo: Todo):
    storage.append(todo)
    return todo


# PUT
@app.put("/update-task/{id}")
async def update_task(id: int, todo: UpdateTodo):
    try:
        if todo.name is not None:
            storage[id].name = todo.name

        if todo.description is not None:
            storage[id].description = todo.description

        if todo.status is not None:
            storage[id].status = todo.status

        return storage[id]
    except LookupError:
        raise HTTPException(status_code=404, detail="id not found")


# DELETE
@app.delete("/delete/{id}")
async def delete_task(id: int):
    try:
        obj = storage.pop(id)
        return "this object id is" + " " + str(id), obj
    except LookupError:
        raise HTTPException(status_code=404, detail="id not found")
