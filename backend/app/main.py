from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import models
from app.database import engine
from app.router import router

# declare app
app = FastAPI()


@app.on_event('startup')
def startup_event():
    """
    Create tables on app start.
    """
    models.Base.metadata.create_all(bind=engine)


# Allow cors requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount buy endpoints to /api/*
app.include_router(router, prefix='/api')
