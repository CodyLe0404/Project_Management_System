import logging
from datetime import datetime
from pathlib import Path, PurePosixPath
from uuid import uuid4

from fastapi import UploadFile

from app.config import get_file_upload_directory

logger = logging.getLogger(__name__)


def get_month_upload_directory(now: datetime | None = None) -> Path:
    base_directory = get_file_upload_directory()
    upload_time = now or datetime.now()
    month_directory = base_directory / upload_time.strftime("%Y") / upload_time.strftime("%m")

    try:
        month_directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        logger.exception("Failed to create upload directory: %s", month_directory)
        raise

    return month_directory


async def save_attachment(upload: UploadFile) -> dict[str, str | int | None]:
    original_name = PurePosixPath((upload.filename or "attachment").replace("\\", "/")).name
    suffix = Path(original_name).suffix[:20]
    stored_name = f"{uuid4().hex}{suffix}"
    file_path: Path | None = None

    try:
        upload_directory = get_month_upload_directory()
        file_path = upload_directory / stored_name
        with file_path.open("wb") as destination:
            while chunk := await upload.read(1024 * 1024):
                destination.write(chunk)
    except Exception:
        if file_path is not None:
            file_path.unlink(missing_ok=True)
        logger.exception("Failed to save uploaded attachment: %s", original_name)
        raise

    return {
        "fileName": original_name,
        "filePath": str(file_path.resolve()),
        "fileSize": file_path.stat().st_size,
        "contentType": upload.content_type,
        "storedName": stored_name,
    }


def resolve_stored_attachment(stored_name: str) -> Path | None:
    if not stored_name:
        return None

    normalized_name = PurePosixPath(stored_name.replace("\\", "/")).name
    if normalized_name != stored_name:
        return None

    upload_directory = get_file_upload_directory().resolve()
    file_path = (upload_directory / stored_name).resolve()
    if file_path.parent == upload_directory and file_path.is_file():
        return file_path

    try:
        for candidate in upload_directory.rglob("*"):
            if candidate.name != stored_name:
                continue
            resolved_candidate = candidate.resolve()
            if resolved_candidate.is_relative_to(upload_directory) and resolved_candidate.is_file():
                return resolved_candidate
    except OSError:
        logger.exception("Failed to resolve stored attachment: %s", stored_name)

    return None

