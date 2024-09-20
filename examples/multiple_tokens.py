from fastapi import Depends, FastAPI

from fastapi_simple_bearer import FSB, FSBToken

app = FastAPI()

fsb = FSB(token=["TOKEN1", "TOKEN2", "TOKEN3"])


@app.get("/secure")
async def secure(auth: FSBToken = Depends(fsb)):
    return {"token": auth.token}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("multiple_tokens:app", host="0.0.0.0", port=8000, reload=True)
