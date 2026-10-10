
from datetime import datetime,timezone
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from db import Prisma

router = APIRouter()

#post
#create the routes for the following:
#put<update.product.info>
#delete<>
#get.product.by.id
#get.all.products
class ProductSchema(BaseModel):
    description: Optional[str] = None
    selling_price: float=0.0
    buying_price: float=0.0
    qty: int=1

class updateProductSchema(BaseModel):
    description: Optional[str] = None
    selling_price: Optional[float] = None
    buying_price: Optional[float] = None
    qty: Optional[int] = None

@router.post("/", status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def add_product(payload: ProductSchema):
    
    new_product = await Prisma.product.create(data={
        "description": payload.description,
        "selling_price": payload.selling_price,
        "buying_price": payload.buying_price,
        "qty": payload.qty
    })
    
    return {"message": "New item added", "product": new_product}

@router.put("/{product_id}", status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def update_product(product_id: str, payload: updateProductSchema):
    
    existing_product = await Prisma.product.find_unique(where={
        "identity": product_id})
    
    if not existing_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
        
    update_data=payload.model_dump(exclude_unset=True) #to remove null values from the payload and only update the fields that are provided in the request.
    
    update_data["updated_at"]=datetime.now(timezone.utc)
    updated_product = await Prisma.product.update(
        where={"identity": product_id},
        data={
            **update_data
        }
    )
    
    return {"message": "Product updated", "product": updated_product}

@router.get("/{product_id}")
async def get_by_id(product_id: str):
    
        product = await Prisma.product.find_unique(where={
        "identity": product_id
        })
   
        if not product:
           raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

        return product
    
@router.get("/")
async def get_all_products():
    
        products = await Prisma.product.find_many()
   
        return products
    
    
@router.delete("/{product_id}")
async def delete_product(product_id: str):
    
        product = await Prisma.product.find_unique(where={
        "identity": product_id
        })
   
        if not product:
           raise HTTPException(
            status_code=404,
            detail="Product to delete not found"
        )

        await Prisma.product.delete(where={"identity": product_id})
        return {"message": "Product deleted successfully"}