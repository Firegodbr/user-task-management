from fastapi.routing import APIRouter
from fastapi import Depends, UploadFile, File, HTTPException, status
from pathlib import Path
import uuid
from app.core.security import verify_csrf
from app.core.settings import settings
from magika import Magika
from app.utils.auth import get_admin_user
from app.models.user import User as UserModel
from app.db.db import get_session
from app.db.user import get_users
from app.api.schema.admin import UsersResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
router = APIRouter(tags=["Admin"])
magika = Magika()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_TYPES = {
    "text/csv",
    "application/vnd.ms-excel",  # .xls
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
}


def get_csrf_dependency():
    """Return CSRF dependency only in production"""
    if settings.ENV == "production":
        return Depends(verify_csrf)
    return None

@router.post("/upload", dependencies=[dep for dep in [get_csrf_dependency(), Depends(get_admin_user)] if dep is not None])
async def upload_excel(current_user: Annotated[UserModel, Depends(get_admin_user)], file: UploadFile = File(...)):
    # Read file bytes
    file_bytes = await file.read()

    # Detect file type using Magika
    result = magika.identify_bytes(file_bytes)

    # Check if Magika analysis was successful
    if not result.ok:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to analyze file type: {result.status.message if hasattr(result.status, 'message') else 'Unknown error'}"
        )

    detected_type = result.output.mime_type
    confidence = result.score  # Use result.score instead of result.output.confidence

    # Validate type
    if detected_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Only Excel and CSV files are allowed. Detected: {detected_type}"
        )

    # Optional: confidence check
    if confidence < 0.9:
        raise HTTPException(
            status_code=400,
            detail="Low confidence file type detection"
        )

    # Generate safe filename
    suffix = Path(file.filename).suffix
    safe_name = f"{uuid.uuid4()}{suffix}"

    file_path = UPLOAD_DIR / safe_name
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return {
        "original_filename": file.filename,
        "saved_as": safe_name,
        "mime_type": detected_type,
        "confidence": confidence,
        "status": "saved"
    }

@router.get("/users", response_model=UsersResponse)
async def get_all_users(current_user: Annotated[UserModel, Depends(get_admin_user)], db: AsyncSession = Depends(get_session)):
    try:
        users = await get_users(db)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    return UsersResponse(users=users, success=True)