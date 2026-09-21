from __future__ import annotations

from typing import Any, Callable


class FcostDataBuilder:
    """Build the complete Failure Cost common-data response from existing queries."""

    _CONDITIONS = {
        "departments": "All_Departments",
        "errorCatalogRows": "Error_Catalog",
        "analysis4m": "4M",
        "projects": "All_Projects",
        "users": "All_Users",
        "errorList": "Error_List",
    }

    def __init__(self, fetch_condition: Callable[[str], list[dict[str, Any]]]) -> None:
        self.fetch_condition = fetch_condition

    def build(self) -> dict[str, Any]:
        data = {
            key: self.fetch_condition(condition)
            for key, condition in self._CONDITIONS.items()
        }

        data["errorCatalogs"] = self._group_error_catalogs(data.pop("errorCatalogRows"))
        return data

    @staticmethod
    def _group_error_catalogs(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in rows or []:
            department_id = row.get("departmentId")
            if department_id is None:
                continue
            grouped.setdefault(str(department_id), []).append(row)
        return grouped
