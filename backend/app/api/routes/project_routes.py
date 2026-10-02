import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse

from app.api.dependencies import get_project_service
from app.core.exceptions import ServiceError
from app.models.schemas import ChangePasswordRequest, DeleteRowRequest, InsertRowRequest, LoginRequest, ProjectItemUpdate, ProjectPayload, FailureCostResponse
from app.services.project_service import ProjectService
from app.utils.file_attachments import resolve_stored_attachment

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/testconnection")
def test_connection(service: ProjectService = Depends(get_project_service)) -> dict[str, str]:
    try:
        service.get_project_details()
        return {"status": "success", "message": "Connected to SQL Server Express successfully!"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(exc)}") from exc


@router.post("/projects")
def create_project(payload: ProjectPayload, service: ProjectService = Depends(get_project_service)) -> dict[str, object]:
    try:
        return service.create_project(payload.model_dump(), payload.general.get("userId", ""))
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.get("/projects/details")
def get_project_details(service: ProjectService = Depends(get_project_service)) -> list[dict]:
    return service.get_project_details()


@router.get("/projects/summary")
def get_project_summary(service: ProjectService = Depends(get_project_service)) -> dict[str, int]:
    return service.get_project_summary()


@router.post("/project-items/delete")
def delete_project_row(payload: DeleteRowRequest, service: ProjectService = Depends(get_project_service)) -> dict[str, object]:
    return service.delete_project_row(payload.item_ids, payload.user_id)


@router.post("/project-items/insert")
def insert_project_row(payload: list[InsertRowRequest], service: ProjectService = Depends(get_project_service)) -> dict[str, object]:
    return service.insert_project_row([item.model_dump() for item in payload], payload)


@router.put("/project-items/bulk-update")
def bulk_update(items: list[ProjectItemUpdate], service: ProjectService = Depends(get_project_service)) -> dict[str, object]:
    return service.bulk_update([item.model_dump() for item in items])


@router.post("/Common/Login")
def login(request: LoginRequest, service: ProjectService = Depends(get_project_service)) -> dict[str, object]:
    try:
        return service.login(request.userId, request.password)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.post("/changeuserpw")
def change_user_password(request: ChangePasswordRequest, service: ProjectService = Depends(get_project_service)) -> dict[str, object]:
    try:
        return service.change_user_password(request.userId, request.currentPassword, request.newPassword)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.get("/kpi/personal")
def get_personal_kpi(service: ProjectService = Depends(get_project_service)) -> dict:
    return service.get_personal_kpi_data()


@router.get("/kpi/dept")
def get_dept_kpi(service: ProjectService = Depends(get_project_service)) -> dict:
    return service.get_dept_kpi_data()


@router.get("/dashboard/summary")
def get_dashboard_data(service: ProjectService = Depends(get_project_service)) -> dict:
    return service.get_dashboard_data()


@router.get("/dashboard/itemmissing")
def get_item_missing_assignee(service: ProjectService = Depends(get_project_service)) -> list:
    return service.get_item_missing_data()


@router.post("/fcost/commondata")
def get_fcost_common_data(payload: FailureCostResponse, service: ProjectService = Depends(get_project_service)) -> dict | list:
    return service.get_common_data_fcost(payload)


@router.post("/fcost/createlistitem")
async def create_fcost_list(request: Request, service: ProjectService = Depends(get_project_service)) -> dict:
    uploads = []
    if request.headers.get("content-type", "").startswith("multipart/form-data"):
        form = await request.form()
        raw_payload = form.get("payload")
        if not isinstance(raw_payload, str):
            raise HTTPException(status_code=400, detail="Multipart request must include a JSON 'payload' field.")
        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail="The 'payload' field must contain valid JSON.") from exc
        uploads = [value for key, value in form.multi_items() if key == "files" and hasattr(value, "filename")]
    else:
        payload = await request.json()

    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="Failure cost payload must be a JSON object.")
    result = await service.create_failure_cost_list(payload, uploads)
    return result


@router.get("/fcost/attachments/{stored_name}")
def download_fcost_attachment(stored_name: str, download_name: str | None = None) -> FileResponse:
    file_path = resolve_stored_attachment(stored_name)
    if file_path is None:
        raise HTTPException(status_code=404, detail="Attachment not found.")
    safe_download_name = Path(download_name or file_path.name).name
    return FileResponse(file_path, filename=safe_download_name)


@router.put("/fcost/editerrorlist")
async def update_fcost_list(request: Request, service: ProjectService = Depends(get_project_service)) -> dict:
    uploads = []
    if request.headers.get("content-type", "").startswith("multipart/form-data"):
        form = await request.form()
        raw_payload = form.get("payload")
        if not isinstance(raw_payload, str):
            raise HTTPException(status_code=400, detail="Multipart request must include a JSON 'payload' field.")
        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail="The 'payload' field must contain valid JSON.") from exc
        uploads = [value for key, value in form.multi_items() if key == "files" and hasattr(value, "filename")]
    else:
        payload = await request.json()

    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="Failure cost payload must be a JSON object.")
    return await service.update_failure_cost_list(payload, uploads)


@router.put("/fcost/delerroritem")
def remove_fcost_item(payload: dict, service: ProjectService = Depends(get_project_service)) -> dict:
    return service.remove_failure_cost_item(payload)


@router.post("/projects/commondata")
def get_project_common_data(payload: FailureCostResponse, service: ProjectService = Depends(get_project_service)) -> dict | list:
    return service.get_common_data_project(payload)


