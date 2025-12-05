"""
EditalShield Modules
"""

from .memorial_protector import MemorialProtector, MemorialAnalysis, ParagraphAnalysis
from .edital_matcher import EditalMatcher, MatchResult
from .juridical_agent import JuridicalAgent, LegalOpinion
from .knowledge_connectors import KnowledgeConnector, ExternalResource

__all__ = [
    'MemorialProtector', 'MemorialAnalysis', 'ParagraphAnalysis',
    'EditalMatcher', 'MatchResult',
    'JuridicalAgent', 'LegalOpinion',
    'KnowledgeConnector', 'ExternalResource'
]
