from pathlib import Path, PurePosixPath
from uuid import uuid4

from fastapi import UploadFile

from app.config import get_file_upload_directory


async def save_attachment(upload: UploadFile) -> dict[str, str | int | None]:
    upload_directory = get_file_upload_directory()
    upload_directory.mkdir(parents=True, exist_ok=True)

    original_name = PurePosixPath((upload.filename or "attachment").replace("\\", "/")).name
    suffix = Path(original_name).suffix[:20]
    stored_name = f"{uuid4().hex}{suffix}"
    file_path = upload_directory / stored_name

    try:
        with file_path.open("wb") as destination:
            while chunk := await upload.read(1024 * 1024):
                destination.write(chunk)
    except Exception:
        file_path.unlink(missing_ok=True)
        raise

    return {
        "fileName": original_name,
        "filePath": str(file_path.resolve()),
        "fileSize": file_path.stat().st_size,
        "contentType": upload.content_type,
        "storedName": stored_name,
    }


def resolve_stored_attachment(stored_name: str) -> Path | None:
    if not stored_name or Path(stored_name).name != stored_name:
        return None

    upload_directory = get_file_upload_directory().resolve()
    file_path = (upload_directory / stored_name).resolve()
    if file_path.parent != upload_directory or not file_path.is_file():
        return None
    return file_path

