# ESHIELD-002-RULE-MODEL

## 1. COMPONENTES FORMAIS DE UMA RULE
Toda Rule no EditalShield e composta pelos seguintes atributos conceituais:
- **id**: Identificador unico (URN).
- **version**: Versao da regra (para lidar com retificacoes).
- **subject**: A entidade ou atributo sendo avaliado (ex: project.proponent.revenue).
- **predicate**: A intencao da avaliacao (ex: is_eligible_for_subvention).
- **operator**: A operacao logica/matematica (ex: LTE).
- **value**: O valor de referencia normativo (ex: 16000000).
- **unit**: A unidade do valor (ex: BRL, months, TRL_level).
- **condition**: (Opcional) Expressao logica que define se a regra e ativada.
- **scope**: O contexto de aplicacao (ex: 	hematic_line_A).
- **consequence**: O impacto caso a regra falhe (ex: INELIGIBLE, SCORE_PENALTY).
- **severity**: A criticidade da consequencia (ex: CRITICAL, MEDIUM).
- **source**: O rastreio documental (Provenance).
- **evidence_requirement**: O tipo de evidencia esperada (ex: NORMATIVE_EVIDENCE, PROJECT_EVIDENCE).

## 2. TAXONOMIA DE OPERADORES
- **EQUALITY**: EQ, NEQ
- **ORDERING**: GT, GTE, LT, LTE
- **RANGE**: BETWEEN, NOT_BETWEEN
- **SET**: IN, NOT_IN, CONTAINS, NOT_CONTAINS
- **LOGICAL**: AND, OR, NOT, XOR
- **EXISTENCE**: EXISTS, NOT_EXISTS
- **COMPARISON**: MATCH, NOT_MATCH
- **TEMPORAL**: BEFORE, AFTER, BETWEEN_DATES, VALID_AT

## 3. EXPRESSOES COMPOSTAS E CONDICIONAIS
As regras podem formar arvores de sintaxe abstrata (AST).
- **Composite Rule**: Representacao aninhada de multiplas regras via operadores LOGICAL.
- **Conditional Rule**: IF <condition> THEN <consequence> ELSE <consequence>.

## 4. SEMANTICA DE ESTADOS (UNKNOWN SEMANTICS)
A avaliacao de uma Rule NUNCA assume falso na ausencia de evidencia. Os estados sao:
- **SATISFIED**: Evidencia prova que a regra foi cumprida.
- **FAILED**: Evidencia prova que a regra foi violada.
- **UNKNOWN**: Ausencia de evidencia impede a avaliacao.
- **NOT_APPLICABLE**: O Scope ou Condition inativaram a regra para este contexto.
- **CONFLICT**: Duas regras ou duas evidencias estabelecem axiomas mutualmente exclusivos.

## 5. CONSEQUENCE VS SEVERITY
- **Consequences**: INFORMATIONAL, WARNING, FAIL, INELIGIBLE, SCORE_PENALTY, SCORE_BONUS, REQUIRED_ACTION.
- **Severities**: INFORMATION, LOW, MEDIUM, HIGH, CRITICAL.
