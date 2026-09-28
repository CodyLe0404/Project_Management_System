import os
from pathlib import Path
import configparser

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config.ini"


def _load_config() -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    if CONFIG_PATH.exists():
        parser.read(CONFIG_PATH)
    return parser


def get_database_config() -> dict[str, str]:
    config = _load_config()
    section = config["DATABASE"] if config.has_section("DATABASE") else {}

    return {
        "server": os.getenv("DB_SERVER", section.get("server", "localhost")),
        "database": os.getenv("DB_NAME", section.get("database", "master")),
        "username": os.getenv("DB_USERNAME", section.get("username", "")),
        "password": os.getenv("DB_PASSWORD", section.get("password", "")),
        "port": os.getenv("DB_PORT", section.get("port", "1433")),
    }


def get_file_upload_directory() -> Path:
    config = _load_config()
    section = config["FILE_STORAGE"] if config.has_section("FILE_STORAGE") else {}
    configured_path = os.getenv(
        "FCOST_UPLOAD_DIRECTORY",
        section.get("upload_directory", r"D:\Workplace\03_Testing\PM_System\Failure_Cost_File"),
    )
    return Path(configured_path)


def get_api_base_url() -> str:
    config = _load_config()
    section = config["API"] if config.has_section("API") else {}
    return os.getenv("API_BASE_URL", section.get("link_access", "")).rstrip("/")
