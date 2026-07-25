from collections.abc import Generator

from app.core.database import get_db_connection
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService


def get_project_service() -> Generator[ProjectService, None, None]:
    with get_db_connection() as conn:
        repository = ProjectRepository(conn)
        service = ProjectService(repository)
        yield service
