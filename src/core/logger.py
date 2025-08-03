"""
Logging configuration for the Autonomous Personal Assistant.
Provides structured logging with rich formatting and multiple outputs.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

import structlog
from rich.logging import RichHandler
from rich.console import Console

from config.settings import Settings

def setup_logging(settings: Settings) -> None:
    """Setup comprehensive logging configuration."""
    
    # Ensure logs directory exists
    log_file_path = Path(settings.monitoring.log_file_path)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure standard library logging
    logging.basicConfig(
        level=getattr(logging, settings.monitoring.log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=Console(stderr=True),
                show_time=True,
                show_path=True,
                markup=True,
                rich_tracebacks=True,
                tracebacks_show_locals=settings.app.debug
            )
        ]
    )
    
    # Add file handler for persistent logging
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        maxBytes=_parse_size(settings.monitoring.log_rotation_size),
        backupCount=settings.monitoring.log_retention_days,
        encoding='utf-8'
    )
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
    
    # Get root logger and add file handler
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if not settings.app.debug 
            else structlog.dev.ConsoleRenderer(colors=True)
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Set specific logger levels
    _configure_logger_levels(settings)

def _parse_size(size_str: str) -> int:
    """Parse size string like '10MB' to bytes."""
    size_str = size_str.upper()
    if size_str.endswith('KB'):
        return int(size_str[:-2]) * 1024
    elif size_str.endswith('MB'):
        return int(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024 * 1024 * 1024
    else:
        return int(size_str)

def _configure_logger_levels(settings: Settings) -> None:
    """Configure specific logger levels."""
    
    # Set third-party library log levels
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.INFO)
    logging.getLogger("redis").setLevel(logging.WARNING)
    
    # Set our application loggers
    if settings.app.debug:
        logging.getLogger("autonomous_assistant").setLevel(logging.DEBUG)
    else:
        logging.getLogger("autonomous_assistant").setLevel(logging.INFO)

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)

class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    @property
    def logger(self) -> structlog.BoundLogger:
        """Get a logger instance for this class."""
        return get_logger(self.__class__.__name__)

# Application-specific loggers
def get_orchestrator_logger() -> structlog.BoundLogger:
    """Get logger for orchestrator components."""
    return get_logger("orchestrator")

def get_agent_logger() -> structlog.BoundLogger:
    """Get logger for AI agents."""
    return get_logger("agent")

def get_mcp_logger() -> structlog.BoundLogger:
    """Get logger for MCP components."""
    return get_logger("mcp")

def get_api_logger() -> structlog.BoundLogger:
    """Get logger for API integrations."""
    return get_logger("api")

def get_memory_logger() -> structlog.BoundLogger:
    """Get logger for memory components."""
    return get_logger("memory")

def get_workflow_logger() -> structlog.BoundLogger:
    """Get logger for workflow components."""
    return get_logger("workflow")

def get_security_logger() -> structlog.BoundLogger:
    """Get logger for security components."""
    return get_logger("security")
