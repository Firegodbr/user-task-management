from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from loguru import logger
from app.db.db import create_db, engine
from app.api.routes.task import router as task_router
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router
from contextlib import asynccontextmanager
from app.core.settings import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting server")
    if settings.ENV != "test":
        await create_db()
    yield
    logger.info("Stopping server")
    await engine.dispose()


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="User task management API",
              docs_url="/docs", redoc_url="/redocs", lifespan=lifespan)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root_call():
    return RedirectResponse("/docs")
app.include_router(task_router, prefix="/tasks")
app.include_router(auth_router, prefix="/auth")
app.include_router(admin_router, prefix="/admin")


