import os

import uvicorn
import json
from fastapi import FastAPI
from datetime import datetime

from starlette.requests import Request

from app.routes.api_message import app_message

app = FastAPI()

app.include_router(
    app_message,
    prefix='/api'
)

if os.environ.get("DOCKER_ENV"):
    # Running in Docker container
    file_path = "/code/app/templates/openapi.json"
else:
    # Running locally
    file_path = "templates/openapi.json"

with open(file_path) as json_file:
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
