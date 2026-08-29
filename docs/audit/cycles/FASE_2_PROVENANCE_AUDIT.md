# FASE 2 - PROVENANCE AUDIT

## RASTREABILIDADE NORMATIVA E PROBATORIA
- A decisao de usar apenas source_id atomico foi auditada. Ele deve ser uma referencia estruturada (ProvenancePointer).
- Rule.source = NormativeProvenance (Edict, Version, Node, Span)
- Evidence.source = ProjectProvenance (Project, Submission, Document, Span)
- Evaluation retera ponteiros duplos (a Regra avaliada e a Evidencia consumida).
**Status:** Aprovado. source_id sera expandido para objeto completo no modelo de dados.
