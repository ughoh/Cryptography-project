import uvicorn
from fastapi import FastAPI
from app.api import router_v1

app = FastAPI()
app.include_router(router_v1)


if __name__ == "__main__":
    uvicorn.run("main:app")
