"""
KalaiPaalam AI - Master FastAPI Application Entrypoint
SIH26090: AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans
"""

import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

from app.services.database import init_db
from app.api.products import router as products_router
from app.api.marketplaces import router as marketplaces_router
from app.api.media import router as media_router
from app.api.sync import router as sync_router
from app.api.admin import router as admin_router
from app.api.catalog import router as catalog_router

app = FastAPI(
    title="KalaiPaalam AI",
    description="SIH26090: AI-Driven Market Linkage & Smart Cataloging for Marginalized Artisans",
    version="1.0.0"
)

# Enable CORS for Flutter mobile client, React, and browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount API Routers
app.include_router(products_router)
app.include_router(marketplaces_router)
app.include_router(media_router)
app.include_router(sync_router)
app.include_router(admin_router)
app.include_router(catalog_router)

@app.on_event("startup")
def on_startup():
    """Initializes tables and seeds initial demo data."""
    init_db(seed=True)

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "KalaiPaalam AI Backend",
        "version": "1.0.0",
        "problem_statement": "SIH26090",
        "theme": "Heritage & Culture"
    }

# Serve interactive Web Application console at root
INDEX_HTML_PATH = os.path.join(STATIC_DIR, "index.html")

@app.get("/", response_class=HTMLResponse)
async def serve_interactive_demo():
    if os.path.exists(INDEX_HTML_PATH):
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>KalaiPaalam AI Backend Running</h1><p>Visit /docs for API documentation.</p>")
