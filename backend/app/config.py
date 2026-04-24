import os


def _db_url() -> str:
    url = os.environ.get("DATABASE_URL", "sqlite:///taskflow.db")
    # Render (and some other platforms) still emit the legacy postgres:// scheme;
    # SQLAlchemy 1.4+ requires postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    SQLALCHEMY_DATABASE_URI = _db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    # Restrict CORS in production — set to your frontend URL
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
