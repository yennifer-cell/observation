from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from orm import inventory
from db import Database

app = FastAPI()


class InventoryItem(BaseModel):
    name: str
    qty: int
    buying_price: int
    selling_price: int


db = Database()
inventory= inventory(db)

@app.get("/inventory")
def list_inventory():
    return inventory.get_all_items()

@app.post("/inventory",status_code=status.HTTP_201_CREATED)
def add_inventory(item: InventoryItem):
    #data verification
    if not item.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item name is required")
    
    new_item = inventory.add_item(
        item.name,
        item.qty,
        item.buying_price,
        item.selling_price,
    )
    
    return {"message": "Item added successfully", "item": new_item}