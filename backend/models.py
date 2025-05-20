from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Report(BaseModel):
    machine_id: str
    os: str
    disk_encrypted: bool
    os_updated: bool
    antivirus_present: bool
    sleep_configured: bool
    timestamp: Optional[datetime] = None
