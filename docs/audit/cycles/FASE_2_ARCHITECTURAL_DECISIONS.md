# FASE 2 - ARCHITECTURAL DECISIONS

## DECISION: Semantica de UNKNOWN vs FAILED
- RATIONALE: O EditalShield baseia-se em logica de terceira via (three-valued logic). A ausencia de comprovacao do proponente gera UNKNOWN, nao FAILED.
- STATUS: VERIFIED

## DECISION: Separacao entre Consequence e Severity
- RATIONALE: Uma violacao pode ter severidade baixa em fases de diligencia previa, mas critica na fase final.
- STATUS: VERIFIED

## DECISION: Rule Provenance em Nivel Atomico
- RATIONALE: Cada Rule possui um source_id apontando para o span exato, garantindo Auditabilidade.
- STATUS: VERIFIED

## DECISION: Revisao Fase 1 (ParticipationStructure & Evidence)
- RATIONALE: Conforme Secao 9, Consortium expandido para ParticipationStructure e Evidence cindida entre Normative/Project.
- STATUS: VERIFIED
