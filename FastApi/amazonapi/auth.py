import os

from datetime import datetime, timedelta, timezone

import jwt

from dotenv import load_dotenv

load_dotenv() 


def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=int(os.getenv('JWT_EXPIRE_MINUTES')))
    to_encode.update({"exp": expire})
    token=jwt.encode(to_encode, os.getenv('JWT_SECRET'), algorithm=os.getenv('JWT_ALGORITHM'))
    return token