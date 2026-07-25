from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.project_routes import router
from app.core.middleware import register_request_logging

app = FastAPI(title="Project Management Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://10.13.227.253:8000",
        "http://10.13.227.253:80",
        "http://10.13.227.253",
        "http://localhost:8000",
        "http://10.13.227.119:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_request_logging(app)
app.include_router(router)
