import os

import uvicorn
import json
from fastapi import FastAPI, Depends
from datetime import datetime

from starlette.requests import Request

from app.routes.api_message import app_message
from app.utils.constants import get_file_path
from app.utils.helper_langchain import validate_token

app = FastAPI()

app.include_router(
    app_message,
    prefix='/api',
    dependencies=[Depends(validate_token)],
)

with open(get_file_path("templates", "openapi.json")) as json_file:
    custom_openapi = json.load(json_file)
app.openapi_schema = custom_openapi


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=3000, reload=True)
