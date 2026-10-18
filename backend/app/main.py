import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.routes import api_router
from app.graph.service import get_graph_service

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("nexus.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode...")
    # Initialize graph service and verify seeding
    graph_svc = get_graph_service()
    stats = graph_svc.get_stats()
    logger.info(f"FalkorDB status: {stats['engine_mode']} | Nodes: {stats['total_nodes']} | Edges: {stats['total_edges']}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous Company Intelligence, Graph Reasoning, Persistent Memory, and Multi-Agent Coordination",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local Next.js frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
