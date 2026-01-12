from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from loguru import logger
from app.db.db import create_db, engine
from app.api.routes.task import router as task_router
from app.api.routes.auth import router as auth_router
from contextlib import asynccontextmanager
from app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting server")
    if settings.ENV != "test":
        await create_db()
    yield
    logger.info("Stopping server")
    await engine.dispose()


app = FastAPI(title="User task management API",
              docs_url="/docs", redoc_url="/redocs", lifespan=lifespan)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="server:app", port=8000, host="0.0.0.0", reload=True)
