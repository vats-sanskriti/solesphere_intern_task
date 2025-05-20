from fastapi import FastAPI, Request
from models import Report
from database import reports
from datetime import datetime
from fastapi.responses import StreamingResponse
import pandas as pd

app = FastAPI()

@app.post("/api/report")
async def receive_report(report: Report):
    report.timestamp = datetime.utcnow()
    await reports.insert_one(report.dict())
    return {"message": "Report received"}

@app.get("/api/machines")
async def list_machines(os: str = None, issues: bool = False):
    query = {}
    if os:
        query["os"] = os
    if issues:
        query["$or"] = [
            {"disk_encrypted": False},
            {"os_updated": False},
            {"antivirus_present": False},
            {"sleep_configured": False}
        ]
    cursor = reports.aggregate([
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$machine_id",
            "latest": {"$first": "$$ROOT"}
        }},
        {"$replaceRoot": {"newRoot": "$latest"}}
    ])
    data = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        data.append(doc)
    return data

@app.get("/api/export")
async def export_csv():
    cursor = reports.find()
    all_reports = []
    async for doc in cursor:
        doc.pop("_id")
        all_reports.append(doc)
    df = pd.DataFrame(all_reports)
    stream = df.to_csv(index=False)
    return StreamingResponse(
        iter([stream]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=reports.csv"}
    )
