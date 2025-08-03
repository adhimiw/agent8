"""
Configuration management for the Autonomous Personal Assistant.
Handles environment variables, API keys, and application settings.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APISettings(BaseSettings):
    """API configuration settings."""
    
    # Gemini API
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-2.5-flash", env="GEMINI_MODEL")
    gemini_temperature: float = Field(0.7, env="GEMINI_TEMPERATURE")
    gemini_max_tokens: int = Field(8192, env="GEMINI_MAX_TOKENS")
    
    # Perplexity API
    perplexity_api_key: str = Field(..., env="PERPLEXITY_API_KEY")
    perplexity_model: str = Field("sonar-pro", env="PERPLEXITY_MODEL")
    perplexity_temperature: float = Field(0.3, env="PERPLEXITY_TEMPERATURE")
    perplexity_max_tokens: int = Field(4096, env="PERPLEXITY_MAX_TOKENS")
    
    # OpenAI API (Optional)
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4-turbo-preview", env="OPENAI_MODEL")

class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    # ChromaDB
    chroma_db_path: str = Field("./data/chroma_db", env="CHROMA_DB_PATH")
    chroma_collection_name: str = Field("assistant_memory", env="CHROMA_COLLECTION_NAME")
    
    # Redis
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")
    redis_password: Optional[str] = Field(None, env="REDIS_PASSWORD")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    # PostgreSQL
    postgres_host: str = Field("localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("autonomous_assistant", env="POSTGRES_DB")
    postgres_user: str = Field("assistant_user", env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    database_url: str = Field(..., env="DATABASE_URL")

class MCPSettings(BaseSettings):
    """MCP server configuration settings."""
    
    # Memory Server
    memory_server_path: str = Field("./data/memory.json", env="MEMORY_SERVER_PATH")
    memory_server_port: int = Field(3001, env="MEMORY_SERVER_PORT")
    
    # Filesystem Server
    filesystem_server_root: str = Field("./data/workspace", env="FILESYSTEM_SERVER_ROOT")
    filesystem_server_port: int = Field(3002, env="FILESYSTEM_SERVER_PORT")
    
    # Git Server
    git_server_root: str = Field("./data/repositories", env="GIT_SERVER_ROOT")
    git_server_port: int = Field(3003, env="GIT_SERVER_PORT")

class IntegrationSettings(BaseSettings):
    """Third-party service integration settings."""
    
    # Gmail
    gmail_client_id: Optional[str] = Field(None, env="GMAIL_CLIENT_ID")
    gmail_client_secret: Optional[str] = Field(None, env="GMAIL_CLIENT_SECRET")
    gmail_refresh_token: Optional[str] = Field(None, env="GMAIL_REFRESH_TOKEN")
    
    # Google Drive
    drive_client_id: Optional[str] = Field(None, env="DRIVE_CLIENT_ID")
    drive_client_secret: Optional[str] = Field(None, env="DRIVE_CLIENT_SECRET")
    drive_refresh_token: Optional[str] = Field(None, env="DRIVE_REFRESH_TOKEN")
    
    # Google Calendar
    calendar_client_id: Optional[str] = Field(None, env="CALENDAR_CLIENT_ID")
    calendar_client_secret: Optional[str] = Field(None, env="CALENDAR_CLIENT_SECRET")
    calendar_refresh_token: Optional[str] = Field(None, env="CALENDAR_REFRESH_TOKEN")
    
    # Notion
    notion_api_key: Optional[str] = Field(None, env="NOTION_API_KEY")
    notion_database_id: Optional[str] = Field(None, env="NOTION_DATABASE_ID")
    
    # GitHub
    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")
    github_username: Optional[str] = Field(None, env="GITHUB_USERNAME")
    
    # Slack
    slack_bot_token: Optional[str] = Field(None, env="SLACK_BOT_TOKEN")
    slack_app_token: Optional[str] = Field(None, env="SLACK_APP_TOKEN")
    slack_channel_id: Optional[str] = Field(None, env="SLACK_CHANNEL_ID")
    
    # Discord
    discord_bot_token: Optional[str] = Field(None, env="DISCORD_BOT_TOKEN")
    discord_guild_id: Optional[str] = Field(None, env="DISCORD_GUILD_ID")
    discord_channel_id: Optional[str] = Field(None, env="DISCORD_CHANNEL_ID")

class ApplicationSettings(BaseSettings):
    """Application configuration settings."""
    
    # Environment
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    
    # Web Interface
    streamlit_port: int = Field(8501, env="STREAMLIT_PORT")
    fastapi_port: int = Field(8000, env="FASTAPI_PORT")
    web_host: str = Field("localhost", env="WEB_HOST")
    
    # Autonomous Agent
    autonomous_mode: bool = Field(True, env="AUTONOMOUS_MODE")
    proactive_monitoring: bool = Field(True, env="PROACTIVE_MONITORING")
    trigger_check_interval: int = Field(60, env="TRIGGER_CHECK_INTERVAL")
    max_autonomous_actions_per_hour: int = Field(10, env="MAX_AUTONOMOUS_ACTIONS_PER_HOUR")

class FeatureFlags(BaseSettings):
    """Feature flag settings."""
    
    enable_email_processing: bool = Field(True, env="ENABLE_EMAIL_PROCESSING")
    enable_calendar_integration: bool = Field(True, env="ENABLE_CALENDAR_INTEGRATION")
    enable_github_monitoring: bool = Field(True, env="ENABLE_GITHUB_MONITORING")
    enable_slack_notifications: bool = Field(True, env="ENABLE_SLACK_NOTIFICATIONS")
    enable_notion_sync: bool = Field(True, env="ENABLE_NOTION_SYNC")
    enable_voice_interface: bool = Field(False, env="ENABLE_VOICE_INTERFACE")
    enable_mobile_notifications: bool = Field(False, env="ENABLE_MOBILE_NOTIFICATIONS")

class MonitoringSettings(BaseSettings):
    """Monitoring and logging settings."""
    
    # Sentry
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN")
    
    # Prometheus
    prometheus_port: int = Field(9090, env="PROMETHEUS_PORT")
    enable_metrics: bool = Field(True, env="ENABLE_METRICS")
    
    # Logging
    log_file_path: str = Field("./logs/assistant.log", env="LOG_FILE_PATH")
    log_rotation_size: str = Field("10MB", env="LOG_ROTATION_SIZE")
    log_retention_days: int = Field(30, env="LOG_RETENTION_DAYS")

class RateLimitSettings(BaseSettings):
    """Rate limiting and quota settings."""
    
    # API Rate Limits (requests per minute)
    gemini_rate_limit: int = Field(60, env="GEMINI_RATE_LIMIT")
    perplexity_rate_limit: int = Field(20, env="PERPLEXITY_RATE_LIMIT")
    gmail_rate_limit: int = Field(100, env="GMAIL_RATE_LIMIT")
    notion_rate_limit: int = Field(30, env="NOTION_RATE_LIMIT")
    
    # Daily Quotas
    max_daily_api_calls: int = Field(1000, env="MAX_DAILY_API_CALLS")
    max_daily_emails_processed: int = Field(500, env="MAX_DAILY_EMAILS_PROCESSED")
    max_daily_autonomous_actions: int = Field(50, env="MAX_DAILY_AUTONOMOUS_ACTIONS")

class Settings(BaseSettings):
    """Main settings class that combines all configuration."""
    
    # Sub-settings
    api: APISettings = APISettings()
    database: DatabaseSettings = DatabaseSettings()
    mcp: MCPSettings = MCPSettings()
    integrations: IntegrationSettings = IntegrationSettings()
    app: ApplicationSettings = ApplicationSettings()
    features: FeatureFlags = FeatureFlags()
    monitoring: MonitoringSettings = MonitoringSettings()
    rate_limits: RateLimitSettings = RateLimitSettings()
    
    # Project paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "logs")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    @validator('project_root', 'data_dir', 'logs_dir', pre=True)
    def ensure_path(cls, v):
        if isinstance(v, str):
            return Path(v)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings

def reload_settings() -> Settings:
    """Reload settings from environment."""
    global settings
    settings = Settings()
    return settings
