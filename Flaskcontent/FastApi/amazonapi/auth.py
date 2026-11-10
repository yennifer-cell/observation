import os

from datetime import datetime, timedelta, timezone

import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from dotenv import load_dotenv

from db import Prisma

load_dotenv()


JWT_SECRET_KEY = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE_MINUTES'))


def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token


# decode and get the information

async def get_current_member(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials

    try:
        decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    member_identity = decoded.get("identity")
    if not member_identity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    member = await Prisma.member.find_unique(
        where={"identity": member_identity}
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Member does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return member