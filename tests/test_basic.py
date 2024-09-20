import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from fastapi_simple_bearer import FSB, FSBToken


@pytest.fixture(scope="function")
def client():
    app = FastAPI()

    fsb = FSB("SECRET_TOKEN")

    @app.get("/secure")
    async def secure(auth: FSBToken = Depends(fsb)):
        return {"token": auth.token}

    client = TestClient(app)
    return client


async def test_basic(client):
    response = client.get("/secure", headers={"Authorization": "Bearer SECRET_TOKEN"})
    assert response.status_code == 200
    assert response.json() == {"token": "SECRET_TOKEN"}


async def test_invalid_token(client):
    response = client.get("/secure", headers={"Authorization": "Bearer INVALID_TOKEN"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


async def test_invalid_header(client):
    response = client.get("/secure", headers={"Authorization": "INVALID_TOKEN"})
    assert response.status_code == 403
    print(response.json())
    assert response.json() == {"detail": "Not authenticated"}


async def test_no_header(client):
    response = client.get("/secure")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
