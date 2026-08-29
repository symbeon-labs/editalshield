import pytest
from datetime import datetime
from pydantic import ValidationError
from editalshield.modules.rule_engine.domain import (
    EvaluationStatus, ConsequenceType, Severity, ProvenancePointer,
    EvidenceReference, Fact, FactStatus, Context, Condition,
    RuleExpression, Rule, Evaluation, RuleEngineContract
)

def test_provenance_pointer_creation():
    prov = ProvenancePointer(
        source_type="NORMATIVE",
        document_id="doc_123",
        section="Sec 3.1"
    )
    assert prov.document_id == "doc_123"
    assert prov.span is None

def test_evidence_reference_validation():
    prov = ProvenancePointer(source_type="PROJECT", document_id="doc_xyz")
    
    # Valid
    ev = EvidenceReference(evidence_id="ev_001", source=prov, confidence=0.85)
    assert ev.confidence == 0.85
    
    # Invalid confidence
    with pytest.raises(ValidationError):
        EvidenceReference(evidence_id="ev_002", source=prov, confidence=1.5)

def test_fact_creation():
    fact = Fact(
        key="project.revenue",
        value=15000000,
        datatype="integer",
        unit="BRL",
        status=FactStatus.VALID
    )
    assert fact.value == 15000000
    assert fact.status == "VALID"
    
def test_context_management():
    fact = Fact(key="project.trl", value=4, datatype="integer")
    ctx = Context(facts={"project.trl": fact})
    
    assert ctx.get_fact("project.trl").value == 4
    assert ctx.get_fact("non_existent") is None

def test_rule_creation():
    expr = RuleExpression(operator="GTE", arguments=["project.revenue", 16000000])
    rule = Rule(
        rule_id="rule_001",
        version="v1.0",
        subject="project.revenue",
        predicate=expr,
        consequence=ConsequenceType.INELIGIBLE,
        severity=Severity.CRITICAL
    )
    assert rule.consequence == "INELIGIBLE"

def test_evaluation_creation():
    eval_obj = Evaluation(
        evaluation_id="eval_999",
        rule_id="rule_001",
        rule_version="v1.0",
        status=EvaluationStatus.SATISFIED,
        context_reference="ctx_456",
        evaluated_at=datetime.utcnow().isoformat(),
        consequence=ConsequenceType.INELIGIBLE,
        severity=Severity.CRITICAL
    )
    assert eval_obj.status == EvaluationStatus.SATISFIED

def test_rule_engine_contract():
    engine = RuleEngineContract()
    with pytest.raises(NotImplementedError):
        engine.evaluate(rule=None, context=None, evidence=None)
