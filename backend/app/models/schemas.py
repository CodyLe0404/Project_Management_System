from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel


class ProjectPayload(BaseModel):
    general: dict[str, Any]
    items: list[dict[str, Any]]
    userId: str


class ProjectItemUpdate(BaseModel):
    item_id: int
    main_task: Optional[str] = None
    sub_task: str
    qty: Optional[int] = None
    user_id: str
    assignee: Optional[str] = None
    process: Optional[float] = None
    status: Optional[str] = None
    plan_start: Optional[str] = None
    plan_end: Optional[str] = None
    actual_start: Optional[str] = None
    actual_end: Optional[str] = None
    actual_cost: Optional[float] = None
    remark: Optional[str] = None


class DeleteRowRequest(BaseModel):
    item_ids: str
    user_id: str


class InsertRowRequest(BaseModel):
    user_id: str
    project_id: Optional[str] = None
    task_no: int
    main_task: str
    sub_task: Optional[str] = None
    qty: Optional[int] = None
    budget: Optional[float] = None
    actual_cost: Optional[float] = None
    assignee: Optional[str] = None
    percent: Optional[float] = None
    status: Optional[str] = None
    plan_start: Optional[date] = None
    plan_end: Optional[date] = None
    actual_start: Optional[date] = None
    actual_end: Optional[date] = None
    order_no: Optional[int] = None
    remark: Optional[str] = None


class LoginRequest(BaseModel):
    ldapName: str
    userId: str
    password: str


class ChangePasswordRequest(BaseModel):
    userId: str
    currentPassword: str
    newPassword: str


class UserInfo(BaseModel):
    userId: str
    displayName: str
    email: str
    userConfig: list[str]


class LoginResponse(BaseModel):
    message: str
    setUserInfoStatus: int
    user: UserInfo | None = None


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None
