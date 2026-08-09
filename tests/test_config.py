import os
import sys
import importlib
import pytest
from pathlib import Path

@pytest.fixture(autouse=True)
def cleanup_config(monkeypatch):
    # Before each test, clear the config module from sys.modules and clean environment
    monkeypatch.delenv("VERCEL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    if "app.core.config" in sys.modules:
        del sys.modules["app.core.config"]
    yield
    # After each test, restore standard local environment and reload config cleanly
    monkeypatch.delenv("VERCEL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    if "app.core.config" in sys.modules:
        del sys.modules["app.core.config"]
    import app.core.config

def test_local_config(monkeypatch):
    # Ensure VERCEL is not in env
    monkeypatch.delenv("VERCEL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    
    import app.core.config
    
    assert app.core.config.IS_VERCEL is False
    assert "sqlite" in app.core.config.settings.DATABASE_URL
    assert app.core.config.UPLOAD_DIR.name == "uploads"
    assert app.core.config.UPLOAD_DIR.parent.name == "static"

def test_vercel_config_missing_db_url(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    
    with pytest.raises(RuntimeError) as exc_info:
        import app.core.config
    
    assert "DATABASE_URL environment variable is missing on Vercel deployment" in str(exc_info.value)

def test_vercel_config_with_postgres_url(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@host:5432/dbname")
    
    import app.core.config
    
    assert app.core.config.IS_VERCEL is True
    assert app.core.config.UPLOAD_DIR == Path("/tmp/atscope_uploads")
    assert app.core.config.settings.DATABASE_URL == "postgresql+psycopg://user:pass@host:5432/dbname"

def test_vercel_config_with_postgresql_url(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host:5432/dbname")
    
    import app.core.config
    
    assert app.core.config.settings.DATABASE_URL == "postgresql+psycopg://user:pass@host:5432/dbname"
