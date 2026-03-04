from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from database import engine
from models import Base
from routers import auth, campers, parents, groups, medical

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Camp Management System API",
    description="Sprint 1: Core Camp Management Foundation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(campers.router, prefix="/api/campers", tags=["Campers"])
app.include_router(parents.router, prefix="/api/parents", tags=["Parents"])
app.include_router(groups.router, prefix="/api/groups", tags=["Groups"])
app.include_router(medical.router, prefix="/api/medical", tags=["Medical"])

@app.get("/")
async def root():
    return {
        "message": "Camp Management System API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "status": "operational"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "sprint": 1, "timestamp": "2026-02-28"}