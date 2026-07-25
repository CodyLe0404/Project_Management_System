from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.dependencies import get_project_service
from app.core.exceptions import ServiceError
from app.models.schemas import ChangePasswordRequest, DeleteRowRequest, InsertRowRequest, LoginRequest, ProjectItemUpdate, ProjectPayload
from app.services.project_service import ProjectService

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


@router.get("/kpi/summary")
def get_kpi_summary(service: ProjectService = Depends(get_project_service)) -> list[dict]:
    return service.get_kpi_summary()
