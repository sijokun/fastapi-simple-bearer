from fastapi import Depends, FastAPI

from fastapi_simple_bearer import FSB, FSBToken

app = FastAPI()

fsb = FSB(token="SECRET_TOKEN")


@app.get("/secure")
async def secure(auth: FSBToken = Depends(fsb)):
    return {"token": auth.token}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("basic:app", host="0.0.0.0", port=8000, reload=True)
