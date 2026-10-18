import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "NEXUS GRAPH AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8080
    HOST: str = "0.0.0.0"
    DEFAULT_TENANT_ID: str = "tenant_nexus_main"

    # Graph DB (FalkorDB)
    FALKORDB_HOST: str = "172.17.109.154"
    FALKORDB_PORT: int = 6379
    FALKORDB_GRAPH_NAME: str = "nexus_company_graph"
    FALKORDB_PASSWORD: str = ""

    # Relational DB
    DATABASE_URL: str = "sqlite+aiosqlite:///./nexus_metadata.db"

    # Caching & Ephemeral
    REDIS_URL: str = "redis://localhost:6380/0"

    # AI Model Strategy
    LLM_PROVIDER: str = "huggingface"  # 'huggingface', 'vllm', 'openai', 'mock'
    MODEL_NAME: str = "Qwen/Qwen2.5-0.5B-Instruct"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    HF_DEVICE: str = "cpu"
    DEVICE_MAP: str = "auto"
    TORCH_DTYPE: str = "float32"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    # Security
    SECRET_KEY: str = "nexus_super_secret_production_key_change_in_real_env_38192849"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Human-in-the-loop Action Approvals
    REQUIRE_HUMAN_APPROVAL_FOR_ACTIONS: bool = True
    AUTO_APPROVE_READONLY: bool = True

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

@lru_cache()
def get_settings() -> Settings:
    return Settings()
