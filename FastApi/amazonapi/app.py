from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from prisma import Prisma

Prisma=Prisma()

from routes.member import router as member_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Prisma.connect()
    yield
    await Prisma.disconnect()
    
app=FastAPI(title="AmazonApi", lifespan=lifespan)

#register routers
app.include_router(member_router, prefix="/member")

@app.get("/")
async def root():
    member=await Prisma.member.find_many()
    print(member)
    return {"message":"API is running"}

if __name__=="__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)