# ESHIELD-001-EDICTAL-ONTOLOGY

## 1. INVENTARIO CONCEITUAL (CORE ENTITIES)
- **Edict**: O instrumento convocatorio mestre. Um container semantico e juridico.
- **EdictVersion**: Representacao de um estado do edital no tempo (retificacoes).
- **ThematicLine**: Subdivisoes do edital com orcamento, regras e escopos proprios.
- **Requirement**: O que o projeto/proponente DEVE SER ou POSSUIR. Uma declaracao de estado ou capacidade.
- **Rule**: A logica computavel que avalia a satisfacao de um Requirement, Constraint ou Criterion.
- **Constraint**: O que o projeto/proponente NAO PODE SER ou FAZER. Uma restricao de contorno.
- **Criterion**: Um eixo de valoracao. Diferente de Requirement (binario), Criterion define graduacao/pontuacao.
- **Evidence**: Um fragmento de dado ou texto fornecido pelo proponente que visa comprovar algo.
- **Source**: A origem da Evidence (ex: "Memorial Descritivo", "Balanco Patrimonial", "Receita Federal").
- **Condition**: Uma variavel ambiental ou temporal que ativa/desativa uma Rule (ex: "Se MEI, entao...").
- **Violation**: O resultado de uma Rule avaliada como FALHA.
- **Evaluation**: O resultado agregado da aplicacao de Rules contra Evidences.
- **Project**: O alvo da avaliacao, contendo metadados do proponente e a proposta em si.

## 2. TAXONOMIA

**REQUIREMENT TYPES**
- eligibility, technical, institutional, financial, geographic, consortium, documentation, execution, regulatory

**RULE TYPES**
- mandatory, conditional, quantitative, comparative, temporal, logical, exclusion, allocation

**CRITERION TYPES**
- merit, technical, economic, strategic, elimination

**EVIDENCE TYPES**
- textual, numerical, documentary, inferred, externally_verified

## 3. RELACOES (RELATIONS)
- Edict HAS_VERSION EdictVersion
- EdictVersion HAS_LINE ThematicLine
- ThematicLine HAS_REQUIREMENT Requirement
- ThematicLine HAS_RULE Rule
- ThematicLine HAS_CRITERION Criterion
- Rule APPLIES_TO Requirement | Constraint | Criterion
- Rule DEPENDS_ON Condition
- Evidence SUPPORTS Requirement
- Evidence DERIVED_FROM Source
- Project SATISFIES / VIOLATES Rule
- Project EVALUATED_AGAINST EdictVersion
