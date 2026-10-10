
from datetime import datetime, timezone
from fastapi import APIRouter, status, Request, HTTPException, Form, UploadFile, File
from pydantic import BaseModel, EmailStr
from typing import Optional
from db import Prisma
from pathlib import Path
import shutil
from datetime import datetime, timezone
from routes.cloud import upload_to_cloud
from uuid import UUID

router = APIRouter()

UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", status_code=201)
async def upload_file(
    product_id: UUID = Form(...),
    document: UploadFile = File(...)
):
    product_id_value = str(product_id)
    print(f"received file for product id {product_id_value}")

    product = await Prisma.product.find_unique(
        where={"identity": product_id_value}
    )

    if not product:
        raise HTTPException(
            status_code=400,
            detail=f"Product with id {product_id_value} not found"
        )

    # one.txt
    original_file = Path(document.filename)
    f_name = original_file.stem  # one
    f_ext = original_file.suffix  # .txt
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    unique_filename = f"{f_name}_{ts}{f_ext}"

    # one_<ts>.txt
    # unique_filename=f"{ts}_{document.filename}"

    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)

    image_link = upload_to_cloud(file_path=file_path)

    if not image_link:
        raise HTTPException(
            status_code=500,
            detail="Failed to upload image to cloud."
        )

    new_product = await Prisma.product_image.create(
        data={
            "product_id": product_id_value,
            "image": image_link
        }
    )

    return {
        "message": "File received successfully",
        "product_id": product_id_value,
        "filename": unique_filename,
        "saved_path": str(file_path),
        "upload": image_link,
        "new_product_image": new_product
    }