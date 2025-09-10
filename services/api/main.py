"""
FastAPI application with AI-powered product search and recommendations.
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sys
import os

# Add shared to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from shared.config import api_settings
from shared.database import get_db
from .routers import products, search, ai
from .middleware.logging import setup_logging

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=api_settings.title,
    description=api_settings.description,
    version=api_settings.version,
    debug=api_settings.debug
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])

@app.get("/")
async def root():
    """Health check and API information."""
    return {
        "status": "ok",
        "message": "Welcome to the AI-Powered Supermarket Scraper API!",
        "version": api_settings.version,
        "docs": "/docs",
        "features": [
            "Product search with AI",
            "Vector similarity search", 
            "Hybrid text + semantic search",
            "Product recommendations",
            "Multi-supermarket support"
        ]
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Comprehensive health check."""
    from shared.database import test_connection
    from shared.ai.embeddings.generator import embedding_generator
    
    db_status = "ok" if test_connection() else "error"
    ai_status = "ok" if embedding_generator.is_available() else "unavailable"
    
    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "database": db_status,
        "ai_embeddings": ai_status,
        "timestamp": "2025-09-10T19:10:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=api_settings.host,
        port=api_settings.port,
        reload=api_settings.debug
    )
