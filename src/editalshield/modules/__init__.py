"""
EditalShield Modules
"""

from .memorial_protector import MemorialProtector, MemorialAnalysis, ParagraphAnalysis
from .edital_matcher import EditalMatcher, MatchResult

__all__ = [
    'MemorialProtector', 'MemorialAnalysis', 'ParagraphAnalysis',
    'EditalMatcher', 'MatchResult'
]
