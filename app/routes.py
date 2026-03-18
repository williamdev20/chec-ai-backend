from fastapi import APIRouter, UploadFile, File
from io import BytesIO
from app.services.check_poster_service import check_poster

router = APIRouter()

@router.post("/check")
async def check_fake_news(img: UploadFile = File(...)):
    img_bytes = await img.read()
    img_stream = BytesIO(img_bytes)

    result = check_poster(img_stream)

    return {"is_real": result}