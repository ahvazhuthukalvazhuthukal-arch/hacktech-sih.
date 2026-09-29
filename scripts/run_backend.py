"""
KalaiPaalam AI - Server Runner Script
Starts the FastAPI application with Uvicorn.
Serves both REST API and Interactive Web/Mobile PWA at http://localhost:8000
"""

import sys
import os
import uvicorn

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.getenv("PORT", 8040))
    print("=" * 70)
    print(f"Starting KalaiPaalam AI Backend & Interactive Console on port {port}...")
    print("Problem Statement: SIH26090 • Heritage & Culture")
    print(f"Web Console URL: http://localhost:{port}")
    print(f"Swagger API Docs: http://localhost:{port}/docs")
    print("=" * 70)
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
