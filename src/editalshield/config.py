"""Configurações globais do EditalShield.

Este módulo contém configurações padrão e caminhos para recursos do framework.
Todas as configurações são genéricas e parametrizáveis.
"""

from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente se existir arquivo .env
load_dotenv()

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).parent.parent.parent

# Diretórios de recursos
SRC_DIR = ROOT_DIR / "src" / "editalshield"
DATA_DIR = SRC_DIR / "data"
TEMPLATES_DIR = SRC_DIR / "templates"
EXAMPLES_DIR = ROOT_DIR / "examples"
DOCS_DIR = ROOT_DIR / "docs"

# Arquivos de dados
EDITAIS_DATA_FILE = DATA_DIR / "editais_brasil.json"
CRITERIOS_DATA_FILE = DATA_DIR / "criterios_padrao.json"
KEYWORDS_DATA_FILE = DATA_DIR / "trade_secrets_keywords.json"
FORMULAS_DATA_FILE = DATA_DIR / "formulas.json"

# Configurações padrão
DEFAULT_CONFIG: Dict[str, Any] = {
    "sensitivity_levels": {
        "low": {"threshold": 30, "keywords_weight": 0.3},
        "medium": {"threshold": 20, "keywords_weight": 0.5},
        "high": {"threshold": 10, "keywords_weight": 0.7},
    },
    "nda_defaults": {
        "confidencialidade_anos": 5,
        "multa_min": 250000,
        "multa_max": 500000,
        "jurisdicao": "Salvador, BA",
    },
    "cost_calculator": {
        "default_parcelas": 3,
        "default_glosa_estimada": 0,
    },
    "edital_selector": {
        "max_results": 10,
        "min_fit_score": 50,
    },
}

# Configurações de output
OUTPUT_FORMATS = ["json", "markdown", "html", "pdf"]
DEFAULT_OUTPUT_FORMAT = "markdown"

# Logging
LOG_LEVEL = os.getenv("EDITALSHIELD_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_config(key: str, default: Any = None) -> Any:
    """Obtém valor de configuração.

    Args:
        key: Chave de configuração (pode usar notação de ponto, ex: 'nda_defaults.multa_min')
        default: Valor padrão se chave não existir

    Returns:
        Valor da configuração ou default
    """
    keys = key.split(".")
    value = DEFAULT_CONFIG

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value


def validate_paths() -> bool:
    """Valida se diretórios essenciais existem.

    Returns:
        True se todos os diretórios existem, False caso contrário
    """
    required_dirs = [DATA_DIR, TEMPLATES_DIR]

    for directory in required_dirs:
        if not directory.exists():
            return False

    return True
