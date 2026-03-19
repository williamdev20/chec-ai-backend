from fastapi import APIRouter, UploadFile, File, HTTPException
from io import BytesIO
from app.services.check_poster_service import check_poster

router = APIRouter()

@router.post("/check")
async def check_fake_news(img: UploadFile = File(...)):
    img_bytes = await img.read()
    if len(img_bytes) > 50 * 1024 * 1024:  # 50MB
        raise HTTPException(status_code=413, detail="Tamanho da imagem é maior que 50MB")

    img_stream = BytesIO(img_bytes)

    result = check_poster(img_stream)

    return {"is_real": result}