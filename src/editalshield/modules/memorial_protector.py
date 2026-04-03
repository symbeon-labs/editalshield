"""
EditalShield - Memorial Protector (Module 4)
Core module for analyzing and protecting IP in technical memorials
"""

import re
import math
import pickle
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class ParagraphAnalysis:
    """Analysis result for a single paragraph"""

    index: int
    text: str
    section_type: str
    entropy: float
    entropy_normalized: float
    sensitive_patterns: List[str]
    risk_score: int
    has_exposure: bool
    suggestions: List[str] = field(default_factory=list)


@dataclass
class MemorialAnalysis:
    """Complete memorial analysis result"""

    total_paragraphs: int
    high_risk_paragraphs: int
    medium_risk_paragraphs: int
    low_risk_paragraphs: int
    overall_risk_score: float
    paragraphs: List[ParagraphAnalysis]
    protected_text: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "total_paragraphs": self.total_paragraphs,
            "high_risk_paragraphs": self.high_risk_paragraphs,
            "medium_risk_paragraphs": self.medium_risk_paragraphs,
            "low_risk_paragraphs": self.low_risk_paragraphs,
            "overall_risk_score": self.overall_risk_score,
            "paragraphs": [asdict(p) for p in self.paragraphs],
        }


class MemorialProtector:
    """
    Analyzes and protects intellectual property in technical memorials.
    Uses Bayesian model for risk assessment and pattern matching for detection.
    """

    # Sensitive patterns by category
    SENSITIVE_PATTERNS = {
        "algorithm": [
            r"\b[A-Z][a-zA-Z]+(?:Analyzer|Engine|Model|Net|Algorithm)\s*V?\d*\.?\d*\b",
            r"\bproprietário\b",
            r"\bpatenteado\b",
            r"\bexclusivo\b",
        ],
        "parameters": [
            r"\b(?:threshold|decay|learning.?rate|epsilon|gamma|alpha|beta)\s*[=:]\s*[\d.]+\b",
            r"\b[A-Z]\s*[=:]\s*[\d.]+\b",
            r"\bparâmetros?\s*(?:de|do|da)?\s*[\w]+\s*[=:]\s*[\d.]+",
            r"\b(?:W|K|N|M|T)\s*[=:]\s*[\d.]+\b",
        ],
        "dataset": [
            r"\b\d+[MK]?\s*(?:registros?|transações?|amostras?|dados?|clientes?)\b",
            r"\bdataset\s+(?:privado|proprietário|interno)\b",
            r"\bacurácia\s*(?:de)?\s*\d+[.,]\d+\s*%?\b",
            r"\b(?:precision|recall|f1)\s*[=:]\s*[\d.]+\b",
        ],
        "contacts": [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            r"\b(?:Dr\.|Prof\.|Eng\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b",
            r"\b\(\d{2}\)\s*\d{4,5}[-.]?\d{4}\b",
        ],
        "metrics": [
            r"\bROI\s*(?:de)?\s*\d+[.,]?\d*\s*[x%]?\b",
            r"\bCAC\s*[=:]\s*R?\$?\s*[\d.,]+\b",
            r"\bLTV\s*[=:]\s*R?\$?\s*[\d.,]+\b",
            r"\b\d+x\s*(?:retorno|crescimento|margem)\b",
        ],
        "clients": [
            r"\bclientes?\s*(?:incluem|como|são)?\s*:?\s*[A-Z][a-zA-Z]+(?:\s*,\s*[A-Z][a-zA-Z]+)*\b",
            r"\b(?:CinemaChain|RetailCorp|FinTechBR|TechVision)\b",
        ],
        "lpi_patent": [
            r"\bnovidade.?(?:absoluta)?\b",
            r"\batividade.?(?:inventiva)?\b",
            r"\baplicação.?(?:industrial)?\b",
            r"\bestado.?(?:da.?)?técnica\b",
            r"\breivindicação.?independente\b",
        ],
        "software_law": [
            r"\bcódigo.?(?:fonte|objeto)\b",
            r"\bregistro.?(?:di?o.?)?software\b",
            r"\bobra.?(?:literária|técnica)\b",
            r"\bengenharia.?(?:reversa|interoperabilidade)\b",
        ],
        "tax_incentive": [
            r"\blei.?(?:di?o.?)?bem\b",
            r"\bsubvenção.?(?:econômica)?\b",
            r"\bPD&I\b",
            r"\bFINEP|FAPESP|CNPq\b",
        ],
        "ai_governance": [
            r"\brisco.?(?:alto|inaceitável|crítico)\b",
            r"\bexplicabilidade\b",
            r"\bviés.?(?:algorítmico)?\b",
            r"\btransparência.?(?:algorítmica)?\b",
        ],
        "lgpd_privacy": [
            r"\bdados?.?(?:pessoais|sensíveis)\b",
            r"\btitular.?(?:di?os.?)?dados?\b",
            r"\banonimização\b",
            r"\bfinalidade.?(?:do.?)?tratamento\b",
        ],
        "innovation_law": [
            r"\blei.?(?:da.?)?inovação\b",
            r"\bICT.?pública\b",
            r"\bencomenda.?(?:tecnológica)?\b",
        ],
    }

    # Pattern weights for risk calculation (0.0 to 1.0)
    PATTERN_WEIGHTS = {
        "algorithm": 1.0,
        "parameters": 0.8,
        "dataset": 0.6,
        "contacts": 1.0,
        "metrics": 0.7,
        "clients": 0.9,
        "lpi_patent": 0.4,
        "software_law": 0.5,
        "tax_incentive": 0.3,
        "ai_governance": 0.8,
        "lgpd_privacy": 1.0,
        "innovation_law": 0.4,
    }

    # Generic replacement suggestions
    PROTECTION_SUGGESTIONS = {
        "algorithm": 'Substituir por: "algoritmo proprietário desenvolvido internamente"',
        "parameters": 'Remover valores específicos, usar: "parâmetros otimizados empiricamente"',
        "dataset": 'Generalizar: "base de dados representativa do mercado-alvo"',
        "contacts": "Remover informações de contato pessoal",
        "metrics": 'Usar ranges: "ROI entre 2x e 5x" ao invés de valores exatos',
        "clients": 'Substituir por: "clientes em setores estratégicos"',
        "lpi_patent": "Verificar Art. 10 da LPI para evitar negação por abstração",
        "software_law": 'Assegurar registro no INPI para proteção de "código-objeto"',
        "tax_incentive": "Mapear este componente para créditos da Lei do Bem",
        "ai_governance": "Realizar Avaliação de Risco Algorítmico (PL 2338)",
        "lgpd_privacy": "Implementar Privacy-by-Design e Anonimização",
        "innovation_law": "Explorar parcerias com ICTs sob a Lei 10.973/04",
    }

    def __init__(self, model_path: str = None):
        """Initialize with optional pre-trained model"""
        self.model = None
        self.scaler_stats = None

        if model_path:
            self.load_model(model_path)
        else:
            # Try default path
            default_path = Path("models/bayesian_model_latest.pkl")
            if default_path.exists():
                self.load_model(str(default_path))

    def load_model(self, model_path: str):
        """Load trained Bayesian model"""
        try:
            with open(model_path, "rb") as f:
                checkpoint = pickle.load(f)
            self.model = checkpoint["model"]
            self.scaler_stats = checkpoint.get("scaler_stats", {})
            print(f"[✓] Model loaded from {model_path}")
        except Exception as e:
            print(f"[!] Could not load model: {e}")

    def calculate_entropy(self, text: str) -> Tuple[float, float]:
        """Calculate Shannon entropy of text"""
        words = text.lower().split()
        if not words:
            return 0.0, 0.0

        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        total = len(words)
        entropy = 0.0
        for freq in word_freq.values():
            p = freq / total
            if p > 0:
                entropy -= p * math.log2(p)

        # Normalize to [0, 1]
        max_entropy = math.log2(len(word_freq)) if len(word_freq) > 1 else 1
        entropy_normalized = entropy / max_entropy if max_entropy > 0 else 0

        return round(entropy, 4), round(entropy_normalized, 4)

    def calculate_zipf_score(self, text: str) -> float:
        """
        Calculate Zipfian Deviation Score.
        Measures how 'rare' the vocabulary is compared to standard language.
        Higher score = more technical/specific/rare content.
        """
        words = re.findall(r"\b[a-zA-ZÀ-ÿ]{3,}\b", text.lower())
        if not words:
            return 0.0

        # Heuristic: Common Portuguese words (Top ~50)
        common_words = {
            "que",
            "para",
            "com",
            "não",
            "uma",
            "dos",
            "por",
            "mais",
            "das",
            "como",
            "mas",
            "foi",
            "ao",
            "ele",
            "das",
            "tem",
            "seu",
            "sua",
            "ou",
            "ser",
            "quando",
            "muito",
            "nos",
            "já",
            "está",
            "eu",
            "também",
            "só",
            "pelo",
            "pela",
            "até",
            "isso",
            "ela",
            "entre",
            "depois",
            "sem",
            "mesmo",
            "aos",
            "seus",
            "quem",
            "nas",
            "me",
            "esse",
            "eles",
            "estão",
            "você",
            "tinha",
            "foram",
            "essa",
            "num",
            "nem",
            "suas",
            "meu",
            "às",
            "minha",
            "têm",
            "numa",
            "pelos",
            "elas",
            "qual",
            "nós",
            "lhe",
            "deles",
            "essas",
            "esses",
            "pelas",
            "este",
            "dele",
            "tu",
            "te",
            "vocês",
            "vos",
            "lhes",
            "meus",
            "minhas",
            "teu",
            "tua",
            "teus",
            "tuas",
            "nosso",
            "nossa",
            "nossos",
            "nossas",
            "dela",
            "delas",
            "esta",
            "estes",
            "estas",
            "aquele",
            "aquela",
            "aqueles",
            "aquelas",
            "isto",
            "aquilo",
            "estou",
            "está",
            "estamos",
            "estão",
            "estive",
            "esteve",
            "estivemos",
            "estiveram",
            "estava",
            "estávamos",
            "estavam",
            "estivera",
            "estivéramos",
            "esteja",
            "estejamos",
            "estejam",
            "estivesse",
            "estivéssemos",
            "estivessem",
            "estiver",
            "estivermos",
            "estiverem",
            "hei",
            "há",
            "havemos",
            "hão",
            "houve",
            "houvemos",
            "houveram",
            "houvera",
            "houvéramos",
            "haja",
            "hajamos",
            "hajam",
            "houvesse",
            "houvéssemos",
            "houvessem",
            "houver",
            "houvermos",
            "houverem",
            "houverei",
            "houverá",
            "houveremos",
            "houverão",
            "houveria",
            "houveríamos",
            "houveriam",
            "sou",
            "somos",
            "são",
            "era",
            "éramos",
            "eram",
            "fui",
            "foi",
            "fomos",
            "foram",
            "fora",
            "fôramos",
            "seja",
            "sejamos",
            "sejam",
            "fosse",
            "fôssemos",
            "fossem",
            "for",
            "formos",
            "forem",
            "serei",
            "será",
            "seremos",
            "serão",
            "seria",
            "seríamos",
            "seriam",
            "tenho",
            "tem",
            "temos",
            "têm",
            "tinha",
            "tínhamos",
            "tinham",
            "tive",
            "teve",
            "tivemos",
            "tiveram",
            "tivera",
            "tivéramos",
            "tenha",
            "tenhamos",
            "tenham",
            "tivesse",
            "tivéssemos",
            "tivessem",
            "tiver",
            "tivermos",
            "tiverem",
            "terei",
            "terá",
            "teremos",
            "terão",
            "teria",
            "teríamos",
            "teriam",
        }

        rare_word_count = 0
        total_length_weight = 0

        for word in words:
            if word not in common_words:
                # Rare word found
                weight = 1.0

                # Bonus for length (technical terms tend to be longer)
                if len(word) > 7:
                    weight += 0.5
                if len(word) > 10:
                    weight += 0.5

                rare_word_count += 1
                total_length_weight += weight

        # Zipf Score: Density of rare/complex words
        # Normalized roughly to 0-1 range for typical text
        score = (total_length_weight / len(words)) if words else 0

        return min(score, 1.0)

    def detect_sensitive_patterns(self, text: str) -> Dict[str, List[str]]:
        """Detect sensitive patterns in text"""
        found = {}

        for category, patterns in self.SENSITIVE_PATTERNS.items():
            matches = []
            for pattern in patterns:
                found_matches = re.findall(pattern, text, re.IGNORECASE)
                matches.extend(found_matches)
            if matches:
                found[category] = list(set(matches))

        return found

    def classify_section(self, text: str) -> str:
        """Classify paragraph section type"""
        text_lower = text.lower()

        if any(
            kw in text_lower
            for kw in ["algoritmo", "modelo", "técnic", "desenvolv", "pipeline", "api"]
        ):
            return "technical"
        elif any(kw in text_lower for kw in ["mercado", "cliente", "tam", "receita", "pricing"]):
            return "market"
        elif any(kw in text_lower for kw in ["equipe", "ceo", "cto", "fundador", "experiência"]):
            return "team"
        elif any(kw in text_lower for kw in ["orçamento", "cronograma", "milestone", "gestão"]):
            return "admin"
        else:
            return "general"

    def calculate_risk_score(
        self, entropy_norm: float, pattern_score: float, section_type: str, zipf_score: float = 0.0
    ) -> int:
        """Calculate risk score (0-100) using Bayesian model or heuristics"""

        if self.model is not None:
            # Use trained model (add zipf as feature if retrained, or use as booster)
            features = [
                [
                    entropy_norm,
                    min(pattern_score, 5),  # Model was trained with count, so we cap/scale
                    0,  # edital_type (public)
                    1 if section_type == "technical" else 0,
                ]
            ]

            # Normalize if scaler stats available
            if self.scaler_stats:
                for i in range(len(features[0])):
                    if self.scaler_stats["stds"][i] > 0:
                        features[0][i] = (
                            features[0][i] - self.scaler_stats["means"][i]
                        ) / self.scaler_stats["stds"][i]

            prob = self.model.predict_proba(features)[0][1]
            base_score = int(prob * 100)

            # Boost with Zipf score (since model wasn't trained with it yet)
            zipf_boost = int(zipf_score * 20)
            return min(base_score + zipf_boost, 100)
        else:
            # Fallback heuristic
            base_score = entropy_norm * 30
            # Use weighted pattern score
            pat_score_val = min(pattern_score * 25, 60)  # Increased multiplier for weighted score
            section_bonus = 20 if section_type == "technical" else 0
            zipf_bonus = zipf_score * 30
            return min(int(base_score + pat_score_val + section_bonus + zipf_bonus), 100)

    def analyze_paragraph(self, text: str, index: int) -> ParagraphAnalysis:
        """Analyze a single paragraph for IP exposure risk"""

        entropy, entropy_norm = self.calculate_entropy(text)
        zipf_score = self.calculate_zipf_score(text)
        patterns = self.detect_sensitive_patterns(text)
        section_type = self.classify_section(text)

        all_patterns = []
        suggestions = []
        for category, matches in patterns.items():
            all_patterns.extend(matches)
            if matches:
                suggestions.append(self.PROTECTION_SUGGESTIONS.get(category, ""))

        # Calculate weighted pattern score
        pattern_score = 0.0
        for category, matches in patterns.items():
            weight = self.PATTERN_WEIGHTS.get(category, 0.5)
            pattern_score += len(matches) * weight

        risk_score = self.calculate_risk_score(
            entropy_norm, pattern_score, section_type, zipf_score
        )
        has_exposure = risk_score >= 50 or pattern_score >= 1.5

        return ParagraphAnalysis(
            index=index,
            text=text,
            section_type=section_type,
            entropy=entropy,
            entropy_normalized=entropy_norm,
            sensitive_patterns=all_patterns,
            risk_score=risk_score,
            has_exposure=has_exposure,
            suggestions=suggestions,
        )

    def analyze_memorial(self, text: str) -> MemorialAnalysis:
        """Analyze complete memorial text"""

        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        if not paragraphs:
            paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

        analyses = []
        high_risk = 0
        medium_risk = 0
        low_risk = 0

        for i, para in enumerate(paragraphs):
            if len(para) < 20:  # Skip very short paragraphs
                continue

            analysis = self.analyze_paragraph(para, i)
            analyses.append(analysis)

            if analysis.risk_score >= 70:
                high_risk += 1
            elif analysis.risk_score >= 40:
                medium_risk += 1
            else:
                low_risk += 1

        # Calculate overall risk (weighted average with emphasis on high-risk)
        if analyses:
            weights = [
                a.risk_score * (1.5 if a.section_type == "technical" else 1.0) for a in analyses
            ]
            overall_score = sum(weights) / len(weights)
        else:
            overall_score = 0

        return MemorialAnalysis(
            total_paragraphs=len(analyses),
            high_risk_paragraphs=high_risk,
            medium_risk_paragraphs=medium_risk,
            low_risk_paragraphs=low_risk,
            overall_risk_score=round(overall_score, 1),
            paragraphs=analyses,
        )

    def protect_text(self, text: str, patterns: Dict[str, List[str]], level: str = "MEDIUM") -> str:
        """
        Apply protection by replacing sensitive patterns.
        Levels: LOW, MEDIUM, HIGH
        """
        protected = text

        # Replacements for MEDIUM level (Standard)
        replacements_medium = {
            "algorithm": "[ALGORITMO PROPRIETÁRIO]",
            "parameters": "[PARÂMETROS OTIMIZADOS]",
            "dataset": "[BASE DE DADOS REPRESENTATIVA]",
            "contacts": "[CONTATO OMITIDO]",
            "metrics": "[MÉTRICAS CONFIDENCIAIS]",
            "clients": "[CLIENTES ESTRATÉGICOS]",
        }

        for category, matches in patterns.items():
            for match in matches:
                if level == "LOW":
                    # Low protection: Remove values but keep context
                    if category == "parameters":
                        # Regex to find the value part and replace it
                        # Simple heuristic: replace digits
                        protected_match = re.sub(r"[\d.]+", "[VALOR]", match)
                        protected = protected.replace(match, protected_match)
                    elif category == "metrics":
                        protected_match = re.sub(r"[\d.,]+", "[VALOR]", match)
                        protected = protected.replace(match, protected_match)
                    else:
                        # Fallback to medium for others
                        replacement = replacements_medium.get(category, "[PROTEGIDO]")
                        protected = protected.replace(match, replacement)

                elif level == "HIGH":
                    # High protection: Redact aggressively
                    protected = protected.replace(match, "[REMOVIDO - ALTO RISCO]")

                else:  # MEDIUM (Default)
                    replacement = replacements_medium.get(category, "[INFORMAÇÃO PROTEGIDA]")
                    protected = protected.replace(match, replacement)

        return protected

    def generate_protected_memorial(
        self, text: str, protection_level: str = "MEDIUM"
    ) -> Tuple[str, MemorialAnalysis]:
        """Generate protected version of memorial"""

        analysis = self.analyze_memorial(text)

        protected_text = text
        for para in analysis.paragraphs:
            if para.has_exposure:
                # For HIGH protection, if risk is very high, redact whole paragraph
                if protection_level == "HIGH" and para.risk_score > 80:
                    protected_text = protected_text.replace(
                        para.text, f"[SEÇÃO CRÍTICA REMOVIDA - RISCO {para.risk_score}]"
                    )
                else:
                    patterns = self.detect_sensitive_patterns(para.text)
                    protected_para = self.protect_text(para.text, patterns, level=protection_level)
                    protected_text = protected_text.replace(para.text, protected_para)

        analysis.protected_text = protected_text
        return protected_text, analysis

    def generate_report(self, analysis: MemorialAnalysis, format: str = "text") -> str:
        """Generate analysis report"""

        if format == "json":
            return json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False)

        # Text format
        report = []
        report.append("=" * 70)
        report.append("EDITALSHIELD - MEMORIAL ANALYSIS REPORT")
        report.append("=" * 70)
        report.append("")
        report.append(f"📊 SUMMARY")
        report.append(f"   Total paragraphs analyzed: {analysis.total_paragraphs}")
        report.append(f"   Overall risk score: {analysis.overall_risk_score}/100")
        report.append("")
        report.append(f"   🔴 High risk paragraphs: {analysis.high_risk_paragraphs}")
        report.append(f"   🟡 Medium risk paragraphs: {analysis.medium_risk_paragraphs}")
        report.append(f"   🟢 Low risk paragraphs: {analysis.low_risk_paragraphs}")
        report.append("")

        # Status
        if analysis.overall_risk_score < 20:
            status = "✅ SAFE - Low IP exposure risk"
        elif analysis.overall_risk_score < 50:
            status = "⚠️  CAUTION - Some sensitive content detected"
        elif analysis.overall_risk_score < 75:
            status = "🔴 WARNING - Significant IP exposure risk"
        else:
            status = "🚨 CRITICAL - High IP exposure risk!"

        report.append(f"   Status: {status}")
        report.append("")
        report.append("-" * 70)
        report.append("")

        # Details for high-risk paragraphs
        high_risk_paras = [p for p in analysis.paragraphs if p.risk_score >= 50]
        if high_risk_paras:
            report.append("🔍 HIGH-RISK PARAGRAPHS:")
            report.append("")
            for para in high_risk_paras:
                report.append(f"   Paragraph {para.index + 1} (Risk: {para.risk_score}/100)")
                report.append(f"   Section: {para.section_type}")
                report.append(f"   Patterns found: {', '.join(para.sensitive_patterns[:3])}")
                if para.suggestions:
                    report.append(f"   Suggestion: {para.suggestions[0]}")
                report.append("")

        report.append("=" * 70)

        return "\n".join(report)


# ============================================================================
# CLI Interface
# ============================================================================


def analyze_file(filepath: str, output_format: str = "text") -> str:
    """Analyze a memorial file"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    protector = MemorialProtector()
    analysis = protector.analyze_memorial(text)
    return protector.generate_report(analysis, output_format)


def protect_file(filepath: str, output_path: str = None) -> str:
    """Protect a memorial file"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    protector = MemorialProtector()
    protected_text, analysis = protector.generate_protected_memorial(text)

    if output_path is None:
        output_path = filepath.replace(".txt", "_protected.txt").replace(".md", "_protected.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(protected_text)

    return output_path


if __name__ == "__main__":
    # Demo
    sample_text = """
    Nossa solução TechVision utiliza o algoritmo BehaviorAnalyzer V2 com parâmetros 
    W=0.7, K=1.5 para otimizar processos de varejo. Dataset privado de 2M transações 
    com acurácia 94.2%. ROI validado em 3 clientes: CinemaChain, RetailCorp, FinTechBR.
    
    O mercado de varejo tech está em expansão de 25-30% a.a. Nosso TAM é conservador.
    CAC: R$ 2500, LTV: R$ 85000 (34x retorno).
    
    Equipe com 5 pessoas. CTO formado no MIT com 10+ anos de experiência.
    Contato: dr.silva@techvision.com
    """

    protector = MemorialProtector()

    print("\n" + "=" * 70)
    print("ANALYZING SAMPLE MEMORIAL...")
    print("=" * 70 + "\n")

    analysis = protector.analyze_memorial(sample_text)
    print(protector.generate_report(analysis))

    print("\n" + "=" * 70)
    print("PROTECTED VERSION:")
    print("=" * 70 + "\n")

    protected, _ = protector.generate_protected_memorial(sample_text)
    print(protected)
