
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.member import router as member_router
from routes.product import router as product_router
from routes.product_image import router as product_image_router
from routes.client_order_product import router as client_order_product_router
from routes.client_order import router as client_order_router
from db import prisma
from auth import get_current_member
from seed import seed_status


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    await seed_status()
    yield
    await prisma.disconnect()


app = FastAPI(title="Amazon api", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# register router
app.include_router(member_router, prefix="/member")
app.include_router(
    product_router,
    prefix="/product",
    dependencies=[Depends(get_current_member)]
)
app.include_router(
    product_image_router,
    prefix="/product_image",
    dependencies=[Depends(get_current_member)]
)
app.include_router(
    client_order_product_router,
    prefix="/client_order_product",
    dependencies=[Depends(get_current_member)]
)
app.include_router(
    client_order_router,
    prefix="/client_order",
    dependencies=[Depends(get_current_member)]
)


@app.get("/")
async def root():
    members = await prisma.member.find_many()
    print(members)
    return {"message": "API is running"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
        reload_excludes=["uploads/*"]
    )
