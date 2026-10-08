from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, EmailStr
import bcrypt

router = APIRouter()

from app import Prisma


class MemberSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup", status_code=status.HTTP_201_CREATED)
@router.post("/sign-up", status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def sign_up(payload: MemberSchema):
    existing = await Prisma.member.find_unique(
        where={"email": payload.email}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already in use"
        )

    async with Prisma.tx() as tx:
        member = await tx.member.create(
            data={
                "name": payload.name,
                "email": payload.email
            }
        )

        user_pass = payload.password
        password_bytes = user_pass.encode("utf-8")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

        await tx.member_password.create(
            data={
                "member_id": member.identity,
                "password": password_hash
            }
        )

    return {
        "message": "Signup successful",
        "member": {
            "identity": member.identity,
            "name": member.name,
            "email": member.email,
        },
    }



@router.post("/login", status_code=status.HTTP_200_OK)
async def login(payload: LoginSchema):

    member = await Prisma.member.find_unique(
        where={"email": payload.email},
        include={
            "member_password": True
        }
    )

    if not member or not member.member_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    hashed_password = member.member_password.password.encode('utf-8')
    user_password = payload.password.encode('utf-8')

    if not bcrypt.checkpw(user_password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {
        "message": "Login successful",
        "member": {
            "identity": member.identity,
            "name": member.name,
            "email": member.email,
        },
    }