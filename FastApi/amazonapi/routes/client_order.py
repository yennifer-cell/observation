

from datetime import datetime, timezone
from fastapi import APIRouter, status, Request, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from db import prisma
from auth import get_current_member
from seed import PENDING_STATUS
from prisma import Json

router = APIRouter()


async def calculate_order_total(client_order_id):
    client_order = await prisma.client_order.find_unique(
        where={
            "id": client_order_id
        }
    )

    if not client_order:
        raise HTTPException(status_code=404, detail="client order not found")

    group_results = await prisma.client_order_product.group_by(
        by=["client_order_id"],
        where={
            "client_order_id": client_order_id
        },
        sum={
            "total_selling_price": True,
            "total_buying_price": True
        }
    )

    total_selling_price = 0
    total_buying_price = 0

    if group_results:
        sum_results = group_results[0].get("_sum") or {}
        total_selling_price = float(sum_results.get("total_selling_price") or 0)
        total_buying_price = float(sum_results.get("total_buying_price") or 0)

    total_profit = total_selling_price - total_buying_price

    updated_client_order = await prisma.client_order.update(
        where={
            "id": client_order_id
        },
        data={
            "total_selling_price": total_selling_price,
            "total_buying_price": total_buying_price,
            "total_profit": total_profit,
            "updated_at": datetime.now(timezone.utc)
        },
        include={
            "client_order_status": True,
            "client_order_product": {
                "include": {
                    "product": True
                }
            }
        }
    )

    return updated_client_order


@router.get("/active-order", status_code=200)
async def get_active_order(current_member=Depends(get_current_member)):
    client_order = await prisma.client_order.find_first(
        where={
            "member_id": current_member.id,
            "client_order_status_id": PENDING_STATUS["id"]
        }
    )

    client_order = await calculate_order_total(client_order.id)
    return {"message": "", "data": client_order}


@router.get("/{client_order_id}", status_code=200)
async def get_client_order_by_id(client_order_id: str):
    client_order = await calculate_order_total(client_order_id)
    return {"message": "", "data": client_order}

