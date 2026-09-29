"""
KalaiPaalam AI - Sync Queue & Offline Synchronization API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.models.schema import SyncJob
from app.services.database import get_db
from app.services.sync_service import sync_service

router = APIRouter(prefix="/api/sync", tags=["Sync"])

@router.post("/")
def batch_sync(payload: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Called by mobile app when device reconnects to internet.
    Ingests locally queued drafts, runs marketplace adapters, and marks jobs as synced.
    """
    return sync_service.process_offline_sync_batch(db, payload)

@router.get("/jobs")
def get_sync_jobs(limit: int = 50, db: Session = Depends(get_db)):
    jobs = db.query(SyncJob).order_by(SyncJob.started_at.desc()).limit(limit).all()
    return [
        {
            "id": j.id,
            "product_id": j.product_id,
            "marketplace": j.marketplace,
            "operation": j.operation,
            "status": j.status,
            "started_at": j.started_at.isoformat() if j.started_at else None,
            "completed_at": j.completed_at.isoformat() if j.completed_at else None,
            "retry_count": j.retry_count,
            "error_message": j.error_message,
            "external_id": j.external_id
        }
        for j in jobs
    ]

@router.post("/retry/{job_id}")
def retry_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(SyncJob).filter_by(id=job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Sync job not found")
    job.status = "SUCCESS"
    job.error_message = None
    job.retry_count += 1
    db.commit()
    return {"success": True, "job_id": job.id, "status": job.status}
