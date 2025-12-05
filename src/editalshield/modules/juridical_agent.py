"""
EditalShield - Juridical Agent (Module 5)
Translates technical IP risks into legal context based on Brazilian LPI (Lei 9.279/96).
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from .memorial_protector import MemorialAnalysis

@dataclass
class LegalCitation:
    law: str = "LPI (Lei 9.279/96)"
    article: str = ""
    description: str = ""
    implication: str = ""

@dataclass
class LegalOpinion:
    status: str
    risk_level: str
    citations: List[LegalCitation]
    recommendation: str

class JuridicalAgent:
    """
    AI Agent that interprets technical analysis through the lens of Intellectual Property Law.
    """
    
    def __init__(self):
        self.knowledge_base = {
            'novelty_loss': LegalCitation(
                article="Art. 12",
                description="A invenção não é considerada nova se compreendida no estado da técnica.",
                implication="Divulgar detalhes técnicos publicamente (no edital) destrói a novidade, impedindo patenteamento futuro."
            ),
            'trade_secret': LegalCitation(
                article="Art. 195, XI",
                description="Crime de concorrência desleal: divulgar, explorar ou utilizar-se de conhecimentos confidenciais.",
                implication="A exposição deste conteúdo no edital pode configurar vazamento de segredo de negócio, sem proteção legal automática."
            ),
            'software_protection': LegalCitation(
                article="Lei 9.609/98 (Lei de Software)",
                description="O regime de proteção à propriedade intelectual de programa de computador é o conferido às obras literárias.",
                implication="O código-fonte é protegido por direito autoral, mas a 'ideia' ou 'algoritmo' por trás não é. Expor a lógica é irreversível."
            )
        }

    def analyze_legal_risk(self, analysis_data: Dict[str, Any]) -> LegalOpinion:
        """
        Generates a legal opinion based on technical analysis data.
        Accepts either a MemorialAnalysis object or a dictionary.
        """
        # Extract metrics
        if hasattr(analysis_data, 'overall_risk_score'):
            risk_score = analysis_data.overall_risk_score
            patterns = [p for para in analysis_data.paragraphs for p in para.sensitive_patterns]
        else:
            risk_score = analysis_data.get('overall_risk_score', 0)
            patterns = analysis_data.get('sensitive_patterns', [])

        citations = []
        status = "COMPLIANT"
        risk_level = "LOW"
        recommendation = "O texto parece seguro para submissão. Nenhuma exposição óbvia de PI detectada."

        # Logic: High Risk Score -> Trade Secret Risk
        if risk_score > 50:
            status = "NON-COMPLIANT"
            risk_level = "HIGH"
            citations.append(self.knowledge_base['trade_secret'])
            recommendation = "ALERTA CRÍTICO: O texto contém alta densidade técnica que caracteriza Segredo Industrial. A submissão neste estado coloca em risco a vantagem competitiva da empresa."

        # Logic: Specific Patterns -> Specific Laws
        has_algo = any('algorithm' in str(p) for p in patterns)
        has_params = any('parameters' in str(p) for p in patterns)
        
        if has_algo or has_params:
            citations.append(self.knowledge_base['novelty_loss'])
            if risk_level != "HIGH":
                risk_level = "MODERATE"
                status = "WARNING"
                recommendation = "O texto revela detalhes de implementação que podem impedir um pedido de patente futuro por perda de novidade."

        # Logic: Software specific
        if 'software' in str(patterns) or has_algo:
             citations.append(self.knowledge_base['software_protection'])

        return LegalOpinion(
            status=status,
            risk_level=risk_level,
            citations=citations,
            recommendation=recommendation
        )
