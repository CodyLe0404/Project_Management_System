from __future__ import annotations

import json
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import quote

from app.config import get_api_base_url


class AttachmentDataBuilder:
    @staticmethod
    def build_insert_data(error_id: int, metadata: dict[str, Any], created_by: Any) -> dict[str, Any]:
        return {
            "errorId": error_id,
            "fileName": metadata["fileName"],
            "filePath": metadata["filePath"],
            "fileSize": metadata["fileSize"],
            "contentType": metadata["contentType"],
            "createdBy": created_by,
        }

    @classmethod
    def enrich_rows(cls, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        enriched_rows: list[dict[str, Any]] = []
        rows_by_error_id: dict[str, dict[str, Any]] = {}
        for row in rows:
            enriched = cls._enrich_row(row)
            error_id = cls._get_case_insensitive(row, "errorId", "id")
            if error_id is None:
                enriched_rows.append(enriched)
                continue

            key = str(error_id)
            existing = rows_by_error_id.get(key)
            if existing is None:
                rows_by_error_id[key] = enriched
                enriched_rows.append(enriched)
                continue

            known_attachments = {
                (item.get("fileName"), item.get("downloadUrl"), item.get("fileSize"))
                for item in existing["attachments"]
            }
            for attachment in enriched["attachments"]:
                identity = (attachment.get("fileName"), attachment.get("downloadUrl"), attachment.get("fileSize"))
                if identity not in known_attachments:
                    existing["attachments"].append(attachment)
                    known_attachments.add(identity)
        return enriched_rows

    @classmethod
    def _enrich_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        enriched = dict(row)
        attachment_value = cls._get_case_insensitive(row, "attachments", "attachmentList", "files")
        attachments = cls._parse_attachment_value(attachment_value)

        if not attachments:
            file_name = cls._get_case_insensitive(row, "attachmentFileName", "fileName")
            file_path = cls._get_case_insensitive(row, "attachmentFilePath", "filePath")
            if file_name and file_path:
                attachments = [{
                    "fileName": file_name,
                    "filePath": file_path,
                    "fileSize": cls._get_case_insensitive(row, "attachmentFileSize", "fileSize"),
                    "contentType": cls._get_case_insensitive(row, "attachmentContentType", "contentType"),
                }]

        private_fields = {
            "attachments", "attachmentlist", "files", "attachmentfilename", "filename",
            "attachmentfilepath", "filepath", "attachmentfilesize", "filesize",
            "attachmentcontenttype", "contenttype",
        }
        for key in list(enriched):
            if str(key).lower() in private_fields:
                enriched.pop(key)
        enriched["attachments"] = [cls._public_attachment(item) for item in attachments if isinstance(item, dict)]
        return enriched

    @staticmethod
    def _get_case_insensitive(data: dict[str, Any], *names: str) -> Any:
        values = {str(key).lower(): value for key, value in data.items()}
        for name in names:
            if name.lower() in values:
                return values[name.lower()]
        return None

    @classmethod
    def _parse_attachment_value(cls, value: Any) -> list[Any]:
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return [value]
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except (TypeError, ValueError):
                return []
            return parsed if isinstance(parsed, list) else [parsed] if isinstance(parsed, dict) else []
        return []

    @classmethod
    def _public_attachment(cls, attachment: dict[str, Any]) -> dict[str, Any]:
        file_name = cls._get_case_insensitive(attachment, "fileName", "originalFileName", "name")
        file_path = cls._get_case_insensitive(attachment, "filePath", "storedPath")
        stored_name = PurePosixPath(str(file_path or "").replace("\\", "/")).name
        download_url = cls._get_case_insensitive(attachment, "downloadUrl", "url")
        if not download_url and stored_name and file_name:
            download_url = (
                f"{get_api_base_url()}/fcost/attachments/{quote(stored_name)}"
                f"?download_name={quote(str(file_name))}"
            )

        return {
            "fileName": file_name or stored_name,
            "fileSize": cls._get_case_insensitive(attachment, "fileSize", "size"),
            "contentType": cls._get_case_insensitive(attachment, "contentType", "mimeType"),
            "downloadUrl": download_url,
        }