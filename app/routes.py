# routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from io import BytesIO
from app.services.check_poster_service import check_poster
import uuid
import asyncio

router = APIRouter()

jobs = {}

@router.post("/start-check")
async def start_check(img: UploadFile = File(...)):
    img_bytes = await img.read()
    print(f"[DEBUG] Tamanho recebido: {len(img_bytes)} bytes")
    print(f"[DEBUG] Content-type: {img.content_type}")
    print(f"[DEBUG] Filename: {img.filename}")

    if len(img_bytes) > 50 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Tamanho da imagem é maior que 50MB")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "result": None}

    img_stream = BytesIO(img_bytes)

    asyncio.create_task(run_job(job_id, img_stream))

    return {"job_id": job_id}


async def run_job(job_id: str, img_stream: BytesIO):
    try:
        result = await run_in_threadpool(check_poster, img_stream)
        jobs[job_id] = {"status": "done", "result": result}
    except Exception as e:
        jobs[job_id] = {"status": "error", "result": str(e)}


@router.get("/check/{job_id}")
async def get_result(job_id: str):
    job = jobs.get(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job não encontrado")

    return job