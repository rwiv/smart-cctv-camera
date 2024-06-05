import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cam_server import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(router.router)


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
