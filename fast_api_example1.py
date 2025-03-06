
""" very simple FastAPI example"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

items = []

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

