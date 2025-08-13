# api/main.py
from fastapi import FastAPI
from .endpoints import data, auth, reports

app = FastAPI(title="InsightX MVP")

app.include_router(auth.router, prefix="/auth")
app.include_router(data.router, prefix="/ingest")
app.include_router(reports.router, prefix="/reports")
