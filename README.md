# FastAPI Simple Bearer (FSB)
This library provides you with ability to secure your endpoints with preset token (or tokens) in the "Authorization: Bearer" header

## Installation

The easiest way to start working with this library is to install it from pip

`pip install fastapi-simple-bearer`

## Example of usage
Basic usage:
```python
from fastapi import Depends, FastAPI
from fastapi_simple_bearer import FSB, FSBToken

app = FastAPI()

fsb = FSB(token="SUPER_SECRET_TOKEN")

@app.get("/secure")
async def secure(auth: FSBToken = Depends(fsb)):
    return {"token": auth.token}

```
Other examples are available in [examples](examples) folder