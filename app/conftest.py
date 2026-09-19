import pytest
from fastapi.testclient import TestClient

from app.database import engine, Base, get_db
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Crée les tables dans la base de test
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)