from fastapi import FastAPI
from .database import engine
from . import models
from .routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Live Portfolio Risk Platform")

app.include_router(router)