import uvicorn
from fastapi import FastAPI
from cam_server import router

app = FastAPI()

app.include_router(router.router)


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
