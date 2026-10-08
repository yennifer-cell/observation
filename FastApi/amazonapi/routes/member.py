from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, EmailStr, Field
import bcrypt

router = APIRouter()
Prisma = None


def get_prisma():
    global Prisma
    if Prisma is None:
        from app import Prisma as app_prisma

        Prisma = app_prisma
    return Prisma


class MemberSchema(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(payload: MemberSchema):
    db = get_prisma()

    clean_name = payload.name.strip()
    if not clean_name:
        raise HTTPException(status_code=400, detail="Name is required")

    normalized_email = payload.email.lower()
    existing = await db.member.find_unique(where={"email": normalized_email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    async with db.tx() as tx:
        member = await tx.member.create(
            data={"name": clean_name, "email": normalized_email}
        )
        password_hash = bcrypt.hashpw(
            payload.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        await tx.member_password.create(
            data={"member_id": member.identity, "password": password_hash}
        )

        return {
            "message": "user signup",
            "member": {
                "identity": member.identity,
                "name": member.name,
                "email": member.email,
            },
        }