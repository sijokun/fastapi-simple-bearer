from fastapi import Depends, FastAPI

from fastapi_simple_bearer import FSB, FSBToken

app = FastAPI()

fsb1 = FSB(token="TOKEN1")
fsb2 = FSB(token="TOKEN2")


@app.get("/secure1")
async def secure1(auth: FSBToken = Depends(fsb1)):
    return "TOKEN1 was used"


@app.get("/secure2")
async def secure2(auth: FSBToken = Depends(fsb2)):
    return "TOKEN2 was used"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("different_scopes:app", host="0.0.0.0", port=8000, reload=True)
