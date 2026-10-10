from contextlib import asynccontextmanager
from fastapi import FastAPI
import socket
import uvicorn
from db import Prisma
from routes.member import router as member_router
from routes.product import router as product_router
from routes.product_image import router as product_image_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Prisma.connect()
    yield
    await Prisma.disconnect()
    
app=FastAPI(title="AmazonApi", lifespan=lifespan)

#register routers
app.include_router(member_router, prefix="/member")
app.include_router(product_router, prefix="/product")
app.include_router(product_image_router, prefix="/product_image")

@app.get("/")
async def root():
    member=await Prisma.member.find_many()
    print(member)
    return {"message":"API is running"}


def find_available_port(start: int = 8000, end: int = 8100) -> int:
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
                server_socket.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port

    raise RuntimeError(f"No available port found between {start} and {end}")


if __name__=="__main__":
    port = find_available_port()
    print(f"Starting API at http://127.0.0.1:{port}")
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)