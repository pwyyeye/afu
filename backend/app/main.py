from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.session import engine, Base
from app.api.v1.router import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="阿福健康 API",
    description="AI健康助手后端服务",
    version="0.1.0",
    debug=settings.DEBUG,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
def root():
    return {"name": "阿福健康 API", "version": "0.1.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
