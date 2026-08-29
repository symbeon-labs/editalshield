from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

class EvaluationStatus(str, Enum):
    SATISFIED = "SATISFIED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    CONFLICT = "CONFLICT"

class ConsequenceType(str, Enum):
    INFORMATIONAL = "INFORMATIONAL"
    WARNING = "WARNING"
    FAIL = "FAIL"
    INELIGIBLE = "INELIGIBLE"
    SCORE_PENALTY = "SCORE_PENALTY"
    SCORE_BONUS = "SCORE_BONUS"
    REQUIRED_ACTION = "REQUIRED_ACTION"

class Severity(str, Enum):
    INFORMATION = "INFORMATION"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ProvenancePointer(BaseModel):
    source_type: str
    document_id: str
    version: Optional[str] = None
    section: Optional[str] = None
    span: Optional[str] = None
    extracted_proposition: Optional[str] = None

class EvidenceReference(BaseModel):
    evidence_id: str
    source: ProvenancePointer
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class FactStatus(str, Enum):
    VALID = "VALID"
    UNKNOWN = "UNKNOWN"
    MISSING = "MISSING"
    INVALID = "INVALID"

class Fact(BaseModel):
    key: str
    value: Any = None
    datatype: str
    unit: Optional[str] = None
    status: FactStatus = FactStatus.VALID
    source: Optional[ProvenancePointer] = None
    timestamp: Optional[str] = None

class Context(BaseModel):
    facts: Dict[str, Fact] = Field(default_factory=dict)
    
    def get_fact(self, key: str) -> Optional[Fact]:
        return self.facts.get(key)

class Condition(BaseModel):
    expression_type: str = "ast_node"
    operator: str
    arguments: List[Any]

class RuleExpression(BaseModel):
    expression_type: str = "ast_node"
    operator: str
    arguments: List[Any]

class Rule(BaseModel):
    rule_id: str
    version: str
    subject: str
    predicate: RuleExpression
    condition: Optional[Condition] = None
    scope: Optional[str] = None
    consequence: ConsequenceType
    severity: Severity
    source: Optional[ProvenancePointer] = None
    
class Evaluation(BaseModel):
    evaluation_id: str
    rule_id: str
    rule_version: str
    status: EvaluationStatus
    context_reference: str
    facts_used: List[str] = Field(default_factory=list)
    evidence_used: List[EvidenceReference] = Field(default_factory=list)
    provenance: Optional[ProvenancePointer] = None
    consequence: Optional[ConsequenceType] = None
    severity: Optional[Severity] = None
    evaluated_at: str
    explanation: Optional[str] = None
    conflict_reference: Optional[str] = None

class RuleEngineContract:
    def evaluate(self, rule: Rule, context: Context, evidence: List[EvidenceReference]) -> Evaluation:
        raise NotImplementedError("Implementacao do evaluate sera realizada no Cycle 2G")
