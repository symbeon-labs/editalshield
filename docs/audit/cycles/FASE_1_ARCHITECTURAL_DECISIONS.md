# FASE 1 - ARCHITECTURAL DECISIONS

## DECISION: Separacao estrita entre Requirement e Rule
- RATIONALE: Requisitos sao inertes. Regras sao a computacao que os avalia. Mistura-los forca hardcoding.
- ALTERNATIVES: Uma classe unica Requirement que contivesse a logica de validacao.
- CONSEQUENCES: Requer um Rule Engine separado (a ser desenhado no Cycle 2).
- STATUS: VERIFIED

## DECISION: Evidence e tratada como entidade de primeira classe
- RATIONALE: O modelo precisa de rastreabilidade (proveniencia). O avaliador precisa saber de onde o sistema tirou a certeza de que a regra passou.
- ALTERNATIVES: Apenas salvar um booleano is_eligible = True.
- CONSEQUENCES: Aumenta a complexidade do grafo de avaliacao, mas permite explicabilidade total.
- STATUS: VERIFIED

## DECISION: Condicoes (Conditions) como modificadores de Regras
- RATIONALE: No benchmark Finep, a regiao geografica altera a taxa de contrapartida.
- ALTERNATIVES: Criar regras separadas.
- CONSEQUENCES: Evita explosao combinatoria de regras e mantem a base DRY.
- STATUS: VERIFIED

## MINIMUM VIABLE ONTOLOGY (CORE VS EXTENSIONS)
- CORE UNIVERSAL: Edict, Requirement, Rule, Criterion, Project, Evidence, Evaluation, Condition, Violation, Source.
- EXTENSIONS: ThematicLine, Consortium.
- BENCHMARK-SPECIFIC: Classificacoes TRL diretas (alguns editais usam MRL ou CRL).
