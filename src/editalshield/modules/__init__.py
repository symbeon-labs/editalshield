"""
EditalShield Modules
"""

from .memorial_protector import MemorialProtector, MemorialAnalysis, ParagraphAnalysis
from .edital_matcher import EditalMatcher, MatchResult
from .juridical_agent import JuridicalAgent, LegalOpinion

__all__ = [
    'MemorialProtector', 'MemorialAnalysis', 'ParagraphAnalysis',
    'EditalMatcher', 'MatchResult',
    'JuridicalAgent', 'LegalOpinion'
]
