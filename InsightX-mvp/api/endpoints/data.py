# api/endpoints/data.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy import create_engine, text
import pandas as pd
import os
from ..workers.tasks import ingest_sales_task

router = APIRouter()

@router.post("/sales/csv")
async def upload_sales_csv(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    contents = await file.read()
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as f:
        f.write(contents)
    # enqueue background ingestion
    ingest_sales_task.delay(tmp_path)
    return {"status":"ingest_queued", "file": file.filename}
