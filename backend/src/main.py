from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from src.utils.settings import get_settings
from time import time
from .routers import auth

settings = get_settings()
app = FastAPI(title="Neural Filter", version="0.1.0")

# =========================================
# Middlewares
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)


@app.middleware("http")
async def add_process_time_header(req: Request, call_next) -> Response:
    start_time = time()
    response = await call_next(req)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# =========================================
# Routes
# =========================================


@app.get("/", tags=["testing"])
async def root():
    return {"message": "Welcome to Neural Filter"}


app.include_router(auth.router)
