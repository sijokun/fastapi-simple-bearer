import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from fastapi_simple_bearer import FSB, FSBToken

tokens = ["TOKEN1", "TOKEN2", "TOKEN3"]


@pytest.fixture(scope="function")
def client():
    app = FastAPI()

    fsb = FSB(token=tokens)

    @app.get("/secure")
    async def secure(auth: FSBToken = Depends(fsb)):
        return {"token": auth.token}

    client = TestClient(app)
    return client


@pytest.mark.parametrize("token", tokens)
async def test_tokens(client, token):
    response = client.get("/secure", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"token": token}
