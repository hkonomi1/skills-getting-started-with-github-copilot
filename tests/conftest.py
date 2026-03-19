from fastapi.testclient import TestClient
import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = app_module.create_initial_activities()
    yield
    app_module.activities = app_module.create_initial_activities()


@pytest.fixture
def client():
    return TestClient(app_module.app)