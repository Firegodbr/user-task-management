from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger
from app.db.db import create_db, engine
from app.api.routes.task import router as task_router
from app.api.routes.user import router as user_router


async def lifespan(app: FastAPI):
    logger.info("Starting server")
    await create_db()
    yield
    logger.info("Stopping server")
    await engine.dispose()


app = FastAPI(title="User task management API",
              docs_url="/docs", redoc_url="/redocs", lifespan=lifespan)


@app.get("/", tags=["Root"])
async def root_call():
    return RedirectResponse("/docs")
app.include_router(task_router, prefix="/tasks")
app.include_router(user_router, prefix="/user")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="server:app", port=8000, host="0.0.0.0", reload=True)
