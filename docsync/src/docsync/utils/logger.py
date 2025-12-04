import logging
from rich.logging import RichHandler

def setup_logger(name: str = "docsync", level: int = logging.INFO) -> logging.Logger:
    """Configura e retorna um logger com RichHandler.
    
    Args:
        name: Nome do logger
        level: Nível de log
        
    Returns:
        Logger configurado
    """
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger(name)
