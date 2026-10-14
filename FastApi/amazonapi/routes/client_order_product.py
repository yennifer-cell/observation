from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from prisma import Json

from db import Prisma
from seed import PENDING_STATUS
from auth import get_current_member
from routes.client_order import calculate_order_total

router = APIRouter()


class CLIENT_ORDER_PRODUCT_SCHEMA(BaseModel):
    product_id: str
    qty: int = Field(default=1, gt=0)


@router.post("/", status_code=201)
async def upsert_product(
    payload: CLIENT_ORDER_PRODUCT_SCHEMA,
    current_member=Depends(get_current_member),
):
    
    product = await Prisma.product.find_unique(where={
        "identity": payload.product_id,
    })
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    client_order = await Prisma.client_order.find_first(
        where={
            "member_id": current_member.identity,
            "client_order_status_id": PENDING_STATUS["identity"],
        }
    )

    if not client_order:
        client_order = await Prisma.client_order.create(
            data={
                "member_obj": Json({
                    "identity": current_member.identity,
                    "name": current_member.name,
                    "email": current_member.email,
                }),
                "member": {
                    "connect": {"identity": current_member.identity},
                },
                "client_order_status": {
                    "connect": {"identity": PENDING_STATUS["identity"]},
                },
            }
        )

    qty = payload.qty
    unit_selling_price = product.selling_price
    unit_buying_price = product.buying_price

    client_order_product = await Prisma.client_order_product.find_first(
        where={
            "client_order_id": client_order.identity,
            "product_id": product.identity,
        }
    )

    if client_order_product:
        client_order_product = await Prisma.client_order_product.update(
            where={"identity": client_order_product.identity},
            data={
                "client_order_id": client_order.identity,
                "product_id": product.identity,
                "qty": qty,
                "unit_selling_price": unit_selling_price,
                "unit_buying_price": unit_buying_price,
                "total_selling_price": unit_selling_price * qty,
                "total_buying_price": unit_buying_price * qty,
                "updated_at": datetime.now(timezone.utc),
            },
        )
    else:
        client_order_product = await Prisma.client_order_product.create(
            data={
                "client_order_id": client_order.identity,
                "product_id": product.identity,
                "qty": qty,
                "unit_selling_price": unit_selling_price,
                "unit_buying_price": unit_buying_price,
                "total_selling_price": unit_selling_price * qty,
                "total_buying_price": unit_buying_price * qty,
            }
        )
        
    updated_client_order= await calculate_order_total(client_order_id=client_order.id)    

    return {
        "message":"carts updated successfully",
        "client_order":client_order,
        "client_order_product":client_order_product,
        "updated_client_order":updated_client_order
        
    }
